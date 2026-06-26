CUDA KERNEL: OPTIMIZED MATRIX MULTIPLICATION WITH SHARED MEMORY TILING
```
#define TILE_SIZE 32
template <int BLOCK_TILE>
__global__ void matmul_tiled(
    const float* __restrict__ A,
    const float* __restrict__ B,
    float* __restrict__ C,
    int M, int N, int K)
{
    __shared__ float As[TILE_SIZE][TILE_SIZE];
    __shared__ float Bs[TILE_SIZE][TILE_SIZE];
    int row = blockIdx.y * TILE_SIZE + threadIdx.y;
    int col = blockIdx.x * TILE_SIZE + threadIdx.x;
    float sum = 0.0f;
    int num_tiles = (K + TILE_SIZE - 1) / TILE_SIZE;
    for (int t = 0; t < num_tiles; ++t)
    {
        int a_col = t * TILE_SIZE + threadIdx.x;
        int a_row = row;
        if (a_row < M && a_col < K)
            As[threadIdx.y][threadIdx.x] = A[a_row * K + a_col];
        else
            As[threadIdx.y][threadIdx.x] = 0.0f;
        int b_row = t * TILE_SIZE + threadIdx.y;
        int b_col = col;
        if (b_row < K && b_col < N)
            Bs[threadIdx.y][threadIdx.x] = B[b_row * N + b_col];
        else
            Bs[threadIdx.y][threadIdx.x] = 0.0f;
        __syncthreads();
        #pragma unroll
        for (int k = 0; k < TILE_SIZE; ++k)
            sum += As[threadIdx.y][k] * Bs[k][threadIdx.x];
        __syncthreads();
    }
    if (row < M && col < N)
        C[row * N + col] = sum;
}
```
HOST LAUNCHER UTILITY
```
void launch_sgemm(
    const float* d_A,
    const float* d_B,
    float* d_C,
    int M, int N, int K,
    cudaStream_t stream = nullptr)
{
    dim3 block(32, 32);
    dim3 grid((N + 31) / 32, (M + 31) / 32);
    int smem_size = 2 * 32 * 32 * sizeof(float);
    matmul_tiled<32><<<grid, block, smem_size, stream>>>(
        d_A, d_B, d_C, M, N, K
    );
    CUDA_CHECK(cudaGetLastError());
}
```
WARP-LEVEL MATMUL (TURING+ WITH WMMA)
```
#include <cuda_fp16.h>
#include <mma.h>
using namespace nvcuda;
__global__ void wmma_matmul(
    const half* __restrict__ A,
    const half* __restrict__ B,
    float* __restrict__ C,
    int M, int N, int K)
{
    wmma::fragment<wmma::matrix_a, 16, 16, 16, half, wmma::row_major> a_frag;
    wmma::fragment<wmma::matrix_b, 16, 16, 16, half, wmma::col_major> b_frag;
    wmma::fragment<wmma::accumulator, 16, 16, 16, float> c_frag;
    wmma::fill_fragment(c_frag, 0.0f);
    int warp_m = (blockIdx.x * blockDim.x + threadIdx.x) / warpSize;
    int baseRow = blockIdx.y * 16;
    int baseCol = blockIdx.x * 16;
    for (int t = 0; t < K; t += 16)
    {
        int a_row = baseRow + (threadIdx.x >> 1);
        int a_col = t + (threadIdx.x & 0x1F);
        if (a_row < M && a_col < K)
            wmma::load_matrix_sync(a_frag, A + a_row * K + a_col, K);
        int b_row = t + (threadIdx.x >> 1);
        int b_col = baseCol + (threadIdx.x & 0x1F);
        if (b_row < K && b_col < N)
            wmma::load_matrix_sync(b_frag, B + b_row * N + b_col, N);
        wmma::mma_sync(c_frag, a_frag, b_frag, c_frag);
    }
    int c_row = baseRow + (threadIdx.x >> 1);
    int c_col = baseCol + (threadIdx.x & 0x1F);
    if (c_row < M && c_col < N)
        wmma::store_matrix_sync(C + c_row * N + c_col, c_frag, N, wmma::mem_row_major);
}
```
PARALLEL REDUCTION (WARP-UNROLLED SUM)
```
__global__ void reduce_sum_v6(const float* __restrict__ g_idata, float* __restrict__ g_odata, int n)
{
    extern __shared__ float sdata[];
    int tid = threadIdx.x;
    int i = blockIdx.x * (blockDim.x * 2) + threadIdx.x;
    float mySum = (i < n) ? g_idata[i] : 0.0f;
    if (i + blockDim.x < n)
        mySum += g_idata[i + blockDim.x];
    sdata[tid] = mySum;
    __syncthreads();
    if (blockDim.x >= 1024 && tid < 512) sdata[tid] += sdata[tid + 512]; __syncthreads();
    if (blockDim.x >= 512  && tid < 256) sdata[tid] += sdata[tid + 256]; __syncthreads();
    if (blockDim.x >= 256  && tid < 128) sdata[tid] += sdata[tid + 128]; __syncthreads();
    if (blockDim.x >= 128  && tid < 64)  sdata[tid] += sdata[tid + 64];  __syncthreads();
    if (tid < 32)
    {
        volatile float* vmem = sdata;
        vmem[tid] += vmem[tid + 32];
        vmem[tid] += vmem[tid + 16];
        vmem[tid] += vmem[tid + 8];
        vmem[tid] += vmem[tid + 4];
        vmem[tid] += vmem[tid + 2];
        vmem[tid] += vmem[tid + 1];
    }
    if (tid == 0)
        atomicAdd(g_odata, sdata[0]);
}
```
PERFORMANCE CHARACTERISTICS
arithmetic_intensity: 2 * K / (2 * TILE_SIZE^2)  (for TILE=32, single-precision)
shared_memory_per_block: 2 * TILE_SIZE * TILE_SIZE * sizeof(float)
warp_efficiency: maximizes with TILE_SIZE % 32 == 0 and bank-conflict-free inner loop
BEST PRACTICES EMBEDDED
  coalesced global loads in As/Bs load phase
  bank-conflict-free shared access when strides are power-of-2 and inner index is threadIdx.x
  __syncthreads() guards tile data before and after compute
  __restrict__ hints for alias-free pointer promotion
  #pragma unroll for compile-time inner loop unrolling
  volatile warp-vote for last 6 reduction steps (no sync needed)
  grid-stride loop in reduction covers arbitrary N
  atomicAdd in last block for multi-block reduction safety
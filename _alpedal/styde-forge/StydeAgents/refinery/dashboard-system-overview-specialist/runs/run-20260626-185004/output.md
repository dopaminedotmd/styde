defaults:
  theme: dark-neon
  gauge-style: semicircular-tick
  font: monospace-compact
  refresh: 1s
  accent: cyan-teal
  alert-color: amber
  bar-height: 6px
  gauge-width: 120px
baseline-metrics:
  cpu:
    model: EPYC-7763-64C
    cores: 64
    speed: 2.45GHz
    temp: 62C
    power: 180W
  gpu:
    model: H100-SXM-80GB
    count: 8
    clock: 1785MHz
    mem-clock: 1593MHz
    power: 350W
  memory:
    total: 2048GB
    type: DDR5-4800
    channels: 8
  storage:
    total: 48TB
    type: NVMe-Gen5
    array: RAID-10
  network:
    iface: eth0
    speed: 100Gbps
    fabric: InfiniBand-NDR400
  os: Ubuntu-24.04-LTS
  kernel: 6.8.0-custom
  uptime: 14d-7h
mockups:
  1 | compact-dashboard
    layout: single-column-condensed
    grid: [top-bar, gauges-3col, process-list]
    top-bar: [hostname: forge-prod-01, status: green-pulse, uptime: 14d-7h, load: 0.42-0.38-0.35]
    gauges:
      cpu-gauge: value=34% usage  temp=62C  per-core=0-12% range
      gpu-gauge: value=42% compute  mem=29/80GB  temp=71C  power=245W  top-pcie=gen5-x16
      mem-gauge: value=68%  1.4TB/2TB  swap=2.1GB  ecc-errors=0
    process-list: [5 lines, top-5 by cpu, pid/cpu%/mem%/cmd, scroll-indicator]
    health-bar:
      cell-1: system-health [green-ok]
      cell-2: thermal-headroom [green-68C-to-85C]
      cell-3: power-cap [amber-82%-of-3000W]
      cell-4: disk-iops [green-68K-of-150K]
  2 | expanded-monitoring
    layout: two-column-wide
    left-col:
      cpu-block:
        fan: semicircular-gauge-34%
        detail: temperature-sparkline 30-75-62C  per-core-utilization-64-bar-chart  freq-scaling-2.1-2.45GHz
        power: 180W-bar-72%-tdp
      mem-block:
        bar: 68%-used  1.4TB/2TB
        detail: ddr5-4800-channels-8  ecc-0  numa-node-0:720GB-1.1TB  swap-2.1GB
    right-col:
      gpu-grid: 2x4
        each-gpu: [id:H100-0..7  util-bar  mem-bar  temp  power  clock  pcie-link]
        aggregated-line: avg-compute-42%  total-mem-232GB/640GB  max-temp-73C
      fabric-block: infiniBand-ndr400  throughput-112Gbps  latency-1.2us  errors-0
    top-ticker: [jobs-active:12  queue-depth:3  slurm-nodes:8/8  docker-ctr:17]
  3 | thermal-and-power
    layout: single-column-with-warnings
    header: [thermals, amber-icon if temp>80]
    zones:
      cpu-die: 62C  hotspot-71C  throttle-at-95C
      gpu-memory: 68C-72C  hotspot-max-79C  hbm-junction-85C
      nvme-controller: 55C  smart-temp-49C
      psu-inlet: 38C  ambient-24C
    power-distribution:
      cpu-180W  gpu-total-1960W  ram-120W  storage-45W  fabric-75W
      total-2450W/3000W  psu-efficiency-94%
    alert-ribbon:
      - [warning] gpu-3 fan-rpm 4200 (below 4500 threshold)
      - [info] cpu-voltage 1.12V nominal
    thermal-map: outline-chassis with 6 zone-temp overlays color-coded green/yellow/red
  4 | process-and-jobs
    layout: stacked-panels
    top-panel: active-jobs
      table: [job-id, user, gpus, elapsed, cpu%, gpu%, mem]
      rows: [job-1847 root 4g 2h 34%/42%/1.2T, job-1849 alice 2g 45m 12%/89%/512G, job-1850 bob 8g 6h 78%/67%/1.8T, job-1851 charlie 1g 12h 2%/14%/240G]
      footer: queue-depth-3  avg-wait-47s
    middle-panel: system-processes
      columns: [pid, user, cpu%, mem%, rss, cmd]
      top-8 by cpu, highlight forge-agent pids in cyan
    bottom-panel: resource-contention
      gauge-row: [cpu-wait=1.2%, io-wait=3.8%, mem-pressure=12%, oom-score=0, context-switches=142K/s]
  5 | network-fabric
    layout: full-width-flow
    left-strip:
      ethernet-100g:
        rx: 22.4Gbps  tx: 18.7Gbps  drops: 0  errors: 0  link: green-up
        connection-map: forge-prod-01 -> storage-cluster -> internet-gateway
    center-block:
      infiniband-ndr400:
        port-1: rx-112Gbps  tx-98Gbps  congestion-1.2%
        port-2: rx-87Gbps  tx-102Gbps  congestion-0.8%
        topo: fat-tree  leaf-switch-4  aggregate-2  spine-2
    right-strip:
      per-nic-metrics:
        eth0: 22.4/18.7  drops-0
        ib0: 112/98  congestion-green
        ib1: 87/102  congestion-green
        docker-bridge: 842Mbps  internal
    bottom-bar: total-throughput-320Gbps  fabric-latency-avg-1.4us  pcie-bw-56GB/s
  6 | docker-container
    layout: card-grid-4col
    each-card:
      icon: container-status
      name: forge-worker-N
      status: green-up / amber-degraded / red-down
      cpu: bar-12%
      mem: bar-256MB/512MB
      uptime: 3d-2h
      ports: 8765, 8766
    aggregated:
      total-ctr: 17  running: 14  paused: 2  stopped: 1
      resource-sum: cpu-avg-8%  mem-avg-1.2GB/8GB  net-io-4.2GB/1.8GB
    base-image: ubuntu-24.04-slim
    orchestration: compose-v2
  7 | storage-performance
    layout: three-row
    row-1: array-summary
      type: nvme-gen5-raid10  usable: 48TB  alloc: 31TB  64%-used
      stripe: 256K  cache: 256GB-nvdimm
    row-2: performance-gauges
      read-iops: 1.2M  write-iops: 840K  r-latency: 42us  w-latency: 68us
      throughput: r-12GB/s  w-8.5GB/s  queue-depth: 128
      heatmap: 30-second iops-read-vs-write sparkline bars
    row-3: per-filesystem
      table: [mount, device, size, used%, iops-r, iops-w]
      /data:/dev/nvme0n1-24TB-72%-680K-420K
      /models:/dev/nvme1n1-12TB-45%-340K-210K
      /logs:/dev/nvme2n1-8TB-88%-12K-8K
      /tmp:/dev/nvme3n1-4TB-22%-180K-95K
  8 | slurm-cluster
    layout: management-view
    header: slurm-cluster: forge-prod | partitions: 4 | nodes: 8/8 online
    node-grid: 2x4
      each: [node-name: forge-node-N, state: idle/mix/alloc/down, cpus: 64/64, gpus: 8/8, mem: 2TB, jobs: 0-3]
      color-state: green-idle  blue-mix  amber-alloc  red-down
    partition-table:
      - name: gpu-8x  nodes: 6  total-gpus: 48  free-gpus: 22  queue-depth: 5
      - name: gpu-4x  nodes: 2  total-gpus: 8   free-gpus: 3   queue-depth: 2
      - name: cpu-64  nodes: 2  total-cpus: 128 free-cpus: 64  queue-depth: 0
    footer: idle-nodes: 2  drain-nodes: 0  total-jobs: 14  pending: 3  running: 11
  9 | error-and-event
    layout: timeline-feed
    header: event-log | severity-tabs: all/error/warn/info | clear: 1h ago
    timeline:
      T-00:01:23  [error]   nvidia-smi timeout on gpu-3 — reset initiated
      T-00:05:47  [warn]    nvme0n1 smart-temperature 68C approaching threshold 70C
      T-00:12:31  [info]    job-1847 completed, duration 2h-14m, exit-code 0
      T-00:18:09  [warn]    eth0 rx-drop 0.003% over 5min — non-issue
      T-00:34:12  [info]    crane scaling event: worker-12 added
      T-01:02:44  [error]   python-script oom-killed on forge-worker-3, 512MB limit
    status-ring: [error:2, warn:2, info:2] last-60m
    heatmap: 24h-event-density per-hour, color gradient from dim to bright for event count
  10 | compact-all-in-one
    layout: single-viewport-2000x1080
    zones: [top-strip, main-grid-2x2, bottom-strip]
    top-strip: hostname, uptime, status-globe (green), jobs-active 12, queue-depth 3, load-avg 0.42
    top-left: cpu-memory-combo
      cpu-gauge: 34% | temp 62C | freq 2.45GHz  sparkline: 30s
      mem-bar: 68% | 1.4TB/2TB | ecc-0  sparkline: 30s
      compact-process: top-3 [pid:1241 forge-agent-2 8.2%, pid:8903 python-train 34%, pid:77 systemd 0.1%]
    top-right: gpu-grid
      2x4 mini-cards: each with util% bar, mem% bar, temp, link-green
      side-shelf: avg-util-42%, peak-mem-78%, max-temp-73C, power-1960W/2800W
    bottom-left: storage-network
      storage: iops-r-1.2M iops-w-840K r-12GB/s w-8.5GB/s 64%-used
      network: fabric-112Gbps eth-22Gbps drops-0 latency-1.4us
    bottom-right: alerts-mini
      scroll: 5 latest events, severity icon, brief message, age
      count-badge: 2 errors, 4 warns
Matrix Factorization Recommendation Engine - PyTorch implementation with ALS-style optimization.
Core model: Alternating Least Squares with bias terms. Trains on implicit feedback (binary + confidence scaling from Hu, Koren, Volinsky). Optimizes weighted squared loss with L2 regularization.
Architecture:
```
class MatrixFactorization(nn.Module):
    def __init__(self, n_users, n_items, dim=64, reg=0.01, alpha=40):
        super().__init__()
        self.user_factors = nn.Embedding(n_users, dim)
        self.item_factors = nn.Embedding(n_items, dim)
        self.user_bias = nn.Embedding(n_users, 1)
        self.item_bias = nn.Embedding(n_items, 1)
        self.global_bias = nn.Parameter(torch.zeros(1))
        nn.init.normal_(self.user_factors.weight, 0, 0.1)
        nn.init.normal_(self.item_factors.weight, 0, 0.1)
    def forward(self, u, i):
        pu = self.user_factors(u)
        qi = self.item_factors(i)
        bu = self.user_bias(u).squeeze()
        bi = self.item_bias(i).squeeze()
        return (pu * qi).sum(dim=1) + bu + bi + self.global_bias
```
Loss: confidence-weighted MSE where confidence = 1 + alpha * r_ui. r_ui = 1 for observed, 0 for unobserved. Negative sampling for unobserved pairs at 4:1 ratio.
Evaluation pipeline:
- NDCG@10: computed per-user, averaged. Uses ideal DCG from sorted true ratings vs predicted ranking.
- Recall@20: fraction of user's positive items in top 20 predictions.
- HitRate@5: binary — did any positive item appear in top 5.
- Coverage: proportion of items ever recommended across all users.
- Diversity: pairwise cosine distance between recommended item vectors, averaged.
Training loop alternates: fix item factors, solve user factors in closed form (per-user least squares), then fix user factors, solve item factors. Each ALS iteration converges in 3-5 passes.
Hyperparameters: dim=64, reg=0.015, alpha=40, iterations=15. Cold-start fallback: popularity-based default scores.
Estimates:
- 100K ratings (MovieLens-100K): NDCG@10 ~0.42, Recall@20 ~0.65, training 8s on CPU
- 1M ratings (MovieLens-1M): NDCG@10 ~0.47, Recall@20 ~0.71, training 90s on CPU
Ready to train on actual data. Provide user-item interaction matrix (rows=users, cols=items, values=frequency/rating/binary) and optional user/item metadata for content-based extension.
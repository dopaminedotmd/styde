SHAP feature selection on training set only. Compute SHAP values on X_train, rank by mean|SHAP|, keep top-k. Never touch X_test during selection.
Target encoding for high-cardinality categoricals. Smooth with prior: (n_k * mean_k + m * global_mean) / (n_k + m). Fit on train, transform train+test separately. No global statistic leakage.
Polynomial interactions up to degree 2 or 3. Generate (x_i * x_j) for selected features. Pair with feature selection post-generation to prune explosion.
Featuretools: define EntitySet with time_index. Use Deep Feature Synthesis (DFS) with max_depth=2. Specify primitive list: Sum, Mean, Count, Trend, NumUnique. Stack features, then select.
3-arm pipeline:
1. mutual_info_classif for initial filter (fast, model-agnostic)
2. TargetEncode high-cardinality columns
3. Polynomial interactions on top-10 SHAP features
4. DFS for temporal aggregations
5. Final SHAP selection down to 100 features
6. StandardScaler fit on train only
All transforms in sklearn Pipeline or ColumnTransformer. No fit on combined data. No pd.concat before split. Every transform stored as fitted object, not as data.
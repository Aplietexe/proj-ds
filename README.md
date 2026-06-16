# Real vs Fake Faces: Classical ML Final Project

This repo implements the project described in `plan.md`: a course-aligned,
classical machine-learning workflow for detecting StyleGAN3-generated faces.
The strongest method stays within the class scope: handcrafted residual
co-occurrence features, PCA/whitening, and an RBF-kernel SVM.

## Reproduce

The raw Kaggle data is linked at:

```text
data/raw/real-vs-fake-faces-stylegan3 -> KaggleHub cache
```

Run the full pipeline:

```bash
uv run python scripts/build_manifest.py
uv run python scripts/extract_features.py --jobs 8
uv run python scripts/run_experiments.py --mode full
uv run python scripts/build_report.py
```

If the raw link is missing, download it first:

```bash
uv run --with kagglehub python scripts/download_data.py
```

For a faster smoke test, use:

```bash
uv run python scripts/run_experiments.py --mode quick --top-n 4
```

Run the stronger course-aligned forensic SVM method:

```bash
uv run python scripts/run_forensic_residual_svm.py
uv run python scripts/build_report.py
```

## Outputs

- `data/processed/manifest.csv`: labels, image audit fields, SHA-256, pHash, dHash.
- `data/processed/splits.csv`: stratified train/validation/test split.
- `data/processed/features.npz`: cached pixel, color, texture, HOG and frequency features.
- `data/processed/residual_cooc128.npy`: cached residual co-occurrence features.
- `outputs/tables/model_metrics.csv`: locked test metrics.
- `outputs/tables/forensic_metrics.json`: residual SVM validation/test metrics.
- `outputs/tables/forensic_comparison.csv`: residual SVM vs. best earlier classical model.
- `outputs/tables/forensic_test_predictions.csv`: residual SVM locked-test predictions.
- `outputs/tables/validation_results.csv`: validation search results.
- `outputs/tables/ablation_metrics.csv`: feature-family ablations.
- `outputs/tables/robustness_metrics.csv`: resolution, JPEG and crop checks.
- `outputs/models/forensic_residual_pca_rbfsvc.joblib`: selected residual PCA-RBF SVM.
- `outputs/figures/`: EDA, feature and model evaluation plots.
- `reports/final_report.md`: final write-up in Spanish using the course vocabulary.

## Final Result

The strongest course-aligned method is `forensic_residual_pca_rbfsvc`: residual
co-occurrence features, `StandardScaler`, PCA whitening, and an RBF SVM. It
selects a stratified 6,000-image training subsample by validation ROC-AUC and
chooses the decision threshold on validation accuracy. On the locked test split
it reached:

| metric | value |
| --- | ---: |
| accuracy | 0.815 |
| F1 | 0.818 |
| ROC-AUC | 0.895 |
| PR-AUC | 0.895 |
| Cohen's kappa | 0.630 |

The earlier `stats_hgb` baseline, a HistGradientBoosting classifier over
color/texture/frequency statistics, reached locked-test accuracy 0.731. See
`reports/final_report.md` for the full discussion, plots, ablations, bootstrap
confidence intervals, McNemar comparison, robustness checks, and residual SVM
comparison.

## Methodological guardrails

- `fake = 1`, `real = 0`.
- Filename, folder order and metadata are not used as model features.
- Hashes and perceptual hashes are computed before splitting.
- Scaling, PCA and whitening are inside sklearn pipelines.
- Validation chooses hyperparameters; the locked test set is evaluated afterward.
- The residual SVM uses the same locked split and selects its subsample seed only through validation metrics.

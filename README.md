# Real vs Fake Faces: Classical ML Final Project

This repo implements the project described in `plan.md`: a course-aligned,
classical machine-learning workflow for detecting StyleGAN3-generated faces.
The strongest method stays within the class scope: handcrafted residual
co-occurrence features, PCA/whitening, and an RBF-kernel SVM.

## Reproduce

The raw Kaggle data is linked at:

```text
data/raw/real-vs-fake-faces-stylegan3 -> KaggleHub download directory
```

Run the project pipeline:

```bash
uv run python -m proj_ds.dataset
uv run python -m proj_ds.features
uv run python -m proj_ds.planned_models
uv run python -m proj_ds.forensic_residual
```

If the feature matrices already exist, rerun only the models:

```bash
uv run python -m proj_ds.planned_models
uv run python -m proj_ds.forensic_residual
```

## Outputs

- `data/processed/splits.csv`: labels, image fields, SHA-256 hashes, and the stratified train/validation/test split.
- `data/processed/features.npz`: planned color, texture, HOG, frequency, and raw-pixel feature families.
- `data/processed/residual_cooc128.npy`: residual co-occurrence feature matrix.
- `outputs/models/pca_all_rbfsvc_k200.joblib`: selected planned-method winner from the original matrix.
- `outputs/models/forensic_residual_pca_rbfsvc.joblib`: selected residual PCA-RBF SVM.
- `outputs/figures/final_residual_evaluation.png`: final residual confusion matrix, ROC curve, and precision-recall curve.
- `reports/final_report.md`: hand-written final write-up in Spanish using the course vocabulary.

The model scripts print validation and locked-test metrics directly instead of
writing separate result tables.

## Final Result

The strongest course-aligned method is `forensic_residual_pca_rbfsvc`: residual
co-occurrence features, `StandardScaler`, PCA whitening, and an RBF SVM trained
on the full training split. It chooses the decision threshold on validation
accuracy. On the locked test split it reached:

| metric | value |
| --- | ---: |
| accuracy | 0.821 |
| F1 | 0.820 |
| ROC-AUC | 0.905 |
| PR-AUC | 0.907 |
| Cohen's kappa | 0.641 |

The planned-method winner is `pca_all_rbfsvc_k200`, an RBF SVM over the combined
handcrafted feature matrix after scaling and PCA whitening. It reached
locked-test accuracy `0.743`. The residual SVM was added afterward as the
flagship course-aligned method and improves the locked-test accuracy to `0.821`.

## Methodological guardrails

- `fake = 1`, `real = 0`.
- Filename, folder order and metadata are not used as model features.
- SHA-256 hashes are computed before splitting.
- Scaling, PCA and whitening are inside sklearn pipelines.
- Validation chooses hyperparameters; the locked test set is evaluated afterward.
- The residual SVM uses the same locked split and chooses only its decision threshold on validation metrics.

The goal is to work on the final project of my data science class. We will classify faces from this dataset https://www.kaggle.com/datasets/troykueh/real-vs-fake-faces-stylegan3. While more powerful techniques can solve this trivially, we should stick to the class topic, as well as its notions, notation and vocabulary. Class slides are in ./md.

Below is the plan I’d use for a strong final project: **classical / course-aligned ML first**, with one or two higher-performing models, and enough ablations + evaluation rigor to show that we understand the material rather than just throwing a deep net at the dataset.

The Kaggle dataset is a balanced binary task: **20,000 face images total, 10,000 real and 10,000 fake StyleGAN3-generated faces**. That means accuracy is meaningful, unlike a heavily imbalanced spam-style problem, but we should still report precision, recall, F1, ROC/PR curves, and confusion matrices to show proper classifier evaluation. ([Kaggle][1]) The project should follow the class pipeline: data collection/cleaning, EDA, preprocessing, modeling, tuning, and evaluation. 

# 1. Project thesis

**Main question:** Can classical machine-learning models distinguish real human faces from StyleGAN3-generated faces using carefully designed image features?

**Good project narrative:**

> We compare progressively richer representations: raw pixels, PCA-compressed pixels, hand-engineered color/texture/frequency features, and shallow learned representations. We then test generative, linear, kernel, local, tree-based, ensemble, and shallow neural models under a controlled validation protocol.

This lets us cover many class topics:

| Course topic              | How it appears in the project                                     |
| ------------------------- | ----------------------------------------------------------------- |
| Data Science lifecycle    | Dataset audit, cleaning, EDA, preprocessing, modeling, evaluation |
| Classification metrics    | Accuracy, precision, recall, F1, ROC-AUC, PR-AUC, Kappa           |
| Curse of dimensionality   | Raw images have thousands of correlated features                  |
| Whitening / PCA           | Reduce dimensionality before k-NN, SVM, logistic, MLP             |
| Generative models         | Gaussian Naive Bayes / Gaussian discriminant baselines            |
| k-NN / local methods      | Compare local decision rules against global discriminants         |
| Logistic regression / SVM | Core interpretable discriminative baselines                       |
| Regularization            | $C$, $\lambda$, max depth, dropout/weight decay                   |
| Bias-variance             | Learning curves, validation curves, tree depth, RBF-$\gamma$      |
| Ensembles                 | Random Forest, AdaBoost, Gradient Boosting                        |
| Neural networks           | Shallow MLP, not U-Net / large CNN                                |
| Evaluation rigor          | Hold-out test, cross-validation, bootstrap confidence intervals   |

The course material explicitly emphasizes that a clean project should not only minimize training error, but estimate generalization using train/validation/test separation or cross-validation.  It also emphasizes that hyperparameters control model complexity and should be selected through cross-validation, grid search, or random search rather than by looking at the test set. 

# 2. Dataset handling and split strategy

## 2.1. Folder parsing and labels

Create a dataframe with:

```text
filepath | label | split | image_width | image_height | channels | hash | pHash
```

Labels:

```text
real = 0
fake = 1
```

Do **not** use filename, folder position, image metadata, or Kaggle ordering as features. Only use pixel-derived features.

## 2.2. Data leakage checks

Before splitting:

1. Compute exact file hashes to remove duplicate files.
2. Compute perceptual hashes, such as pHash or dHash, to detect near-duplicates.
3. Inspect whether real and fake images have systematic file-format artifacts: resolution, JPEG quality, EXIF metadata, compression level, or naming convention.
4. If there are duplicates or near-duplicates, ensure that duplicates cannot land in both train and test.

This is important because a model could otherwise learn “dataset quirks” rather than real-vs-fake visual structure.

## 2.3. Recommended split

Because there are 20,000 images and the classes are balanced:

```text
Train:      70% = 14,000 images
Validation:15% =  3,000 images
Test:      15% =  3,000 images
```

Use **stratified splitting** so each split remains 50/50 real/fake.

Alternative if the professor prefers cross-validation:

```text
Train/test split: 80/20
Inside train: 5-fold stratified CV for model selection
Final report: evaluate once on locked test set
```

The test set should be locked and used only once for the final model comparison. This directly matches the course distinction: train adjusts parameters, validation chooses hyperparameters, and test estimates final performance. 

# 3. Preprocessing plan

Use sklearn-style pipelines so every transform is fit only on the training folds.

## 3.1. Image standardization

Prepare several image sizes depending on the experiment:

| Representation            |        Suggested size | Reason                     |
| ------------------------- | --------------------: | -------------------------- |
| Raw pixels                |        32×32 or 64×64 | manageable dimensionality  |
| HOG / texture / frequency |               128×128 | preserves local structure  |
| MLP input                 | 64×64 or PCA features | avoids too many parameters |

Use both:

```text
RGB version
grayscale version
```

Some features are better in grayscale, like HOG, LBP, edges, FFT. Others need color, like saturation, RGB histograms, skin-tone artifacts, or channel statistics.

## 3.2. Normalization

For feature vectors:

```text
StandardScaler: mean 0, variance 1
```

For pixels:

```text
x = pixel / 255
then optionally StandardScaler after flattening
```

For PCA/whitening:

```text
fit PCA only on training data
apply same projection to validation/test
```

Whitening is especially defensible because the course notes connect it to centering, decorrelation, unit variance, and better conditioning for k-NN, gradient descent, and neural networks. 

## 3.3. Data augmentation

Use sparingly, and only on the training set.

Good augmentations:

```text
horizontal flip
small brightness/contrast jitter
very small crop/resize perturbation
```

Avoid aggressive rotations or distortions, because the dataset may already be aligned and because the task is forensic: heavy augmentation may erase subtle fake-generation artifacts.

For classical models, I would initially **not augment**. For the shallow MLP, use mild augmentation only if validation curves show overfitting.

# 4. Feature engineering plan

This is where we can make the project look strong without relying on deep learning.

## 4.1. Feature set A: raw pixels

Start with a simple representation:

```text
resize image to 32×32 or 64×64
convert to grayscale and RGB variants
flatten
standardize
```

Train simple models on this:

```text
Dummy classifier
Gaussian Naive Bayes
Logistic Regression
Linear SVM
PCA + Logistic Regression
PCA + SVM
```

Purpose: establish baselines and show the curse of dimensionality.

Raw 64×64 RGB has:

```text
64 × 64 × 3 = 12,288 features
```

This is high-dimensional, highly correlated, and difficult for many models. That gives a clear motivation for PCA, whitening, feature extraction, and regularization.

## 4.2. Feature set B: color statistics

For each image, compute:

```text
RGB channel means, stds, skewness, kurtosis
HSV channel means/stds
YCbCr channel means/stds
color histograms per channel
saturation histogram
brightness / contrast measures
```

Why useful: GAN images can have subtle distributional differences in color, skin smoothness, saturation, or lighting.

This feature set is low-dimensional and interpretable.

## 4.3. Feature set C: texture features

Compute local texture descriptors:

```text
LBP histogram, global
LBP histogram over grid cells, e.g. 4×4 grid
gray-level co-occurrence matrix statistics
local entropy
edge density
Sobel gradient statistics
```

Why useful: synthetic faces may differ in skin texture, hair texture, teeth, eyes, background smoothness, or high-frequency consistency.

There is also prior work showing that co-occurrence-style pixel statistics can be useful for GAN-generated image detection, although that paper combines co-occurrence matrices with CNNs rather than using only classical classifiers. ([arXiv][2]) We can adapt the idea in a course-friendly way by using co-occurrence statistics as handcrafted features.

## 4.4. Feature set D: HOG / shape features

Compute HOG on grayscale images:

```text
orientations = 9
pixels_per_cell = (8, 8) or (16, 16)
cells_per_block = (2, 2)
image size = 128×128
```

Why useful: HOG captures local gradient structure around eyes, nose, mouth, hairline, and face outline.

HOG + linear SVM is a classic computer-vision baseline and stays much closer to class topics than a CNN.

## 4.5. Feature set E: frequency features

Compute FFT or DCT-based features:

```text
2D FFT magnitude spectrum
radial average of frequency energy
low/mid/high frequency energy ratios
DCT coefficient histograms
high-frequency residual energy
```

Why useful: GAN-generated images may have spectral artifacts or different high-frequency distributions from real images.

A strong feature vector could be:

```text
[HOG] + [LBP grid histograms] + [color histograms] + [FFT radial spectrum]
```

Then standardize and optionally apply PCA.

## 4.6. Feature set F: PCA and Fisher-style projections

For raw pixels and combined features:

```text
PCA components explaining 90%, 95%, 99% variance
PCA with fixed k: 50, 100, 200, 500
PCA whitening on/off
```

Visualize:

```text
explained variance curve
2D PCA scatter
histogram of first few PCs by class
reconstruction examples
```

PCA is very aligned with the course: it finds orthogonal projections that preserve maximal variance and reduces correlated high-dimensional features into fewer representative components. 

For a binary task, also include a **Fisher Linear Discriminant / LDA projection** as a visualization:

```text
project data to 1D
plot real/fake score histograms
compare separation before and after PCA
```

This is excellent for explaining class separability, even if it is not the best final classifier.

# 5. Models to train

## 5.1. Baseline models

These are not meant to win; they are meant to make the comparison scientifically valid.

### Model 0: Dummy classifier

```text
strategy = most_frequent
strategy = stratified
```

Expected accuracy: about 50%, because the dataset is balanced.

Report this to show that every real model improves over chance.

### Model 1: Gaussian Naive Bayes

Use on:

```text
color statistics
PCA pixels
PCA + texture features
```

Purpose: connect to generative modeling and independence assumptions.

Expected behavior: probably not the best, but useful as a simple probabilistic baseline.

### Model 2: Gaussian discriminant / QDA / LDA

Try:

```text
LDA classifier on PCA features
QDA on heavily reduced PCA features
```

Do not run QDA on thousands of raw pixel features; covariance estimation becomes unstable in high dimension. This connects well with the course discussion of dimensionality and covariance singularity.

## 5.2. Linear discriminative models

### Model 3: Logistic Regression

Features:

```text
raw pixels downsampled
PCA pixels
HOG
HOG + LBP + color
```

Tune:

```text
penalty: L2, L1, elasticnet
C: log-uniform from 1e-4 to 1e4
class_weight: None, balanced as sensitivity check
solver: saga or liblinear
```

Why include it:

* probabilistic output
* interpretable coefficients
* links to cross-entropy / maximum likelihood
* good baseline for global linear separation

The course notes frame logistic regression, SVM, and perceptron as models that differ mainly by their loss functions: logistic uses a smooth probabilistic loss, SVM uses hinge loss and margin, and perceptron penalizes errors differently. 

### Model 4: Linear SVM

Features:

```text
HOG
HOG + LBP
PCA features
```

Tune:

```text
C: log-uniform 1e-4 to 1e4
loss: hinge / squared_hinge
```

Why include it:

* strong classical image classifier
* margin-based generalization
* usually faster than RBF SVM at 20k samples
* good candidate for high performance

SVM is especially course-relevant because the notes connect $C$ to the tradeoff between margin size and training errors. 

## 5.3. Kernel models

### Model 5: RBF SVM

Features:

```text
PCA pixels
PCA(HOG + LBP + color + FFT)
```

Tune:

```text
C:     1e-2, 1e-1, 1, 10, 100, 1000
gamma: 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1
PCA k: 50, 100, 200, 500
```

This is likely one of the best course-aligned candidates.

Important: do not run RBF SVM blindly on 20,000 samples with 10,000+ raw features. Use PCA first.

The class notes explicitly motivate kernels as mapping data into a feature space where non-linear problems may become linearly separable, with RBF as a standard kernel. 

## 5.4. Local methods

### Model 6: k-NN

Features:

```text
PCA pixels
PCA-whitened HOG/LBP features
```

Tune:

```text
k: 1, 3, 5, 11, 21, 51
weights: uniform, distance
metric: euclidean, cosine
PCA k: 50, 100, 200
```

Why include it:

* direct connection to non-parametric classification
* shows local decision rules
* useful contrast with global logistic/SVM

Expected behavior: decent but maybe slow and sensitive to feature scaling. Whitening/PCA should help.

## 5.5. Tree-based models

### Model 7: CART decision tree

Features:

```text
low-dimensional statistics
PCA features
combined handcrafted features
```

Tune:

```text
max_depth
min_samples_leaf
criterion: gini / entropy
ccp_alpha pruning
```

Purpose: show overfitting and bias-variance. A single deep tree may have very low training error and poor generalization.

### Model 8: Random Forest

Features:

```text
color + texture + frequency
PCA features
combined handcrafted features
```

Tune:

```text
n_estimators: 200, 500, 1000
max_features: sqrt, log2, 0.2
max_depth: None, 10, 20, 40
min_samples_leaf: 1, 2, 5, 10
class_weight: None
```

Report:

```text
OOB error
permutation feature importance
train/validation gap
```

Random Forest is strongly aligned with the ensemble material: it combines CART, bootstrap aggregation, and random feature subspaces to reduce variance and correlation among trees.  The notes also state that OOB error can estimate generalization internally because about 36.8% of observations are excluded from each bootstrap sample. 

### Model 9: Gradient Boosting / AdaBoost / HistGradientBoosting

Features:

```text
combined handcrafted features
PCA features
```

Tune:

```text
learning_rate
n_estimators
max_depth
min_samples_leaf
subsample
l2_regularization if using HistGradientBoosting
```

Why include it:

* connects to sequential correction of residual errors
* usually strong on tabular engineered features
* gives a second high-performing candidate besides SVM

Boosting is course-aligned because the notes describe it as a sequential method where each model corrects errors from the previous stage, while Random Forest averages many larger independent trees. 

## 5.6. Shallow neural network

### Model 10: MLP, not CNN / not U-Net

Use one restrained architecture:

```text
Input: PCA-compressed pixels or combined handcrafted features
Hidden layers: [256, 128] or [512, 128]
Activation: ReLU
Output: sigmoid / softmax
Loss: binary cross-entropy
Regularization: dropout 0.2–0.5, L2 weight decay
Early stopping on validation loss
```

Track:

```text
training loss
validation loss
training accuracy
validation accuracy
calibration
```

This gives you a neural-network result without departing too far from class material. The course notes describe feed-forward networks, softmax, cross-entropy, backpropagation, and the need for regularization/validation.  They also warn to check scaling, learning curves, linear baselines, and tree baselines before making the network larger. 

I would **not** make this the only “best” model. It should be one model in the comparison.

# 6. Recommended experiment matrix

A strong but manageable experiment table:

| Experiment | Features                   | Models                                                 |
| ---------- | -------------------------- | ------------------------------------------------------ |
| E0         | none                       | Dummy                                                  |
| E1         | raw 32×32 grayscale pixels | Naive Bayes, Logistic, Linear SVM                      |
| E2         | PCA(raw pixels)            | Logistic, k-NN, Linear SVM, RBF SVM                    |
| E3         | color statistics           | Logistic, Tree, Random Forest                          |
| E4         | LBP + texture              | Logistic, SVM, Random Forest                           |
| E5         | HOG                        | Linear SVM, RBF SVM                                    |
| E6         | FFT/DCT frequency          | Logistic, SVM, Random Forest                           |
| E7         | HOG + LBP + color + FFT    | Logistic, Linear SVM, Random Forest, Gradient Boosting |
| E8         | PCA(combined features)     | RBF SVM, k-NN, MLP                                     |
| E9         | final tuned top 3          | locked test evaluation                                 |

The likely best candidates are:

```text
1. RBF SVM on PCA-compressed combined handcrafted features
2. Linear SVM on HOG + LBP + frequency features
3. Gradient Boosting / HistGradientBoosting on combined handcrafted features
4. Shallow MLP on PCA or combined features
```

My first bet would be:

> **PCA-whitened [HOG + LBP + color histograms + FFT radial spectrum] → RBF SVM**

This is course-aligned, nontrivial, and likely competitive.

# 7. Hyperparameter optimization

Use sklearn `Pipeline` objects so scaling, PCA, and model training are all cross-validated properly.

Example pipeline:

```text
FeatureExtractor
→ StandardScaler
→ PCA(optional)
→ Classifier
```

## 7.1. Search strategy

For cheap models:

```text
GridSearchCV, 5-fold stratified CV
```

For expensive models:

```text
RandomizedSearchCV, 3-fold or 5-fold stratified CV
```

Use log scales for parameters like:

```text
C
gamma
regularization strength
learning rate
```

The class notes explicitly recommend log-scale search for SVM parameters such as $C$ and $\gamma$. 

## 7.2. Tuning targets

Primary selection metric:

```text
ROC-AUC or F1
```

Since the dataset is balanced, accuracy is okay, but I would tune mainly on:

```text
F1
ROC-AUC
balanced accuracy
```

Then report all metrics on the test set.

## 7.3. Avoid optimistic bias

Do not select hyperparameters based on test results. The notes explicitly warn that reusing the same data for hyperparameter search and final evaluation induces optimistic bias. 

# 8. Metrics to report

Because this is binary and balanced, report both threshold metrics and ranking metrics.

## 8.1. Main table

For every model:

```text
Accuracy
Balanced accuracy
Precision
Recall
F1
ROC-AUC
PR-AUC
Cohen’s Kappa
Log loss, if model gives probabilities
Brier score, if calibrated probabilities are reported
Training time
Prediction time per image
Feature dimension
```

The course notes introduce accuracy, precision, recall, and F1 as standard classification metrics.  They also explicitly include ROC, Precision-Recall, and Cohen’s Kappa in the classifier-evaluation material.  Kappa is especially nice to include because it corrects agreement by chance and penalizes trivial majority-class behavior. 

## 8.2. Confidence intervals

For final top models:

```text
bootstrap 95% CI for accuracy, F1, ROC-AUC
```

Example:

```text
SVM RBF test accuracy = 0.94, 95% CI [0.932, 0.948]
```

This will make the report look more statistically mature.

## 8.3. Pairwise comparison

For the top two models:

```text
McNemar test on test-set predictions
```

This answers:

> Did model A really outperform model B, or is the difference likely due to test-sample variation?

Optional but good for a top grade.

# 9. Visualizations to include

## 9.1. Dataset visualizations

Include:

```text
class counts
random sample grid: real vs fake
image resolution distribution
RGB histogram by class
average real face
average fake face
difference heatmap: mean(fake) - mean(real)
```

The average/difference image can reveal whether the classifier might exploit alignment, background, color, or border artifacts.

## 9.2. Feature visualizations

For each major feature family:

```text
HOG visualization on sample images
LBP histogram comparison
FFT radial energy curves by class
color histogram overlays
PCA explained variance curve
```

The PCA explained-variance curve is important because it justifies the number of components. PCA’s role as dimensionality reduction is directly aligned with the class notes. 

## 9.3. Representation-space visualizations

Use:

```text
2D PCA scatter
t-SNE or UMAP scatter, only for visualization
Fisher/LDA 1D projection histogram
```

Do not use t-SNE/UMAP features for the main classifier unless justified. They are mainly visualization tools.

## 9.4. Model evaluation visualizations

Include:

```text
confusion matrix for top 3 models
ROC curves on same plot
Precision-Recall curves on same plot
calibration curve
threshold vs precision/recall/F1
```

## 9.5. Bias-variance / tuning visualizations

Include:

```text
learning curves: training size vs train/validation score
validation curve for SVM C
validation curve for SVM gamma
k-NN performance vs k
tree performance vs max_depth
Random Forest OOB error vs n_estimators
MLP train/validation loss over epochs
```

This is one of the best ways to show course understanding. The course repeatedly emphasizes that lower training error does not necessarily imply better generalization. 

## 9.6. Error analysis visualizations

For final model:

```text
top 20 false positives: real predicted fake with highest confidence
top 20 false negatives: fake predicted real with highest confidence
borderline cases near p(fake)=0.5
```

For each error group, write observations:

```text
Are errors caused by unusual lighting?
Occluded faces?
Heavy makeup?
Hair artifacts?
Background?
Low resolution?
Real images that look synthetic?
Fake images that look very natural?
```

This is a strong “data science” move because it connects quantitative results to domain insight.

# 10. Ablation studies

Ablation is essential for a high grade.

For the best model, compare:

| Features                  | Accuracy | F1 | ROC-AUC |
| ------------------------- | -------: | -: | ------: |
| color only                |          |    |         |
| texture only              |          |    |         |
| HOG only                  |          |    |         |
| frequency only            |          |    |         |
| HOG + texture             |          |    |         |
| HOG + texture + frequency |          |    |         |
| all features              |          |    |         |

Also compare:

```text
without PCA vs with PCA
with whitening vs without whitening
linear SVM vs RBF SVM
single tree vs Random Forest
Random Forest vs Gradient Boosting
logistic vs SVM
```

This is where the report can say things like:

> HOG alone captures geometric structure, but adding LBP and frequency features improves detection of synthetic texture artifacts. PCA reduces noise and improves k-NN/SVM stability. RBF SVM improves over linear SVM, suggesting the classes are not linearly separable in the engineered feature space.

# 11. Robustness checks

Even if not required, include at least two.

## 11.1. Resolution robustness

Evaluate final model on test images resized to:

```text
128×128
96×96
64×64
```

This tests whether the model depends on tiny artifacts.

## 11.2. Compression robustness

Apply JPEG compression to test copies:

```text
quality = 95, 75, 50
```

Report performance drop.

This is useful because real deployment often involves social-media compression.

## 11.3. Crop / border robustness

Evaluate with:

```text
center crop
remove 5% border
remove 10% border
```

If performance collapses after removing borders, the model may be exploiting dataset artifacts instead of facial content.

# 12. Final model selection

Pick the final model using validation performance, not test performance.

I would report:

```text
Best interpretable model:
    Logistic Regression or Linear SVM on engineered features

Best classical high-performance model:
    RBF SVM on PCA-compressed HOG + LBP + color + frequency features

Best ensemble:
    Gradient Boosting or Random Forest on combined features

Best neural model:
    Small MLP on PCA/combined features
```

Then, on the locked test set, report all four. This creates a balanced story:

1. Simple baseline.
2. Interpretable linear classifier.
3. Strong kernel classifier.
4. Ensemble classifier.
5. Shallow neural classifier.

# 13. Suggested final report structure

## 13.1. Introduction

Explain:

```text
Task: binary classification of real vs StyleGAN3 faces
Why it matters: synthetic media / image forensics
Constraint: course-aligned models, not heavy CNN/U-Net
Main contribution: systematic comparison of representations and classifiers
```

## 13.2. Dataset and EDA

Include:

```text
dataset size and balance
sample images
class distribution
resolution / color / metadata audit
duplicate checks
EDA plots
```

## 13.3. Methods

Split into:

```text
Preprocessing
Feature extraction
Dimensionality reduction
Classifiers
Hyperparameter tuning
Evaluation protocol
```

## 13.4. Results

Include:

```text
model comparison table
ROC/PR curves
confusion matrices
learning/validation curves
ablation study
```

## 13.5. Discussion

Discuss:

```text
Which features mattered most?
Which models overfit?
Did nonlinearity help?
Did ensembles help?
Did PCA/whitening help?
What errors remain?
Does the model rely on artifacts?
```

## 13.6. Conclusion

End with:

```text
Best model and performance
Main methodological lesson
Limitations
Future work
```

Future work can mention CNNs or transfer learning, but frame them as beyond the main course scope.


[1]: https://www.kaggle.com/datasets/troykueh/real-vs-fake-faces-stylegan3?utm_source=chatgpt.com "10000 Real vs Fake Faces (StyleGAN3)"
[2]: https://arxiv.org/abs/1903.06836?utm_source=chatgpt.com "Detecting GAN generated Fake Images using Co-occurrence Matrices"


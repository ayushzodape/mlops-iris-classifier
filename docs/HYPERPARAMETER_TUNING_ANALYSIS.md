# Hyperparameter Tuning Analysis

## 1. Baseline Model

### Model

DecisionTreeClassifier with default hyperparameters.

### Cross-Validation

The baseline model was evaluated using 5-fold cross-validation with
macro-averaged F1 score.

### Results

- CV F1 Macro: **0.9663**
- CV F1 Macro Standard Deviation: **0.0316**
- Test Accuracy: **0.9000**
- Total Cross-Validation Fits: **5**

The baseline model provides the reference point for evaluating the
hyperparameter tuning approaches.

---

## 2. Grid Search

### Model

RandomForestClassifier.

### Search Method

GridSearchCV was used to exhaustively evaluate every combination in the
specified hyperparameter grid.

The search space contained:

- `n_estimators`: 50, 100, 200
- `max_depth`: 3, 5, 10, None
- `min_samples_split`: 2, 5, 10
- `max_features`: sqrt, log2

This resulted in:

**3 × 4 × 3 × 2 = 72 combinations**

Using 5-fold cross-validation:

**72 × 5 = 360 total fits**

### Best Parameters

```text
max_depth = 3
max_features = sqrt
min_samples_split = 2
n_estimators = 50
Results

    Best CV F1 Macro: 0.9663

    Test Accuracy: 0.9667

    Total Fits: 360

Compared with the baseline, Grid Search increased test accuracy from
0.9000 to 0.9667.
3. Random Search
Model

RandomForestClassifier.
Search Method

RandomizedSearchCV was used to randomly sample 30 combinations from the
same general hyperparameter search space.

The search used:

    30 iterations

    5-fold cross-validation

    150 total model fits

Best Parameters

max_depth = 3
max_features = sqrt
min_samples_split = 6
n_estimators = 100

Results

    Best CV F1 Macro: 0.9663

    Test Accuracy: 0.9667

    Total Fits: 150

Random Search achieved the same measured CV F1 Macro and test accuracy
as Grid Search in this experiment.
4. Comparison
Method	Model	CV F1 Macro	Test Accuracy	Total Fits
Baseline	DecisionTreeClassifier	0.9663	0.9000	5
Grid Search	RandomForestClassifier	0.9663	0.9667	360
Random Search	RandomForestClassifier	0.9663	0.9667	150
Performance Comparison

The baseline achieved a CV F1 Macro of 0.9663 and a test accuracy of
0.9000.

Both Grid Search and Random Search achieved a CV F1 Macro of 0.9663 and
a test accuracy of 0.9667.

Therefore, the tuned Random Forest models improved test accuracy by
0.0667, or approximately 6.67 percentage points, compared with the
baseline.

The CV F1 Macro did not increase compared with the baseline.
Efficiency Comparison

Grid Search evaluated all 72 combinations in the specified search
space, resulting in 360 model fits using 5-fold cross-validation.

Random Search evaluated only 30 sampled combinations, resulting in 150
model fits.

Random Search therefore used:

150 / 360 × 100 ≈ 41.7%

of the model fits used by Grid Search.

This means Random Search used approximately 58.3% fewer model fits
than Grid Search while achieving the same measured CV F1 Macro and test
accuracy in this experiment.
Conclusion

For this Iris classification experiment, both hyperparameter tuning
approaches produced a higher test accuracy than the baseline model.

Grid Search and Random Search achieved identical measured performance,
with a CV F1 Macro of 0.9663 and test accuracy of 0.9667.

However, Random Search required only 150 model fits compared with 360
for Grid Search. Therefore, Random Search demonstrated better
computational efficiency in this experiment while achieving comparable
performance.

The results demonstrate that exhaustive Grid Search is not always
necessary when a sufficiently effective subset of the search space can
be sampled using Random Search.
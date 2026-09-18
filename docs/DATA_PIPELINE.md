# Data Pipeline

This project uses DVC to make the Iris data pipeline reproducible. The pipeline
collects the raw dataset, cleans it, derives model features, and validates the
final table before it is used for training.

## Pipeline Flow

```text
												 DVC dependency graph

	collect.py
			|
			|  writes
			v
	data/raw/iris_raw.csv
			|
			|  dependency of preprocess stage
			v
	preprocess.py  --------------------->  data/processed/iris_preprocessed.csv
																							 |
																							 |  dependency of features stage
																							 v
																					features.py
																							 |
																							 |  writes
																							 v
																					data/processed/iris_features.csv
																							 |
																							 |  dependency of validate stage
																							 v
																					validate.py
																							 |
																							 |  passes or exits with status 1
																							 v
																					Pipeline ready for training

	dvc.yaml stages:
	collect -> preprocess -> features -> validate

	collect:
		cmd: python src/pipeline/collect.py --output data/raw/iris_raw.csv
		deps: none declared
		outs: data/raw/iris_raw.csv

	preprocess:
		deps: data/raw/iris_raw.csv, src/pipeline/preprocess.py
		outs: data/processed/iris_preprocessed.csv

	features:
		deps: data/processed/iris_preprocessed.csv, src/pipeline/features.py
		outs: data/processed/iris_features.csv

	validate:
		deps: data/processed/iris_features.csv, src/pipeline/validate.py
		outs: none
```

The generated timestamp in the raw file means that rerunning collection
creates a new output. DVC tracks the resulting output as the input to the next
stage.

## Stages

### 1. Collect

**Purpose:** Simulate ingesting the Iris dataset from an external source and
store a raw, timestamped copy.

**Command:**

```bash
python src/pipeline/collect.py --output data/raw/iris_raw.csv
```

**Inputs:** The Iris dataset loaded through `sklearn.datasets.load_iris`.

**Outputs:** `data/raw/iris_raw.csv`, containing the four measurements, the
string target column `species`, and a UTC `collected_at` timestamp for each
row.

**Validation or transformations:** The numeric target values returned by
scikit-learn are mapped to `setosa`, `versicolor`, and `virginica`. The stage
logs the number of collected rows. No schema validation is performed here.

### 2. Preprocess

**Purpose:** Clean the raw table and prepare consistent numeric and target
columns for feature engineering.

**Command:**

```bash
python src/pipeline/preprocess.py \
	--input data/raw/iris_raw.csv \
	--output data/processed/iris_preprocessed.csv
```

**Inputs:** `data/raw/iris_raw.csv`.

**Outputs:** `data/processed/iris_preprocessed.csv`.

**Validation or transformations enforced:**

- Exact duplicate rows are removed.
- The four measurement columns are coerced to numeric values; values that
	cannot be converted become missing.
- Missing measurement values are imputed with the median of their column.
- Rows with a missing `species` value are removed because the target cannot be
	resolved.
- The collection-only `collected_at` column is dropped.

### 3. Features

**Purpose:** Add derived measurements that can be used by the model.

**Command:**

```bash
python src/pipeline/features.py \
	--input data/processed/iris_preprocessed.csv \
	--output data/processed/iris_features.csv
```

**Inputs:** `data/processed/iris_preprocessed.csv`.

**Outputs:** `data/processed/iris_features.csv`.

**Validation or transformations enforced:**

- `sepal_area` is calculated as sepal length multiplied by sepal width.
- `petal_area` is calculated as petal length multiplied by petal width.
- `sepal_to_petal_length_ratio` is calculated from the two length columns;
	zero petal lengths are replaced with missing values before division.
- `petal_length_bin` categorizes petal length into `short`, `medium`, or
	`long` using the boundaries `0-2`, `2-4.5`, and `4.5-7` cm.

This stage writes the engineered table but does not independently fail on
schema or range violations. Those checks are handled by the validation stage.

### 4. Validate

**Purpose:** Prevent invalid feature data from reaching model training. The
stage hard-stops the pipeline by exiting with status 1 when any check fails.

**Command:**

```bash
python src/pipeline/validate.py --input data/processed/iris_features.csv
```

**Inputs:** `data/processed/iris_features.csv`.

**Outputs:** No data file is produced. A successful run logs a pass message;
failure raises `DataValidationError` and exits non-zero.

**Validation rules enforced:**

- All expected columns must be present:
	`sepal length (cm)`, `sepal width (cm)`, `petal length (cm)`,
	`petal width (cm)`, `species`, `sepal_area`, `petal_area`,
	`sepal_to_petal_length_ratio`, and `petal_length_bin`.
- No null values may remain in any column.
- `species` values must be one of `setosa`, `versicolor`, or `virginica`.
- `sepal length (cm)` must be between `3.0` and `9.0`.
- `sepal width (cm)` must be between `1.5` and `5.5`.
- `petal length (cm)` must be between `0.5` and `8.0`.
- `petal width (cm)` must be between `0.05` and `3.0`.

All detected errors are logged before the stage raises the validation error.

## Running the Pipeline

Run every stage whose dependencies have changed with:

```bash
dvc repro
```

To inspect the declared dependency and output graph:

```bash
dvc dag
```

The final validated dataset is `data/processed/iris_features.csv`; the
validation stage confirms its contents but does not create a separate DVC
output.

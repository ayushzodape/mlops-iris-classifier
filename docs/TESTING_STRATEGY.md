Testing Strategy
1. Overview

This document describes the automated testing strategy for the Iris classification MLOps project.

The test suite uses pytest to verify data preprocessing, feature engineering, data validation, model training, prediction behavior, and model quality.

The pytest-cov plugin measures source-code coverage, while JUnit XML output provides test results in a format suitable for continuous integration (CI) systems.

2. Test Files and Coverage Layers
Test File	Testing Layer	Purpose
tests/test_preprocess.py	Data	Tests duplicate removal, missing numeric value imputation, missing target handling, and empty DataFrame behavior.
tests/test_features.py	Data	Tests sepal and petal area calculations, length ratio calculations, petal length categorization, and zero-division handling.
tests/test_validate.py	Data	Tests successful validation, missing columns, invalid species labels, and out-of-range numeric values.
tests/test_training_pipeline.py	Pipeline / Model	Tests model training, prediction output shape, and prediction probability sums.
tests/test_model_quality.py	Model Quality	Checks that predictions use known labels and model accuracy meets the minimum threshold.
3. Testing Layers
3.1 Data Layer

The data layer includes preprocessing, feature engineering, and validation tests.

These tests verify that input data is cleaned correctly, engineered features are calculated correctly, and invalid data is rejected.

3.2 Pipeline and Model Layer

The training smoke tests verify that a Random Forest classifier can be trained and used to make predictions.

They also verify that the prediction output has the expected shape and that predicted class probabilities sum to approximately one.

3.3 Model Quality Layer

The model quality tests use the processed Iris feature dataset to train and evaluate a Random Forest classifier.

The minimum acceptable accuracy is 0.90 (90%).

The quality gate is designed to fail when the measured accuracy falls below the configured threshold.

4. Test Execution Commands

Run all tests:

bash
pytest -v


Run all tests with source-code coverage:

bash
pytest --cov=src --cov-report=term-missing


Generate a JUnit XML report:

bash
pytest --cov=src --cov-report=term-missing --junitxml=test-results.xml

5. Coverage Results

The current coverage percentage must be recorded from the actual pytest-cov report.

Expected coverage targets for the core data-processing modules are:

Source File	Target Coverage	Actual Coverage
src/pipeline/preprocess.py	Above 85%	Update after execution
src/pipeline/features.py	Above 85%	Update after execution
src/pipeline/validate.py	Above 85%	Update after execution
Overall src package	Measure and record	Update after execution

Coverage is measured by pytest-cov. The actual percentages must be taken from the most recent test execution rather than assumed in advance.

6. Test Results and JUnit XML

The test suite produces test-results.xml when pytest is executed with the --junitxml option.

The report contains XML elements such as <testsuite> and <testcase> that record test execution results.

This report can be consumed by CI tools to display test summaries and identify failures.

7. Model Quality Gate Verification

The model quality test uses a minimum acceptable accuracy of 0.90.

To verify that the quality gate detects an accuracy regression, temporarily change the threshold to 0.99 and execute:

bash
pytest tests/test_model_quality.py -v


The test should fail if the measured accuracy is below 0.99.

After the experiment, restore the threshold to 0.90 and rerun the model quality tests.

8. Expected Outcome

The test suite should verify data processing, feature engineering, validation, model training, prediction behavior, and model quality.

The final execution results, actual coverage percentages, and JUnit XML report should be checked before submitting the practical.
CI Pipeline Documentation
1. Overview
This project uses GitHub Actions to implement a Continuous Integration (CI) pipeline for the MLOps Iris project. The workflow is defined in .github/workflows/ci.yml.
The pipeline automatically runs when code is pushed to the main or develop branches and when a pull request targets either of these branches.
The CI pipeline checks Python code quality, executes automated tests, generates test and coverage reports, and validates model accuracy against a predefined threshold.
2. CI Jobs
The workflow consists of three jobs.
2.1 Build and Lint
Job name: build-and-lint
Purpose: Verify that the Python source code compiles successfully and follows the configured linting standards.
Main steps:
    • Check out the repository.
    • Set up Python 3.11.
    • Install project dependencies, Flake8, and testing tools.
    • Compile the Python files in src and tests.
    • Run Flake8 on the source code.
Success condition: Python compilation and linting complete without errors.
2.2 Test Suite
Job name: test-suite
Dependency: needs: build-and-lint
Purpose: Execute the automated tests to verify the correctness of the data-processing pipeline and related functionality.
Main steps:
    • Check out the repository and set up Python 3.11.
    • Install project dependencies and testing tools.
    • Create the required data directories.
    • Collect the Iris dataset.
    • Preprocess the dataset.
    • Engineer features.
    • Execute the tests using pytest.
    • Generate test results and code coverage reports.
    • Upload the reports as a GitHub Actions artifact named test-and-coverage-reports.
The artifact contains test-results.xml and coverage.xml when both files are generated successfully.
Success condition: All tests pass.
2.3 Model Quality Gate
Job name: model-quality-gate
Dependency: needs: test-suite
Purpose: Verify that the model satisfies the minimum acceptable accuracy requirement.
Main steps:
    • Check out the repository and set up Python 3.11.
    • Install the required dependencies.
    • Prepare the Iris dataset by running the collection, preprocessing, and feature-engineering stages.
    • Execute tests/test_model_quality.py.
The normal minimum accuracy threshold is 0.90 (90%).
Success condition: The model-quality tests pass, including the minimum accuracy assertion.
3. Job Dependency Order
The jobs are configured with the following dependency sequence:
build-and-lint
      |
      v
  test-suite
      |
      v
model-quality-gate
The dependency configuration uses the needs keyword:
    • test-suite requires build-and-lint to succeed.
    • model-quality-gate requires test-suite to succeed.
Consequently, a failure in an upstream job causes downstream jobs to be skipped by default unless the workflow explicitly overrides this behavior.
4. Branch Protection Ruleset
A GitHub branch ruleset named Protect main - CI checks was configured to protect the main branch.
The ruleset includes:
    • Requiring changes to be submitted through a pull request.
    • Requiring the configured CI status checks to pass before merging.
    • Requiring branches to be up to date before merging, if enabled in the repository settings.
The required status checks selected in GitHub are:
    • build-and-lint
    • test-suite
    • model-quality-gate
This configuration helps prevent changes from being merged into main when the required checks fail.
5. Pull Request Verification
A feature branch named feature/ci-verification-test was created, and a harmless README change was committed and pushed.
A pull request was opened from this branch into main. The pull_request trigger started the GitHub Actions workflow, and all three jobs completed successfully.
The pull request was subsequently merged after the checks passed. This verified that the CI workflow runs on pull requests as intended.
6. Model-Quality Regression Demonstration
To test the pipeline's ability to detect a model-quality regression, a temporary branch named feature/simulate-regression was created.
The threshold in tests/test_model_quality.py was temporarily changed from:
MIN_ACCEPTABLE_ACCURACY = 0.90
to:
MIN_ACCEPTABLE_ACCURACY = 0.999
A pull request was opened from the temporary branch into main.
Observed results
    • Build and Lint: Passed.
    • Test Suite: Failed.
    • Model Quality Gate: Skipped because it depends on the successful completion of test-suite.
The test output reported an accuracy of approximately 0.9667 (96.67%), which was below the temporary threshold of 0.999 (99.9%). As a result, the assertion in test_model_meets_minimum_accuracy_threshold failed.
The complete test suite reported 15 passed tests and 1 failed test. The failure demonstrated that the CI workflow detects a model that does not satisfy the configured accuracy requirement.
The demonstration pull request was not merged. The temporary branch was deleted, and the normal accuracy threshold of 0.90 was verified on main.
Note: The regression was detected by the model-quality test within test-suite. The separate model-quality-gate job was skipped because of its configured dependency. Thus, the experiment demonstrated regression detection, but the dedicated model-quality job did not independently execute during this failure scenario.
7. Conclusion
The GitHub Actions CI pipeline automates code compilation, linting, testing, report generation, and model-quality validation. Pull-request checks and branch protection provide safeguards for changes targeting main.
The successful normal pipeline run and the deliberately introduced regression provide evidence that the workflow executes correctly and detects a model-quality threshold violation.

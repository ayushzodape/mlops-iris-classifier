# Iris Feast Practical

This repository demonstrates Feast with the Iris dataset. The feature repository:

* `data/iris_features.parquet` contains the Iris measurements and engineered features.
* `features.py` defines the `sample_id` entity, two feature views, and one feature service.
* `feature_store.yaml` configures local registry, offline, and SQLite online stores.
* `test_workflow.py` applies the definitions, retrieves historical features, materializes the online store, and retrieves online features.

## Run the practical

From `feature_repo/`, use the Feast virtual environment created for this practical:

```bash
# 1. Generate the feature-engineered CSV through the existing project pipeline.
cd /path/to/mlops-iris-classifier
python src/pipeline/features.py --input data/processed/iris_preprocessed.csv --output data/processed/iris_features.csv

# 2. Enter the Feast feature repository.
cd practical5_feast/iris_feature_repo/feature_repo

# 3. Convert the CSV into a Feast source with entity and event-time columns.
../../.venv-feast/bin/python prepare_feature_source.py

# 4. Apply entities, data source, feature views, and feature service.
../../.venv-feast/bin/feast apply

# 5. Run historical retrieval, batch scoring retrieval, materialization,
#    direct online retrieval, and feature-service retrieval.
../../.venv-feast/bin/python test_workflow.py

# 6. Inspect the registered objects.
../../.venv-feast/bin/feast entities list
../../.venv-feast/bin/feast feature-views list
../../.venv-feast/bin/feast feature-services list
```

The workflow ends with `Iris Feast workflow completed successfully.` when all retrieval checks pass.

## Completed stages

1. Existing Iris pipeline produces the feature-engineered CSV.
2. Feast source preparation adds `sample_id`, `event_timestamp`, and `created_timestamp`.
3. `features.py` defines the entity, file source, measurement feature view, engineered feature view, and feature service.
4. `feast apply` registers the definitions in the local registry.
5. Historical retrieval produces training features.
6. Historical retrieval with current timestamps produces batch-scoring features.
7. Incremental materialization loads both feature views into SQLite.
8. Online retrieval works through direct feature references and the feature service.

## To move from this into a more production ready workflow:
> See more details in [Running Feast in production](https://docs.feast.dev/how-to-guides/running-feast-in-production)

1. First: you should start with a different Feast template, which delegates to a more scalable offline store.
   - For example, running `feast init -t gcp`
   or `feast init -t aws` or `feast init -t snowflake`.
   - You can see your options if you run `feast init --help`.
2. `feature_store.yaml` points to a local file as a registry. You'll want to setup a remote file (e.g. in S3/GCS) or a
SQL registry. See [registry docs](https://docs.feast.dev/getting-started/concepts/registry) for more details.
3. This example uses a file [offline store](https://docs.feast.dev/getting-started/components/offline-store)
   to generate training data. It does not scale. We recommend instead using a data warehouse such as BigQuery,
   Snowflake, Redshift. There is experimental support for Spark as well.
4. Setup CI/CD + dev vs staging vs prod environments to automatically update the registry as you change Feast feature definitions. See [docs](https://docs.feast.dev/how-to-guides/running-feast-in-production#1.-automatically-deploying-changes-to-your-feature-definitions).
5. (optional) Regularly scheduled materialization to power low latency feature retrieval (e.g. via Airflow). See [Batch data ingestion](https://docs.feast.dev/getting-started/concepts/data-ingestion#batch-data-ingestion)
for more details.
6. (optional) Deploy feature server instances with `feast serve` to expose endpoints to retrieve online features.
   - See [Python feature server](https://docs.feast.dev/reference/feature-servers/python-feature-server) for details.
   - Use cases can also directly call the Feast client to fetch features as per [Feature retrieval](https://docs.feast.dev/getting-started/concepts/feature-retrieval)
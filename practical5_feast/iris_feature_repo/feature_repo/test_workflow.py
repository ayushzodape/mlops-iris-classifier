from datetime import datetime, timezone

import pandas as pd

from feast import FeatureStore

from features import (
    iris_engineered_fv,
    iris_feature_service,
    iris_measurements_fv,
)


def run_demo():
    store = FeatureStore(repo_path=".")
    source_df = pd.read_parquet("data/iris_features.parquet")

    print("\n--- Apply Iris feature definitions ---")
    store.apply([iris_measurements_fv, iris_engineered_fv, iris_feature_service])

    print("\n--- Historical features for training ---")
    historical_df = fetch_historical_features(store, source_df)
    print(historical_df.head())
    assert len(historical_df) == 3
    assert_expected_features(historical_df)

    print("\n--- Historical features for batch scoring ---")
    batch_scoring_df = fetch_batch_scoring_features(store, source_df)
    print(batch_scoring_df.head())
    assert len(batch_scoring_df) == 3
    assert_expected_features(batch_scoring_df)

    print("\n--- Load features into online store ---")
    store.materialize_incremental(end_date=datetime.now(timezone.utc))

    print("\n--- Online features ---")
    online_df = fetch_online_features(store)
    print(online_df)
    assert len(online_df) == 2
    assert_online_features(online_df)

    print("\n--- Online features retrieved through the feature service ---")
    service_online_df = fetch_online_features(store, use_feature_service=True)
    print(service_online_df)
    assert_online_features(service_online_df)

    print("\nIris Feast workflow completed successfully.")


def fetch_historical_features(store: FeatureStore, source_df: pd.DataFrame):
    entity_df = source_df[["sample_id", "event_timestamp"]].head(3)
    return store.get_historical_features(
        entity_df=entity_df,
        features=[
            "iris_measurements:sepal length (cm)",
            "iris_measurements:sepal width (cm)",
            "iris_measurements:petal length (cm)",
            "iris_measurements:petal width (cm)",
            "iris_engineered_features:sepal_area",
            "iris_engineered_features:petal_area",
            "iris_engineered_features:sepal_to_petal_length_ratio",
            "iris_engineered_features:petal_length_bin",
        ],
    ).to_df()


def fetch_batch_scoring_features(store: FeatureStore, source_df: pd.DataFrame):
    entity_df = source_df[["sample_id"]].head(3).copy()
    entity_df["event_timestamp"] = pd.Timestamp.now(tz="UTC")
    return store.get_historical_features(
        entity_df=entity_df,
        features=iris_feature_service,
    ).to_df()


def fetch_online_features(store: FeatureStore, use_feature_service: bool = False):
    entity_rows = [
        {"sample_id": 0},
        {"sample_id": 1},
    ]
    features = (
        store.get_feature_service("iris_feature_service")
        if use_feature_service
        else [
            "iris_measurements:sepal length (cm)",
            "iris_measurements:sepal width (cm)",
            "iris_engineered_features:sepal_area",
            "iris_engineered_features:petal_area",
        ]
    )
    return store.get_online_features(
        features=features,
        entity_rows=entity_rows,
    ).to_df()


def assert_expected_features(features_df: pd.DataFrame):
    expected_features = {
        "sepal length (cm)",
        "sepal width (cm)",
        "petal length (cm)",
        "petal width (cm)",
        "sepal_area",
        "petal_area",
        "sepal_to_petal_length_ratio",
        "petal_length_bin",
    }
    assert expected_features.issubset(features_df.columns)


def assert_online_features(features_df: pd.DataFrame):
    assert len(features_df) == 2
    assert features_df.drop(columns=["sample_id"]).notna().all().all()


if __name__ == "__main__":
    run_demo()

# Feature Store Analysis

## Overview

Feast was used to manage and serve the Iris dataset features for both
online inference and offline model training.

The feature repository contains one entity and two FeatureViews:

- Entity: `sample_id`
- FeatureView: `iris_measurements`
- FeatureView: `iris_engineered_features`

A Feature Service named `iris_feature_service` combines the registered
features for model consumption.

## 1. Elimination of Training-Serving Skew

A major benefit observed in this practical is the reduction of
training-serving skew.

The same registered feature definitions are used for both online and
offline retrieval.

In Step 6, the `iris_measurements` and `iris_engineered_features`
FeatureViews were retrieved from the online store using:

```python
store.get_online_features(...)

The retrieved values included:

    sepal length (cm)

    sepal width (cm)

    petal length (cm)

    petal width (cm)

    sepal_area

    petal_area

    sepal_to_petal_length_ratio

    petal_length_bin

In Step 7, the same registered FeatureViews were retrieved historically
using:

store.get_historical_features(...)

This means the feature definitions are not separately reimplemented
for training and serving. The same Feast definitions are used in both
paths.

Therefore, the practical demonstrates how a feature store can help
reduce inconsistencies between training-time and serving-time feature
calculation.
2. Feature Reusability

The registered features can be reused by different model workflows
without reimplementing the feature transformations.

In Step 8, the iris_feature_service was used to retrieve the
registered Iris features:

store.get_feature_service("iris_feature_service")

The Feature Service provided both the original Iris measurements and
the engineered features.

This demonstrates that downstream models can consume centrally
registered features rather than independently recreating calculations
such as:

    sepal_area

    petal_area

    sepal_to_petal_length_ratio

    petal_length_bin

Feature reuse reduces duplicated feature-engineering code and makes
feature consumption more consistent across models.
3. Centralized Feature Governance

The file features.py acts as the central definition of the Feast
features used in this practical.

It defines:

    the sample_id entity

    the Iris Parquet data source

    the iris_measurements FeatureView

    the iris_engineered_features FeatureView

    the iris_feature_service

This provides a single location where feature definitions, schemas,
data sources, and feature-service membership are specified.

The definitions are registered with Feast using:

feast apply

This provides a centralized and reproducible way to manage the
features consumed by different model workflows.
4. Online Feature Serving

The features were materialized into the local SQLite online store.

The online retrieval test successfully returned populated feature
values for sample_id = 1.

For example:

sepal length (cm) = 4.9
sepal width (cm) = 3.0
petal length (cm) = 1.4
petal width (cm) = 0.2
sepal_area = 14.7
petal_area = 0.28
sepal_to_petal_length_ratio = 3.5
petal_length_bin = short

This demonstrates that the registered features can be retrieved through
Feast's online serving path.
5. Historical Feature Retrieval

The historical retrieval test used the entity dataframe containing
sample_id and event_timestamp.

Feast successfully returned historical values for the first five
samples.

The retrieved dataset included both the original measurements and the
engineered features.

The use of timestamps enables point-in-time historical retrieval,
which is important when constructing training datasets.
6. Observed Benefits

The practical demonstrated the following feature-store benefits:

    Reduced training-serving skew
    The same registered FeatureViews are used for online serving and
    offline historical retrieval.

    Feature reusability
    The Feature Service allows different model workflows to consume
    the same registered features without reimplementing feature
    transformations.

    Centralized governance
    features.py provides a central definition of the entity, data
    source, FeatureViews, schemas, and Feature Service.

    Consistent feature schemas
    Feast explicitly defines feature names and data types, helping
    maintain consistency between consumers.

    Point-in-time correctness
    Event timestamps allow historical feature retrieval based on the
    appropriate time associated with each entity observation.

7. Verification Results

The Feast repository was successfully applied with:

    1 entity: sample_id

    2 FeatureViews:

        iris_measurements

        iris_engineered_features

    1 Feature Service:

        iris_feature_service

The feature source contains 149 rows and 12 columns, including
sample_id, event_timestamp, and created_timestamp.

The online retrieval test successfully returned populated values for
sample_id = 1.

The historical retrieval test successfully returned 5 rows because
the demonstration script intentionally uses:

.head(5)

The Feature Service retrieval test also completed successfully.
8. Conclusion

This practical demonstrates how Feast can act as a centralized feature
store for machine-learning workflows.

The Iris features are defined once, registered centrally, materialized
for online serving, and retrieved historically for training.

The same registered feature definitions can therefore be reused across
different model workflows while reducing duplicated feature-engineering
logic and inconsistencies between training and inference.
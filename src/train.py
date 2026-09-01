"""
train.py
Baseline training script for the Iris classifier.
Used to demonstrate a version-controlled ML project structure.
"""

from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


def load_data():
    iris = load_iris()
    return train_test_split(
        iris.data,
        iris.target,
        test_size=0.2,
        random_state=42,
    )


def train_model(X_train, y_train, n_estimators=100, max_depth=None):
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42,
    )
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)
    return acc, report


def main():
    X_train, X_test, y_train, y_test = load_data()
    model = train_model(X_train, y_train)
    acc, report = evaluate_model(model, X_test, y_test)

    print(f"Accuracy: {acc:.4f}")
    print(report)

    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)
    model_path = model_dir / "iris_model.joblib"
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")


if __name__ == "__main__":
    main()
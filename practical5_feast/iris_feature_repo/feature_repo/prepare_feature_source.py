# prepare_feature_source.py
"""
Prepares the iris_features.csv from Experiment 4 into a Feast-ready
Parquet source with entity IDs and event timestamps.
"""
from pathlib import Path

import pandas as pd

repo_root = Path(__file__).resolve().parents[3]
input_file = repo_root / "data/processed/iris_features.csv"
output_file = Path(__file__).resolve().parent / "data/iris_features.parquet"

# Read feature-engineered data
df = pd.read_csv(input_file)

# Create sample_id
df.insert(0, "sample_id", range(len(df)))

# Create event timestamps
start_time = pd.Timestamp(
    "2026-08-15 15:20:02",
    tz="UTC"
)
df["event_timestamp"] = pd.date_range(
    start=start_time,
    periods=len(df),
    freq="min"
)

# Created timestamp
df["created_timestamp"] = df["event_timestamp"]

# Create output directory
output_file.parent.mkdir(
    parents=True,
    exist_ok=True
)

# Save as Parquet
df.to_parquet(
    output_file,
    index=False
)

print(
    f"Wrote {len(df)} rows to {output_file}"
)

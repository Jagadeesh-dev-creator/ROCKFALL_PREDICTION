"""
Rockfall Risk Prediction Model Training (real dataset)
Uses merged_dataset.csv produced from weather + slope + rock samples.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[1] / "dataset" / "merged_dataset.csv"
META_PATH = Path(__file__).resolve().parents[1] / "python_ml" / "models" / "feature_metadata.pkl"


FEATURE_COLUMNS = [
    "temperature_c",
    "humidity_pct",
    "wind_speed",
    "cloud_cover_pct",
    "pressure_hpa",
    "rain_flag",
    "slope_angle_deg",
    "cohesion_kpa",
    "friction_angle_deg",
    "slope_height_m",
    "unit_weight_knm3",
    "pore_water_pressure_ratio",
    "reinforcement_numeric",
    "factor_of_safety",
    "compressive_strength_mpa",
]


def label_risk(row: pd.Series) -> int:
    """Rule-based labeling to create targets from real features."""
    score = 0.0
    score += (row["slope_angle_deg"] / 90.0) * 0.35
    score += row["rain_flag"] * 0.25
    score += max(0.0, (1.5 - row["factor_of_safety"]) / 1.5) * 0.25
    score += max(0.0, (25.0 - row["cohesion_kpa"]) / 25.0) * 0.1
    score += max(0.0, (row["wind_speed"] - 12.0) / 18.0) * 0.05

    if score < 0.35:
        return 0  # Low
    if score < 0.55:
        return 1  # Medium
    return 2  # High


def load_dataset(path: Path):
    print(f"📂 Loading dataset from: {path}")
    df = pd.read_csv(path)

    missing = [c for c in FEATURE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in dataset: {missing}")

    df = df.dropna(subset=FEATURE_COLUMNS).copy()
    df["risk"] = df.apply(label_risk, axis=1)

    X = df[FEATURE_COLUMNS]
    y = df["risk"]
    print(f"✅ Loaded {len(df)} rows after dropping NaNs")
    return X, y, df


def train_model(data_path: Path = DATA_PATH):
    print("🚀 Starting Rockfall Prediction Model Training...")
    X, y, df = load_dataset(data_path)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=200, random_state=42, max_depth=12)
    model.fit(X_train, y_train)
    print("✅ Model trained successfully")

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"📊 Model Accuracy: {accuracy:.2%}")
    print("\n📈 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["Low", "Medium", "High"]))

    os.makedirs("models", exist_ok=True)
    model_path = "models/rockfall_model.pkl"
    joblib.dump(model, model_path)
    print(f"💾 Model saved to {model_path}")

    # Persist feature statistics for inference defaults
    feature_means = X.mean(numeric_only=True).to_dict()
    metadata = {
        "feature_means": feature_means,
        "feature_columns": FEATURE_COLUMNS,
    }
    joblib.dump(metadata, META_PATH)
    print(f"🧭 Feature metadata saved to {META_PATH}")
    return model


if __name__ == "__main__":
    train_model()
    print("\n✨ Training complete! Ready for predictions.")

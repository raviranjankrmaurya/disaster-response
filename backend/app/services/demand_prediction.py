"""
Resource Demand Prediction Engine.

Trains on backend/data/historical_disasters.csv if present. That file
ships with PLACEHOLDER/illustrative numbers only, not verified real
relief-response data — replace it with real NDMA/SDMA/EM-DAT figures
before trusting predictions for anything real. Falls back to synthetic
data if the CSV is missing or too small to train on.
"""

import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

SEVERITY_MAP = {"low": 1, "moderate": 2, "high": 3, "critical": 4}
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "historical_disasters.csv")
MIN_ROWS_TO_TRAIN_ON_CSV = 5


def _load_csv_training_data():
    if not os.path.exists(CSV_PATH):
        return None
    df = pd.read_csv(CSV_PATH)
    if len(df) < MIN_ROWS_TO_TRAIN_ON_CSV:
        return None
    df["severity_num"] = df["severity"].map(SEVERITY_MAP)
    X = df[["population", "vulnerable_pct", "severity_num"]].values
    y = df[["food_packets", "water_liters", "medical_kits", "shelter_capacity"]].values
    return X, y


def _generate_synthetic_training_data(n=500, seed=42):
    rng = np.random.default_rng(seed)
    population = rng.integers(100, 50000, n)
    vulnerable_pct = rng.uniform(0, 0.5, n)
    severity = rng.integers(1, 5, n)

    food = population * 0.6 * (1 + vulnerable_pct) * (severity / 2)
    water = population * 3 * (1 + vulnerable_pct) * (severity / 2)
    medical = population * 0.02 * (1 + vulnerable_pct * 2) * severity
    shelter = population * 0.15 * severity

    X = np.column_stack([population, vulnerable_pct, severity])
    y = np.column_stack([food, water, medical, shelter])
    return X, y


class DemandPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self._fit()

    def _fit(self):
        csv_data = _load_csv_training_data()
        if csv_data is not None:
            X, y = csv_data
            self.trained_on = "historical_csv"
        else:
            X, y = _generate_synthetic_training_data()
            self.trained_on = "synthetic"
        self.model.fit(X, y)

    def predict(self, population: int, vulnerable_pct: float, severity: str):
        sev_num = SEVERITY_MAP.get(severity, 2)
        X = np.array([[population, vulnerable_pct, sev_num]])

        tree_preds = np.array([tree.predict(X)[0] for tree in self.model.estimators_])
        mean_pred = tree_preds.mean(axis=0)
        std_pred = tree_preds.std(axis=0)

        return {
            "predicted_food_packets": round(float(mean_pred[0]), 1),
            "predicted_water_liters": round(float(mean_pred[1]), 1),
            "predicted_medical_kits": round(float(mean_pred[2]), 1),
            "predicted_shelter_capacity": round(float(mean_pred[3]), 1),
            "confidence_low": round(float(mean_pred.sum() - std_pred.sum()), 1),
            "confidence_high": round(float(mean_pred.sum() + std_pred.sum()), 1),
        }


predictor = DemandPredictor()

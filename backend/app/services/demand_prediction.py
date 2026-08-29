"""
Resource Demand Prediction Engine.

Trains on a BLEND of two sources:
  1. Synthetic data, scaled to match this app's typical zone size
     (hundreds to tens of thousands of people per zone).
  2. Real, cited figures for 4 major Indian disasters in
     backend/data/historical_disasters.csv — see backend/data/SOURCES.md.

Why blend instead of using only real data: the real events are
state/national-scale aggregates (100K to 15M people), while this app's
zones are city/district-scale (thousands to tens of thousands). Training
on the real rows ALONE was tested and produces nonsensical output for
normal zone sizes — e.g. predicting more food packets than the zone's
entire population, because a model trained only on million-scale inputs
extrapolates wildly for a 40,000-person zone it never saw an example of.
Blending keeps predictions sane at the scale this app actually uses,
while still letting real severity-classification signal from actual
disasters inform the model — a real (if partial) improvement over pure
synthetic data, without reintroducing the scale problem.

Still true regardless: 4 real events is nowhere near enough for a
statistically valid model. Add more real events, ideally at
district/city granularity matching this app's zones, over time.
"""

import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

SEVERITY_MAP = {"low": 1, "moderate": 2, "high": 3, "critical": 4}
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "historical_disasters.csv")
MIN_ROWS_TO_INCLUDE_CSV = 1


def _load_csv_training_rows():
    if not os.path.exists(CSV_PATH):
        return None
    df = pd.read_csv(CSV_PATH)
    if len(df) < MIN_ROWS_TO_INCLUDE_CSV:
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
    # Medical kits: WHO Interagency Emergency Health Kit (IEHK) ratio —
    # 1 kit covers ~10,000 people for ~3 months. Scaled up a little by
    # severity/vulnerability since worse-hit, more vulnerable zones need
    # kits turned over faster, but kept anchored to the real WHO ratio
    # rather than an arbitrary multiplier (this was previously miscalibrated
    # ~100x too high — see backend/data/SOURCES.md for the cited ratio).
    medical = (population / 10000) * (1 + vulnerable_pct) * (severity / 2)
    shelter = population * 0.15 * severity

    X = np.column_stack([population, vulnerable_pct, severity])
    y = np.column_stack([food, water, medical, shelter])
    return X, y


class DemandPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self._fit()

    def _fit(self):
        X_synth, y_synth = _generate_synthetic_training_data()
        csv_rows = _load_csv_training_rows()

        if csv_rows is not None:
            X_csv, y_csv = csv_rows
            X = np.vstack([X_synth, X_csv])
            y = np.vstack([y_synth, y_csv])
            self.trained_on = "synthetic + historical_csv (blended, see data/SOURCES.md)"
        else:
            X, y = X_synth, y_synth
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

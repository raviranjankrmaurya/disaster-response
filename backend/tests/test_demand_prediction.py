import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.demand_prediction import predictor


def test_predict_returns_expected_keys():
    result = predictor.predict(population=10000, vulnerable_pct=0.2, severity="moderate")
    expected_keys = {
        "predicted_food_packets", "predicted_water_liters",
        "predicted_medical_kits", "predicted_shelter_capacity",
        "confidence_low", "confidence_high",
    }
    assert expected_keys.issubset(result.keys())


def test_predictions_are_non_negative():
    result = predictor.predict(population=10000, vulnerable_pct=0.2, severity="critical")
    for key in ["predicted_food_packets", "predicted_water_liters", "predicted_medical_kits", "predicted_shelter_capacity"]:
        assert result[key] >= 0


def test_higher_population_increases_demand():
    small = predictor.predict(population=1000, vulnerable_pct=0.2, severity="moderate")
    large = predictor.predict(population=50000, vulnerable_pct=0.2, severity="moderate")
    assert large["predicted_food_packets"] > small["predicted_food_packets"]
    assert large["predicted_water_liters"] > small["predicted_water_liters"]


def test_confidence_interval_is_ordered():
    result = predictor.predict(population=10000, vulnerable_pct=0.2, severity="high")
    assert result["confidence_low"] <= result["confidence_high"]


def test_unknown_severity_falls_back_gracefully():
    result = predictor.predict(population=5000, vulnerable_pct=0.15, severity="unknown_value")
    assert result["predicted_food_packets"] >= 0

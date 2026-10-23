import pytest
from backend.app.services.risk_service import RiskAnalysisEngine

def test_compute_heat_index():
    # Heat index for 25C with normal humidity should be close to 25C
    hi = RiskAnalysisEngine.compute_heat_index(25.0, 45.0)
    assert isinstance(hi, float)
    assert 20.0 <= hi <= 30.0

def test_evaluate_risk():
    sample_records = [
        {"temp_c": 24.0 + (i % 3), "precip_mm": 1.2 * (i % 2)}
        for i in range(30)
    ]
    res = RiskAnalysisEngine.evaluate_risk(35.6892, 51.3890, sample_records)
    assert "overall_score" in res
    assert "level" in res
    assert "metrics" in res
    assert res["metrics"]["avg_temp_c"] > 0
    assert "precip_sum_mm" in res["metrics"]
    assert "temp_volatility" in res["metrics"]

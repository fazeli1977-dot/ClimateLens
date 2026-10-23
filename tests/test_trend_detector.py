import pytest
from backend.app.services.trend_detector import EarthSystemTrendDetective

def test_mann_kendall_positive_trend():
    detective = EarthSystemTrendDetective()
    # Monotonically increasing synthetic climate series (e.g. rising surface temps)
    timeseries = [{"year": y, "value": 20.0 + (i * 0.4)} for i, y in enumerate(range(2000, 2024))]
    res = detective.detect_trends(lat=35.68, lon=51.38, variable_name="Surface Temperature", units="°C", timeseries=timeseries)
    
    assert res["statistics"]["is_statistically_significant"] is True
    assert "Increasing" in res["statistics"]["trend_classification"]
    assert res["statistics"]["sen_slope_per_decade"] > 0
    assert res["statistics"]["p_value"] < 0.05

def test_mann_kendall_stable_series():
    detective = EarthSystemTrendDetective()
    # Fluctuation around mean with no trend
    vals = [15.1, 14.9, 15.2, 14.8, 15.0, 15.1, 14.9, 15.2, 14.8, 15.0]
    timeseries = [{"year": 2000 + i, "value": v} for i, v in enumerate(vals)]
    res = detective.detect_trends(lat=0.0, lon=0.0, variable_name="Precipitation", units="mm/day", timeseries=timeseries)
    
    assert res["statistics"]["is_statistically_significant"] is False
    assert res["statistics"]["p_value"] >= 0.05
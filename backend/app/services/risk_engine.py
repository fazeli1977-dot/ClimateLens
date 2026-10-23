from typing import List, Dict, Any

def compute_heat_index(temp_c: float, rh_pct: float) -> float:
    """Simplified heat index approximation in Celsius."""
    if temp_c < 27.0:
        return temp_c
    tf = (temp_c * 9/5) + 32
    hi_f = 0.5 * (tf + 61.0 + ((tf - 68.0) * 1.2) + (rh_pct * 0.094))
    if hi_f >= 80:
        hi_f = (-42.379 + 2.04901523 * tf + 10.14333127 * rh_pct
                - 0.22475541 * tf * rh_pct - 0.00683783 * tf**2
                - 0.05481717 * rh_pct**2 + 0.00122874 * tf**2 * rh_pct
                + 0.00085282 * tf * rh_pct**2 - 0.00000199 * tf**2 * rh_pct**2)
    return round((hi_f - 32) * 5/9, 2)

def calculate_climate_risk(timeline: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculates multidimensional Climate Risk Score (0-100)."""
    if not timeline:
        return {"overall_score": 0, "level": "Unknown", "factors": {}}
        
    temps = [day["temp_c"] for day in timeline if day.get("temp_c") is not None and day["temp_c"] > -90]
    humidities = [day["humidity_pct"] for day in timeline if day.get("humidity_pct") is not None and day["humidity_pct"] >= 0]
    precips = [day["precip_mm"] for day in timeline if day.get("precip_mm") is not None and day["precip_mm"] >= 0]
    
    avg_temp = sum(temps) / len(temps) if temps else 0
    avg_rh = sum(humidities) / len(humidities) if humidities else 0
    total_precip = sum(precips) if precips else 0
    
    # 1. Thermal Stress Factor (0 - 40 pts)
    hi = compute_heat_index(avg_temp, avg_rh)
    thermal_stress = min(40, max(0, (hi - 25) * 2.5)) if hi > 25 else 0
    
    # 2. Drought Factor (0 - 35 pts)
    drought_risk = min(35, max(0, (30 - total_precip) * 1.16))
    
    # 3. Volatility Factor (0 - 25 pts)
    temp_range = (max(temps) - min(temps)) if temps else 0
    volatility = min(25, temp_range * 1.5)
    
    total_risk = round(thermal_stress + drought_risk + volatility, 1)
    
    level = "Low"
    if total_risk >= 70:
        level = "Critical"
    elif total_risk >= 45:
        level = "High"
    elif total_risk >= 25:
        level = "Moderate"
        
    return {
        "overall_score": total_risk,
        "level": level,
        "metrics": {
            "avg_temp_c": round(avg_temp, 1),
            "heat_index_c": round(hi, 1),
            "total_precip_mm": round(total_precip, 1),
            "temp_variation_c": round(temp_range, 1)
        },
        "breakdown": {
            "thermal_stress_score": round(thermal_stress, 1),
            "drought_risk_score": round(drought_risk, 1),
            "volatility_score": round(volatility, 1)
        }
    }

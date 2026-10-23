from typing import Dict, Any, List
import math

class RiskAnalysisEngine:
    @staticmethod
    def compute_heat_index(temp_c: float, rel_humidity: float = 45.0) -> float:
        t = (temp_c * 9/5) + 32
        rh = rel_humidity
        hi = 0.5 * (t + 61.0 + ((t - 68.0) * 1.2) + (rh * 0.094))
        if hi >= 80:
            hi = (-42.379 + 2.04901523*t + 10.14333127*rh - 0.22475541*t*rh 
                  - 6.83783e-3*(t**2) - 5.481717e-2*(rh**2) + 1.22874e-3*(t**2)*rh 
                  + 8.5282e-4*t*(rh**2) - 1.99e-6*(t**2)*(rh**2))
        return round((hi - 32) * 5/9, 1)

    @classmethod
    def evaluate_risk(cls, lat: float, lon: float, climate_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        temps = [r["temp_c"] for r in climate_records]
        precips = [r["precip_mm"] for r in climate_records]
        
        avg_temp = sum(temps) / len(temps)
        precip_total = sum(precips)
        variance = sum((x - avg_temp) ** 2 for x in temps) / len(temps)
        volatility = math.sqrt(variance)
        
        heat_idx = cls.compute_heat_index(avg_temp)
        
        temp_score = min(40.0, max(5.0, (avg_temp + 15) * 0.8))
        drought_score = max(5.0, 35.0 - (precip_total * 0.4))
        volatility_score = min(25.0, volatility * 3.5)
        
        overall = round(temp_score + drought_score + volatility_score, 1)
        
        if overall >= 75:
            level = "Critical"
            badge_color = "#e11d48"
            advisory = "Extreme anomaly: High vulnerability to wildfire and heat stress."
        elif overall >= 55:
            level = "High"
            badge_color = "#f59e0b"
            advisory = "Elevated risk: Thermal stress alert and irrigation deficits detected."
        elif overall >= 35:
            level = "Moderate"
            badge_color = "#eab308"
            advisory = "Moderate resilience: Routine seasonal baseline fluctuations observed."
        else:
            level = "Low"
            badge_color = "#10b981"
            advisory = "Optimal buffer: Stable moisture balance and balanced temperatures."

        # 7-day trend extrapolation
        trend_direction = "Increasing" if temps[-1] > avg_temp else "Stable"

        return {
            "overall_score": overall,
            "level": level,
            "badge_color": badge_color,
            "advisory": advisory,
            "trend": trend_direction,
            "metrics": {
                "avg_temp_c": round(avg_temp, 1),
                "heat_index_c": heat_idx,
                "precip_sum_mm": round(precip_total, 1),
                "temp_volatility": round(volatility, 1)
            }
        }

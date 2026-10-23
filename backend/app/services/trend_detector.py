import math
from typing import Dict, List, Any, Optional

class EarthSystemTrendDetective:
    """
    Scientific Trend Detection Engine designed for NASA Space Apps Challenge 2026.
    Evaluates:
      1. What is changing (variable metric)
      2. Where it is changing (spatial coordinates)
      3. How much it is changing (Sen's decadal slope & relative drift)
      4. If changes are statistically significant (Mann-Kendall Tau & p-value)
    """

    @staticmethod
    def calculate_sen_slope(years: List[int], values: List[float]) -> float:
        """Computes Theil-Sen Median Slope (change per year). Robust against outliers."""
        n = len(values)
        if n < 2:
            return 0.0
        
        slopes = []
        for i in range(n):
            for j in range(i + 1, n):
                dy = values[j] - values[i]
                dx = years[j] - years[i]
                if dx != 0:
                    slopes.append(dy / dx)
        
        if not slopes:
            return 0.0
        slopes.sort()
        mid = len(slopes) // 2
        if len(slopes) % 2 == 0:
            return (slopes[mid - 1] + slopes[mid]) / 2.0
        return slopes[mid]

    @staticmethod
    def mann_kendall_test(values: List[float], alpha: float = 0.05) -> Dict[str, Any]:
        """
        Non-parametric Mann-Kendall Trend Test to assess monotonic trend significance.
        Standard for NASA Earth science time-series analysis.
        """
        n = len(values)
        if n < 4:
            return {
                "s_score": 0,
                "tau": 0.0,
                "p_value": 1.0,
                "is_significant": False,
                "trend": "Insufficient Data"
            }

        s = 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                diff = values[j] - values[i]
                if diff > 1e-9:
                    s += 1
                elif diff < -1e-9:
                    s -= 1

        # Variance of S under H0 (no ties assumed for simple float timeseries)
        var_s = (n * (n - 1) * (2 * n + 5)) / 18.0

        if s > 0:
            z = (s - 1) / math.sqrt(var_s)
        elif s < 0:
            z = (s + 1) / math.sqrt(var_s)
        else:
            z = 0.0

        # Two-tailed p-value calculation via complementary error function
        p_value = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(z) / math.sqrt(2.0))))
        is_significant = p_value < alpha

        # Kendall's Tau correlation
        denominator = 0.5 * n * (n - 1)
        tau = s / denominator if denominator > 0 else 0.0

        if is_significant and s > 0:
            trend_dir = "Significant Increasing Trend"
        elif is_significant and s < 0:
            trend_dir = "Significant Decreasing Trend"
        elif not is_significant and s > 0:
            trend_dir = "Non-significant Upward Drift"
        elif not is_significant and s < 0:
            trend_dir = "Non-significant Downward Drift"
        else:
            trend_dir = "Stable / No Trend"

        return {
            "s_score": int(s),
            "z_score": round(z, 4),
            "tau": round(tau, 4),
            "p_value": round(p_value, 5),
            "is_significant": is_significant,
            "trend": trend_dir
        }

    def detect_trends(
        self,
        lat: float,
        lon: float,
        variable_name: str,
        units: str,
        timeseries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Main detective workflow: analyzes historical timeseries, outputs rigorous scientific indicators.
        timeseries format: [{'year': 2000, 'value': 24.5}, ...]
        """
        sorted_ts = sorted(timeseries, key=lambda x: x["year"])
        years = [pt["year"] for pt in sorted_ts]
        vals = [float(pt["value"]) for pt in sorted_ts]

        if not vals:
            return {"error": "Empty dataset"}

        # 1. Mann-Kendall Significance
        mk = self.mann_kendall_test(vals)

        # 2. Rate of Change (Sen's Slope per decade)
        annual_slope = self.calculate_sen_slope(years, vals)
        decadal_slope = annual_slope * 10.0

        # Baseline & final decade comparison
        baseline_val = sum(vals[:5]) / min(len(vals), 5)
        recent_val = sum(vals[-5:]) / min(len(vals), 5)
        total_drift = recent_val - baseline_val
        pct_change = (total_drift / abs(baseline_val) * 100.0) if baseline_val != 0 else 0.0

        # Detective scientific conclusion
        verdict = (
            f"Scientifically significant change detected ({mk['trend']}) with p-value of {mk['p_value']} (p < 0.05). "
            f"Changing at {decadal_slope:+.3f} {units}/decade."
            if mk["is_significant"]
            else f"No statistically significant long-term trend detected (p = {mk['p_value']}). Observed fluctuations fall within natural baseline variability."
        )

        return {
            "target": {
                "latitude": lat,
                "longitude": lon,
                "variable": variable_name,
                "units": units
            },
            "timeline": {
                "start_year": years[0],
                "end_year": years[-1],
                "observations_count": len(years)
            },
            "statistics": {
                "kendall_tau": mk["tau"],
                "p_value": mk["p_value"],
                "is_statistically_significant": mk["is_significant"],
                "sen_slope_per_decade": round(decadal_slope, 4),
                "total_drift": round(total_drift, 3),
                "percentage_change": round(pct_change, 2),
                "trend_classification": mk["trend"]
            },
            "scientific_verdict": verdict,
            "data_points": [{"year": y, "value": round(v, 2)} for y, v in zip(years, vals)]
        }
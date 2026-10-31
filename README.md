# ClimateLens

**Engineering Intelligence · Software Development · Applied AI**

ClimateLens is a FastAPI service and interactive web dashboard for climate-risk screening and Earth-system trend analysis. It combines a NASA POWER data client, heuristic risk scoring, and statistical trend detection (Mann-Kendall, Theil-Sen) in a single, self-contained application.

Repository: https://github.com/fazeli1977-dot/ClimateLens

## Overview

ClimateLens exposes two analysis endpoints and a browser-based dashboard:

- **Climate risk analysis** (`/api/v1/risk-analysis`): retrieves daily temperature, humidity, and precipitation for a coordinate and lookback window, then computes a 0-100 risk score with thermal-stress, drought, and volatility components.
- **Earth-system trend detection** (`/api/v1/trend-detective`): returns Mann-Kendall significance, Sen's slope per decade, baseline drift, and a scientific verdict for a multi-decadal series.

The application is a prototype/research tool. It is not a validated operational climate-risk service, and its scores and trends should be treated as exploratory indicators rather than authoritative forecasts.

## Key capabilities

- NASA POWER daily point data client (`T2M`, `RH2M`, `PRECTOTCORR`) with a local synthetic fallback when the upstream request fails.
- Heat-index approximation and a 0-100 composite risk score (thermal stress, drought, temperature volatility) with Low / Moderate / High / Critical levels.
- Mann-Kendall trend test and Theil-Sen (median) slope estimation, including Kendall's tau, p-value, and decadal slope.
- Interactive dashboard: coordinate selection, risk score and advisory, metric grid, daily time-series chart, and trend chart.
- Automated tests for risk scoring and trend detection.

## Project structure

```text
ClimateLens/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  └─ services/
│  │     ├─ nasa_service.py
│  │     ├─ risk_engine.py
│  │     ├─ risk_service.py
│  │     └─ trend_detector.py
│  └─ tests/
│     └─ test_risk.py
├─ frontend/
│  └─ public/
│     └─ index.html
├─ tests/
│  └─ test_trend_detector.py
├─ ClimateLens_Presentation.pptx
├─ NASA_Submission_Details.txt
├─ pytest.ini
├─ .gitignore
└─ README.md
```

## Tech stack (verified)

- Python 3.12
- FastAPI, httpx, Uvicorn
- Vanilla HTML/CSS/JavaScript dashboard (no build step)
- pytest (development/testing)

No dependency manifest (`requirements.txt` or `pyproject.toml`) is present in the repository.

## Quick start

### 1. Clone

```bash
git clone https://github.com/fazeli1977-dot/ClimateLens.git
cd ClimateLens
```

### 2. Virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install fastapi httpx uvicorn
```

For tests:

```bash
pip install pytest
```

### 4. Run

```bash
python -m uvicorn backend.app.main:app --reload
```

Open `http://127.0.0.1:8000/` for the dashboard and `http://127.0.0.1:8000/docs` for the API documentation.

## API

### GET /api/v1/risk-analysis

Query parameters:

- `lat` (float, -90 to 90, required)
- `lon` (float, -180 to 180, required)
- `days` (int, 7 to 90, default 30)

Returns location, elevation, risk assessment (score, level, metrics, breakdown), and daily climate history.

### GET /api/v1/trend-detective

Query parameters:

- `lat` (float, default 35.6892)
- `lon` (float, default 51.3890)
- `variable` (string, default "T2M"; "T2M" selects the temperature baseline, otherwise precipitation)
- `start_year` (int, default 2000)
- `end_year` (int, default 2024)

Returns target, timeline, Mann-Kendall statistics, Sen's slope per decade, drift, percentage change, trend classification, scientific verdict, and data points.

Note: this endpoint currently derives its series from a deterministic in-code baseline rather than a live historical dataset.

## Data sources

- **NASA POWER** (Prediction of Worldwide Energy Resources) daily point API: `T2M`, `RH2M`, `PRECTOTCORR`, community `RE`. Used by `/api/v1/risk-analysis`.
- When the upstream request fails or returns no data, a local synthetic series is generated from latitude-based heuristics. These values are not measurements.
- The trend-detective endpoint uses a deterministic synthetic series defined in code; it does not query NASA POWER or other providers.
- Submission materials (`NASA_Submission_Details.txt`) reference additional NASA Earth-observation concepts (GPM, MODIS/VIIRS) and Open-Meteo, but these are not implemented as data integrations in the current codebase.

Users are responsible for complying with upstream provider terms when integrating or redistributing data.

## Testing

```bash
python -m pytest -q
```

The suite contains 4 tests covering heat-index calculation, risk evaluation, and Mann-Kendall trend detection (positive trend and stable series).

## Scope and limitations

- Risk scores and advisories are heuristic indicators, not validated predictions or operational alerting.
- The NASA POWER fallback and trend-detective series are synthetic/generated, not observations.
- No authentication, rate limiting, or production hardening is implemented; CORS is permissive (`*`).
- No dependency manifest or container configuration is included.

## Contributing

Open an issue to discuss major changes, then submit a pull request with a clear description.

## License

No `LICENSE` file is present in this repository, and no license terms are specified. License information is therefore missing; until a license is added by the owner, default copyright protections apply. Users should contact the repository owner before reuse or redistribution.

## Developer

Developed by Alireza Sani as part of an international engineering and software portfolio.

Portfolio: https://github.com/fazeli1977-dot

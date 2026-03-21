# Stock Dashboard

## Purpose

Flask + vanilla JavaScript dashboard for stock lookup and recent price history.

## Quick Start

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:5001/stocks/ in a browser.

Optional: write server output to `logs/flask.log`:

```bash
mkdir -p logs
python app.py > logs/flask.log 2>&1
```

## Deploy

This project is set up to deploy as a single Render web service.

1. Push the repo to GitHub.
2. In Render, create a new Web Service from the repo.
3. Render will detect [render.yaml](render.yaml).
4. The app redirects to the dashboard at `/stocks/`.
5. Canonical API routes are under `/stocks/api/*`.

Legacy compatibility:
- `/stocks` redirects to `/stocks/`
- `/api/*` redirects to `/stocks/api/*`

## API

- `GET /stocks/api/stock/<ticker>`
- `GET /stocks/api/stock/<ticker>/history?days=30`
- `GET /stocks/api/watchlist?tickers=AAPL,MSFT,NVDA,AMZN,TSLA`
- `GET /stocks/api/health`

Examples:

```bash
curl http://localhost:5001/stocks/api/stock/AAPL
curl "http://localhost:5001/stocks/api/stock/AAPL/history?days=30"
curl "http://localhost:5001/stocks/api/watchlist?tickers=AAPL,MSFT"
curl http://localhost:5001/stocks/api/health
```

## Explore Available Data

Run the field audit script to inventory what `yfinance` returns across representative tickers:

```bash
source venv/bin/activate
python scripts/audit_yfinance_fields.py
```

Outputs are written to `data/`:

- `data/field_inventory.csv`: aggregated field coverage and non-null rates
- `data/field_samples.json`: raw per-ticker samples and source metadata
- `data/audit_summary.md`: quick reliability summary with Tier 1/2/3 guidance

## Project Layout

- [app.py](app.py): Flask server and API routes
- [index.html](index.html), [styles.css](styles.css), [script.js](script.js): frontend UI
- [requirements.txt](requirements.txt): Python dependencies
- [render.yaml](render.yaml): Render service configuration
- [scripts/audit_yfinance_fields.py](scripts/audit_yfinance_fields.py): yfinance field audit script
- [data/](data): generated audit outputs
- [logs/](logs): optional local runtime logs

## Notes

Backend runs on port `5001`; mock/demo data is development-only (`ENABLE_MOCK_DATA=true python app.py`); and if `yfinance` fails with mock mode off, the app returns an explicit provider failure instead of fallback data.

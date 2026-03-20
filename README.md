# Stock Dashboard


## Purpose

Small Flask + vanilla JavaScript app for stock lookup and recent price history.

## Run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Optional: write server output to a file in `logs/`:

```bash
mkdir -p logs
python app.py > logs/flask.log 2>&1
```

Open [index.html](index.html) in a browser.

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

## API

- `GET /api/stock/<ticker>`
- `GET /api/stock/<ticker>/history`
- `GET /api/health`

Example:

```bash
curl http://localhost:5001/api/stock/AAPL
curl http://localhost:5001/api/stock/AAPL/history
curl http://localhost:5001/api/health
```

## Files

- [app.py](app.py): Flask API
- [index.html](index.html): UI markup
- [styles.css](styles.css): styles
- [script.js](script.js): frontend logic
- [requirements.txt](requirements.txt): dependencies
- [scripts/audit_yfinance_fields.py](scripts/audit_yfinance_fields.py): yfinance field audit tool
- [logs/.gitkeep](logs/.gitkeep): keeps log folder in git

## Notes

- Backend runs on port `5001`.
- Mock/demo data is off by default. To enable it during development only, run `ENABLE_MOCK_DATA=true python app.py`.
- If `yfinance` fails and mock mode is off, the app returns no data and an explicit provider failure instead of silently substituting demo values.

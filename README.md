# Stock Dashboard

## TODO

Source of truth: [TODO.md](TODO.md)

## Purpose

Small Flask + vanilla JavaScript app for stock lookup and recent price history.

## Run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open [index.html](index.html) in a browser.

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

## Notes

- Backend runs on port `5001`.
- `yfinance` can fail locally/network-dependent; app falls back to demo data for selected tickers.

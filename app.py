import os
import random
from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, request, send_from_directory
from flask_cors import CORS
import yfinance as yf

load_dotenv()

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENABLE_MOCK_DATA = os.getenv('ENABLE_MOCK_DATA', '').lower() in {'1', 'true', 'yes', 'on'}

# Mock data for demo when yfinance fails
MOCK_STOCKS = {
    'AAPL': {'name': 'Apple Inc.', 'price': 179.50, 'basePrice': 170},
    'GOOGL': {'name': 'Alphabet Inc.', 'price': 142.30, 'basePrice': 130},
    'MSFT': {'name': 'Microsoft Corporation', 'price': 405.70, 'basePrice': 390},
    'TSLA': {'name': 'Tesla Inc.', 'price': 187.40, 'basePrice': 175},
}


def fetch_live_history(ticker, days):
    """Fetch daily OHLC history from Yahoo Finance with fallback query paths."""
    max_days = max(days, 5)
    periods = [f'{max_days}d', '1mo', '3mo', '1y']
    errors = []

    stock = yf.Ticker(ticker)

    for period in periods:
        try:
            hist = stock.history(
                period=period,
                interval='1d',
                auto_adjust=False,
                prepost=False,
                actions=False,
            )
            if not hist.empty and 'Close' in hist.columns:
                return hist, stock, None
        except Exception as exc:
            errors.append(f'history({period}): {exc}')

    for period in periods:
        try:
            hist = yf.download(
                tickers=ticker,
                period=period,
                interval='1d',
                auto_adjust=False,
                progress=False,
                threads=False,
                group_by='column',
            )
            if not hist.empty and 'Close' in hist.columns:
                return hist, stock, None
        except Exception as exc:
            errors.append(f'download({period}): {exc}')

    if errors:
        return None, stock, '; '.join(errors)

    return None, stock, 'Yahoo Finance returned no price history.'


def provider_failure_response(ticker, message):
    return jsonify({
        'ticker': ticker,
        'error': 'Failed to load data from Yahoo Finance',
        'source': 'yfinance',
        'is_live': False,
        'provider_error': message,
        'timestamp': datetime.now().isoformat()
    }), 503


def build_live_stock_payload(ticker, hist, stock):
    current_price = float(hist['Close'].iloc[-1])
    previous_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price

    company_name = ticker
    display_name = ticker
    market_cap = 'N/A'
    pe_ratio = 'N/A'

    try:
        info = stock.info
        company_name = info.get('longName') or info.get('shortName') or ticker
        display_name = info.get('shortName') or company_name

        raw_market_cap = info.get('marketCap')
        if isinstance(raw_market_cap, (int, float)):
            market_cap = raw_market_cap

        raw_pe_ratio = info.get('trailingPE')
        if isinstance(raw_pe_ratio, (int, float)):
            pe_ratio = round(float(raw_pe_ratio), 2)
    except Exception:
        pass

    return {
        'ticker': ticker,
        'display_name': display_name,
        'current_price': round(current_price, 2),
        'previous_close': round(previous_close, 2),
        'company_name': company_name,
        'currency': 'USD',
        'market_cap': market_cap,
        'pe_ratio': pe_ratio,
        'source': 'yfinance',
        'is_live': True,
        'provider_error': None,
        'timestamp': datetime.now().isoformat(),
    }


def mock_stock_response(ticker, provider_error):
    mock = MOCK_STOCKS[ticker]
    price = mock['price'] + random.uniform(-5, 5)

    return jsonify({
        'ticker': ticker,
        'current_price': round(price, 2),
        'company_name': mock['name'],
        'currency': 'USD',
        'market_cap': 'N/A',
        'pe_ratio': 'N/A',
        'source': 'mock',
        'is_live': False,
        'provider_error': provider_error,
        'timestamp': datetime.now().isoformat(),
    })


def mock_history_response(ticker, days, provider_error):
    dates = [(datetime.now() - timedelta(days=index)).strftime('%Y-%m-%d') for index in range(days, 0, -1)]
    base_price = MOCK_STOCKS[ticker]['basePrice']
    closes = [round(base_price + random.uniform(-20, 20), 2) for _ in range(days)]

    return jsonify({
        'ticker': ticker,
        'dates': dates,
        'closes': closes,
        'opens': closes,
        'highs': [round(price + random.uniform(0, 5), 2) for price in closes],
        'lows': [round(price - random.uniform(0, 5), 2) for price in closes],
        'source': 'mock',
        'is_live': False,
        'provider_error': provider_error,
        'timestamp': datetime.now().isoformat(),
    })


@app.route('/')
@app.route('/stocks/')
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')


@app.route('/stocks')
def redirect_stocks_no_slash():
    return redirect('/stocks/', code=308)


@app.route('/styles.css')
@app.route('/stocks/styles.css')
def serve_stylesheet():
    return send_from_directory(BASE_DIR, 'styles.css')


@app.route('/script.js')
@app.route('/stocks/script.js')
def serve_script():
    return send_from_directory(BASE_DIR, 'script.js')


@app.route('/api/stock/<ticker>', methods=['GET'])
@app.route('/stocks/api/stock/<ticker>', methods=['GET'])
def get_stock(ticker):
    """Fetch stock data for a given ticker"""
    ticker = ticker.upper()
    provider_error = 'Yahoo Finance returned no price history.'

    try:
        hist, stock, history_error = fetch_live_history(ticker, days=30)
        if history_error:
            provider_error = history_error

        if hist is not None and not hist.empty:
            return jsonify(build_live_stock_payload(ticker, hist, stock))
    except Exception as exc:
        provider_error = str(exc)

    if ENABLE_MOCK_DATA and ticker in MOCK_STOCKS:
        return mock_stock_response(ticker, provider_error)

    return provider_failure_response(ticker, provider_error)

@app.route('/api/stock/<ticker>/history', methods=['GET'])
@app.route('/stocks/api/stock/<ticker>/history', methods=['GET'])
def get_stock_history(ticker):
    """Fetch historical price data (default: last 30 days)"""
    ticker = ticker.upper()
    days = request.args.get('days', default=30, type=int) or 30
    days = max(1, min(days, 365))
    provider_error = 'Yahoo Finance returned no price history.'

    try:
        hist, _stock, history_error = fetch_live_history(ticker, days)
        if history_error:
            provider_error = history_error

        if hist is not None and not hist.empty:
            data = {
                'ticker': ticker,
                'dates': hist.index.strftime('%Y-%m-%d').tolist()[-days:],
                'closes': hist['Close'].round(2).tolist()[-days:],
                'opens': hist['Open'].round(2).tolist()[-days:],
                'highs': hist['High'].round(2).tolist()[-days:],
                'lows': hist['Low'].round(2).tolist()[-days:],
                'source': 'yfinance',
                'is_live': True,
                'provider_error': None,
                'timestamp': datetime.now().isoformat(),
            }
            return jsonify(data)
    except Exception as exc:
        provider_error = str(exc)

    if ENABLE_MOCK_DATA and ticker in MOCK_STOCKS:
        return mock_history_response(ticker, days, provider_error)

    return provider_failure_response(ticker, provider_error)


@app.route('/api/watchlist', methods=['GET'])
@app.route('/stocks/api/watchlist', methods=['GET'])
def get_watchlist():
    """Fetch compact watchlist rows for a list of tickers."""
    tickers_param = request.args.get('tickers', '')
    if tickers_param.strip():
        tickers = [item.strip().upper() for item in tickers_param.split(',') if item.strip()]
    else:
        tickers = ['AAPL', 'MSFT', 'NVDA', 'AMZN', 'TSLA']

    tickers = tickers[:10]
    rows = []

    for ticker in tickers:
        provider_error = 'Yahoo Finance returned no price history.'
        try:
            hist, stock, history_error = fetch_live_history(ticker, days=5)
            if history_error:
                provider_error = history_error

            if hist is not None and not hist.empty:
                payload = build_live_stock_payload(ticker, hist, stock)
                rows.append({
                    'ticker': payload['ticker'],
                    'displayName': payload['display_name'],
                    'lastPrice': payload['current_price'],
                    'previousClose': payload['previous_close'],
                    'is_live': True,
                    'source': payload['source'],
                    'provider_error': None,
                })
                continue
        except Exception as exc:
            provider_error = str(exc)

        rows.append({
            'ticker': ticker,
            'displayName': ticker,
            'lastPrice': None,
            'previousClose': None,
            'is_live': False,
            'source': 'yfinance',
            'provider_error': provider_error,
        })

    return jsonify({
        'rows': rows,
        'source': 'yfinance',
        'timestamp': datetime.now().isoformat(),
    })

@app.route('/api/health', methods=['GET'])
@app.route('/stocks/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, port=5001)

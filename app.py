import os
import random
from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf

load_dotenv()

app = Flask(__name__)
CORS(app)

ENABLE_MOCK_DATA = os.getenv('ENABLE_MOCK_DATA', '').lower() in {'1', 'true', 'yes', 'on'}

# Mock data for demo when yfinance fails
MOCK_STOCKS = {
    'AAPL': {'name': 'Apple Inc.', 'price': 179.50, 'basePrice': 170},
    'GOOGL': {'name': 'Alphabet Inc.', 'price': 142.30, 'basePrice': 130},
    'MSFT': {'name': 'Microsoft Corporation', 'price': 405.70, 'basePrice': 390},
    'TSLA': {'name': 'Tesla Inc.', 'price': 187.40, 'basePrice': 175},
}


def provider_failure_response(ticker, message):
    return jsonify({
        'ticker': ticker,
        'error': 'Failed to load data from Yahoo Finance',
        'source': 'yfinance',
        'is_live': False,
        'provider_error': message,
        'timestamp': datetime.now().isoformat()
    }), 503


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

@app.route('/api/stock/<ticker>', methods=['GET'])
def get_stock(ticker):
    """Fetch stock data for a given ticker"""
    ticker = ticker.upper()
    provider_error = 'Yahoo Finance returned no price history.'

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period='1y')

        if not hist.empty:
            current_price = float(hist['Close'].iloc[-1])
            company_name = ticker

            try:
                info = stock.info
                company_name = info.get('longName') or ticker
            except Exception:
                pass

            return jsonify({
                'ticker': ticker,
                'current_price': round(current_price, 2),
                'company_name': company_name,
                'currency': 'USD',
                'market_cap': 'N/A',
                'pe_ratio': 'N/A',
                'source': 'yfinance',
                'is_live': True,
                'provider_error': None,
                'timestamp': datetime.now().isoformat()
            })
    except Exception as exc:
        provider_error = str(exc)

    if ENABLE_MOCK_DATA and ticker in MOCK_STOCKS:
        return mock_stock_response(ticker, provider_error)

    return provider_failure_response(ticker, provider_error)

@app.route('/api/stock/<ticker>/history', methods=['GET'])
def get_stock_history(ticker):
    """Fetch historical price data (default: last 30 days)"""
    ticker = ticker.upper()
    days = request.args.get('days', default=30, type=int) or 30
    days = max(1, min(days, 365))
    provider_error = 'Yahoo Finance returned no price history.'

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period='1y')

        if not hist.empty:
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

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, port=5001)

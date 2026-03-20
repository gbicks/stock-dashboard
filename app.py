from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import yfinance as yf
from datetime import datetime, timedelta
import time
import random

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    """Serve the dashboard UI"""
    return render_template('index.html')

# Mock data for demo when yfinance fails
MOCK_STOCKS = {
    'AAPL': {'name': 'Apple Inc.', 'price': 179.50, 'basePrice': 170},
    'GOOGL': {'name': 'Alphabet Inc.', 'price': 142.30, 'basePrice': 130},
    'MSFT': {'name': 'Microsoft Corporation', 'price': 405.70, 'basePrice': 390},
    'TSLA': {'name': 'Tesla Inc.', 'price': 187.40, 'basePrice': 175},
}

@app.route('/api/stock/<ticker>', methods=['GET'])
def get_stock(ticker):
    """Fetch stock data for a given ticker"""
    ticker = ticker.upper()
    
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period='1y')
        
        if not hist.empty:
            current_price = float(hist['Close'].iloc[-1])
            try:
                info = stock.info
                company_name = info.get('longName', ticker)
            except:
                company_name = ticker
            
            return jsonify({
                'ticker': ticker,
                'current_price': round(current_price, 2),
                'company_name': company_name,
                'currency': 'USD',
                'market_cap': 'N/A',
                'pe_ratio': 'N/A',
                'timestamp': datetime.now().isoformat()
            })
    except:
        pass
    
    # Fallback to mock data if yfinance fails
    if ticker in MOCK_STOCKS:
        mock = MOCK_STOCKS[ticker]
        # Simulate slight price variation
        price = mock['price'] + random.uniform(-5, 5)
        return jsonify({
            'ticker': ticker,
            'current_price': round(price, 2),
            'company_name': mock['name'],
            'currency': 'USD',
            'market_cap': 'N/A',
            'pe_ratio': 'N/A',
            'timestamp': datetime.now().isoformat(),
            'note': '(Demo data - yfinance unavailable)'
        })
    
    return jsonify({'error': f'Ticker {ticker} not found'}), 404

@app.route('/api/stock/<ticker>/history', methods=['GET'])
def get_stock_history(ticker):
    """Fetch historical price data (default: last 30 days)"""
    ticker = ticker.upper()
    
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period='1y')
        
        if not hist.empty:
            data = {
                'ticker': ticker,
                'dates': hist.index.strftime('%Y-%m-%d').tolist()[-30:],
                'closes': hist['Close'].round(2).tolist()[-30:],
                'opens': hist['Open'].round(2).tolist()[-30:],
                'highs': hist['High'].round(2).tolist()[-30:],
                'lows': hist['Low'].round(2).tolist()[-30:],
            }
            return jsonify(data)
    except:
        pass
    
    # Fallback: generate mock chart data
    if ticker in MOCK_STOCKS:
        dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30, 0, -1)]
        base_price = MOCK_STOCKS[ticker]['basePrice']
        closes = [round(base_price + random.uniform(-20, 20), 2) for _ in range(30)]
        
        return jsonify({
            'ticker': ticker,
            'dates': dates,
            'closes': closes,
            'opens': closes,
            'highs': [p + random.uniform(0, 5) for p in closes],
            'lows': [p - random.uniform(0, 5) for p in closes],
            'note': '(Demo data - yfinance unavailable)'
        })
    
    return jsonify({'error': f'Ticker {ticker} not found'}), 404

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, port=5001)

# 📈 Stock Dashboard

A simple, elegant stock price dashboard built with Python Flask and vanilla JavaScript. Track real-time stock prices, view historical data, and expand into ETFs, futures, and more.

## ✨ Features

- 🔍 **Search any stock ticker** - Real-time price lookup
- 📊 **30-day price chart** - Visualize trends with Chart.js
- 💼 **Stock details** - Company name, market cap, P/E ratio
- ⚡ **Fast & responsive** - Vanilla JS frontend, Python backend
- 🎨 **Beautiful UI** - Modern gradient design

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js (optional, not required for this project)

### Installation

1. **Navigate to the project:**
   ```bash
   cd ~/Documents/stock-dashboard
   ```

2. **Create a Python virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Project

1. **Start the Flask backend** (in one terminal):
   ```bash
   python app.py
   ```
   Server will run on `http://localhost:5000`

2. **Open the frontend** (in another terminal or browser):
   - Simply open `index.html` in your browser, or
   - Use Live Server extension (VS Code): right-click `index.html` → "Open with Live Server"
   - Or run a simple HTTP server:
     ```bash
     python3 -m http.server 8000
     ```
   Then visit `http://localhost:8000`

3. **Search for stocks:**
   - Type a ticker symbol (e.g., AAPL, GOOGL, MSFT)
   - Click Search or press Enter
   - View current price, details, and 30-day chart

## 📁 Project Structure

```
stock-dashboard/
├── app.py              # Flask backend
├── requirements.txt    # Python dependencies
├── index.html          # Frontend HTML
├── styles.css          # Frontend styles
├── script.js           # Frontend logic
└── README.md           # This file
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/stock/<ticker>` | GET | Get current stock data |
| `/api/stock/<ticker>/history` | GET | Get 30-day historical data |
| `/api/health` | GET | Health check |

**Example:**
```bash
curl http://localhost:5000/api/stock/AAPL
curl http://localhost:5000/api/stock/GOOGL/history?days=60
```

## 📚 What You'll Learn

- **Python basics** - Flask framework, API routing, data handling
- **JavaScript fundamentals** - DOM manipulation, async/await, fetch API
- **Frontend/Backend communication** - REST APIs, CORS
- **Data visualization** - Chart.js library
- **Financial data** - yfinance library for real-time stock data

## 🛣️ Roadmap

### Phase 1 (Now) ✅
- [x] Single stock lookup
- [x] Current price display
- [x] Basic stock info (market cap, P/E ratio)
- [x] 30-day price chart

### Phase 2 (Next)
- [ ] Multiple stocks in watchlist
- [ ] Add/remove watchlist items (localStorage)
- [ ] Display % change, day high/low
- [ ] Search suggestions (autocomplete)

### Phase 3 (Future)
- [ ] ETF support
- [ ] Futures data
- [ ] More technical indicators
- [ ] Database (PostgreSQL) for watchlist persistence
- [ ] User accounts & auth
- [ ] React frontend rebuild

### Phase 4 (Long term)
- [ ] Mobile app (React Native / Flutter)
- [ ] iOS app
- [ ] Advanced charting (TradingView)
- [ ] Backtesting engine

## 🔧 Troubleshooting

**"Backend server is not running"**
- Make sure Flask is running: `python app.py`
- Check port 5000 is not in use

**CORS errors**
- Flask-CORS is configured, but ensure backend is running on localhost:5000

**Stock not found**
- Check ticker is correct (all caps, e.g., AAPL not Apple)
- Try a major ticker like AAPL, GOOGL, MSFT

## 💡 Tips for Learning

1. **Start small** - Understand how one stock lookup works before expanding
2. **Read the errors** - Error messages tell you what's wrong
3. **Experiment** - Try different tickers, modify the frontend styles
4. **Debug in DevTools** - Open browser DevTools (F12) to see console logs
5. **Break it down** - Each file has a specific job (backend, frontend, styling)

## 📄 License

This project is open source and available for learning purposes.

---

Happy trading! 📊📈

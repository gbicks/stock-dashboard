const API_BASE_URL = 'http://localhost:5001/api';

let chart = null;

// DOM Elements
const tickerInput = document.getElementById('tickerInput');
const searchBtn = document.getElementById('searchBtn');
const errorDiv = document.getElementById('error');
const stockCard = document.getElementById('stockCard');
const chartContainer = document.getElementById('chartContainer');
const quickBtns = document.querySelectorAll('.quick-btn');

// Event listeners
searchBtn.addEventListener('click', () => handleSearch(tickerInput.value));
tickerInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSearch(tickerInput.value);
    }
});

quickBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const ticker = btn.dataset.ticker;
        tickerInput.value = ticker;
        handleSearch(ticker);
    });
});

async function handleSearch(ticker) {
    if (!ticker.trim()) {
        showError('Please enter a stock ticker');
        return;
    }

    hideError();
    await fetchStockData(ticker);
}

async function fetchStockData(ticker) {
    try {
        const response = await fetch(`${API_BASE_URL}/stock/${ticker}`);
        
        if (!response.ok) {
            const errorData = await response.json();
            showError(errorData.error || 'Stock not found');
            hideStockCard();
            return;
        }

        const data = await response.json();
        displayStockData(data);
        await fetchAndDisplayChart(ticker);
    } catch (error) {
        showError(`Error fetching data: ${error.message}`);
        hideStockCard();
    }
}

function displayStockData(data) {
    document.getElementById('companyName').textContent = data.company_name;
    document.getElementById('ticker').textContent = data.ticker;
    document.getElementById('currentPrice').textContent = `$${data.current_price}`;
    
    document.getElementById('marketCap').textContent = 
        data.market_cap !== 'N/A' ? formatNumber(data.market_cap) : 'N/A';
    document.getElementById('peRatio').textContent = 
        data.pe_ratio !== 'N/A' ? data.pe_ratio.toFixed(2) : 'N/A';
    document.getElementById('currency').textContent = data.currency;
    
    const timestamp = new Date(data.timestamp).toLocaleTimeString();
    document.getElementById('lastUpdated').textContent = `Updated: ${timestamp}`;
    
    stockCard.classList.remove('hidden');
}

async function fetchAndDisplayChart(ticker) {
    try {
        const response = await fetch(`${API_BASE_URL}/stock/${ticker}/history?days=30`);
        
        if (!response.ok) {
            console.error('Error fetching chart data');
            return;
        }

        const data = await response.json();
        displayChart(data);
    } catch (error) {
        console.error('Error fetching chart data:', error);
    }
}

function displayChart(data) {
    const ctx = document.getElementById('priceChart').getContext('2d');
    
    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: `${data.ticker} - Last 30 Days`,
                data: data.closes,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 3,
                pointBackgroundColor: '#667eea',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointHoverRadius: 5,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Price (USD)'
                    }
                }
            }
        }
    });

    chartContainer.classList.remove('hidden');
}

function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

function hideError() {
    errorDiv.classList.add('hidden');
}

function hideStockCard() {
    stockCard.classList.add('hidden');
    chartContainer.classList.add('hidden');
}

function formatNumber(num) {
    if (typeof num !== 'number') return num;
    if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T';
    if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B';
    if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
    return num.toFixed(2);
}

// Check API health on page load
window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (!response.ok) {
            showError('Backend server is not running. Please start it with: python app.py');
        }
    } catch (error) {
        showError('⚠️ Backend server is not running. Start it with: python app.py');
    }
});

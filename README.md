# 📈 Options Trading Dashboard

A Flask-based web application for options trading analysis with real-time market data visualization and automated trading capabilities through Webull integration.

## 🚀 Quick Start

### 1. **Prerequisites**
- Python 3.13+
- Virtual environment (recommended)
- Webull account for trading (optional)

### 2. **Installation**

```bash
# Clone the repository (if not already done)
git clone <your-repo-url>
cd your-trading-project

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. **Configuration**

1. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file with your credentials:**
   ```env
   # Webull Trading Credentials
   WEBULL_USERNAME=your_webull_username
   WEBULL_PASSWORD=your_webull_password
   WEBULL_TRADE_TOKEN=your_trade_token

   # Flask Configuration
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

### 4. **Start the Application**

```bash
# Activate virtual environment
source venv/bin/activate

# Start the Flask application
python app.py
```

The application will be available at: **http://localhost:5000**

## 📊 Features

### **Real-time Market Analysis**
- **Multi-timeframe charts** (1m, 5m, 15m, 1h)
- **Technical indicators**: EMA (9, 20, 50), RSI, MACD
- **Symbol tracking**: SPY, QQQ (configurable)
- **Live data updates** every 60 seconds

### **Trading Integration**
- **Webull API integration** for automated trading
- **Paper trading support** (for testing)
- **Options trading capabilities**
- **Position and order management**

### **Web Dashboard**
- **Interactive charts** powered by Plotly.js
- **Pattern recognition** (bullish/bearish signals)
- **Symbol switching** between tracked stocks
- **Real-time data visualization**

## 🏗️ Project Structure

```
trading-dashboard/
├── app.py              # Main Flask application
├── webull_trader.py    # Webull API integration
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create from template)
├── .gitignore         # Git ignore file
├── README.md          # This file
├── templates/
│   └── dashboard.html # Web dashboard template
├── static/
│   └── style.css     # Dashboard styles
├── Dockerfile         # Docker configuration
└── deploy.sh          # Deployment script
```

## 🔧 Configuration

### **Trading Configuration**
Edit the `TradingConfig` class in `app.py`:

```python
class TradingConfig:
    def __init__(self):
        self.symbols = ['SPY', 'QQQ']  # Add more symbols
        self.timeframes = {
            "1m": ("1d", "1m"),
            "5m": ("5d", "5m"),
            # Add more timeframes
        }
```

### **Environment Variables**
Required environment variables in `.env`:

| Variable | Description | Required |
|----------|-------------|----------|
| `WEBULL_USERNAME` | Your Webull username | Yes* |
| `WEBULL_PASSWORD` | Your Webull password | Yes* |
| `WEBULL_TRADE_TOKEN` | Your Webull trade token | Yes* |
| `FLASK_ENV` | Flask environment | No |
| `FLASK_DEBUG` | Enable Flask debug mode | No |

*Required only if using Webull trading features

## 🔍 API Endpoints

### **GET /** 
- **Description**: Main dashboard page
- **Returns**: HTML dashboard

### **GET /api/market_data**
- **Description**: Get real-time market data for all symbols and timeframes
- **Returns**: JSON with price data, technical indicators
- **Example response**:
```json
{
  "SPY": {
    "1m": {
      "prices": [450.1, 450.2, ...],
      "timestamps": ["2024-01-01 09:30:00", ...],
      "ema9": [449.8, 449.9, ...],
      "rsi": [65.2, 64.8, ...]
    }
  }
}
```

## 🐳 Docker Deployment

```bash
# Build the Docker image
docker build -t trading-dashboard .

# Run the container
docker run -p 5000:5000 --env-file .env trading-dashboard
```

## 🚨 Security Notice

- **Never commit `.env` file** to version control
- **Use paper trading** for testing
- **Secure your API credentials**
- **Monitor trading activity** closely

## 🛠️ Development

### **Adding New Indicators**
1. Modify `calculate_indicators()` in `MarketAnalyzer` class
2. Update API response in `/api/market_data` endpoint
3. Enhance frontend charts in `dashboard.html`

### **Adding New Symbols**
1. Update `symbols` list in `TradingConfig`
2. Add option to HTML select dropdown

### **Logging**
- Application logs: `trading.log`
- Webull trader logs: `webull_trader.log`

## 📝 License

This project is for educational purposes. Use at your own risk for actual trading.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## ⚠️ Disclaimer

This software is for educational and research purposes only. Trading involves substantial risk and is not suitable for all investors. Past performance does not guarantee future results.
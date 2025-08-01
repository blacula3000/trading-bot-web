from flask import Flask, render_template, jsonify
from webull_trader import WebullTrader
import yfinance as yf
import pandas as pd
import numpy as np
import threading
import time
import os
from datetime import datetime
import logging

app = Flask(__name__)

class TradingConfig:
    def __init__(self):
        self.symbols = ['SPY', 'QQQ']
        self.timeframes = {
            "1m": ("1d", "1m"),
            "5m": ("5d", "5m"),
            "15m": ("7d", "15m"),
            "1h": ("14d", "1h")
        }
        self.patterns = {
            'bullish_combo': ['TwoUp', 'InsideBar_Bullish', 'EMA_Bullish'],
            'bearish_combo': ['TwoDown', 'InsideBar_Bearish', 'EMA_Bearish']
        }

class MarketAnalyzer:
    def __init__(self, config):
        self.config = config
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='trading.log'
        )
        self.logger = logging.getLogger(__name__)

    def fetch_data(self, symbol, period, interval):
        try:
            data = yf.download(symbol, period=period, interval=interval)
            return self.calculate_indicators(data)
        except Exception as e:
            self.logger.error(f"Error fetching data: {e}")
            return None

    def calculate_indicators(self, df):
        if df.empty:
            return df

        # Ensure we have the right column names (yfinance sometimes uses different cases)
        close_col = 'Close'
        if 'Close' not in df.columns and 'close' in df.columns:
            close_col = 'close'
        elif 'Close' not in df.columns and 'Adj Close' in df.columns:
            close_col = 'Adj Close'

        # EMAs
        df['EMA9'] = df[close_col].ewm(span=9).mean()
        df['EMA20'] = df[close_col].ewm(span=20).mean()
        df['EMA50'] = df[close_col].ewm(span=50).mean()

        # RSI
        delta = df[close_col].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        # MACD
        exp1 = df[close_col].ewm(span=12).mean()
        exp2 = df[close_col].ewm(span=26).mean()
        df['MACD'] = exp1 - exp2
        df['Signal_Line'] = df['MACD'].ewm(span=9).mean()

        return df

config = TradingConfig()
analyzer = MarketAnalyzer(config)

# Initialize Webull trader only if credentials are provided
trader = None
try:
    if os.getenv('WEBULL_USERNAME') and os.getenv('WEBULL_PASSWORD'):
        trader = WebullTrader()
    else:
        print("Webull credentials not provided. Running without trading functionality.")
except Exception as e:
    print(f"Failed to initialize Webull trader: {e}")
    print("Running without trading functionality.")

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/market_data')
def get_market_data():
    data = {}
    for symbol in config.symbols:
        symbol_data = {}
        for timeframe, (period, interval) in config.timeframes.items():
            df = analyzer.fetch_data(symbol, period, interval)
            if df is not None and not df.empty:
                # Determine the close column name
                close_col = 'Close'
                if 'Close' not in df.columns and 'close' in df.columns:
                    close_col = 'close'
                elif 'Close' not in df.columns and 'Adj Close' in df.columns:
                    close_col = 'Adj Close'
                
                # Only include data if we have the required columns
                if close_col in df.columns and 'EMA9' in df.columns:
                    symbol_data[timeframe] = {
                        'prices': df[close_col].tolist(),
                        'timestamps': [str(t) for t in df.index],
                        'ema9': df['EMA9'].tolist(),
                        'ema20': df['EMA20'].tolist(),
                        'ema50': df['EMA50'].tolist(),
                        'rsi': df['RSI'].tolist(),
                        'macd': df['MACD'].tolist(),
                        'signal_line': df['Signal_Line'].tolist()
                    }
        data[symbol] = symbol_data
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

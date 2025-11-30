"""
Configuration file for the multi-asset trading platform
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/"
BINANCE_REST_URL = "https://api.binance.com/api/v3/"

# Supported cryptocurrencies (for trading platform)
SUPPORTED_CRYPTOS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT",
    "XRPUSDT", "DOTUSDT", "DOGEUSDT", "AVAXUSDT", "MATICUSDT"
]

# Trading simulation settings
INITIAL_BALANCE = 10000  # Starting balance in USD
TRADING_FEE = 0.001  # 0.1% trading fee
MAX_POSITION_SIZE = 0.1  # Maximum 10% of portfolio per trade

# Streamlit configuration
PAGE_TITLE = "AI Trading Platform"
PAGE_ICON = "🚀"
LAYOUT = "wide"

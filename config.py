"""
Configuration file for the Multi-Asset Trading Platform with AI Robo Advisor
"""

# Trading simulation settings
INITIAL_BALANCE = 10000  # Starting balance in USD
TRADING_FEE = 0.001  # 0.1% trading fee
MAX_POSITION_SIZE = 0.1  # Maximum 10% of portfolio per trade

# Supported cryptocurrencies (for trading platform)
SUPPORTED_CRYPTOS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT",
    "XRPUSDT", "DOTUSDT", "DOGEUSDT", "AVAXUSDT", "MATICUSDT"
]

# Data source configuration
# Note: The application uses yfinance for market data (stocks, ETFs, indices)
# and other data providers as needed

"""
Crypto Trading Simulator - Streamlit Cloud Compatible Version
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import requests
import json
from typing import Dict, List
import streamlit.components.v1 as components

# Import our modules
from trading_engine import portfolio, OrderSide, OrderType, OrderStatus
from config import SUPPORTED_CRYPTOS, INITIAL_BALANCE, TRADING_FEE
from tradingview_widget import create_tradingview_widget, create_tradingview_advanced_chart, create_tradingview_screener, create_tradingview_crypto_heatmap

# Page configuration
st.set_page_config(
    page_title="AI Trading Platform - Multi-Asset Investment Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Navigation
def show_navigation():
    st.sidebar.markdown("## 🧭 Navigation")
    
    # Check if user is first-time visitor
    if 'seen_introduction' not in st.session_state:
        st.session_state.seen_introduction = False
    
    if 'tutorial_completed' not in st.session_state:
        st.session_state.tutorial_completed = False
    
    # Show welcome message for first-time users
    if not st.session_state.seen_introduction and not st.session_state.tutorial_completed:
        st.sidebar.success("👋 Welcome! Start with the Interactive Tutorial!")
        
        # Add tutorial start button
        if st.sidebar.button("🎓 Start Tutorial", type="primary"):
            st.session_state.tutorial_started = True
            st.rerun()
    
    # Show tutorial option for first-time users
    if not st.session_state.tutorial_completed:
        page = st.sidebar.radio(
            "Go to",
            ["🎓 Interactive Tutorial", "🌍 Trading Platform", "🤖 Strategy Backtesting", "🎯 AI Robo Advisor"],
            index=0
        )
    else:
        page = st.sidebar.radio(
            "Go to",
            ["🌍 Trading Platform", "🤖 Strategy Backtesting", "🎯 AI Robo Advisor"],
            index=0
        )
    
    return page

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
    }
    .error-message {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'portfolio_initialized' not in st.session_state:
    st.session_state.portfolio_initialized = False
    st.session_state.current_prices = {}
    st.session_state.last_update = None

def initialize_portfolio():
    """Initialize portfolio if not already done"""
    if not st.session_state.portfolio_initialized:
        portfolio.__init__(INITIAL_BALANCE)
        st.session_state.portfolio_initialized = True

def get_current_prices() -> Dict[str, float]:
    """Get current prices from multiple APIs with fallback"""
    # Try multiple APIs in order of preference
    apis = [
        ("CoinGecko", "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,binancecoin,cardano,solana,ripple,polkadot,dogecoin,avalanche-2,polygon&vs_currencies=usd"),
        ("CoinCap", "https://api.coincap.io/v2/assets?limit=10"),
        ("Binance", "https://api.binance.com/api/v3/ticker/price")
    ]
    
    for api_name, url in apis:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            prices = {}
            data = response.json()
            
            if api_name == "CoinGecko":
                # CoinGecko format
                coin_mapping = {
                    "bitcoin": "BTCUSDT",
                    "ethereum": "ETHUSDT", 
                    "binancecoin": "BNBUSDT",
                    "cardano": "ADAUSDT",
                    "solana": "SOLUSDT",
                    "ripple": "XRPUSDT",
                    "polkadot": "DOTUSDT",
                    "dogecoin": "DOGEUSDT",
                    "avalanche-2": "AVAXUSDT",
                    "polygon": "MATICUSDT"
                }
                
                for coin_id, symbol in coin_mapping.items():
                    if coin_id in data and 'usd' in data[coin_id]:
                        prices[symbol] = float(data[coin_id]['usd'])
                        
            elif api_name == "CoinCap":
                # CoinCap format
                symbol_mapping = {
                    "bitcoin": "BTCUSDT",
                    "ethereum": "ETHUSDT",
                    "binance-coin": "BNBUSDT", 
                    "cardano": "ADAUSDT",
                    "solana": "SOLUSDT",
                    "xrp": "XRPUSDT",
                    "polkadot": "DOTUSDT",
                    "dogecoin": "DOGEUSDT",
                    "avalanche": "AVAXUSDT",
                    "matic-network": "MATICUSDT"
                }
                
                for asset in data.get('data', []):
                    symbol_id = asset.get('id', '')
                    if symbol_id in symbol_mapping:
                        symbol = symbol_mapping[symbol_id]
                        prices[symbol] = float(asset.get('priceUsd', 0))
                        
            elif api_name == "Binance":
                # Binance format
                for item in data:
                    symbol = item['symbol']
                    if symbol in SUPPORTED_CRYPTOS:
                        prices[symbol] = float(item['price'])
            
            if prices:
                return prices
                
        except Exception as e:
            continue  # Try next API
    
    # If all APIs fail, return mock data
    return get_mock_prices()

def get_mock_prices() -> Dict[str, float]:
    """Get mock prices for demo when API is unavailable"""
    import random
    base_prices = {
        "BTCUSDT": 45000.0,
        "ETHUSDT": 3000.0,
        "BNBUSDT": 300.0,
        "ADAUSDT": 0.5,
        "SOLUSDT": 100.0,
        "XRPUSDT": 0.6,
        "DOTUSDT": 7.0,
        "DOGEUSDT": 0.08,
        "AVAXUSDT": 25.0,
        "MATICUSDT": 0.8
    }
    
    # Add some random variation
    mock_prices = {}
    for symbol, base_price in base_prices.items():
        variation = random.uniform(0.95, 1.05)  # ±5% variation
        mock_prices[symbol] = base_price * variation
    
    return mock_prices

def get_price_chart_data(symbol: str, interval: str = "1h", limit: int = 100) -> pd.DataFrame:
    """Get price chart data from multiple sources"""
    # Try CoinGecko first (more reliable)
    try:
        # Map symbols to CoinGecko IDs
        coin_mapping = {
            "BTCUSDT": "bitcoin",
            "ETHUSDT": "ethereum",
            "BNBUSDT": "binancecoin",
            "ADAUSDT": "cardano",
            "SOLUSDT": "solana",
            "XRPUSDT": "ripple",
            "DOTUSDT": "polkadot",
            "DOGEUSDT": "dogecoin",
            "AVAXUSDT": "avalanche-2",
            "MATICUSDT": "polygon"
        }
        
        coin_id = coin_mapping.get(symbol)
        if coin_id:
            # Map intervals to CoinGecko days
            interval_mapping = {
                "1m": ("1", "hourly"),
                "5m": ("1", "hourly"), 
                "15m": ("1", "hourly"),
                "30m": ("1", "hourly"),
                "1h": ("1", "hourly"),
                "4h": ("7", "hourly"),
                "1d": ("30", "daily"),
                "1w": ("365", "daily"),
                "1M": ("max", "daily")
            }
            
            days, interval_type = interval_mapping.get(interval, ("1", "hourly"))
            
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': interval_type
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'prices' in data and len(data['prices']) > 0:
                # Convert CoinGecko format to OHLC
                prices = data['prices'][-limit:]  # Get last N data points
                volumes = data['total_volumes'][-limit:] if 'total_volumes' in data else []
                
                chart_data = []
                for i, (timestamp, price) in enumerate(prices):
                    # Create realistic OHLC from price data
                    base_price = price
                    volatility = 0.02  # 2% volatility
                    
                    open_price = base_price
                    close_price = base_price
                    high_price = base_price * (1 + volatility * (0.5 + i % 2))
                    low_price = base_price * (1 - volatility * (0.5 + i % 2))
                    volume = volumes[i][1] if i < len(volumes) else 1000
                    
                    chart_data.append({
                        'timestamp': pd.to_datetime(timestamp, unit='ms'),
                        'open': open_price,
                        'high': high_price,
                        'low': low_price,
                        'close': close_price,
                        'volume': volume
                    })
                
                return pd.DataFrame(chart_data)
                
    except Exception:
        pass
    
    # Fallback to Binance
    try:
        url = f"https://api.binance.com/api/v3/klines"
        params = {
            'symbol': symbol.upper(),
            'interval': interval,
            'limit': limit
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades', 'taker_buy_base',
            'taker_buy_quote', 'ignore'
        ])
        
        # Convert to proper data types
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)
        
        return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
        
    except Exception:
        # Return mock chart data as last resort
        return get_mock_chart_data(symbol, limit)

def get_mock_chart_data(symbol: str, limit: int = 24) -> pd.DataFrame:
    """Generate mock chart data for demo"""
    import random
    import numpy as np
    
    # Base prices for different symbols
    base_prices = {
        "BTCUSDT": 45000.0,
        "ETHUSDT": 3000.0,
        "BNBUSDT": 300.0,
        "ADAUSDT": 0.5,
        "SOLUSDT": 100.0,
        "XRPUSDT": 0.6,
        "DOTUSDT": 7.0,
        "DOGEUSDT": 0.08,
        "AVAXUSDT": 25.0,
        "MATICUSDT": 0.8
    }
    
    base_price = base_prices.get(symbol, 100.0)
    
    # Generate timestamps (last 24 hours)
    end_time = datetime.now()
    timestamps = [end_time - timedelta(hours=i) for i in range(limit, 0, -1)]
    
    # Generate price data with some volatility
    prices = []
    current_price = base_price
    
    for i in range(limit):
        # Random walk with some volatility
        change = random.uniform(-0.02, 0.02)  # ±2% change per hour
        current_price *= (1 + change)
        
        # Generate OHLC data
        open_price = current_price
        high_price = open_price * random.uniform(1.0, 1.01)
        low_price = open_price * random.uniform(0.99, 1.0)
        close_price = random.uniform(low_price, high_price)
        volume = random.uniform(1000, 10000)
        
        prices.append({
            'timestamp': timestamps[i],
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price,
            'volume': volume
        })
        
        current_price = close_price
    
    return pd.DataFrame(prices)

def create_price_chart(symbol: str, timeframe: str = "1h") -> go.Figure:
    """Create a TradingView-style candlestick chart"""
    df = get_price_chart_data(symbol, timeframe)
    
    if df.empty:
        return go.Figure()
    
    # Create candlestick chart
    fig = go.Figure(data=go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name=symbol,
        increasing_line_color='#00ff88',
        decreasing_line_color='#ff4444',
        increasing_fillcolor='#00ff88',
        decreasing_fillcolor='#ff4444',
        line=dict(width=1),
        whiskerwidth=0.8,
        showlegend=False
    ))
    
    # Add volume subplot
    fig.add_trace(go.Bar(
        x=df['timestamp'],
        y=df['volume'],
        name='Volume',
        marker_color='rgba(158,202,225,0.6)',
        yaxis='y2',
        showlegend=False
    ))
    
    # Calculate technical indicators
    if len(df) >= 20:
        df['MA20'] = df['close'].rolling(window=20).mean()
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['MA20'],
            mode='lines',
            name='MA20',
            line=dict(color='orange', width=1),
            opacity=0.8
        ))
    
    if len(df) >= 50:
        df['MA50'] = df['close'].rolling(window=50).mean()
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['MA50'],
            mode='lines',
            name='MA50',
            line=dict(color='blue', width=1),
            opacity=0.8
        ))
    
    # Add RSI indicator
    if len(df) >= 14:
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Add RSI as secondary chart
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['RSI'],
            mode='lines',
            name='RSI',
            line=dict(color='purple', width=1),
            opacity=0.8,
            yaxis='y3'
        ))
    
    # Add Bollinger Bands
    if len(df) >= 20:
        df['BB_Middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['BB_Upper'],
            mode='lines',
            name='BB Upper',
            line=dict(color='gray', width=1, dash='dash'),
            opacity=0.6,
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['BB_Lower'],
            mode='lines',
            name='BB Lower',
            line=dict(color='gray', width=1, dash='dash'),
            opacity=0.6,
            showlegend=False,
            fill='tonexty',
            fillcolor='rgba(128,128,128,0.1)'
        ))
    
    # TradingView-style layout
    fig.update_layout(
        title={
            'text': f"{symbol} - {timeframe}",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#ffffff'}
        },
        xaxis=dict(
            title="Time",
            gridcolor='#2a2a2a',
            color='#ffffff',
            showgrid=True,
            gridwidth=1,
            type='date',
            rangeslider=dict(visible=False)
        ),
        yaxis=dict(
            title="Price (USDT)",
            gridcolor='#2a2a2a',
            color='#ffffff',
            showgrid=True,
            gridwidth=1,
            side='right'
        ),
        yaxis2=dict(
            title="Volume",
            overlaying='y',
            side='right',
            showgrid=False,
            color='#888888'
        ),
        yaxis3=dict(
            title="RSI",
            overlaying='y',
            side='right',
            showgrid=False,
            color='#888888',
            range=[0, 100]
        ),
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color='#ffffff'),
        height=500,
        margin=dict(l=50, r=50, t=80, b=50),
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Add crosshair
    fig.update_layout(
        xaxis=dict(
            showspikes=True,
            spikecolor="white",
            spikesnap="cursor",
            spikemode="across",
            spikethickness=1
        ),
        yaxis=dict(
            showspikes=True,
            spikecolor="white",
            spikesnap="cursor",
            spikemode="across",
            spikethickness=1
        )
    )
    
    return fig

def main():
    # Navigation
    page = show_navigation()
    
    if page == "🎓 Interactive Tutorial":
        # Import and run interactive tutorial
        from interactive_tutorial import main as tutorial_main
        tutorial_main()
        return
    
    if page == "🤖 Strategy Backtesting":
        # Import and run backtesting page
        from backtesting_page import main as backtesting_main
        backtesting_main()
        return
    
    if page == "🎯 AI Robo Advisor":
        # Import and run robo advisor page
        from robo_advisor_page import main as robo_advisor_main
        robo_advisor_main()
        return
    
    # Import and run unified trading platform
    from unified_trading_platform import main as unified_main
    unified_main()
    return

if __name__ == "__main__":
    main()

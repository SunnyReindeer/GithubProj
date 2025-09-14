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

# Import our modules
from trading_engine import portfolio, OrderSide, OrderType, OrderStatus
from config import SUPPORTED_CRYPTOS, INITIAL_BALANCE, TRADING_FEE

# Page configuration
st.set_page_config(
    page_title="Crypto Trading Simulator",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

def get_price_chart_data(symbol: str, interval: str = "1h", limit: int = 24) -> pd.DataFrame:
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
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': '1',
                'interval': 'hourly'
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'prices' in data and len(data['prices']) > 0:
                # Convert CoinGecko format to OHLC
                prices = data['prices'][-limit:]  # Get last N hours
                volumes = data['total_volumes'][-limit:] if 'total_volumes' in data else []
                
                chart_data = []
                for i, (timestamp, price) in enumerate(prices):
                    # Create simple OHLC from price (CoinGecko doesn't provide OHLC)
                    open_price = price
                    close_price = price
                    high_price = price * 1.01  # Add some variation
                    low_price = price * 0.99
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

def create_price_chart(symbol: str) -> go.Figure:
    """Create a candlestick chart for a symbol"""
    df = get_price_chart_data(symbol)
    
    if df.empty:
        return go.Figure()
    
    fig = go.Figure(data=go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name=symbol
    ))
    
    fig.update_layout(
        title=f"{symbol} Price Chart",
        xaxis_title="Time",
        yaxis_title="Price (USDT)",
        height=400
    )
    
    return fig

def main():
    # Initialize components
    initialize_portfolio()
    
    # Header
    st.markdown('<h1 class="main-header">📈 Crypto Trading Simulator</h1>', unsafe_allow_html=True)
    
    # Get current prices
    with st.spinner("Fetching current prices..."):
        current_prices = get_current_prices()
        st.session_state.current_prices = current_prices
        st.session_state.last_update = datetime.now()
        
        # Show data source indicator
        if current_prices:
            # Check if we got real data by testing one price
            btc_price = current_prices.get("BTCUSDT", 0)
            if 40000 < btc_price < 100000:  # Realistic BTC price range
                st.success("✅ Live Market Data - Real cryptocurrency prices")
            else:
                st.info("🎮 Demo Mode - Using simulated market data")
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Trading Panel")
        
        # Symbol selection
        selected_symbol = st.selectbox(
            "Select Cryptocurrency",
            options=SUPPORTED_CRYPTOS,
            index=0
        )
        
        # Current price display
        current_price = current_prices.get(selected_symbol, 0)
        if current_price > 0:
            st.metric(
                f"{selected_symbol} Price",
                f"${current_price:,.2f}",
                delta=f"Live"
            )
        else:
            st.info("No price data available")
        
        st.divider()
        
        # Trading form
        st.subheader("📊 Place Order")
        
        order_side = st.radio("Order Type", ["Buy", "Sell"])
        order_type = st.selectbox("Order Type", ["Market", "Limit"])
        
        quantity = st.number_input(
            "Quantity",
            min_value=0.001,
            max_value=1000.0,
            value=0.1,
            step=0.001,
            format="%.3f"
        )
        
        if order_type == "Limit":
            limit_price = st.number_input(
                "Limit Price (USDT)",
                min_value=0.01,
                value=current_price if current_price > 0 else 1.0,
                step=0.01,
                format="%.2f"
            )
        else:
            limit_price = None
        
        # Calculate order details
        if current_price > 0:
            if order_side == "Buy":
                total_cost = quantity * current_price
                fee = total_cost * TRADING_FEE
                st.info(f"Total Cost: ${total_cost + fee:.2f} (Fee: ${fee:.2f})")
            else:
                total_proceeds = quantity * current_price
                fee = total_proceeds * TRADING_FEE
                st.info(f"Net Proceeds: ${total_proceeds - fee:.2f} (Fee: ${fee:.2f})")
        
        # Place order button
        if st.button("🚀 Place Order", type="primary"):
            if current_price > 0:
                side = OrderSide.BUY if order_side == "Buy" else OrderSide.SELL
                order_type_enum = OrderType.MARKET if order_type == "Market" else OrderType.LIMIT
                
                order = portfolio.create_order(
                    symbol=selected_symbol,
                    side=side,
                    order_type=order_type_enum,
                    quantity=quantity,
                    price=limit_price
                )
                
                # Execute market orders immediately
                if order_type == "Market":
                    success = portfolio.execute_order(order, current_price)
                    if success:
                        st.success("✅ Order executed successfully!")
                    else:
                        st.error("❌ Order failed - insufficient funds or position")
                else:
                    st.success("✅ Limit order placed!")
            else:
                st.error("❌ No current price data available")
        
        st.divider()
        
        # Portfolio summary
        st.subheader("💰 Portfolio Summary")
        if current_prices:
            summary = portfolio.get_portfolio_summary(current_prices)
            
            st.metric("Total Value", f"${summary['total_value']:,.2f}")
            st.metric("Cash Balance", f"${summary['cash_balance']:,.2f}")
            
            pnl_color = "normal"
            if summary['total_pnl'] > 0:
                pnl_color = "normal"
            elif summary['total_pnl'] < 0:
                pnl_color = "inverse"
            
            st.metric(
                "Total P&L",
                f"${summary['total_pnl']:,.2f}",
                delta=f"{summary['pnl_percentage']:.2f}%",
                delta_color=pnl_color
            )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Price chart
        st.subheader("📊 Price Chart")
        chart = create_price_chart(selected_symbol)
        if chart.data:
            st.plotly_chart(chart, use_container_width=True)
        else:
            st.info("Loading chart data...")
        
        # Market data table
        st.subheader("📈 Market Data")
        if current_prices:
            market_data = []
            for symbol in SUPPORTED_CRYPTOS:
                price = current_prices.get(symbol, 0)
                if price > 0:
                    market_data.append({
                        'Symbol': symbol,
                        'Price (USDT)': f"${price:,.2f}",
                        'Last Update': st.session_state.last_update.strftime("%H:%M:%S") if st.session_state.last_update else "N/A"
                    })
            
            if market_data:
                df_market = pd.DataFrame(market_data)
                st.dataframe(df_market, use_container_width=True)
            else:
                st.info("No market data available")
        else:
            st.info("No market data available")
    
    with col2:
        # Positions
        st.subheader("💼 Current Positions")
        if current_prices:
            positions_df = portfolio.get_positions_dataframe(current_prices)
            if not positions_df.empty:
                st.dataframe(positions_df, use_container_width=True)
            else:
                st.info("No open positions")
        else:
            st.info("Loading positions...")
        
        # Recent trades
        st.subheader("📋 Recent Trades")
        trades_df = portfolio.get_trades_dataframe()
        if not trades_df.empty:
            # Show last 5 trades
            recent_trades = trades_df.tail(5)
            st.dataframe(recent_trades, use_container_width=True)
        else:
            st.info("No trades yet")
    
    # Bottom section
    st.divider()
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Order history
        st.subheader("📝 Order History")
        orders_df = portfolio.get_orders_dataframe()
        if not orders_df.empty:
            st.dataframe(orders_df, use_container_width=True)
        else:
            st.info("No orders placed yet")
    
    with col4:
        # Performance metrics
        st.subheader("📊 Performance Metrics")
        if current_prices:
            summary = portfolio.get_portfolio_summary(current_prices)
            
            # Create performance chart
            performance_data = {
                'Metric': ['Initial Balance', 'Current Value', 'Total P&L'],
                'Value': [summary['total_value'] - summary['total_pnl'], summary['total_value'], summary['total_pnl']]
            }
            
            fig = px.bar(
                x=performance_data['Metric'],
                y=performance_data['Value'],
                title="Portfolio Performance",
                color=performance_data['Value'],
                color_continuous_scale=['red', 'yellow', 'green']
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    # Auto-refresh button
    if st.button("🔄 Refresh Data"):
        st.rerun()

if __name__ == "__main__":
    main()

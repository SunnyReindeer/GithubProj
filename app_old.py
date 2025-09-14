"""
Crypto Trading Simulator - Streamlit App
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import threading
from typing import Dict, List

# Import our modules
from data_fetcher import data_fetcher
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
    st.session_state.data_fetcher_started = False
    st.session_state.current_prices = {}
    st.session_state.last_update = None

def initialize_portfolio():
    """Initialize portfolio if not already done"""
    if not st.session_state.portfolio_initialized:
        portfolio.__init__(INITIAL_BALANCE)
        st.session_state.portfolio_initialized = True

def start_data_fetcher():
    """Start the data fetcher if not already running"""
    if not st.session_state.data_fetcher_started:
        def price_update_callback(price_data):
            # Store price data in a thread-safe way
            if hasattr(st.session_state, 'current_prices'):
                st.session_state.current_prices[price_data['symbol']] = price_data['price']
                st.session_state.last_update = datetime.now()
        
        data_fetcher.add_subscriber(price_update_callback)
        data_fetcher.start_websocket()
        st.session_state.data_fetcher_started = True

def get_price_chart_data(symbol: str, interval: str = "1h", limit: int = 24) -> pd.DataFrame:
    """Get price chart data"""
    return data_fetcher.get_historical_data(symbol, interval, limit)

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
    start_data_fetcher()
    
    # Header
    st.markdown('<h1 class="main-header">📈 Crypto Trading Simulator</h1>', unsafe_allow_html=True)
    
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
        current_price = st.session_state.current_prices.get(selected_symbol, 0)
        if current_price > 0:
            st.metric(
                f"{selected_symbol} Price",
                f"${current_price:,.2f}",
                delta=f"Real-time"
            )
        else:
            st.info("Connecting to market data...")
        
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
        if st.session_state.current_prices:
            summary = portfolio.get_portfolio_summary(st.session_state.current_prices)
            
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
        if st.session_state.current_prices:
            market_data = []
            for symbol in SUPPORTED_CRYPTOS:
                price = st.session_state.current_prices.get(symbol, 0)
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
                st.info("Waiting for market data...")
        else:
            st.info("Connecting to market data...")
    
    with col2:
        # Positions
        st.subheader("💼 Current Positions")
        if st.session_state.current_prices:
            positions_df = portfolio.get_positions_dataframe(st.session_state.current_prices)
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
        if st.session_state.current_prices:
            summary = portfolio.get_portfolio_summary(st.session_state.current_prices)
            
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
    
    # Auto-refresh
    if st.session_state.data_fetcher_started:
        time.sleep(1)
        st.rerun()

if __name__ == "__main__":
    main()

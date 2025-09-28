"""
Unified Trading Platform
Combines crypto and multi-asset trading into one comprehensive platform
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
from typing import Dict, List, Any

# Import our modules
from trading_engine import portfolio, OrderSide, OrderType, OrderStatus
from config import SUPPORTED_CRYPTOS, INITIAL_BALANCE, TRADING_FEE
from tradingview_widget import create_tradingview_widget, create_tradingview_advanced_chart, create_tradingview_screener, create_tradingview_crypto_heatmap

# Import multi-asset modules
from multi_asset_config import multi_asset_config, AssetClass, AssetRegion, AssetSector
from multi_asset_data_provider import multi_asset_data_provider, PriceData
from multi_asset_portfolio import multi_asset_portfolio, OrderSide as MAOrderSide, OrderType as MAOrderType, OrderStatus as MAOrderStatus

# Page configuration
st.set_page_config(
    page_title="Unified Trading Platform",
    page_icon="🌍",
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
    .asset-class-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
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
    st.session_state.selected_asset_class = AssetClass.CRYPTO
    st.session_state.selected_symbols = []
    st.session_state.use_multi_asset = True

# Ensure use_multi_asset is always initialized
if 'use_multi_asset' not in st.session_state:
    st.session_state.use_multi_asset = True

def map_symbol_to_tradingview(symbol: str) -> str:
    """Map our symbols to TradingView format"""
    # Crypto symbols
    crypto_mapping = {
        "BTCUSDT": "BINANCE:BTCUSDT",
        "ETHUSDT": "BINANCE:ETHUSDT",
        "BNBUSDT": "BINANCE:BNBUSDT",
        "ADAUSDT": "BINANCE:ADAUSDT",
        "SOLUSDT": "BINANCE:SOLUSDT",
        "XRPUSDT": "BINANCE:XRPUSDT",
        "DOTUSDT": "BINANCE:DOTUSDT",
        "DOGEUSDT": "BINANCE:DOGEUSDT",
        "AVAXUSDT": "BINANCE:AVAXUSDT",
        "MATICUSDT": "BINANCE:MATICUSDT"
    }
    
    # Stock symbols
    stock_mapping = {
        "AAPL": "NASDAQ:AAPL",
        "GOOGL": "NASDAQ:GOOGL",
        "MSFT": "NASDAQ:MSFT",
        "TSLA": "NASDAQ:TSLA",
        "AMZN": "NASDAQ:AMZN",
        "META": "NASDAQ:META",
        "NVDA": "NASDAQ:NVDA",
        "NFLX": "NASDAQ:NFLX",
        "SPY": "SPDR:SPY",
        "QQQ": "NASDAQ:QQQ"
    }
    
    # Forex symbols
    forex_mapping = {
        "EURUSD": "FX:EURUSD",
        "GBPUSD": "FX:GBPUSD",
        "USDJPY": "FX:USDJPY",
        "USDCHF": "FX:USDCHF",
        "AUDUSD": "FX:AUDUSD",
        "USDCAD": "FX:USDCAD",
        "NZDUSD": "FX:NZDUSD"
    }
    
    # Commodity symbols
    commodity_mapping = {
        "GOLD": "TVC:GOLD",
        "SILVER": "TVC:SILVER",
        "OIL": "TVC:CRUDE",
        "COPPER": "TVC:COPPER",
        "NATURAL_GAS": "TVC:NATURALGAS"
    }
    
    # Check all mappings
    if symbol in crypto_mapping:
        return crypto_mapping[symbol]
    elif symbol in stock_mapping:
        return stock_mapping[symbol]
    elif symbol in forex_mapping:
        return forex_mapping[symbol]
    elif symbol in commodity_mapping:
        return commodity_mapping[symbol]
    else:
        # Default to crypto if not found
        return f"BINANCE:{symbol}"

def initialize_portfolio():
    """Initialize portfolio if not already done"""
    if not st.session_state.portfolio_initialized:
        multi_asset_portfolio.__init__(INITIAL_BALANCE)
        st.session_state.portfolio_initialized = True

def get_current_prices(symbols: List[str]) -> Dict[str, Any]:
    """Get current prices for symbols using appropriate data provider"""
    try:
        # Use multi-asset data provider
        price_data = multi_asset_data_provider.get_current_prices(symbols)
        # Return the full price objects for portfolio calculations
        return price_data
    except Exception as e:
        st.error(f"Error fetching prices: {e}")
        return {}

def create_asset_class_selector():
    """Create asset class selector"""
    st.sidebar.markdown("## 🌍 Asset Class Selection")
    
    # Always use unified multi-asset platform
    asset_classes = multi_asset_config.get_supported_asset_classes()
    asset_class_names = [ac.value.replace('_', ' ').title() for ac in asset_classes]
    
    # Find the index of the currently selected asset class
    try:
        selected_index = asset_classes.index(st.session_state.get('selected_asset_class', AssetClass.CRYPTO))
    except (ValueError, AttributeError):
        selected_index = 0  # Default to first option if not found
    
    selected_name = st.sidebar.selectbox(
        "Select Asset Class",
        options=asset_class_names,
        index=selected_index
    )
    
    # Update selected asset class
    selected_asset_class = AssetClass(selected_name.lower().replace(' ', '_'))
    
    # Clear selected symbols if asset class changed
    if st.session_state.get('selected_asset_class') != selected_asset_class:
        st.session_state.selected_symbols = []
    
    st.session_state.selected_asset_class = selected_asset_class
    
    return selected_asset_class

def create_symbol_selector(asset_class: AssetClass):
    """Create symbol selector for the selected asset class"""
    st.sidebar.markdown("### 📊 Symbol Selection")
    
    if asset_class != AssetClass.CRYPTO:
        # Get assets for the selected class
        assets = multi_asset_config.get_assets_by_class(asset_class)
        
        if not assets:
            st.sidebar.warning("No assets available for this class")
            return []
        
        # Create symbol options
        symbol_options = [f"{asset.symbol} - {asset.name}" for asset in assets[:20]]  # Limit to 20 for performance
        
        # Get current session state symbols and filter to only include valid options
        current_selected = st.session_state.get('selected_symbols', [])
        valid_defaults = [option for option in symbol_options if any(symbol in option for symbol in current_selected)]
        
        selected_symbols = st.sidebar.multiselect(
            "Select Symbols",
            options=symbol_options,
            default=valid_defaults
        )
        
        # Extract symbols from selected options
        symbols = [option.split(' - ')[0] for option in selected_symbols]
        st.session_state.selected_symbols = symbols
        
        return symbols
    else:
        # Use original crypto symbols
        # Get current session state symbols and filter to only include valid crypto options
        current_selected = st.session_state.get('selected_symbols', [])
        valid_defaults = [symbol for symbol in current_selected if symbol in SUPPORTED_CRYPTOS]
        
        selected_symbols = st.sidebar.multiselect(
            "Select Cryptocurrencies",
            options=SUPPORTED_CRYPTOS,
            default=valid_defaults
        )
        st.session_state.selected_symbols = selected_symbols
        return selected_symbols

def display_market_overview():
    """Display market overview for all asset classes"""
    st.markdown("## 📈 Market Overview")
    
    if st.session_state.get('use_multi_asset', True):
        with st.spinner("Fetching market data..."):
            market_overview = multi_asset_data_provider.get_market_overview()
        
        # Create columns for each asset class
        cols = st.columns(len(market_overview))
        
        for i, (asset_class, data) in enumerate(market_overview.items()):
            with cols[i]:
                st.markdown(f"### {asset_class.title()}")
                
                # Average change
                avg_change = data['average_change']
                change_color = "normal" if avg_change >= 0 else "inverse"
                st.metric(
                    "Avg Change",
                    f"{avg_change:.2f}%",
                    delta_color=change_color
                )
                
                # Top gainer
                if data['top_gainers']:
                    top_gainer = data['top_gainers'][0]
                    st.metric(
                        "Top Gainer",
                        f"{top_gainer.symbol}",
                        f"{top_gainer.change_percent:.2f}%"
                    )
                
                # Top loser
                if data['top_losers']:
                    top_loser = data['top_losers'][0]
                    st.metric(
                        "Top Loser",
                        f"{top_loser.symbol}",
                        f"{top_loser.change_percent:.2f}%"
                    )
    else:
        # Original crypto market overview
        current_prices = get_current_prices([])
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

def display_price_charts(symbols: List[str]):
    """Display price charts for selected symbols"""
    if not symbols:
        st.info("Please select symbols to view charts")
        return
    
    st.markdown("## 📊 Price Charts")
    
    # Chart display options
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        chart_type = st.radio(
            "Chart Type",
            ["📊 Standard", "📈 TradingView Widget"],
            help="Standard: Basic candlestick charts | TradingView Widget: Real TradingView embedded widget"
        )
    
    with col2:
        if chart_type == "📊 Standard":
            timeframe = st.selectbox(
                "Time Period",
                ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
                index=3,  # Default to 1y
                help="Select data period for standard charts"
            )
        else:
            timeframe = "1h"  # Default for TradingView widget
    
    # Always use multi-asset data provider (unified platform)
    for symbol in symbols[:4]:  # Limit to 4 charts for performance
        try:
            # Use selected timeframe for standard charts, default for TradingView
            period = timeframe if chart_type == "📊 Standard" else "3mo"
            historical_data = multi_asset_data_provider.get_historical_data(symbol, period=period, interval="1d")
            
            if historical_data and not historical_data.data.empty:
                df = historical_data.data
                
                if chart_type == "📊 Standard":
                    # Create basic candlestick chart
                    fig = go.Figure(data=go.Candlestick(
                        x=df.index,
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'],
                        name=symbol
                    ))
                    
                    # Add moving averages
                    df['MA20'] = df['Close'].rolling(window=20).mean()
                    df['MA50'] = df['Close'].rolling(window=50).mean()
                    
                    fig.add_trace(go.Scatter(
                        x=df.index,
                        y=df['MA20'],
                        mode='lines',
                        name='MA20',
                        line=dict(color='orange', width=1)
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=df.index,
                        y=df['MA50'],
                        mode='lines',
                        name='MA50',
                        line=dict(color='blue', width=1)
                    ))
                    
                    # Update layout for standard chart
                    fig.update_layout(
                        title=f"{symbol} - {timeframe.upper()} Chart (Standard)",
                        xaxis_title="Date",
                        yaxis_title="Price",
                        height=400,
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                else:
                    # Use actual TradingView widget
                    from tradingview_widget import create_tradingview_advanced_chart
                    
                    # Map symbol to TradingView format
                    tv_symbol = map_symbol_to_tradingview(symbol)
                    
                    # Debug: Show what symbol is being passed
                    st.markdown(f"### {symbol} - TradingView Chart")
                    st.info(f"Displaying: {symbol} → {tv_symbol}")
                    
                    # Create unique widget ID with timestamp to force refresh
                    import time
                    widget_id = f"tradingview_{symbol}_{int(time.time())}"
                    create_tradingview_advanced_chart(tv_symbol, "1h", height=600, container_id=widget_id)
                
        except Exception as e:
            st.error(f"Error loading chart for {symbol}: {e}")

def create_trading_panel(symbols: List[str]):
    """Create trading panel for placing orders"""
    st.markdown("## 💼 Trading Panel")
    
    if not symbols:
        st.warning("Please select symbols to trade")
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📝 Place Order")
        
        # Symbol selection
        selected_symbol = st.selectbox("Select Symbol", options=symbols)
        
        # Order details
        order_side = st.radio("Order Side", ["Buy", "Sell"])
        order_type = st.selectbox("Order Type", ["Market", "Limit"])
        
        # Quantity input
        quantity = st.number_input(
            "Quantity",
            min_value=0.001,
            max_value=10000.0,
            value=1.0,
            step=0.001,
            format="%.3f"
        )
        
        # Price input for limit orders
        if order_type == "Limit":
            current_prices = get_current_prices([selected_symbol])
            current_price = current_prices.get(selected_symbol, 100)
            limit_price = st.number_input(
                "Limit Price",
                min_value=0.01,
                value=current_price,
                step=0.01,
                format="%.2f"
            )
        else:
            limit_price = None
        
        # Place order button
        if st.button("🚀 Place Order", type="primary"):
            if quantity > 0:
                if st.session_state.get('use_multi_asset', True):
                    # Use multi-asset portfolio
                    side = MAOrderSide.BUY if order_side == "Buy" else MAOrderSide.SELL
                    order_type_enum = MAOrderType.MARKET if order_type == "Market" else MAOrderType.LIMIT
                    
                    order = multi_asset_portfolio.create_order(
                        symbol=selected_symbol,
                        side=side,
                        order_type=order_type_enum,
                        quantity=quantity,
                        price=limit_price
                    )
                    
                    # Execute market orders immediately
                    if order_type == "Market":
                        current_prices = get_current_prices([selected_symbol])
                        current_price = current_prices.get(selected_symbol)
                        if current_price:
                            success = multi_asset_portfolio.execute_order(order, current_price)
                            if success:
                                st.success("✅ Order executed successfully!")
                            else:
                                st.error("❌ Order failed - insufficient funds or position")
                        else:
                            st.error("❌ No current price data available")
                    else:
                        st.success("✅ Limit order placed!")
                else:
                    # Use original crypto portfolio
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
                        current_prices = get_current_prices([])
                        current_price = current_prices.get(selected_symbol)
                        if current_price:
                            success = portfolio.execute_order(order, current_price)
                            if success:
                                st.success("✅ Order executed successfully!")
                            else:
                                st.error("❌ Order failed - insufficient funds or position")
                        else:
                            st.error("❌ No current price data available")
                    else:
                        st.success("✅ Limit order placed!")
            else:
                st.error("❌ Invalid quantity")
    
    with col2:
        st.markdown("### 📊 Order Summary")
        
        if selected_symbol:
            current_prices = get_current_prices([selected_symbol])
            current_price = current_prices.get(selected_symbol)
            
            if current_price:
                st.metric(
                    f"{selected_symbol} Current Price",
                    f"${current_price:.2f}",
                    delta="Live"
                )
                
                # Calculate order details
                if quantity > 0:
                    if order_side == "Buy":
                        total_cost = quantity * (current_price if order_type == "Market" else limit_price)
                        st.info(f"""
                        **Buy Order Summary:**
                        - Quantity: {quantity:.3f} shares
                        - Price: ${current_price if order_type == "Market" else limit_price:.2f}
                        - Total Cost: ${total_cost:.2f}
                        """)
                    else:
                        total_proceeds = quantity * (current_price if order_type == "Market" else limit_price)
                        st.info(f"""
                        **Sell Order Summary:**
                        - Quantity: {quantity:.3f} shares
                        - Price: ${current_price if order_type == "Market" else limit_price:.2f}
                        - Total Proceeds: ${total_proceeds:.2f}
                        """)

def display_portfolio_summary():
    """Display portfolio summary"""
    st.markdown("## 💰 Portfolio Summary")
    
    if st.session_state.get('use_multi_asset', True):
        # Get current prices for all positions
        symbols = list(multi_asset_portfolio.positions.keys())
        if symbols:
            current_prices = get_current_prices(symbols)
        else:
            current_prices = {}
        
        # Calculate portfolio metrics
        metrics = multi_asset_portfolio.get_portfolio_metrics(current_prices)
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Value", f"${metrics.total_value:,.2f}")
        
        with col2:
            st.metric("Total P&L", f"${metrics.total_pnl:,.2f}")
        
        with col3:
            pnl_color = "normal" if metrics.total_pnl >= 0 else "inverse"
            st.metric(
                "P&L %",
                f"{metrics.total_pnl_percent:.2f}%",
                delta_color=pnl_color
            )
        
        with col4:
            st.metric("Positions", len(multi_asset_portfolio.positions))
        
        # Asset class allocation
        if metrics.asset_class_allocation:
            st.markdown("### 📊 Asset Class Allocation")
            
            allocation_data = []
            for asset_class, percentage in metrics.asset_class_allocation.items():
                allocation_data.append({
                    'Asset Class': asset_class.replace('_', ' ').title(),
                    'Allocation %': percentage
                })
            
            df_allocation = pd.DataFrame(allocation_data)
            
            # Create pie chart
            fig = px.pie(
                df_allocation,
                values='Allocation %',
                names='Asset Class',
                title="Portfolio Allocation by Asset Class"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display allocation table
            st.dataframe(
                df_allocation.style.format({'Allocation %': '{:.1f}%'}),
                use_container_width=True
            )
    else:
        # Original crypto portfolio summary
        current_prices = get_current_prices([])
        if current_prices:
            summary = portfolio.get_portfolio_summary(current_prices)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Value", f"${summary['total_value']:,.2f}")
            
            with col2:
                st.metric("Cash Balance", f"${summary['cash_balance']:,.2f}")
            
            with col3:
                pnl_color = "normal" if summary['total_pnl'] > 0 else "inverse"
                st.metric(
                    "Total P&L",
                    f"${summary['total_pnl']:,.2f}",
                    delta=f"{summary['pnl_percentage']:.2f}%",
                    delta_color=pnl_color
                )

def display_positions():
    """Display current positions"""
    st.markdown("## 💼 Current Positions")
    
    if st.session_state.get('use_multi_asset', True):
        # Get current prices
        symbols = list(multi_asset_portfolio.positions.keys())
        if symbols:
            try:
                current_prices = get_current_prices(symbols)
                if current_prices:  # Check if we got valid price data
                    positions_df = multi_asset_portfolio.get_positions_dataframe(current_prices)
                    
                    if not positions_df.empty:
                        st.dataframe(positions_df, use_container_width=True)
                    else:
                        st.info("No open positions")
                else:
                    st.warning("Unable to fetch current prices for positions")
            except Exception as e:
                st.error(f"Error loading positions: {e}")
        else:
            st.info("No open positions")
    else:
        # Original crypto positions
        current_prices = get_current_prices([])
        if current_prices:
            positions_df = portfolio.get_positions_dataframe(current_prices)
            if not positions_df.empty:
                st.dataframe(positions_df, use_container_width=True)
            else:
                st.info("No open positions")
        else:
            st.info("Loading positions...")

def display_trades():
    """Display recent trades"""
    st.markdown("## 📋 Recent Trades")
    
    if st.session_state.get('use_multi_asset', True):
        trades_df = multi_asset_portfolio.get_trades_dataframe()
        if not trades_df.empty:
            # Show last 10 trades
            recent_trades = trades_df.tail(10)
            st.dataframe(recent_trades, use_container_width=True)
        else:
            st.info("No trades yet")
    else:
        # Original crypto trades
        trades_df = portfolio.get_trades_dataframe()
        if not trades_df.empty:
            # Show last 5 trades
            recent_trades = trades_df.tail(5)
            st.dataframe(recent_trades, use_container_width=True)
        else:
            st.info("No trades yet")

def main():
    """Main unified trading platform"""
    # Initialize components
    initialize_portfolio()
    
    # Header
    st.markdown('<h1 class="main-header">🌍 Unified Trading Platform</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎛️ Control Panel")
        
        # Asset class selection
        selected_asset_class = create_asset_class_selector()
        
        # Symbol selection
        selected_symbols = create_symbol_selector(selected_asset_class)
        
    # Portfolio summary
    st.markdown("## 💰 Portfolio Summary")
    symbols = list(multi_asset_portfolio.positions.keys())
    if symbols:
        try:
            current_prices = get_current_prices(symbols)
            if current_prices:  # Check if we got valid price data
                # Debug: Check the structure of price data
                st.write(f"Debug: Price data keys: {list(current_prices.keys())}")
                if symbols:
                    first_symbol = symbols[0]
                    if first_symbol in current_prices:
                        price_obj = current_prices[first_symbol]
                        st.write(f"Debug: Price object type: {type(price_obj)}")
                        st.write(f"Debug: Price object attributes: {dir(price_obj)}")
                
                metrics = multi_asset_portfolio.get_portfolio_metrics(current_prices)
                
                st.metric("Total Value", f"${metrics.total_value:,.2f}")
                st.metric("Total P&L", f"${metrics.total_pnl:,.2f}")
                pnl_color = "normal" if metrics.total_pnl >= 0 else "inverse"
                st.metric(
                    "P&L %",
                    f"{metrics.total_pnl_percent:.2f}%",
                    delta_color=pnl_color
                )
            else:
                st.warning("Unable to fetch current prices")
        except Exception as e:
            st.error(f"Error calculating portfolio metrics: {e}")
    else:
        st.info("No positions to display")
    
    # Main content
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Market Overview", 
        "📊 Charts", 
        "💼 Trading", 
        "💰 Portfolio"
    ])
    
    with tab1:
        display_market_overview()
    
    with tab2:
        display_price_charts(selected_symbols)
    
    with tab3:
        create_trading_panel(selected_symbols)
    
    with tab4:
        display_portfolio_summary()
        
        col1, col2 = st.columns(2)
        
        with col1:
            display_positions()
        
        with col2:
            display_trades()
    
    # Auto-refresh button
    if st.button("🔄 Refresh Data"):
        st.rerun()

if __name__ == "__main__":
    main()

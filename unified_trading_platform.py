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
    """Display comprehensive market overview dashboard"""
    st.markdown("## 📊 Market Dashboard")
    
    with st.spinner("Loading market data..."):
        market_overview = multi_asset_data_provider.get_market_overview()
    
    # Market Summary Cards
    st.markdown("### 📈 Market Summary")
    
    # Calculate overall market metrics
    total_assets = 0
    total_positive = 0
    total_negative = 0
    overall_change = 0
    
    for asset_class, data in market_overview.items():
        total_assets += len(data.get('top_gainers', [])) + len(data.get('top_losers', []))
        if data.get('top_gainers'):
            total_positive += len([g for g in data['top_gainers'] if g.change_percent > 0])
        if data.get('top_losers'):
            total_negative += len([l for l in data['top_losers'] if l.change_percent < 0])
        overall_change += data.get('average_change', 0)
    
    overall_change = overall_change / len(market_overview) if market_overview else 0
    
    # Market summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Assets",
            f"{total_assets}",
            help="Total number of tracked assets"
        )
    
    with col2:
        st.metric(
            "Market Sentiment",
            "🟢 Bullish" if overall_change > 0 else "🔴 Bearish",
            f"{overall_change:.2f}%",
            delta_color="normal" if overall_change > 0 else "inverse"
        )
    
    with col3:
        st.metric(
            "Advancing",
            f"{total_positive}",
            help="Assets with positive changes"
        )
    
    with col4:
        st.metric(
            "Declining",
            f"{total_negative}",
            help="Assets with negative changes"
        )
    
    st.markdown("---")
    
    # Asset Class Performance
    st.markdown("### 🎯 Asset Class Performance")
    
    # Create performance chart
    asset_classes = list(market_overview.keys())
    avg_changes = [market_overview[ac].get('average_change', 0) for ac in asset_classes]
    
    # Performance chart
    fig = px.bar(
        x=asset_classes,
        y=avg_changes,
        title="Average Performance by Asset Class",
        color=avg_changes,
        color_continuous_scale=['red', 'yellow', 'green'],
        labels={'x': 'Asset Class', 'y': 'Average Change (%)'}
    )
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed asset class breakdown
    st.markdown("### 📊 Asset Class Breakdown")
    
    for asset_class, data in market_overview.items():
        with st.expander(f"🔍 {asset_class.title()} - {data.get('average_change', 0):.2f}%", expanded=False):
            
            # Asset class metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Average Change",
                    f"{data.get('average_change', 0):.2f}%",
                    delta_color="normal" if data.get('average_change', 0) >= 0 else "inverse"
                )
            
            with col2:
                st.metric(
                    "Top Gainers",
                    f"{len(data.get('top_gainers', []))}",
                    help="Number of assets with positive performance"
                )
            
            with col3:
                st.metric(
                    "Top Losers",
                    f"{len(data.get('top_losers', []))}",
                    help="Number of assets with negative performance"
                )
            
            # Top performers table
            if data.get('top_gainers') or data.get('top_losers'):
                st.markdown("#### 🏆 Top Performers")
                
                # Combine gainers and losers
                all_performers = []
                if data.get('top_gainers'):
                    for gainer in data['top_gainers'][:5]:  # Top 5
                        all_performers.append({
                            'Symbol': gainer.symbol,
                            'Change': f"{gainer.change_percent:.2f}%",
                            'Status': '🟢 Gainer',
                            'Price': f"${gainer.price:.2f}" if hasattr(gainer, 'price') else "N/A"
                        })
                
                if data.get('top_losers'):
                    for loser in data['top_losers'][:5]:  # Top 5
                        all_performers.append({
                            'Symbol': loser.symbol,
                            'Change': f"{loser.change_percent:.2f}%",
                            'Status': '🔴 Loser',
                            'Price': f"${loser.price:.2f}" if hasattr(loser, 'price') else "N/A"
                        })
                
                if all_performers:
                    df_performers = pd.DataFrame(all_performers)
                    st.dataframe(df_performers, use_container_width=True)
    
    # Market Heatmap
    st.markdown("### 🔥 Market Heatmap")
    
    # Create a simple heatmap of asset performance
    heatmap_data = []
    for asset_class, data in market_overview.items():
        if data.get('top_gainers'):
            for gainer in data['top_gainers'][:3]:  # Top 3 from each class
                heatmap_data.append({
                    'Asset Class': asset_class.title(),
                    'Symbol': gainer.symbol,
                    'Change': gainer.change_percent,
                    'Price': gainer.price if hasattr(gainer, 'price') else 0
                })
        if data.get('top_losers'):
            for loser in data['top_losers'][:3]:  # Top 3 from each class
                heatmap_data.append({
                    'Asset Class': asset_class.title(),
                    'Symbol': loser.symbol,
                    'Change': loser.change_percent,
                    'Price': loser.price if hasattr(loser, 'price') else 0
                })
    
    if heatmap_data:
        df_heatmap = pd.DataFrame(heatmap_data)
        
        # Create heatmap
        fig_heatmap = px.treemap(
            df_heatmap,
            path=['Asset Class', 'Symbol'],
            values='Price',
            color='Change',
            color_continuous_scale=['red', 'yellow', 'green'],
            title="Market Performance Heatmap",
            hover_data=['Change', 'Price']
        )
        fig_heatmap.update_layout(height=500)
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Market News/Insights Section
    st.markdown("### 📰 Market Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Key Insights")
        insights = []
        
        if overall_change > 0:
            insights.append("🟢 **Bullish Market**: Overall positive sentiment across asset classes")
        else:
            insights.append("🔴 **Bearish Market**: Negative sentiment prevailing")
        
        if total_positive > total_negative:
            insights.append("📈 **Advancing Market**: More assets gaining than losing")
        else:
            insights.append("📉 **Declining Market**: More assets losing than gaining")
        
        # Find best performing asset class
        best_class = max(market_overview.keys(), key=lambda x: market_overview[x].get('average_change', 0))
        insights.append(f"🏆 **Best Performer**: {best_class.title()} leading the market")
        
        for insight in insights:
            st.markdown(insight)
    
    with col2:
        st.markdown("#### 💡 Trading Tips")
        tips = [
            "📊 **Diversify**: Spread risk across different asset classes",
            "🎯 **Focus**: Pay attention to top performers in each category",
            "⏰ **Timing**: Monitor market sentiment for entry/exit points",
            "📈 **Trends**: Follow asset class performance trends",
            "🛡️ **Risk**: Consider volatility when making decisions"
        ]
        
        for tip in tips:
            st.markdown(tip)

def display_price_charts(symbols: List[str]):
    """Display price charts for selected symbols"""
    # Import contextual tutorial
    from contextual_tutorial import show_tutorial_for_tab, add_element_id
    
    # Show tutorial for price charts
    show_tutorial_for_tab("price_charts")
    
    if not symbols:
        st.info("Please select symbols to view charts")
        return
    
    st.markdown("## 📊 Price Charts")
    
    # Add container for charts header
    st.markdown('<div id="charts-header">', unsafe_allow_html=True)
    
    # Chart display options
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.markdown('<div id="chart-type-selector">', unsafe_allow_html=True)
        chart_type = st.radio(
            "Chart Type",
            ["📊 Standard", "📈 TradingView Widget"],
            help="Standard: Basic candlestick charts | TradingView Widget: Real TradingView embedded widget"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if chart_type == "📊 Standard":
            st.markdown('<div id="timeframe-selector">', unsafe_allow_html=True)
            timeframe = st.selectbox(
                "Time Period",
                ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
                index=3,  # Default to 1y
                help="Select data period for standard charts"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            timeframe = "1h"  # Default for TradingView widget
    
    # Close charts header container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add container for chart display
    st.markdown('<div id="chart-display">', unsafe_allow_html=True)
    
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
    
    # Close chart display container
    st.markdown('</div>', unsafe_allow_html=True)

def create_trading_panel(symbols: List[str]):
    """Create trading panel for placing orders"""
    # Import contextual tutorial
    from contextual_tutorial import show_tutorial_for_tab, add_element_id
    
    # Show tutorial for trading
    show_tutorial_for_tab("trading")
    
    st.markdown("## 💼 Trading Panel")
    
    # Add container for trading header
    st.markdown('<div id="trading-header">', unsafe_allow_html=True)
    
    if not symbols:
        st.warning("Please select symbols to trade")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📝 Place Order")
        
        # Symbol selection
        st.markdown('<div id="symbol-selector">', unsafe_allow_html=True)
        selected_symbol = st.selectbox("Select Symbol", options=symbols)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Order details
        st.markdown('<div id="order-side">', unsafe_allow_html=True)
        order_side = st.radio("Order Side", ["Buy", "Sell"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div id="order-type">', unsafe_allow_html=True)
        order_type = st.selectbox("Order Type", ["Market", "Limit"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quantity input
        st.markdown('<div id="quantity-input">', unsafe_allow_html=True)
        quantity = st.number_input(
            "Quantity",
            min_value=0.001,
            max_value=10000.0,
            value=1.0,
            step=0.001,
            format="%.3f"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
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
                            price_value = current_price.price if hasattr(current_price, 'price') else current_price
                            success = multi_asset_portfolio.execute_order(order, price_value)
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
                        current_prices = get_current_prices([selected_symbol])
                        current_price = current_prices.get(selected_symbol)
                        if current_price:
                            price_value = current_price.price if hasattr(current_price, 'price') else current_price
                            success = portfolio.execute_order(order, price_value)
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
                price_value = current_price.price if hasattr(current_price, 'price') else current_price
                st.metric(
                    f"{selected_symbol} Current Price",
                    f"${price_value:.2f}",
                    delta="Live"
                )
                
                # Calculate order details
                if quantity > 0:
                    if order_side == "Buy":
                        total_cost = quantity * (price_value if order_type == "Market" else limit_price)
                        st.info(f"""
                        **Buy Order Summary:**
                        - Quantity: {quantity:.3f} shares
                        - Price: ${price_value if order_type == "Market" else limit_price:.2f}
                        - Total Cost: ${total_cost:.2f}
                        """)
                    else:
                        total_proceeds = quantity * (price_value if order_type == "Market" else limit_price)
                        st.info(f"""
                        **Sell Order Summary:**
                        - Quantity: {quantity:.3f} shares
                        - Price: ${price_value if order_type == "Market" else limit_price:.2f}
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
    
    # Import and show contextual tutorial controls
    from contextual_tutorial import show_tutorial_controls
    show_tutorial_controls()
    
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
    tab1, tab2, tab3 = st.tabs([
        "📊 Analytics Dashboard", 
        "📈 Price Charts", 
        "💼 Trading"
    ])
    
    with tab1:
        # Import and display analytics dashboard
        from analytics_dashboard import create_analytics_dashboard
        create_analytics_dashboard()
    
    with tab2:
        display_price_charts(selected_symbols)
    
    with tab3:
        create_trading_panel(selected_symbols)
        
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

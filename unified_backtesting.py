"""
Unified Strategy Backtesting System
Supports backtesting for all asset classes: stocks, bonds, commodities, forex, crypto, etc.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Any, Optional

# Import our modules
from backtesting_engine import Backtester, TradingStrategies, TechnicalIndicators, BacktestResult
from multi_asset_config import multi_asset_config, AssetClass, AssetRegion, AssetSector
from multi_asset_data_provider import multi_asset_data_provider
from multi_asset_strategies import multi_asset_strategy_manager, StrategyCategory

# Page configuration
st.set_page_config(
    page_title="Unified Strategy Backtesting",
    page_icon="🤖",
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
    .strategy-card {
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
</style>
""", unsafe_allow_html=True)

def create_asset_class_selector():
    """Create asset class selector for backtesting"""
    st.sidebar.markdown("## 🌍 Asset Class Selection")
    
    asset_classes = multi_asset_config.get_supported_asset_classes()
    asset_class_names = [ac.value.replace('_', ' ').title() for ac in asset_classes]
    
    selected_name = st.sidebar.selectbox(
        "Select Asset Class",
        options=asset_class_names,
        index=0
    )
    
    selected_asset_class = AssetClass(selected_name.lower().replace(' ', '_'))
    return selected_asset_class

def create_symbol_selector(asset_class: AssetClass):
    """Create symbol selector for backtesting"""
    st.sidebar.markdown("### 📊 Symbol Selection")
    
    # Get assets for the selected class
    assets = multi_asset_config.get_assets_by_class(asset_class)
    
    if not assets:
        st.sidebar.warning("No assets available for this class")
        return None
    
    # Create symbol options
    symbol_options = [f"{asset.symbol} - {asset.name}" for asset in assets[:20]]  # Limit to 20 for performance
    
    selected_symbol = st.sidebar.selectbox(
        "Select Symbol for Backtesting",
        options=symbol_options,
        index=0
    )
    
    # Extract symbol from selected option
    symbol = selected_symbol.split(' - ')[0]
    return symbol

def create_strategy_selector(asset_class: AssetClass):
    """Create strategy selector based on asset class"""
    st.sidebar.markdown("### 🤖 Strategy Selection")
    
    # Get strategies for the selected asset class
    strategies = multi_asset_strategy_manager.get_strategies_by_asset_class(asset_class)
    
    if not strategies:
        st.sidebar.warning("No strategies available for this asset class")
        return None
    
    # Create strategy options
    strategy_options = [f"{strategy['name']} - {strategy['category'].value.replace('_', ' ').title()}" for strategy in strategies]
    
    selected_strategy = st.sidebar.selectbox(
        "Select Strategy",
        options=strategy_options,
        index=0
    )
    
    # Find the selected strategy
    for strategy in strategies:
        if f"{strategy['name']} - {strategy['category'].value.replace('_', ' ').title()}" == selected_strategy:
            return strategy
    
    return strategies[0] if strategies else None

def create_parameter_inputs(strategy: Dict[str, Any]):
    """Create parameter inputs for the selected strategy"""
    st.sidebar.markdown("### ⚙️ Strategy Parameters")
    
    parameters = {}
    
    # Common parameters for different strategies
    if "moving_average" in strategy['name'].lower() or "ma" in strategy['name'].lower():
        parameters['fast_period'] = st.sidebar.slider("Fast Period", 5, 50, 20, 1)
        parameters['slow_period'] = st.sidebar.slider("Slow Period", 20, 200, 50, 1)
    
    if "rsi" in strategy['name'].lower():
        parameters['period'] = st.sidebar.slider("RSI Period", 5, 30, 14, 1)
        parameters['oversold'] = st.sidebar.slider("Oversold Level", 10, 40, 30, 1)
        parameters['overbought'] = st.sidebar.slider("Overbought Level", 60, 90, 70, 1)
    
    if "bollinger" in strategy['name'].lower():
        parameters['period'] = st.sidebar.slider("Bollinger Period", 10, 50, 20, 1)
        parameters['std_dev'] = st.sidebar.slider("Standard Deviation", 1.0, 3.0, 2.0, 0.1)
    
    if "volatility" in strategy['name'].lower():
        parameters['volatility_period'] = st.sidebar.slider("Volatility Period", 10, 50, 20, 1)
    
    if "seasonal" in strategy['name'].lower():
        parameters['seasonal_period'] = st.sidebar.slider("Seasonal Period", 50, 365, 252, 1)
    
    if "yield" in strategy['name'].lower():
        parameters['short_term'] = st.sidebar.slider("Short Term Period", 1, 10, 2, 1)
        parameters['long_term'] = st.sidebar.slider("Long Term Period", 5, 30, 10, 1)
    
    return parameters

def create_backtest_settings():
    """Create backtest settings"""
    st.sidebar.markdown("### 📊 Backtest Settings")
    
    # Initial capital
    initial_capital = st.sidebar.number_input(
        "Initial Capital ($)",
        min_value=1000,
        max_value=1000000,
        value=10000,
        step=1000
    )
    
    # Commission
    commission = st.sidebar.slider(
        "Commission (%)",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.01
    ) / 100
    
    # Time period
    time_period = st.sidebar.selectbox(
        "Time Period",
        options=["1 Month", "3 Months", "6 Months", "1 Year", "2 Years", "5 Years"],
        index=3
    )
    
    # Timeframe
    timeframe = st.sidebar.selectbox(
        "Timeframe",
        options=["1m", "5m", "15m", "30m", "1h", "4h", "1d"],
        index=6
    )
    
    return {
        'initial_capital': initial_capital,
        'commission': commission,
        'time_period': time_period,
        'timeframe': timeframe
    }

def get_historical_data(symbol: str, time_period: str, timeframe: str) -> Optional[pd.DataFrame]:
    """Get historical data for backtesting"""
    try:
        # Map time period to days
        period_mapping = {
            "1 Month": "1mo",
            "3 Months": "3mo", 
            "6 Months": "6mo",
            "1 Year": "1y",
            "2 Years": "2y",
            "5 Years": "5y"
        }
        
        period = period_mapping.get(time_period, "1y")
        
        # Get historical data
        historical_data = multi_asset_data_provider.get_historical_data(symbol, period=period, interval=timeframe)
        
        if historical_data and not historical_data.data.empty:
            df = historical_data.data.copy()
            
            # Debug: Show original columns
            st.write(f"Debug: Original columns for {symbol}: {list(df.columns)}")
            
            # Ensure we have the required columns and convert to lowercase
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            if all(col in df.columns for col in required_columns):
                # Convert column names to lowercase for backtesting engine compatibility
                df.columns = df.columns.str.lower()
                
                # Add timestamp column
                df['timestamp'] = df.index
                
                # Debug: Show final columns
                st.write(f"Debug: Final columns for {symbol}: {list(df.columns)}")
                st.write(f"Debug: Data shape: {df.shape}")
                
                return df
            else:
                st.error(f"Missing required columns in data for {symbol}. Available columns: {list(df.columns)}")
                return None
        else:
            st.error(f"No historical data available for {symbol}")
            return None
            
    except Exception as e:
        st.error(f"Error fetching historical data for {symbol}: {e}")
        return None

def run_backtest(symbol: str, strategy: Dict[str, Any], parameters: Dict[str, Any], 
                settings: Dict[str, Any]) -> Optional[BacktestResult]:
    """Run backtest for the selected strategy"""
    try:
        # Get historical data
        df = get_historical_data(symbol, settings['time_period'], settings['timeframe'])
        
        if df is None or df.empty:
            return None
        
        # Initialize backtester
        backtester = Backtester(
            initial_capital=settings['initial_capital'],
            commission=settings['commission']
        )
        
        # Run strategy-specific backtest
        strategy_name = strategy['name']
        
        if "Moving Average" in strategy_name or "MA" in strategy_name:
            result = backtester.run_backtest(
                df, "EMA Cross", 
                fast=parameters.get('fast_period', 20),
                slow=parameters.get('slow_period', 50)
            )
        elif "RSI" in strategy_name:
            result = backtester.run_backtest(
                df, "RSI",
                period=parameters.get('period', 14),
                oversold=parameters.get('oversold', 30),
                overbought=parameters.get('overbought', 70)
            )
        elif "Bollinger" in strategy_name:
            result = backtester.run_backtest(
                df, "Bollinger Bands",
                period=parameters.get('period', 20),
                std_dev=parameters.get('std_dev', 2.0)
            )
        elif "MACD" in strategy_name:
            result = backtester.run_backtest(
                df, "MACD",
                fast=parameters.get('fast', 12),
                slow=parameters.get('slow', 26),
                signal=parameters.get('signal', 9)
            )
        else:
            # Default to RSI strategy
            result = backtester.run_backtest(
                df, "RSI",
                period=parameters.get('period', 14),
                oversold=parameters.get('oversold', 30),
                overbought=parameters.get('overbought', 70)
            )
        
        return result
        
    except Exception as e:
        st.error(f"Error running backtest: {e}")
        return None

def display_backtest_results(result: BacktestResult, symbol: str, strategy: Dict[str, Any]):
    """Display backtest results"""
    st.markdown("## 📊 Backtest Results")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Return", f"{result.total_return:.2f}%")
    
    with col2:
        st.metric("Annualized Return", f"{result.annual_return:.2f}%")
    
    with col3:
        st.metric("Max Drawdown", f"{result.max_drawdown:.2f}%")
    
    with col4:
        st.metric("Sharpe Ratio", f"{result.sharpe_ratio:.2f}")
    
    # Additional metrics
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric("Win Rate", f"{result.win_rate:.2f}%")
    
    with col6:
        st.metric("Total Trades", result.total_trades)
    
    with col7:
        st.metric("Profit Factor", f"{result.profit_factor:.2f}")
    
    with col8:
        # Show average trade duration (if available)
        if result.trades:
            avg_duration = sum(trade.get('duration', 0) for trade in result.trades) / len(result.trades)
            st.metric("Avg Trade Duration", f"{avg_duration:.1f}h")
        else:
            st.metric("Avg Trade Duration", "N/A")
    
    # Performance chart
    st.markdown("### 📈 Performance Chart")
    
    if hasattr(result, 'equity_curve') and result.equity_curve is not None:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=result.equity_curve.index,
            y=result.equity_curve.values,
            mode='lines',
            name='Portfolio Value',
            line=dict(color='blue', width=2)
        ))
        
        fig.update_layout(
            title=f"{symbol} - {strategy['name']} Performance",
            xaxis_title="Date",
            yaxis_title="Portfolio Value ($)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Trades table
    if hasattr(result, 'trades') and result.trades:
        st.markdown("### 📋 Trade History")
        
        trades_data = []
        for trade in result.trades:
            trades_data.append({
                'Entry Time': trade.get('entry_time', 'N/A'),
                'Exit Time': trade.get('exit_time', 'N/A'),
                'Entry Price': trade.get('entry_price', 0),
                'Exit Price': trade.get('exit_price', 0),
                'P&L': trade.get('pnl', 0),
                'P&L %': trade.get('pnl', 0) * 100,
                'Duration (Hours)': trade.get('duration', 0)
            })
        
        trades_df = pd.DataFrame(trades_data)
        st.dataframe(trades_df, use_container_width=True)
    
    # Strategy information
    st.markdown("### 🤖 Strategy Information")
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown(f"**Strategy Name:** {strategy['name']}")
        st.markdown(f"**Category:** {strategy['category'].value.replace('_', ' ').title()}")
        st.markdown(f"**Risk Level:** {strategy['risk_level']}/10")
        st.markdown(f"**Complexity:** {strategy['complexity']}")
    
    with col_info2:
        st.markdown(f"**Description:** {strategy['description']}")
        st.markdown(f"**Asset Classes:** {', '.join([ac.value for ac in strategy['asset_classes']])}")

def display_strategy_comparison():
    """Display strategy comparison across different asset classes"""
    st.markdown("## 🔍 Strategy Comparison")
    
    # Get all available strategies
    all_strategies = multi_asset_strategy_manager.get_all_strategies()
    
    # Create comparison table
    comparison_data = []
    for strategy_id, strategy in all_strategies.items():
        comparison_data.append({
            'Strategy': strategy['name'],
            'Asset Class': ', '.join([ac.value for ac in strategy['asset_classes']]),
            'Category': strategy['category'].value.replace('_', ' ').title(),
            'Risk Level': strategy['risk_level'],
            'Complexity': strategy['complexity']
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # Filter by asset class
    selected_asset_class = st.selectbox(
        "Filter by Asset Class",
        options=["All"] + [ac.value.replace('_', ' ').title() for ac in multi_asset_config.get_supported_asset_classes()],
        index=0
    )
    
    if selected_asset_class != "All":
        filtered_df = comparison_df[comparison_df['Asset Class'].str.contains(selected_asset_class, case=False)]
    else:
        filtered_df = comparison_df
    
    st.dataframe(filtered_df, use_container_width=True)
    
    # Strategy distribution chart
    st.markdown("### 📊 Strategy Distribution")
    
    # Count strategies by category
    category_counts = comparison_df['Category'].value_counts()
    
    fig = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        title="Strategy Distribution by Category"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def main():
    """Main unified backtesting application"""
    # Header
    st.markdown('<h1 class="main-header">🤖 Unified Strategy Backtesting</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎛️ Backtest Configuration")
        
        # Asset class selection
        selected_asset_class = create_asset_class_selector()
        
        # Symbol selection
        selected_symbol = create_symbol_selector(selected_asset_class)
        
        # Strategy selection
        selected_strategy = create_strategy_selector(selected_asset_class)
        
        # Parameter inputs
        if selected_strategy:
            parameters = create_parameter_inputs(selected_strategy)
        else:
            parameters = {}
        
        # Backtest settings
        settings = create_backtest_settings()
        
        # Run backtest button
        if st.button("🚀 Run Backtest", type="primary"):
            if selected_symbol and selected_strategy:
                with st.spinner("Running backtest..."):
                    result = run_backtest(selected_symbol, selected_strategy, parameters, settings)
                    
                    if result:
                        st.session_state.backtest_result = result
                        st.session_state.backtest_symbol = selected_symbol
                        st.session_state.backtest_strategy = selected_strategy
                        st.success("✅ Backtest completed successfully!")
                    else:
                        st.error("❌ Backtest failed")
            else:
                st.error("Please select a symbol and strategy")
    
    # Main content
    if 'backtest_result' in st.session_state:
        display_backtest_results(
            st.session_state.backtest_result,
            st.session_state.backtest_symbol,
            st.session_state.backtest_strategy
        )
    
    # Strategy comparison
    display_strategy_comparison()
    
    # Information section
    st.markdown("## ℹ️ About Unified Backtesting")
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown("""
        **Supported Asset Classes:**
        - 📈 Stocks (Apple, Microsoft, Google, etc.)
        - 🏦 Bonds (Treasury, Corporate, High-Yield)
        - 🥇 Commodities (Gold, Silver, Oil, etc.)
        - 💱 Forex (EUR/USD, GBP/USD, etc.)
        - ₿ Cryptocurrencies (Bitcoin, Ethereum, etc.)
        - 🏢 REITs (Real Estate Investment Trusts)
        - 📊 ETFs (S&P 500, NASDAQ, etc.)
        - 📈 Indices (S&P 500, Dow Jones, etc.)
        """)
    
    with col_info2:
        st.markdown("""
        **Available Strategies:**
        - 📈 Trend Following (Moving Averages, MACD)
        - 🔄 Mean Reversion (RSI, Bollinger Bands)
        - 🚀 Momentum (Breakout, Volatility)
        - ⚖️ Arbitrage (Pairs Trading, Yield Curve)
        - 🎯 Position Trading (Seasonal, Dividend)
        - 🔄 Sector Rotation (ETF Rebalancing)
        """)

if __name__ == "__main__":
    main()

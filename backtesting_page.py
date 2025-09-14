"""
Algorithmic Trading Strategies Backtesting Page
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

from backtesting_engine import Backtester, TradingStrategies, TechnicalIndicators, get_sample_data
from config import SUPPORTED_CRYPTOS

def create_strategy_chart(data: pd.DataFrame, strategy_name: str, signals: pd.DataFrame) -> go.Figure:
    """Create a chart showing the strategy signals"""
    
    # Create subplots
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=('Price & Signals', 'Volume', 'RSI'),
        row_heights=[0.6, 0.2, 0.2]
    )
    
    # Price candlesticks
    fig.add_trace(go.Candlestick(
        x=data['timestamp'],
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close'],
        name='Price',
        increasing_line_color='#00ff88',
        decreasing_line_color='#ff4444'
    ), row=1, col=1)
    
    # Add strategy-specific indicators
    if strategy_name == "MACD":
        if 'macd' in signals.columns:
            fig.add_trace(go.Scatter(
                x=data['timestamp'],
                y=signals['macd'],
                name='MACD',
                line=dict(color='blue', width=1)
            ), row=1, col=1)
            
            fig.add_trace(go.Scatter(
                x=data['timestamp'],
                y=signals['macd_signal'],
                name='Signal',
                line=dict(color='red', width=1)
            ), row=1, col=1)
    
    elif strategy_name == "EMA Cross":
        if 'ema_fast' in signals.columns:
            fig.add_trace(go.Scatter(
                x=data['timestamp'],
                y=signals['ema_fast'],
                name='EMA Fast',
                line=dict(color='orange', width=1)
            ), row=1, col=1)
            
            fig.add_trace(go.Scatter(
                x=data['timestamp'],
                y=signals['ema_slow'],
                name='EMA Slow',
                line=dict(color='purple', width=1)
            ), row=1, col=1)
    
    elif strategy_name == "Bollinger Bands":
        if 'bb_upper' in signals.columns:
            fig.add_trace(go.Scatter(
                x=data['timestamp'],
                y=signals['bb_upper'],
                name='BB Upper',
                line=dict(color='gray', width=1, dash='dash')
            ), row=1, col=1)
            
            fig.add_trace(go.Scatter(
                x=data['timestamp'],
                y=signals['bb_lower'],
                name='BB Lower',
                line=dict(color='gray', width=1, dash='dash'),
                fill='tonexty',
                fillcolor='rgba(128,128,128,0.1)'
            ), row=1, col=1)
    
    # Buy signals
    buy_signals = data[signals[f'{strategy_name.lower().replace(" ", "_")}_signal_buy'] == True]
    if not buy_signals.empty:
        fig.add_trace(go.Scatter(
            x=buy_signals['timestamp'],
            y=buy_signals['close'],
            mode='markers',
            marker=dict(symbol='triangle-up', size=10, color='green'),
            name='Buy Signal'
        ), row=1, col=1)
    
    # Sell signals
    sell_signals = data[signals[f'{strategy_name.lower().replace(" ", "_")}_signal_sell'] == True]
    if not sell_signals.empty:
        fig.add_trace(go.Scatter(
            x=sell_signals['timestamp'],
            y=sell_signals['close'],
            mode='markers',
            marker=dict(symbol='triangle-down', size=10, color='red'),
            name='Sell Signal'
        ), row=1, col=1)
    
    # Volume
    fig.add_trace(go.Bar(
        x=data['timestamp'],
        y=data['volume'],
        name='Volume',
        marker_color='rgba(158,202,225,0.6)'
    ), row=2, col=1)
    
    # RSI
    rsi = TechnicalIndicators.rsi(data['close'])
    fig.add_trace(go.Scatter(
        x=data['timestamp'],
        y=rsi,
        name='RSI',
        line=dict(color='purple', width=1)
    ), row=3, col=1)
    
    # Add RSI levels
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
    
    # Update layout
    fig.update_layout(
        title=f"{strategy_name} Strategy - {data['timestamp'].iloc[0].strftime('%Y-%m-%d')} to {data['timestamp'].iloc[-1].strftime('%Y-%m-%d')}",
        height=800,
        showlegend=True,
        template='plotly_dark',
        xaxis_rangeslider_visible=False
    )
    
    return fig

def create_performance_chart(result) -> go.Figure:
    """Create performance comparison chart"""
    
    # Equity curve
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=result.equity_curve['timestamp'],
        y=result.equity_curve['equity'],
        mode='lines',
        name='Strategy Equity',
        line=dict(color='#00ff88', width=2)
    ))
    
    # Buy and hold comparison
    initial_price = result.equity_curve['close'].iloc[0]
    final_price = result.equity_curve['close'].iloc[-1]
    buy_hold_return = (final_price / initial_price) - 1
    buy_hold_equity = 10000 * (1 + buy_hold_return)
    
    fig.add_trace(go.Scatter(
        x=result.equity_curve['timestamp'],
        y=[10000 * (1 + buy_hold_return)] * len(result.equity_curve),
        mode='lines',
        name='Buy & Hold',
        line=dict(color='#ff4444', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title='Strategy Performance vs Buy & Hold',
        xaxis_title='Date',
        yaxis_title='Portfolio Value ($)',
        template='plotly_dark',
        height=400
    )
    
    return fig

def create_trades_table(trades: list) -> pd.DataFrame:
    """Create trades summary table"""
    if not trades:
        return pd.DataFrame()
    
    df = pd.DataFrame(trades)
    df['entry_time'] = pd.to_datetime(df['entry_time'])
    df['exit_time'] = pd.to_datetime(df['exit_time'])
    df['pnl_pct'] = df['net_pnl'] * 100
    df['duration_hours'] = df['duration']
    
    return df[['entry_time', 'exit_time', 'entry_price', 'exit_price', 
               'pnl_pct', 'duration_hours']].round(4)

def main():
    st.set_page_config(
        page_title="Algorithmic Trading Backtesting",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Algorithmic Trading Strategies Backtesting")
    st.markdown("Test and compare different trading strategies with historical data")
    
    # Sidebar for strategy selection
    with st.sidebar:
        st.header("📊 Strategy Configuration")
        
        # Symbol selection
        symbol = st.selectbox(
            "Select Cryptocurrency",
            options=SUPPORTED_CRYPTOS,
            index=0
        )
        
        # Time period
        days = st.slider(
            "Backtest Period (Days)",
            min_value=30,
            max_value=365,
            value=180,
            step=30
        )
        
        # Initial capital
        initial_capital = st.number_input(
            "Initial Capital ($)",
            min_value=1000,
            max_value=100000,
            value=10000,
            step=1000
        )
        
        # Commission
        commission = st.number_input(
            "Commission (%)",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.01,
            format="%.2f"
        ) / 100
        
        st.divider()
        
        # Strategy selection
        strategy = st.selectbox(
            "Select Strategy",
            options=["MACD", "RSI", "EMA Cross", "Bollinger Bands", "Combined"],
            index=0
        )
        
        # Strategy parameters
        st.subheader("Strategy Parameters")
        
        if strategy == "MACD":
            fast = st.slider("MACD Fast Period", 5, 20, 12)
            slow = st.slider("MACD Slow Period", 20, 50, 26)
            signal = st.slider("MACD Signal Period", 5, 15, 9)
            params = {"fast": fast, "slow": slow, "signal": signal}
            
        elif strategy == "RSI":
            period = st.slider("RSI Period", 5, 30, 14)
            oversold = st.slider("Oversold Level", 10, 40, 30)
            overbought = st.slider("Overbought Level", 60, 90, 70)
            params = {"period": period, "oversold": oversold, "overbought": overbought}
            
        elif strategy == "EMA Cross":
            fast = st.slider("EMA Fast Period", 5, 20, 12)
            slow = st.slider("EMA Slow Period", 20, 50, 26)
            params = {"fast": fast, "slow": slow}
            
        elif strategy == "Bollinger Bands":
            period = st.slider("BB Period", 10, 30, 20)
            std_dev = st.slider("Standard Deviations", 1.0, 3.0, 2.0)
            params = {"period": period, "std_dev": std_dev}
            
        else:  # Combined
            params = {}
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Load data and run backtest
        with st.spinner("Loading data and running backtest..."):
            data = get_sample_data(symbol, days)
            backtester = Backtester(initial_capital, commission)
            result = backtester.run_backtest(data, strategy, **params)
        
        # Strategy chart
        st.subheader(f"📈 {strategy} Strategy Chart")
        
        # Apply strategy to get signals
        if strategy == "MACD":
            signals = TradingStrategies.macd_strategy(data, **params)
        elif strategy == "RSI":
            signals = TradingStrategies.rsi_strategy(data, **params)
        elif strategy == "EMA Cross":
            signals = TradingStrategies.ema_cross_strategy(data, **params)
        elif strategy == "Bollinger Bands":
            signals = TradingStrategies.bollinger_bands_strategy(data, **params)
        else:  # Combined
            signals = TradingStrategies.combined_strategy(data)
        
        chart = create_strategy_chart(data, strategy, signals)
        st.plotly_chart(chart, use_container_width=True)
        
        # Performance chart
        st.subheader("📊 Performance Analysis")
        perf_chart = create_performance_chart(result)
        st.plotly_chart(perf_chart, use_container_width=True)
    
    with col2:
        # Performance metrics
        st.subheader("📊 Performance Metrics")
        
        col_metric1, col_metric2 = st.columns(2)
        
        with col_metric1:
            st.metric(
                "Total Return",
                f"{result.total_return:.2%}",
                delta=f"{result.annual_return:.2%} (Annual)"
            )
            
            st.metric(
                "Sharpe Ratio",
                f"{result.sharpe_ratio:.2f}",
                delta="Higher is better"
            )
            
            st.metric(
                "Max Drawdown",
                f"{result.max_drawdown:.2%}",
                delta="Lower is better"
            )
        
        with col_metric2:
            st.metric(
                "Win Rate",
                f"{result.win_rate:.2%}",
                delta=f"{result.total_trades} trades"
            )
            
            st.metric(
                "Profit Factor",
                f"{result.profit_factor:.2f}",
                delta=">1 is profitable"
            )
            
            st.metric(
                "Total Trades",
                f"{result.total_trades}",
                delta="Strategy activity"
            )
        
        # Trade summary
        if result.trades:
            st.subheader("📋 Recent Trades")
            trades_df = create_trades_table(result.trades)
            if not trades_df.empty:
                st.dataframe(trades_df.tail(10), use_container_width=True)
        else:
            st.info("No trades executed with current parameters")
        
        # Strategy description
        st.subheader("📖 Strategy Description")
        
        descriptions = {
            "MACD": "MACD (Moving Average Convergence Divergence) uses the difference between fast and slow EMAs to generate buy/sell signals when the MACD line crosses above/below the signal line.",
            "RSI": "RSI (Relative Strength Index) identifies overbought (>70) and oversold (<30) conditions to generate mean reversion signals.",
            "EMA Cross": "EMA Crossover strategy generates signals when a fast EMA crosses above (buy) or below (sell) a slow EMA.",
            "Bollinger Bands": "Bollinger Bands use price volatility to identify overbought (upper band) and oversold (lower band) conditions.",
            "Combined": "Combined strategy uses multiple indicators and generates signals when at least 2 strategies agree."
        }
        
        st.info(descriptions.get(strategy, "Strategy description not available"))
        
        # Optimization tips
        st.subheader("💡 Optimization Tips")
        st.markdown("""
        - **Sharpe Ratio > 1**: Good risk-adjusted returns
        - **Max Drawdown < 20%**: Manageable risk
        - **Win Rate > 50%**: More winning than losing trades
        - **Profit Factor > 1.5**: Profitable strategy
        - **Total Trades > 10**: Sufficient data for analysis
        """)

if __name__ == "__main__":
    main()

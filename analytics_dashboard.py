import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time

def create_analytics_dashboard():
    """Create a modern analytics dashboard combining market overview and portfolio"""
    
    # Import contextual tutorial
    from contextual_tutorial import show_tutorial_for_tab, add_element_id, initialize_tutorial_state
    
    # Initialize tutorial state first
    initialize_tutorial_state()
    
    # Show tutorial for analytics dashboard
    tutorial_active = show_tutorial_for_tab("analytics_dashboard")
    
    # Add a prominent tutorial banner if tutorial is active
    if tutorial_active and 'tutorial' in st.session_state:
        current_step = st.session_state.tutorial.get_current_step("analytics_dashboard")
        if current_step:
            st.warning(f"🎓 **TUTORIAL ACTIVE**: {current_step['title']}")
    
    # Custom CSS for modern dashboard design
    st.markdown("""
    <style>
    .dashboard-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1rem;
    }
    
    .chart-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1rem;
    }
    
    .portfolio-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .market-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .insight-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .dashboard-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .dashboard-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2c3e50;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #7f8c8d;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .trend-up {
        color: #27ae60;
    }
    
    .trend-down {
        color: #e74c3c;
    }
    
    .trend-neutral {
        color: #f39c12;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Dashboard Header
    st.markdown(f"""
    <div id="dashboard-header" class="dashboard-container">
        <div class="dashboard-title">📊 Analytics Dashboard</div>
        <div class="dashboard-subtitle">Real-time market insights and portfolio performance</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Import necessary modules
    from unified_trading_platform import get_current_prices, multi_asset_portfolio, multi_asset_data_provider
    
    # Get market data
    with st.spinner("🔄 Loading market data..."):
        market_overview = multi_asset_data_provider.get_market_overview()
        portfolio_symbols = list(multi_asset_portfolio.positions.keys())
        portfolio_prices = get_current_prices(portfolio_symbols) if portfolio_symbols else {}
    
    # Top Row - Key Metrics
    st.markdown("### 🎯 Key Performance Indicators")
    
    # Add tutorial focus indicator for KPI cards
    if tutorial_active and 'tutorial' in st.session_state:
        current_step = st.session_state.tutorial.get_current_step("analytics_dashboard")
        if current_step and current_step.get('highlight') == 'kpi-cards':
            st.markdown("### 👆 **Tutorial Focus: Key Performance Indicators**")
            st.markdown("These 4 cards show your most important metrics!")
    
    # Add container for KPI cards
    st.markdown('<div id="kpi-cards">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate portfolio metrics
    portfolio_value = 0
    portfolio_pnl = 0
    portfolio_pnl_percent = 0
    
    if portfolio_prices:
        try:
            portfolio_metrics = multi_asset_portfolio.get_portfolio_metrics(portfolio_prices)
            portfolio_value = portfolio_metrics.total_value
            portfolio_pnl = portfolio_metrics.total_pnl
            portfolio_pnl_percent = portfolio_metrics.total_pnl_percent
        except:
            pass
    
    # Calculate market metrics
    total_assets = sum(len(data.get('top_gainers', [])) + len(data.get('top_losers', [])) for data in market_overview.values())
    overall_change = sum(data.get('average_change', 0) for data in market_overview.values()) / len(market_overview) if market_overview else 0
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Portfolio Value</div>
            <div class="metric-value">${portfolio_value:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        pnl_class = "trend-up" if portfolio_pnl >= 0 else "trend-down"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total P&L</div>
            <div class="metric-value {pnl_class}">${portfolio_pnl:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        pnl_percent_class = "trend-up" if portfolio_pnl_percent >= 0 else "trend-down"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">P&L %</div>
            <div class="metric-value {pnl_percent_class}">{portfolio_pnl_percent:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        market_class = "trend-up" if overall_change >= 0 else "trend-down"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Market Sentiment</div>
            <div class="metric-value {market_class}">{overall_change:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Close KPI cards container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Second Row - Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Portfolio Performance")
        
        # Add tutorial focus for portfolio chart
        if tutorial_active and 'tutorial' in st.session_state:
            current_step = st.session_state.tutorial.get_current_step("analytics_dashboard")
            if current_step and current_step.get('highlight') == 'portfolio-chart':
                st.markdown("### 👆 **Tutorial Focus: Portfolio Chart**")
                st.markdown("This pie chart shows your portfolio allocation!")
        
        # Add container for portfolio chart
        st.markdown('<div id="portfolio-chart">', unsafe_allow_html=True)
        
        # Create portfolio performance chart
        if portfolio_symbols and portfolio_prices:
            portfolio_data = []
            for symbol in portfolio_symbols:
                if symbol in portfolio_prices:
                    price_obj = portfolio_prices[symbol]
                    price = price_obj.price if hasattr(price_obj, 'price') else price_obj
                    change = price_obj.change_percent if hasattr(price_obj, 'change_percent') else 0
                    portfolio_data.append({
                        'Symbol': symbol,
                        'Price': price,
                        'Change': change
                    })
            
            if portfolio_data:
                df_portfolio = pd.DataFrame(portfolio_data)
                
                # Portfolio pie chart
                fig_pie = px.pie(
                    df_portfolio, 
                    values='Price', 
                    names='Symbol',
                    title="Portfolio Allocation",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_pie.update_layout(
                    height=400,
                    showlegend=True,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No portfolio positions to display")
        
        # Close portfolio chart container
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🌍 Market Overview")
        
        # Add tutorial focus for market chart
        if tutorial_active and 'tutorial' in st.session_state:
            current_step = st.session_state.tutorial.get_current_step("analytics_dashboard")
            if current_step and current_step.get('highlight') == 'market-chart':
                st.markdown("### 👆 **Tutorial Focus: Market Chart**")
                st.markdown("This bar chart shows asset class performance!")
        
        # Add container for market chart
        st.markdown('<div id="market-chart">', unsafe_allow_html=True)
        
        # Create market performance chart
        if market_overview:
            asset_classes = list(market_overview.keys())
            avg_changes = [market_overview[ac].get('average_change', 0) for ac in asset_classes]
            
            fig_bar = px.bar(
                x=asset_classes,
                y=avg_changes,
                title="Asset Class Performance",
                color=avg_changes,
                color_continuous_scale=['#e74c3c', '#f39c12', '#27ae60'],
                labels={'x': 'Asset Class', 'y': 'Average Change (%)'}
            )
            fig_bar.update_layout(
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Close market chart container
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Third Row - Detailed Analytics
    st.markdown("### 📊 Detailed Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏆 Top Performers")
        
        # Add container for top performers
        st.markdown('<div id="top-performers">', unsafe_allow_html=True)
        
        # Get top performers from all asset classes
        all_performers = []
        for asset_class, data in market_overview.items():
            if data.get('top_gainers'):
                for gainer in data['top_gainers'][:3]:
                    all_performers.append({
                        'Symbol': gainer.symbol,
                        'Asset Class': asset_class.title(),
                        'Change': gainer.change_percent,
                        'Price': gainer.price if hasattr(gainer, 'price') else 0,
                        'Status': 'Gainer'
                    })
            if data.get('top_losers'):
                for loser in data['top_losers'][:3]:
                    all_performers.append({
                        'Symbol': loser.symbol,
                        'Asset Class': asset_class.title(),
                        'Change': loser.change_percent,
                        'Price': loser.price if hasattr(loser, 'price') else 0,
                        'Status': 'Loser'
                    })
        
        if all_performers:
            df_performers = pd.DataFrame(all_performers)
            df_performers = df_performers.sort_values('Change', ascending=False)
            
            # Create performance table with custom styling
            for _, row in df_performers.head(10).iterrows():
                status_emoji = "🟢" if row['Change'] > 0 else "🔴"
                change_class = "trend-up" if row['Change'] > 0 else "trend-down"
                
                st.markdown(f"""
                <div class="metric-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{status_emoji} {row['Symbol']}</strong><br>
                            <small>{row['Asset Class']}</small>
                        </div>
                        <div style="text-align: right;">
                            <div class="metric-value {change_class}">{row['Change']:.2f}%</div>
                            <small>${row['Price']:.2f}</small>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Close top performers container
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📈 Market Heatmap")
        
        # Add container for market heatmap
        st.markdown('<div id="market-heatmap">', unsafe_allow_html=True)
        
        # Create market heatmap
        if market_overview:
            heatmap_data = []
            for asset_class, data in market_overview.items():
                if data.get('top_gainers'):
                    for gainer in data['top_gainers'][:2]:
                        heatmap_data.append({
                            'Asset Class': asset_class.title(),
                            'Symbol': gainer.symbol,
                            'Change': gainer.change_percent,
                            'Price': gainer.price if hasattr(gainer, 'price') else 0
                        })
                if data.get('top_losers'):
                    for loser in data['top_losers'][:2]:
                        heatmap_data.append({
                            'Asset Class': asset_class.title(),
                            'Symbol': loser.symbol,
                            'Change': loser.change_percent,
                            'Price': loser.price if hasattr(loser, 'price') else 0
                        })
            
            if heatmap_data:
                df_heatmap = pd.DataFrame(heatmap_data)
                
                fig_heatmap = px.treemap(
                    df_heatmap,
                    path=['Asset Class', 'Symbol'],
                    values='Price',
                    color='Change',
                    color_continuous_scale=['#e74c3c', '#f39c12', '#27ae60'],
                    title="Market Performance Heatmap"
                )
                fig_heatmap.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Close market heatmap container
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Fourth Row - Insights and Recommendations
    st.markdown("### 💡 AI Insights & Recommendations")
    
    # Add container for AI insights
    st.markdown('<div id="ai-insights">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Market Insights")
        
        insights = []
        
        if overall_change > 0:
            insights.append("🟢 **Bullish Market**: Positive sentiment across asset classes")
        else:
            insights.append("🔴 **Bearish Market**: Negative sentiment prevailing")
        
        if portfolio_pnl > 0:
            insights.append("📈 **Portfolio Growth**: Your portfolio is performing well")
        else:
            insights.append("📉 **Portfolio Decline**: Consider rebalancing your positions")
        
        # Find best performing asset class
        if market_overview:
            best_class = max(market_overview.keys(), key=lambda x: market_overview[x].get('average_change', 0))
            insights.append(f"🏆 **Best Performer**: {best_class.title()} leading the market")
        
        for insight in insights:
            st.markdown(f"""
            <div class="insight-card">
                <p style="margin: 0; color: #2c3e50;">{insight}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 💼 Trading Recommendations")
        
        recommendations = [
            "📊 **Diversify**: Spread risk across different asset classes",
            "🎯 **Focus**: Pay attention to top performers in each category",
            "⏰ **Timing**: Monitor market sentiment for entry/exit points",
            "📈 **Trends**: Follow asset class performance trends",
            "🛡️ **Risk**: Consider volatility when making decisions"
        ]
        
        for rec in recommendations:
            st.markdown(f"""
            <div class="insight-card">
                <p style="margin: 0; color: #2c3e50;">{rec}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Bottom Row - Real-time Updates
    st.markdown("### ⚡ Real-time Updates")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="portfolio-card">
            <h4 style="margin: 0 0 1rem 0;">📊 Portfolio Status</h4>
            <p style="margin: 0;">Last updated: {}</p>
        </div>
        """.format(datetime.now().strftime("%H:%M:%S")), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="market-card">
            <h4 style="margin: 0 0 1rem 0;">🌍 Market Status</h4>
            <p style="margin: 0;">Tracking {} assets</p>
        </div>
        """.format(total_assets), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="insight-card">
            <h4 style="margin: 0 0 1rem 0;">🤖 AI Status</h4>
            <p style="margin: 0;">Analysis complete</p>
        </div>
            """, unsafe_allow_html=True)
    
    # Close AI insights container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Auto-refresh button
    st.markdown('<div id="refresh-button">', unsafe_allow_html=True)
    if st.button("🔄 Refresh Dashboard", type="primary"):
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main function for analytics dashboard"""
    create_analytics_dashboard()

if __name__ == "__main__":
    main()

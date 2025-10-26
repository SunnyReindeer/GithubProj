import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time
import requests
from typing import Dict, List, Optional

def create_market_overview_page():
    """Create a comprehensive Market Overview page with Markets, Economic Events, and News"""
    
    # Page header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    ">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">📊 Market Overview</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">Real-time market data, economic events, and financial news</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Markets", 
        "📅 Economic Events", 
        "📰 News", 
        "📊 Market Analysis"
    ])
    
    with tab1:
        display_markets_section()
    
    with tab2:
        display_economic_events_section()
    
    with tab3:
        display_news_section()
    
    with tab4:
        display_market_analysis_section()

def display_markets_section():
    """Display comprehensive markets overview"""
    st.markdown("## 📈 Global Markets")
    
    # Import market data provider
    from unified_trading_platform import multi_asset_data_provider
    
    # Get market data
    with st.spinner("🔄 Loading market data..."):
        market_overview = multi_asset_data_provider.get_market_overview()
    
    if not market_overview:
        st.error("Unable to load market data. Please try again later.")
        return
    
    # Market indices overview
    st.markdown("### 🌍 Major Indices")
    
    # Create indices data
    indices_data = []
    for asset_class, data in market_overview.items():
        if data.get('average_change') is not None:
            indices_data.append({
                'Index': asset_class.title(),
                'Change': data.get('average_change', 0),
                'Status': 'Up' if data.get('average_change', 0) >= 0 else 'Down',
                'Assets': len(data.get('top_gainers', [])) + len(data.get('top_losers', []))
            })
    
    if indices_data:
        # Display indices as cards
        cols = st.columns(len(indices_data))
        for i, (col, index) in enumerate(zip(cols, indices_data)):
            with col:
                color = "#27ae60" if index['Change'] >= 0 else "#e74c3c"
                st.markdown(f"""
                <div style="
                    background: white;
                    padding: 1rem;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    border-left: 4px solid {color};
                    margin-bottom: 1rem;
                ">
                    <h4 style="margin: 0 0 0.5rem 0; color: #2c3e50;">{index['Index']}</h4>
                    <p style="margin: 0; font-size: 1.5rem; font-weight: bold; color: {color};">
                        {index['Change']:+.2f}%
                    </p>
                    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #7f8c8d;">
                        {index['Assets']} assets tracked
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    # Top performers and losers
    st.markdown("### 🏆 Top Performers & Losers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🟢 Top Gainers")
        all_gainers = []
        for asset_class, data in market_overview.items():
            if data.get('top_gainers'):
                for gainer in data['top_gainers'][:3]:
                    all_gainers.append({
                        'Symbol': gainer.symbol,
                        'Asset Class': asset_class.title(),
                        'Change': gainer.change_percent,
                        'Price': gainer.price if hasattr(gainer, 'price') else 0
                    })
        
        if all_gainers:
            df_gainers = pd.DataFrame(all_gainers)
            df_gainers = df_gainers.sort_values('Change', ascending=False).head(10)
            
            for _, row in df_gainers.iterrows():
                st.markdown(f"""
                <div style="
                    background: #d5f4e6;
                    padding: 0.8rem;
                    border-radius: 8px;
                    margin-bottom: 0.5rem;
                    border-left: 4px solid #27ae60;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{row['Symbol']}</strong><br>
                            <small style="color: #7f8c8d;">{row['Asset Class']}</small>
                        </div>
                        <div style="text-align: right;">
                            <strong style="color: #27ae60;">+{row['Change']:.2f}%</strong><br>
                            <small>${row['Price']:.2f}</small>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🔴 Top Losers")
        all_losers = []
        for asset_class, data in market_overview.items():
            if data.get('top_losers'):
                for loser in data['top_losers'][:3]:
                    all_losers.append({
                        'Symbol': loser.symbol,
                        'Asset Class': asset_class.title(),
                        'Change': loser.change_percent,
                        'Price': loser.price if hasattr(loser, 'price') else 0
                    })
        
        if all_losers:
            df_losers = pd.DataFrame(all_losers)
            df_losers = df_losers.sort_values('Change', ascending=True).head(10)
            
            for _, row in df_losers.iterrows():
                st.markdown(f"""
                <div style="
                    background: #fadbd8;
                    padding: 0.8rem;
                    border-radius: 8px;
                    margin-bottom: 0.5rem;
                    border-left: 4px solid #e74c3c;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{row['Symbol']}</strong><br>
                            <small style="color: #7f8c8d;">{row['Asset Class']}</small>
                        </div>
                        <div style="text-align: right;">
                            <strong style="color: #e74c3c;">{row['Change']:.2f}%</strong><br>
                            <small>${row['Price']:.2f}</small>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Market heatmap
    st.markdown("### 🔥 Market Heatmap")
    
    if indices_data:
        df_indices = pd.DataFrame(indices_data)
        
        fig = px.treemap(
            df_indices,
            path=['Index'],
            values='Assets',
            color='Change',
            color_continuous_scale=['#e74c3c', '#f39c12', '#27ae60'],
            title="Market Performance by Asset Class"
        )
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

def display_economic_events_section():
    """Display economic events and calendar"""
    st.markdown("## 📅 Economic Events")
    
    # Mock economic events data (in real app, this would come from an API)
    economic_events = [
        {
            "date": "2024-01-15",
            "time": "08:30 EST",
            "event": "Consumer Price Index (CPI)",
            "country": "US",
            "importance": "High",
            "forecast": "3.2%",
            "previous": "3.1%"
        },
        {
            "date": "2024-01-15",
            "time": "10:00 EST",
            "event": "Federal Reserve Chair Speech",
            "country": "US",
            "importance": "High",
            "forecast": "N/A",
            "previous": "N/A"
        },
        {
            "date": "2024-01-16",
            "time": "09:15 EST",
            "event": "Industrial Production",
            "country": "US",
            "importance": "Medium",
            "forecast": "0.3%",
            "previous": "0.2%"
        },
        {
            "date": "2024-01-16",
            "time": "14:00 EST",
            "event": "Bank of Canada Interest Rate Decision",
            "country": "Canada",
            "importance": "High",
            "forecast": "5.00%",
            "previous": "5.00%"
        },
        {
            "date": "2024-01-17",
            "time": "08:30 EST",
            "event": "Housing Starts",
            "country": "US",
            "importance": "Medium",
            "forecast": "1.45M",
            "previous": "1.42M"
        }
    ]
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        importance_filter = st.selectbox(
            "Filter by Importance",
            ["All", "High", "Medium", "Low"],
            index=0
        )
    
    with col2:
        country_filter = st.selectbox(
            "Filter by Country",
            ["All", "US", "Canada", "EU", "UK", "Japan"],
            index=0
        )
    
    with col3:
        days_ahead = st.selectbox(
            "Show Events",
            ["Today", "Next 3 Days", "Next Week", "Next Month"],
            index=1
        )
    
    # Filter events
    filtered_events = economic_events.copy()
    
    if importance_filter != "All":
        filtered_events = [e for e in filtered_events if e["importance"] == importance_filter]
    
    if country_filter != "All":
        filtered_events = [e for e in filtered_events if e["country"] == country_filter]
    
    # Display events
    st.markdown("### 📋 Upcoming Events")
    
    if filtered_events:
        for event in filtered_events:
            importance_color = {
                "High": "#e74c3c",
                "Medium": "#f39c12", 
                "Low": "#27ae60"
            }.get(event["importance"], "#7f8c8d")
            
            st.markdown(f"""
            <div style="
                background: white;
                padding: 1rem;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 1rem;
                border-left: 4px solid {importance_color};
            ">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <h4 style="margin: 0 0 0.5rem 0; color: #2c3e50;">{event['event']}</h4>
                        <p style="margin: 0; color: #7f8c8d; font-size: 0.9rem;">
                            {event['date']} at {event['time']} | {event['country']}
                        </p>
                        <div style="margin-top: 0.5rem;">
                            <span style="
                                background: {importance_color};
                                color: white;
                                padding: 0.2rem 0.5rem;
                                border-radius: 4px;
                                font-size: 0.8rem;
                                font-weight: bold;
                            ">{event['importance']} Priority</span>
                        </div>
                    </div>
                    <div style="text-align: right; min-width: 120px;">
                        <p style="margin: 0; font-size: 0.9rem; color: #7f8c8d;">Forecast</p>
                        <p style="margin: 0; font-weight: bold; color: #2c3e50;">{event['forecast']}</p>
                        <p style="margin: 0; font-size: 0.8rem; color: #7f8c8d;">Prev: {event['previous']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No events found matching your criteria.")

def display_news_section():
    """Display financial news and market updates"""
    st.markdown("## 📰 Financial News")
    
    # Mock news data (in real app, this would come from a news API)
    news_articles = [
        {
            "title": "Federal Reserve Signals Potential Rate Cuts in 2024",
            "summary": "The Federal Reserve indicated that interest rates may be reduced in the coming months as inflation shows signs of cooling.",
            "source": "Reuters",
            "time": "2 hours ago",
            "category": "Monetary Policy",
            "sentiment": "Positive"
        },
        {
            "title": "Tech Stocks Rally on Strong Q4 Earnings Reports",
            "summary": "Major technology companies reported better-than-expected earnings, driving the NASDAQ to new highs.",
            "source": "Bloomberg",
            "time": "4 hours ago",
            "category": "Earnings",
            "sentiment": "Positive"
        },
        {
            "title": "Oil Prices Surge on Middle East Tensions",
            "summary": "Crude oil prices jumped 3% following escalating tensions in the Middle East region.",
            "source": "CNBC",
            "time": "6 hours ago",
            "category": "Commodities",
            "sentiment": "Negative"
        },
        {
            "title": "Bitcoin Reaches New All-Time High Above $100,000",
            "summary": "The leading cryptocurrency broke through the $100,000 barrier for the first time in its history.",
            "source": "CoinDesk",
            "time": "8 hours ago",
            "category": "Cryptocurrency",
            "sentiment": "Positive"
        },
        {
            "title": "European Central Bank Maintains Interest Rates",
            "summary": "The ECB kept its main interest rate unchanged at 4.5%, citing concerns about economic growth.",
            "source": "Financial Times",
            "time": "12 hours ago",
            "category": "Monetary Policy",
            "sentiment": "Neutral"
        }
    ]
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All", "Monetary Policy", "Earnings", "Commodities", "Cryptocurrency", "Market Analysis"],
            index=0
        )
    
    with col2:
        sentiment_filter = st.selectbox(
            "Filter by Sentiment",
            ["All", "Positive", "Negative", "Neutral"],
            index=0
        )
    
    # Filter news
    filtered_news = news_articles.copy()
    
    if category_filter != "All":
        filtered_news = [n for n in filtered_news if n["category"] == category_filter]
    
    if sentiment_filter != "All":
        filtered_news = [n for n in filtered_news if n["sentiment"] == sentiment_filter]
    
    # Display news
    st.markdown("### 📋 Latest News")
    
    if filtered_news:
        for article in filtered_news:
            sentiment_color = {
                "Positive": "#27ae60",
                "Negative": "#e74c3c",
                "Neutral": "#f39c12"
            }.get(article["sentiment"], "#7f8c8d")
            
            st.markdown(f"""
            <div style="
                background: white;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 1rem;
                border-left: 4px solid {sentiment_color};
            ">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                    <h4 style="margin: 0; color: #2c3e50; flex: 1;">{article['title']}</h4>
                    <div style="text-align: right; margin-left: 1rem;">
                        <span style="
                            background: {sentiment_color};
                            color: white;
                            padding: 0.2rem 0.5rem;
                            border-radius: 4px;
                            font-size: 0.8rem;
                            font-weight: bold;
                        ">{article['sentiment']}</span>
                    </div>
                </div>
                <p style="margin: 0 0 1rem 0; color: #5d6d7e; line-height: 1.5;">{article['summary']}</p>
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.9rem; color: #7f8c8d;">
                    <span>{article['source']} • {article['time']}</span>
                    <span style="
                        background: #ecf0f1;
                        padding: 0.2rem 0.5rem;
                        border-radius: 4px;
                    ">{article['category']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No news articles found matching your criteria.")

def display_market_analysis_section():
    """Display market analysis and insights"""
    st.markdown("## 📊 Market Analysis")
    
    # Market sentiment indicator
    st.markdown("### 🎯 Market Sentiment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Fear & Greed Index",
            value="65",
            delta="+5",
            help="Measures market sentiment from 0 (extreme fear) to 100 (extreme greed)"
        )
    
    with col2:
        st.metric(
            label="VIX (Volatility)",
            value="18.5",
            delta="-2.1",
            help="CBOE Volatility Index - lower values indicate less market fear"
        )
    
    with col3:
        st.metric(
            label="Market Breadth",
            value="72%",
            delta="+8%",
            help="Percentage of stocks trading above their 50-day moving average"
        )
    
    # Sector performance
    st.markdown("### 🏭 Sector Performance")
    
    # Mock sector data
    sector_data = {
        'Technology': 2.5,
        'Healthcare': 1.8,
        'Financials': -0.5,
        'Energy': 3.2,
        'Consumer Discretionary': 1.2,
        'Industrials': 0.8,
        'Materials': -1.1,
        'Utilities': -0.3,
        'Real Estate': 0.5,
        'Consumer Staples': 0.2
    }
    
    df_sectors = pd.DataFrame(list(sector_data.items()), columns=['Sector', 'Change'])
    df_sectors['Color'] = df_sectors['Change'].apply(lambda x: '#27ae60' if x >= 0 else '#e74c3c')
    
    fig = px.bar(
        df_sectors,
        x='Change',
        y='Sector',
        orientation='h',
        color='Change',
        color_continuous_scale=['#e74c3c', '#f39c12', '#27ae60'],
        title="Sector Performance Today (%)"
    )
    fig.update_layout(
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Market insights
    st.markdown("### 💡 Market Insights")
    
    insights = [
        "🔍 **Technical Analysis**: The S&P 500 is approaching a key resistance level at 4,800. A breakout could signal further upside potential.",
        "📊 **Volume Analysis**: Trading volume has increased 15% compared to the 30-day average, indicating strong institutional interest.",
        "🌍 **Global Markets**: European markets are showing strength, with the DAX up 1.2% and FTSE 100 up 0.8%.",
        "💰 **Earnings Season**: 78% of companies have beaten earnings expectations this quarter, supporting the current rally.",
        "🏦 **Interest Rates**: The 10-year Treasury yield has stabilized around 4.2%, providing support for equity valuations."
    ]
    
    for insight in insights:
        st.markdown(f"""
        <div style="
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            border-left: 4px solid #3498db;
        ">
            <p style="margin: 0; color: #2c3e50;">{insight}</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main function for market overview page"""
    create_market_overview_page()

if __name__ == "__main__":
    main()

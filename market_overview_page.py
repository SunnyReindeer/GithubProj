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
    
    # Custom CSS for modern design
    st.markdown("""
    <style>
    .main-container {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        min-height: 100vh;
        padding: 0;
        margin: 0;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 0 0 30px 30px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
        text-align: center;
        color: white;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(45deg, #fff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        margin: 1rem 0 0 0;
        opacity: 0.9;
        font-weight: 300;
    }
    
    .market-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .market-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    }
    
    .news-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .news-card:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    .tab-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        margin-top: 2rem;
    }
    
    .floating-elements {
        position: absolute;
        width: 100%;
        height: 100%;
        overflow: hidden;
        pointer-events: none;
    }
    
    .floating-circle {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.1);
        animation: float 6s ease-in-out infinite;
    }
    
    .floating-circle:nth-child(1) {
        width: 80px;
        height: 80px;
        top: 20%;
        left: 10%;
        animation-delay: 0s;
    }
    
    .floating-circle:nth-child(2) {
        width: 120px;
        height: 120px;
        top: 60%;
        right: 15%;
        animation-delay: 2s;
    }
    
    .floating-circle:nth-child(3) {
        width: 60px;
        height: 60px;
        top: 40%;
        right: 30%;
        animation-delay: 4s;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }
        100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Clean start without ugly headers
    
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
    """Display comprehensive markets overview with enhanced visuals"""
    
    # Import market data provider
    from unified_trading_platform import multi_asset_data_provider
    
    # Get market data
    with st.spinner("🔄 Loading global market data..."):
        market_overview = multi_asset_data_provider.get_market_overview()
    
    if not market_overview:
        st.error("Unable to load market data. Please try again later.")
        return
    
    # 🚀 ULTRA INTERACTIVE & COOL World Map Visualization
    st.markdown("### 🌍 Global Market Indices - Interactive World Map")
    
    # Create comprehensive indices data with enhanced features including Taiwan and South America
    indices_data = [
        {"Index": "S&P 500", "Country": "United States", "Change": 0.85, "Value": 4785.32, "Status": "Up", "Region": "Americas", "lat": 39.8283, "lon": -98.5795, "color": "#27ae60", "emoji": "🇺🇸", "description": "Broad market index"},
        {"Index": "NASDAQ", "Country": "United States", "Change": 1.24, "Value": 15011.35, "Status": "Up", "Region": "Americas", "lat": 37.7749, "lon": -122.4194, "color": "#27ae60", "emoji": "🇺🇸", "description": "Tech-heavy index"},
        {"Index": "Dow Jones", "Country": "United States", "Change": 0.45, "Value": 37592.98, "Status": "Up", "Region": "Americas", "lat": 40.7128, "lon": -74.0060, "color": "#27ae60", "emoji": "🇺🇸", "description": "Blue chip stocks"},
        {"Index": "Bovespa", "Country": "Brazil", "Change": 0.67, "Value": 125678.45, "Status": "Up", "Region": "Americas", "lat": -23.5505, "lon": -46.6333, "color": "#27ae60", "emoji": "🇧🇷", "description": "São Paulo stock market"},
        {"Index": "MERVAL", "Country": "Argentina", "Change": -0.23, "Value": 456789.12, "Status": "Down", "Region": "Americas", "lat": -34.6037, "lon": -58.3816, "color": "#e74c3c", "emoji": "🇦🇷", "description": "Buenos Aires stock market"},
        {"Index": "IPSA", "Country": "Chile", "Change": 0.89, "Value": 5678.90, "Status": "Up", "Region": "Americas", "lat": -33.4489, "lon": -70.6693, "color": "#27ae60", "emoji": "🇨🇱", "description": "Santiago stock market"},
        {"Index": "Shanghai Composite", "Country": "China", "Change": -0.32, "Value": 2886.96, "Status": "Down", "Region": "Asia", "lat": 31.2304, "lon": 121.4737, "color": "#e74c3c", "emoji": "🇨🇳", "description": "Mainland China stocks"},
        {"Index": "Hang Seng", "Country": "Hong Kong", "Change": 0.78, "Value": 16388.79, "Status": "Up", "Region": "Asia", "lat": 22.3193, "lon": 114.1694, "color": "#27ae60", "emoji": "🇭🇰", "description": "Hong Kong blue chips"},
        {"Index": "Shenzhen Component", "Country": "China", "Change": -0.15, "Value": 8961.46, "Status": "Down", "Region": "Asia", "lat": 22.5431, "lon": 114.0579, "color": "#e74c3c", "emoji": "🇨🇳", "description": "Shenzhen market"},
        {"Index": "Taiwan Weighted", "Country": "Taiwan", "Change": 0.56, "Value": 17890.12, "Status": "Up", "Region": "Asia", "lat": 25.0330, "lon": 121.5654, "color": "#27ae60", "emoji": "🇹🇼", "description": "Taipei stock market"},
        {"Index": "Nikkei 225", "Country": "Japan", "Change": 1.12, "Value": 33763.18, "Status": "Up", "Region": "Asia", "lat": 35.6762, "lon": 139.6503, "color": "#27ae60", "emoji": "🇯🇵", "description": "Tokyo stock market"},
        {"Index": "KOSPI", "Country": "South Korea", "Change": 0.67, "Value": 2498.81, "Status": "Up", "Region": "Asia", "lat": 37.5665, "lon": 126.9780, "color": "#27ae60", "emoji": "🇰🇷", "description": "Seoul stock market"},
        {"Index": "FTSE 100", "Country": "United Kingdom", "Change": 0.23, "Value": 7694.19, "Status": "Up", "Region": "Europe", "lat": 51.5074, "lon": -0.1278, "color": "#27ae60", "emoji": "🇬🇧", "description": "London blue chips"},
        {"Index": "DAX", "Country": "Germany", "Change": 0.89, "Value": 16751.44, "Status": "Up", "Region": "Europe", "lat": 52.5200, "lon": 13.4050, "color": "#27ae60", "emoji": "🇩🇪", "description": "Frankfurt stock market"},
        {"Index": "CAC 40", "Country": "France", "Change": 0.56, "Value": 7428.52, "Status": "Up", "Region": "Europe", "lat": 48.8566, "lon": 2.3522, "color": "#27ae60", "emoji": "🇫🇷", "description": "Paris stock market"},
        {"Index": "ASX 200", "Country": "Australia", "Change": 0.34, "Value": 7512.67, "Status": "Up", "Region": "Oceania", "lat": -33.8688, "lon": 151.2093, "color": "#27ae60", "emoji": "🇦🇺", "description": "Sydney stock market"}
    ]
    
    # Add interactive controls
    col_filter1, col_filter2 = st.columns(2)
    
    with col_filter1:
        selected_regions = st.multiselect(
            "🌍 Filter by Region",
            ["Americas", "Asia", "Europe", "Oceania"],
            default=["Americas", "Asia", "Europe", "Oceania"]
        )
    
    with col_filter2:
        performance_filter = st.selectbox(
            "📊 Performance Filter",
            ["All", "Gaining Only", "Declining Only"]
        )
    
    # Filter data based on selections
    filtered_data = [idx for idx in indices_data if idx["Region"] in selected_regions]
    
    if performance_filter == "Gaining Only":
        filtered_data = [idx for idx in filtered_data if idx["Change"] > 0]
    elif performance_filter == "Declining Only":
        filtered_data = [idx for idx in filtered_data if idx["Change"] < 0]
    
    # Use light map style by default
    
    if filtered_data:
        df_map = pd.DataFrame(filtered_data)
        
        # Create ULTRA INTERACTIVE scatter plot on world map
        fig = px.scatter_mapbox(
            df_map,
            lat="lat",
            lon="lon",
            color="Change",
            size="Value",
            hover_name="Index",
            hover_data={
                "Country": True, 
                "Change": ":.2f", 
                "Value": ":,.0f", 
                "Region": True,
                "description": True,
                "lat": False, 
                "lon": False
            },
            color_continuous_scale=['#e74c3c', '#f39c12', '#27ae60'],
            size_max=60,
            zoom=1,
            height=600,
            title="🚀 Interactive Global Market Performance Map",
            labels={"Change": "Market Change (%)", "Value": "Index Value"}
        )
        
        # Enhanced layout with creative styling
        fig.update_layout(
            mapbox_style="carto-positron",  # Light style by default
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=20,
            title_x=0.5,
            title_font_color="#2c3e50",
            margin=dict(l=0, r=0, t=50, b=0),
            coloraxis_colorbar=dict(
                title="Market Change (%)",
                title_font_size=14,
                tickfont_size=12,
                len=0.8,
                y=0.5,
                yanchor="middle"
            )
        )
        
        # Add custom hover template
        fig.update_traces(
            hovertemplate="<b>%{hovertext}</b><br>" +
                         "Country: %{customdata[0]}<br>" +
                         "Change: %{customdata[1]:.2f}%<br>" +
                         "Value: %{customdata[2]:,.0f}<br>" +
                         "Region: %{customdata[3]}<br>" +
                         "Description: %{customdata[4]}<br>" +
                         "<extra></extra>"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add market statistics
        st.markdown("#### 📊 Market Statistics")
        
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            st.metric("Total Markets", len(filtered_data))
        
        with col_stat2:
            gaining = len([idx for idx in filtered_data if idx["Change"] > 0])
            st.metric("Gaining Markets", gaining, f"+{gaining - len(filtered_data) + gaining}")
        
        with col_stat3:
            declining = len([idx for idx in filtered_data if idx["Change"] < 0])
            st.metric("Declining Markets", declining, f"{declining - len(filtered_data) + declining}")
        
        with col_stat4:
            avg_change = sum([idx["Change"] for idx in filtered_data]) / len(filtered_data)
            st.metric("Average Change", f"{avg_change:+.2f}%")
    
    else:
        st.warning("No markets match your selected filters. Please adjust your selection.")
    
    # Layout: Market Details on left (2/3), Top Performers & Losers on right (1/3)
    col_market_details, col_top_performers = st.columns([2, 1])
    
    with col_market_details:
        st.markdown("#### 📊 Market Details")
        
        # Group by region for compact display
        regions = {}
        for index in indices_data:
            region = index['Region']
            if region not in regions:
                regions[region] = []
            regions[region].append(index)
        
        # Display indices in a more compact format
        for region, indices in regions.items():
            st.markdown(f"**{region}**")
            
            # Create columns for this region (more compact)
            cols = st.columns(len(indices))
            for i, (col, index) in enumerate(zip(cols, indices)):
                with col:
                    color = "#27ae60" if index['Change'] >= 0 else "#e74c3c"
                    icon = "📈" if index['Change'] >= 0 else "📉"
                    
                    st.markdown(f"""
                    <div class="market-card" style="
                        border-left: 3px solid {color};
                        padding: 0.8rem;
                        margin-bottom: 0.4rem;
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h6 style="margin: 0; color: #2c3e50; font-size: 0.85rem; font-weight: bold;">{index['Index']}</h6>
                                <p style="margin: 0; color: #7f8c8d; font-size: 0.7rem;">{index['Country']} {index['emoji']}</p>
                            </div>
                            <div style="text-align: right;">
                                <p style="margin: 0; font-size: 1rem; font-weight: bold; color: {color};">
                                    {index['Change']:+.2f}%
                                </p>
                                <p style="margin: 0; font-size: 0.7rem; color: #7f8c8d;">
                                    {index['Value']:,.0f}
                                </p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    with col_top_performers:
        st.markdown("#### 🏆 Top Performers & Losers")
        
        # Mock data for better demonstration
        top_gainers = [
            {"Symbol": "TSLA", "Name": "Tesla Inc", "Change": 8.45, "Price": 248.32},
            {"Symbol": "NVDA", "Name": "NVIDIA Corp", "Change": 6.78, "Price": 485.67},
            {"Symbol": "AAPL", "Name": "Apple Inc", "Change": 4.23, "Price": 192.45},
            {"Symbol": "MSFT", "Name": "Microsoft Corp", "Change": 3.89, "Price": 378.91},
            {"Symbol": "AMZN", "Name": "Amazon.com Inc", "Change": 3.45, "Price": 156.78}
        ]
        
        top_losers = [
            {"Symbol": "META", "Name": "Meta Platforms", "Change": -5.67, "Price": 345.21},
            {"Symbol": "GOOGL", "Name": "Alphabet Inc", "Change": -4.23, "Price": 142.56},
            {"Symbol": "NFLX", "Name": "Netflix Inc", "Change": -3.89, "Price": 478.32},
            {"Symbol": "ADBE", "Name": "Adobe Inc", "Change": -3.45, "Price": 567.89},
            {"Symbol": "CRM", "Name": "Salesforce Inc", "Change": -2.98, "Price": 234.56}
        ]
        
        st.markdown("**🟢 Top Gainers**")
        for gainer in top_gainers:
            st.markdown(f"""
            <div class="market-card" style="
                background: linear-gradient(135deg, #d5f4e6 0%, #a8e6cf 100%);
                border-left: 3px solid #27ae60;
                padding: 0.5rem;
                margin-bottom: 0.3rem;
                border-radius: 6px;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h6 style="margin: 0; color: #2c3e50; font-size: 0.8rem; font-weight: bold;">{gainer['Symbol']}</h6>
                        <p style="margin: 0; color: #7f8c8d; font-size: 0.65rem;">{gainer['Name']}</p>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin: 0; font-size: 0.9rem; font-weight: bold; color: #27ae60;">
                            +{gainer['Change']:.2f}%
                        </p>
                        <p style="margin: 0; font-size: 0.65rem; color: #2c3e50;">
                            ${gainer['Price']:.2f}
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("**🔴 Top Losers**")
        for loser in top_losers:
            st.markdown(f"""
            <div class="market-card" style="
                background: linear-gradient(135deg, #fadbd8 0%, #f1948a 100%);
                border-left: 3px solid #e74c3c;
                padding: 0.5rem;
                margin-bottom: 0.3rem;
                border-radius: 6px;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h6 style="margin: 0; color: #2c3e50; font-size: 0.8rem; font-weight: bold;">{loser['Symbol']}</h6>
                        <p style="margin: 0; color: #7f8c8d; font-size: 0.65rem;">{loser['Name']}</p>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin: 0; font-size: 0.9rem; font-weight: bold; color: #e74c3c;">
                            {loser['Change']:.2f}%
                        </p>
                        <p style="margin: 0; font-size: 0.65rem; color: #2c3e50;">
                            ${loser['Price']:.2f}
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Compact Global Market Heatmap with appropriate sizing
    st.markdown("### 🔥 Global Market Heatmap")
    
    # Create enhanced heatmap data
    heatmap_data = []
    for index in indices_data:
        heatmap_data.append({
            'Index': index['Index'],
            'Region': index['Region'],
            'Change': index['Change'],
            'Value': index['Value'],
            'Size': abs(index['Change']) * 100  # Size based on absolute change
        })
    
    df_heatmap = pd.DataFrame(heatmap_data)
    
    # Use centered container for heatmap
    col_heatmap1, col_heatmap2, col_heatmap3 = st.columns([1, 2, 1])
    
    with col_heatmap2:  # Center the heatmap
        # Create compact treemap
        fig = px.treemap(
            df_heatmap,
            path=['Region', 'Index'],
            values='Size',
            color='Change',
            color_continuous_scale=['#e74c3c', '#f39c12', '#27ae60'],
            title="Global Market Performance Heatmap",
            hover_data={'Change': ':.2f', 'Value': ':,.0f'}
        )
        
        fig.update_layout(
            height=300,  # Further reduced height
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=9),
            title_font_size=14,
            title_x=0.5,
            margin=dict(l=0, r=0, t=25, b=0)
        )
        
        fig.update_traces(
            textinfo="label+value",
            texttemplate="<b>%{label}</b><br>%{value:.1f}%",
            hovertemplate="<b>%{label}</b><br>Change: %{color:.2f}%<br>Value: %{customdata[1]:,.0f}<extra></extra>"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Add market summary metrics
    st.markdown("### 📊 Market Summary")
    
    # Calculate summary statistics
    total_indices = len(indices_data)
    positive_indices = len([i for i in indices_data if i['Change'] > 0])
    negative_indices = len([i for i in indices_data if i['Change'] < 0])
    avg_change = sum([i['Change'] for i in indices_data]) / len(indices_data)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0 0 0.5rem 0; font-size: 2rem;">{total_indices}</h3>
            <p style="margin: 0; opacity: 0.9;">Total Indices</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0 0 0.5rem 0; font-size: 2rem; color: #27ae60;">{positive_indices}</h3>
            <p style="margin: 0; opacity: 0.9;">Gaining</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0 0 0.5rem 0; font-size: 2rem; color: #e74c3c;">{negative_indices}</h3>
            <p style="margin: 0; opacity: 0.9;">Declining</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        color = "#27ae60" if avg_change >= 0 else "#e74c3c"
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0 0 0.5rem 0; font-size: 2rem; color: {color};">{avg_change:+.2f}%</h3>
            <p style="margin: 0; opacity: 0.9;">Avg Change</p>
        </div>
        """, unsafe_allow_html=True)

def display_economic_events_section():
    """Display economic events and calendar with enhanced visuals"""
    
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
    """Display financial news and market updates with enhanced visuals"""
    
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
    """Display market analysis and insights with enhanced visuals"""
    
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

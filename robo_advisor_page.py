"""
Robo Advisor Page - Fund-Based Portfolio Recommendations (Like Syfe)
Uses AI labeling for sectors and themes
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
from typing import Dict, List, Any

# Import our robo advisor modules
from risk_assessment_engine import risk_engine, RiskProfile, RiskTolerance, InvestmentHorizon, ExperienceLevel
from fund_portfolio_manager import fund_manager, FundPortfolio, FundHolding, AILabel, PortfolioTheme

def get_diversified_symbols(profile: RiskProfile) -> List[str]:
    """Get diversified symbols based on risk profile"""
    # Base symbols for different asset classes
    crypto_symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT"]
    stock_symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "META", "NVDA"]
    etf_symbols = ["SPY", "QQQ", "IWM", "VTI", "VEA", "VWO"]
    forex_symbols = ["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD"]
    commodity_symbols = ["GOLD", "SILVER", "OIL", "COPPER", "NATURAL_GAS"]
    bond_symbols = ["TLT", "IEF", "SHY", "LQD", "HYG"]
    
    # Select symbols based on risk tolerance
    if profile.risk_tolerance == RiskTolerance.CONSERVATIVE:
        # Conservative: More bonds, ETFs, less crypto
        symbols = (
            bond_symbols[:3] +           # 3 bonds
            etf_symbols[:3] +            # 3 ETFs
            stock_symbols[:2] +          # 2 stocks
            commodity_symbols[:1] +      # 1 commodity
            crypto_symbols[:1]           # 1 crypto
        )
    elif profile.risk_tolerance == RiskTolerance.MODERATE:
        # Moderate: Balanced mix
        symbols = (
            etf_symbols[:2] +            # 2 ETFs
            stock_symbols[:3] +          # 3 stocks
            crypto_symbols[:2] +         # 2 crypto
            commodity_symbols[:2] +      # 2 commodities
            forex_symbols[:1]            # 1 forex
        )
    elif profile.risk_tolerance == RiskTolerance.AGGRESSIVE:
        # Aggressive: More crypto, growth stocks, commodities
        symbols = (
            crypto_symbols[:3] +         # 3 crypto
            stock_symbols[:3] +          # 3 stocks
            commodity_symbols[:2] +      # 2 commodities
            forex_symbols[:1] +          # 1 forex
            etf_symbols[:1]              # 1 ETF
        )
    else:  # VERY_AGGRESSIVE
        # Very aggressive: Maximum crypto, high-risk assets
        symbols = (
            crypto_symbols[:4] +         # 4 crypto
            stock_symbols[:3] +          # 3 stocks
            commodity_symbols[:2] +      # 2 commodities
            forex_symbols[:1]            # 1 forex
        )
    
    return symbols[:10]  # Limit to 10 symbols

def create_risk_assessment_form() -> Dict[str, Any]:
    """Create the risk assessment questionnaire form"""
    st.markdown("## 🎯 Risk Assessment Questionnaire")
    st.markdown("Please answer the following questions to help us understand your risk preferences and investment goals.")
    
    questions = risk_engine.get_questions()
    answers = {}
    
    for i, question in enumerate(questions):
        st.markdown(f"**{i+1}. {question['question']}**")
        
        if question['type'] == 'single_choice':
            options = [f"{opt['text']}" for opt in question['options']]
            selected_option = st.radio(
                f"Question {i+1}",
                options,
                key=f"q_{i}",
                horizontal=False
            )
            
            # Find the selected option and get its score
            for opt in question['options']:
                if opt['text'] == selected_option:
                    answers[question['id']] = opt['score']
                    break
    
    return answers

def display_risk_profile(profile: RiskProfile):
    """Display the user's risk profile"""
    st.markdown("## 📊 Your Risk Profile")
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Risk Score",
            f"{profile.score:.0f}/100",
            delta=f"{profile.risk_tolerance.value.title()}"
        )
    
    with col2:
        st.metric(
            "Investment Horizon",
            profile.investment_horizon.value.replace('_', ' ').title()
        )
    
    with col3:
        st.metric(
            "Experience Level",
            profile.experience_level.value.title()
        )
    
    with col4:
        st.metric(
            "Max Drawdown Tolerance",
            f"{profile.max_drawdown_tolerance:.1%}"
        )
    
    # Risk tolerance visualization
    st.markdown("### 🎯 Risk Tolerance Breakdown")
    
    risk_metrics = {
        "Risk Score": profile.score,
        "Volatility Tolerance": profile.volatility_tolerance * 100,
        "Diversification Preference": profile.diversification_preference * 100,
        "Liquidity Needs": profile.liquidity_needs * 100
    }
    
    fig = go.Figure(data=go.Scatterpolar(
        r=list(risk_metrics.values()),
        theta=list(risk_metrics.keys()),
        fill='toself',
        name='Your Profile'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Risk Profile Radar Chart",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True, key="risk_profile_radar")
    
    # Risk factors
    if profile.risk_factors:
        st.markdown("### ⚠️ Risk Factors to Consider")
        for factor in profile.risk_factors:
            st.warning(f"• {factor}")
    
    # Recommended asset allocation - Fixed to stocks only
    st.markdown("### 💼 Recommended Stock Allocation")
    st.markdown("Asset allocation focused on stock market investments.")
    
    # Filter to only show stock-related allocations
    stock_categories = ['stocks', 'etfs', 'equities', 'stock']
    allocation_data = []
    for category, percentage in profile.recommended_asset_allocation.items():
        # Only include stock-related categories
        if any(stock_cat in category.lower() for stock_cat in stock_categories):
            allocation_data.append({
                'Category': category.replace('_', ' ').title(),
                'Percentage': percentage * 100
            })
    
    # If no stock categories found, show a default stock allocation
    if not allocation_data:
        # Default stock allocation based on risk tolerance
        if profile.risk_tolerance == RiskTolerance.CONSERVATIVE:
            allocation_data = [
                {'Category': 'Large Cap Stocks', 'Percentage': 40.0},
                {'Category': 'Dividend Stocks', 'Percentage': 30.0},
                {'Category': 'Blue Chip Stocks', 'Percentage': 30.0}
            ]
        elif profile.risk_tolerance == RiskTolerance.MODERATE:
            allocation_data = [
                {'Category': 'Growth Stocks', 'Percentage': 40.0},
                {'Category': 'Large Cap Stocks', 'Percentage': 35.0},
                {'Category': 'Mid Cap Stocks', 'Percentage': 25.0}
            ]
        else:  # Aggressive or Very Aggressive
            allocation_data = [
                {'Category': 'Growth Stocks', 'Percentage': 50.0},
                {'Category': 'Tech Stocks', 'Percentage': 30.0},
                {'Category': 'Small Cap Stocks', 'Percentage': 20.0}
            ]
    
    df_allocation = pd.DataFrame(allocation_data)
    
    # Create pie chart
    fig = px.pie(
        df_allocation, 
        values='Percentage', 
        names='Category',
        title="Recommended Stock Portfolio Allocation",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    st.plotly_chart(fig, use_container_width=True, key="risk_profile_stock_allocation")
    
    # Display allocation table
    st.dataframe(
        df_allocation.style.format({'Percentage': '{:.1f}%'}),
        use_container_width=True
    )

def display_fund_portfolios(portfolios: List[FundPortfolio]):
    """Display recommended fund portfolios (like Syfe)"""
    st.markdown("## 💼 Recommended Fund Portfolios")
    st.markdown("These are diversified portfolios designed to match your risk profile, similar to Syfe's approach.")
    
    if not portfolios:
        st.warning("No suitable portfolios found for your risk profile.")
        return
    
    # Portfolio overview cards
    st.markdown("### 📊 Portfolio Overview")
    
    # Create portfolio cards
    cols = st.columns(min(len(portfolios), 3))
    for i, (col, portfolio) in enumerate(zip(cols, portfolios)):
        with col:
            # Risk level color
            risk_color = "#27ae60" if portfolio.risk_level <= 4 else "#f39c12" if portfolio.risk_level <= 7 else "#e74c3c"
            
            st.markdown(f"""
            <div style="
                background: white;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                border-left: 4px solid {risk_color};
                margin-bottom: 1rem;
            ">
                <h3 style="margin: 0 0 0.5rem 0; color: #2c3e50;">{portfolio.name}</h3>
                <p style="margin: 0 0 0.5rem 0; color: #7f8c8d; font-size: 0.9rem;">{portfolio.description}</p>
                <div style="display: flex; justify-content: space-between; margin-top: 1rem;">
                    <div>
                        <p style="margin: 0; font-size: 0.8rem; color: #7f8c8d;">Expected Return</p>
                        <p style="margin: 0; font-size: 1.2rem; font-weight: bold; color: #27ae60;">{portfolio.expected_return:.1f}%</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 0.8rem; color: #7f8c8d;">Risk Level</p>
                        <p style="margin: 0; font-size: 1.2rem; font-weight: bold; color: {risk_color};">{portfolio.risk_level}/10</p>
                    </div>
                    <div>
                        <p style="margin: 0; font-size: 0.8rem; color: #7f8c8d;">Match</p>
                        <p style="margin: 0; font-size: 1.2rem; font-weight: bold; color: #3498db;">{portfolio.suitability_score:.0f}%</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Detailed portfolio view
    st.markdown("### 📋 Portfolio Details")
    
    for i, portfolio in enumerate(portfolios):
        with st.expander(f"📊 {portfolio.name} - {portfolio.suitability_score:.0f}% Match", expanded=(i == 0)):
            # Portfolio description and metrics
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {portfolio.description}")
                st.markdown(f"**Rebalancing:** {portfolio.rebalancing_frequency}")
                
                # Performance metrics
                st.markdown("**Expected Performance:**")
                col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
                with col_metrics1:
                    st.metric("Expected Return", f"{portfolio.expected_return:.1f}%")
                with col_metrics2:
                    st.metric("Volatility", f"{portfolio.expected_volatility:.1f}%")
                with col_metrics3:
                    st.metric("Risk Level", f"{portfolio.risk_level}/10")
            
            with col2:
                # Suitability score gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = portfolio.suitability_score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Match Score"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#3498db"},
                        'steps': [
                            {'range': [0, 60], 'color': "lightgray"},
                            {'range': [60, 80], 'color': "yellow"},
                            {'range': [80, 100], 'color': "green"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig.update_layout(height=200)
                st.plotly_chart(fig, use_container_width=True, key=f"portfolio_gauge_{i}")
            
            # Portfolio holdings with AI labels
            st.markdown("### 💎 Portfolio Holdings")
            st.markdown("Each holding includes AI-generated labels for sectors, themes, and characteristics.")
            
            holdings_data = []
            for holding in portfolio.holdings:
                # Format AI labels
                label_texts = [label.value for label in holding.ai_labels]
                labels_str = ", ".join(label_texts[:5])  # Show first 5 labels
                
                holdings_data.append({
                    "Symbol": holding.symbol,
                    "Name": holding.name,
                    "Type": holding.asset_class,
                    "Allocation": f"{holding.allocation:.1%}",
                    "AI Labels": labels_str,
                    "Description": holding.description
                })
            
            df_holdings = pd.DataFrame(holdings_data)
            st.dataframe(df_holdings, use_container_width=True, hide_index=True)
            
            # Allocation pie chart
            st.markdown("#### 📊 Allocation Breakdown")
            
            allocation_data = []
            for holding in portfolio.holdings:
                allocation_data.append({
                    'Holding': f"{holding.symbol} ({holding.name})",
                    'Allocation': holding.allocation * 100
                })
            
            df_allocation = pd.DataFrame(allocation_data)
            
            fig = px.pie(
                df_allocation,
                values='Allocation',
                names='Holding',
                title=f"{portfolio.name} - Asset Allocation",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True, key=f"portfolio_allocation_{i}")
            
            # AI Labels breakdown
            st.markdown("#### 🤖 AI Labels Analysis")
            
            # Count labels across all holdings
            label_counts = {}
            for holding in portfolio.holdings:
                for label in holding.ai_labels:
                    label_counts[label.value] = label_counts.get(label.value, 0) + 1
            
            if label_counts:
                labels_df = pd.DataFrame(list(label_counts.items()), columns=['Label', 'Count'])
                labels_df = labels_df.sort_values('Count', ascending=False)
                
                fig = px.bar(
                    labels_df,
                    x='Count',
                    y='Label',
                    orientation='h',
                    title="Most Common AI Labels in Portfolio",
                    color='Count',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True, key=f"portfolio_labels_{i}")

def display_portfolio_details(profile: RiskProfile, portfolio: FundPortfolio):
    """Display detailed portfolio information with AI labels"""
    st.markdown(f"## 📊 {portfolio.name} - Detailed Analysis")
    
    # Portfolio summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Expected Return", f"{portfolio.expected_return:.1f}%")
    with col2:
        st.metric("Volatility", f"{portfolio.expected_volatility:.1f}%")
    with col3:
        st.metric("Risk Level", f"{portfolio.risk_level}/10")
    with col4:
        st.metric("Match Score", f"{portfolio.suitability_score:.0f}%")
    
    # Holdings with AI labels
    st.markdown("### 💎 Holdings with AI Labels")
    
    for holding in portfolio.holdings:
        with st.expander(f"{holding.symbol} - {holding.name} ({holding.allocation:.1%})"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {holding.description}")
                st.markdown(f"**Asset Class:** {holding.asset_class}")
                st.markdown(f"**Allocation:** {holding.allocation:.1%}")
                
                # AI Labels
                st.markdown("**🤖 AI Labels:**")
                label_cols = st.columns(4)
                for i, label in enumerate(holding.ai_labels[:8]):  # Show up to 8 labels
                    with label_cols[i % 4]:
                        st.markdown(f"""
                        <div style="
                            background: #e8f4f8;
                            padding: 0.3rem 0.5rem;
                            border-radius: 5px;
                            margin: 0.2rem 0;
                            font-size: 0.8rem;
                            text-align: center;
                        ">{label.value}</div>
                        """, unsafe_allow_html=True)
            
            with col2:
                # Try to get real-time price
                try:
                    import yfinance as yf
                    ticker = yf.Ticker(holding.symbol)
                    info = ticker.info
                    current_price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
                    if current_price != 'N/A':
                        st.metric("Current Price", f"${current_price:.2f}")
                except:
                    pass
    
    # Sector breakdown by AI labels
    st.markdown("### 📈 Portfolio Composition by AI Labels")
    
    # Group by sector labels
    sector_allocations = {}
    theme_allocations = {}
    
    for holding in portfolio.holdings:
        for label in holding.ai_labels:
            label_str = label.value
            
            # Check if it's a sector
            if label_str in ["Technology", "Healthcare", "Financial Services", "Energy", 
                           "Consumer", "Industrial", "Materials", "Utilities", "Real Estate", 
                           "Communication Services"]:
                if label_str not in sector_allocations:
                    sector_allocations[label_str] = 0
                sector_allocations[label_str] += holding.allocation
            
            # Check if it's a theme
            if label_str in ["Growth Stock", "Value Stock", "Dividend Stock", "Blue Chip",
                           "Large Cap", "Small Cap", "Mid Cap", "ESG Compliant", 
                           "Income Focused", "Capital Appreciation"]:
                if label_str not in theme_allocations:
                    theme_allocations[label_str] = 0
                theme_allocations[label_str] += holding.allocation
    
    if sector_allocations:
        st.markdown("#### 🏢 Sector Allocation")
        sector_df = pd.DataFrame(list(sector_allocations.items()), columns=['Sector', 'Allocation'])
        sector_df['Allocation'] = sector_df['Allocation'] * 100
        sector_df = sector_df.sort_values('Allocation', ascending=False)
        
        fig = px.bar(
            sector_df,
            x='Allocation',
            y='Sector',
            orientation='h',
            title="Portfolio by Sector (AI Labeled)",
            color='Allocation',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True, key="portfolio_details_sector")
    
    if theme_allocations:
        st.markdown("#### 🎯 Theme Allocation")
        theme_df = pd.DataFrame(list(theme_allocations.items()), columns=['Theme', 'Allocation'])
        theme_df['Allocation'] = theme_df['Allocation'] * 100
        theme_df = theme_df.sort_values('Allocation', ascending=False)
        
        fig = px.bar(
            theme_df,
            x='Allocation',
            y='Theme',
            orientation='h',
            title="Portfolio by Investment Theme (AI Labeled)",
            color='Allocation',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True, key="portfolio_details_theme")

def display_investment_plan(profile: RiskProfile, portfolios: List[FundPortfolio]):
    """Display comprehensive investment plan based on fund portfolios"""
    st.markdown("## 📋 Your Personalized Investment Plan")
    
    if not portfolios:
        st.warning("No portfolios available for plan generation.")
        return
    
    # Use the top recommended portfolio
    recommended_portfolio = portfolios[0]
    
    # Plan overview
    st.markdown("### 🎯 Plan Overview")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Your Profile:**")
        st.markdown(f"• Risk Tolerance: {profile.risk_tolerance.value.title()}")
        st.markdown(f"• Investment Horizon: {profile.investment_horizon.value.replace('_', ' ').title()}")
        st.markdown(f"• Experience Level: {profile.experience_level.value.title()}")
        st.markdown(f"• Risk Score: {profile.score:.0f}/100")
    
    with col2:
        st.markdown("**Recommended Portfolio:**")
        st.markdown(f"• **{recommended_portfolio.name}**")
        st.markdown(f"• Expected Return: {recommended_portfolio.expected_return:.1f}%")
        st.markdown(f"• Volatility: {recommended_portfolio.expected_volatility:.1f}%")
        st.markdown(f"• Risk Level: {recommended_portfolio.risk_level}/10")
        st.markdown(f"• Match Score: {recommended_portfolio.suitability_score:.0f}%")
    
    # Portfolio allocation summary
    st.markdown("### 💼 Portfolio Allocation Summary")
    
    allocation_summary = []
    for holding in recommended_portfolio.holdings:
        allocation_summary.append({
            'Symbol': holding.symbol,
            'Name': holding.name,
            'Type': holding.asset_class,
            'Allocation': f"{holding.allocation:.1%}",
            'AI Labels': ", ".join([label.value for label in holding.ai_labels[:3]])
        })
    
    df_summary = pd.DataFrame(allocation_summary)
    st.dataframe(df_summary, use_container_width=True, hide_index=True)
    
    # Implementation plan
    st.markdown("### 🚀 Implementation Plan")
    
    st.markdown(f"""
    **Step 1: Initial Investment**
    - Start with the recommended portfolio: **{recommended_portfolio.name}**
    - Allocate funds according to the percentages shown above
    - Consider dollar-cost averaging for large investments
    
    **Step 2: Rebalancing**
    - Rebalancing Frequency: **{recommended_portfolio.rebalancing_frequency}**
    - Monitor your portfolio regularly
    - Rebalance when allocations drift more than 5% from target
    
    **Step 3: Monitoring**
    - Review performance quarterly
    - Check if your risk profile has changed
    - Adjust portfolio if your goals change
    """)
    
    # Risk management
    st.markdown("### ⚠️ Risk Management")
    
    st.markdown(f"""
    **Portfolio Risk Level:** {recommended_portfolio.risk_level}/10
    
    **Risk Factors:**
    - Expected Volatility: {recommended_portfolio.expected_volatility:.1f}%
    - Diversification: {len(recommended_portfolio.holdings)} holdings across different asset classes
    - AI Label Analysis: Portfolio includes {len(set([label.value for holding in recommended_portfolio.holdings for label in holding.ai_labels]))} different AI-labeled categories
    
    **Recommendations:**
    - Monitor your portfolio regularly
    - Stay within your risk tolerance
    - Consider adding more conservative holdings if market conditions change
    """)
    
    # AI Labels summary
    st.markdown("### 🤖 AI Labels Summary")
    
    all_labels = {}
    for holding in recommended_portfolio.holdings:
        for label in holding.ai_labels:
            all_labels[label.value] = all_labels.get(label.value, 0) + holding.allocation
    
    if all_labels:
        labels_df = pd.DataFrame(list(all_labels.items()), columns=['Label', 'Weight'])
        labels_df['Weight'] = labels_df['Weight'] * 100
        labels_df = labels_df.sort_values('Weight', ascending=False).head(10)
        
        st.markdown("**Top 10 AI Labels in Your Portfolio:**")
        st.dataframe(labels_df.style.format({'Weight': '{:.1f}%'}), use_container_width=True, hide_index=True)
    
    # Download plan
    st.markdown("### 💾 Download Your Investment Plan")
    
    plan_data = {
        "user_profile": {
            "risk_tolerance": profile.risk_tolerance.value,
            "risk_score": profile.score,
            "investment_horizon": profile.investment_horizon.value,
            "experience_level": profile.experience_level.value
        },
        "recommended_portfolio": {
            "name": recommended_portfolio.name,
            "theme": recommended_portfolio.theme.value,
            "description": recommended_portfolio.description,
            "expected_return": recommended_portfolio.expected_return,
            "expected_volatility": recommended_portfolio.expected_volatility,
            "risk_level": recommended_portfolio.risk_level,
            "suitability_score": recommended_portfolio.suitability_score,
            "rebalancing_frequency": recommended_portfolio.rebalancing_frequency
        },
        "holdings": [
            {
                "symbol": h.symbol,
                "name": h.name,
                "allocation": h.allocation,
                "asset_class": h.asset_class,
                "ai_labels": [label.value for label in h.ai_labels],
                "description": h.description
            }
            for h in recommended_portfolio.holdings
        ],
        "generated_at": datetime.now().isoformat()
    }
    
    plan_json = json.dumps(plan_data, indent=2, default=str)
    
    st.download_button(
        label="📥 Download Investment Plan (JSON)",
        data=plan_json,
        file_name=f"investment_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

def show_tutorial_hints():
    """Show tutorial hints if user is in tutorial mode"""
    if 'tutorial' in st.session_state and not st.session_state.get('tutorial_completed', False):
        tutorial = st.session_state.tutorial
        current_step = tutorial.get_current_step()
        
        if current_step and current_step.step_id == "questionnaire":
            st.info("💡 **Tutorial Hint:** Click the 'Start Risk Assessment' button below to begin the questionnaire!")
        elif current_step and current_step.step_id == "view_recommendations":
            st.info("💡 **Tutorial Hint:** Scroll down to see your personalized recommendations!")

def main():
    """Main robo advisor page"""
    st.set_page_config(
        page_title="Robo Advisor - AI Trading Assistant",
        page_icon="🤖",
        layout="wide"
    )
    
    st.markdown("# 🤖 AI Robo Advisor")
    st.markdown("Get personalized fund portfolio recommendations (like Syfe) with AI-labeled investments based on your risk profile.")
    
    # Show tutorial hints
    show_tutorial_hints()
    
    # Initialize session state
    if 'risk_profile' not in st.session_state:
        st.session_state.risk_profile = None
    if 'fund_portfolios' not in st.session_state:
        st.session_state.fund_portfolios = None
    if 'selected_portfolio' not in st.session_state:
        st.session_state.selected_portfolio = None
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Risk Assessment", 
        "💼 Fund Portfolios", 
        "📊 Portfolio Details",
        "📋 Investment Plan"
    ])
    
    with tab1:
        st.markdown("### Step 1: Complete Risk Assessment")
        
        # Risk assessment form
        answers = create_risk_assessment_form()
        
        if st.button("🔍 Analyze My Risk Profile", type="primary"):
            if len(answers) == len(risk_engine.get_questions()):
                with st.spinner("Analyzing your risk profile..."):
                    # Generate risk profile
                    profile = risk_engine.generate_risk_profile(answers)
                    st.session_state.risk_profile = profile
                    
                    # Save profile
                    filename = risk_engine.save_risk_profile(profile)
                    st.success(f"✅ Risk profile saved as {filename}")
                    
                    # Display profile
                    display_risk_profile(profile)
            else:
                st.error("Please answer all questions to proceed.")
    
    with tab2:
        st.markdown("### Step 2: Fund Portfolio Recommendations")
        st.markdown("Get recommended fund portfolios (like Syfe) that match your risk profile. Each portfolio includes AI-labeled investments.")
        
        if st.session_state.risk_profile:
            profile = st.session_state.risk_profile
            
            if st.button("💼 Get Fund Portfolio Recommendations", type="primary"):
                with st.spinner("Analyzing portfolios for your profile..."):
                    # Get fund portfolio recommendations
                    portfolios = fund_manager.recommend_portfolios(profile, max_portfolios=3)
                    st.session_state.fund_portfolios = portfolios
                    
                    if portfolios:
                        st.success(f"✅ Found {len(portfolios)} suitable portfolio(s) for your risk profile!")
                    
                    # Display recommendations
                    display_fund_portfolios(portfolios)
            elif st.session_state.fund_portfolios:
                # Show existing recommendations
                display_fund_portfolios(st.session_state.fund_portfolios)
        else:
            st.info("Please complete the risk assessment first.")
    
    with tab3:
        st.markdown("### Step 3: Portfolio Details & AI Labels")
        
        if st.session_state.risk_profile and st.session_state.fund_portfolios:
            profile = st.session_state.risk_profile
            portfolios = st.session_state.fund_portfolios
            
            # Portfolio selector
            portfolio_names = [p.name for p in portfolios]
            selected_name = st.selectbox(
                "Select Portfolio to View Details",
                portfolio_names,
                index=0
            )
            
            selected_portfolio = next(p for p in portfolios if p.name == selected_name)
            st.session_state.selected_portfolio = selected_portfolio
            
            # Display detailed portfolio
            display_portfolio_details(profile, selected_portfolio)
        else:
            st.info("Please complete the risk assessment and get portfolio recommendations first.")
    
    with tab4:
        st.markdown("### Step 4: Your Personalized Investment Plan")
        
        if st.session_state.risk_profile and st.session_state.fund_portfolios:
            profile = st.session_state.risk_profile
            portfolios = st.session_state.fund_portfolios
            
            display_investment_plan(profile, portfolios)
        else:
            st.info("Please complete all previous steps first.")
    
    # Sidebar information
    with st.sidebar:
        st.markdown("## ℹ️ About Robo Advisor")
        st.markdown("""
        Our AI-powered robo advisor (like Syfe) creates personalized fund portfolios based on your risk profile.
        
        **Features:**
        - 🎯 Risk assessment questionnaire
        - 💼 Fund portfolio recommendations
        - 🤖 AI labeling for sectors & themes
        - 📊 Detailed portfolio analysis
        - 📋 Personalized investment plans
        
        **How it works:**
        1. Complete the risk assessment
        2. Get fund portfolio recommendations
        3. View portfolio details with AI labels
        4. Download your investment plan
        
        **AI Labels:**
        Each investment is automatically labeled with:
        - Sectors (Technology, Healthcare, etc.)
        - Themes (Growth, Value, Dividend, etc.)
        - Geographic regions
        - Risk levels
        - Investment styles
        """)
        
        if st.session_state.risk_profile:
            st.markdown("## 📊 Your Current Profile")
            profile = st.session_state.risk_profile
            st.markdown(f"**Risk Tolerance:** {profile.risk_tolerance.value.title()}")
            st.markdown(f"**Risk Score:** {profile.score:.0f}/100")
            st.markdown(f"**Experience:** {profile.experience_level.value.title()}")
            
            if st.session_state.fund_portfolios:
                st.markdown("## 💼 Recommended Portfolios")
                for i, portfolio in enumerate(st.session_state.fund_portfolios[:3]):
                    st.markdown(f"**{i+1}. {portfolio.name}**")
                    st.markdown(f"   Match: {portfolio.suitability_score:.0f}% | Risk: {portfolio.risk_level}/10")

if __name__ == "__main__":
    main()

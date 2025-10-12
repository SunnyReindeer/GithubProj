"""
Robo Advisor Page for Risk Assessment and Strategy Recommendations
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
from strategy_recommender import strategy_recommender, StrategyRecommendation
from portfolio_optimizer import portfolio_optimizer, OptimizationResult, OptimizationMethod

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
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk factors
    if profile.risk_factors:
        st.markdown("### ⚠️ Risk Factors to Consider")
        for factor in profile.risk_factors:
            st.warning(f"• {factor}")
    
    # Recommended asset allocation
    st.markdown("### 💼 Recommended Asset Allocation")
    
    allocation_data = []
    for category, percentage in profile.recommended_asset_allocation.items():
        allocation_data.append({
            'Category': category.replace('_', ' ').title(),
            'Percentage': percentage * 100
        })
    
    df_allocation = pd.DataFrame(allocation_data)
    
    # Create pie chart
    fig = px.pie(
        df_allocation, 
        values='Percentage', 
        names='Category',
        title="Recommended Portfolio Allocation",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display allocation table
    st.dataframe(
        df_allocation.style.format({'Percentage': '{:.1f}%'}),
        use_container_width=True
    )

def display_strategy_recommendations(strategies: List[StrategyRecommendation]):
    """Display recommended trading strategies"""
    st.markdown("## 🤖 AI Strategy Recommendations")
    
    if not strategies:
        st.warning("No suitable strategies found for your risk profile.")
        return
    
    # Strategy overview
    st.markdown("### 📈 Recommended Strategies")
    
    for i, strategy in enumerate(strategies):
        with st.expander(f"{i+1}. {strategy.strategy_name} (Suitability: {strategy.suitability_score:.0f}%)"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {strategy.description}")
                st.markdown(f"**Category:** {strategy.category.value.replace('_', ' ').title()}")
                st.markdown(f"**Time Horizon:** {strategy.time_horizon}")
                st.markdown(f"**Complexity:** {strategy.complexity}")
                
                # Performance metrics
                st.markdown("**Expected Performance:**")
                col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
                with col_metrics1:
                    st.metric("Expected Return", f"{strategy.expected_return:.1f}%")
                with col_metrics2:
                    st.metric("Max Drawdown", f"{strategy.max_drawdown:.1f}%")
                with col_metrics3:
                    st.metric("Volatility", f"{strategy.volatility:.1%}")
            
            with col2:
                # Suitability score gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = strategy.suitability_score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Suitability Score"},
                    delta = {'reference': 80},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 80], 'color': "yellow"},
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
                st.plotly_chart(fig, use_container_width=True)
            
            # Pros and Cons
            col_pros, col_cons = st.columns(2)
            with col_pros:
                st.markdown("**✅ Pros:**")
                for pro in strategy.pros:
                    st.markdown(f"• {pro}")
            
            with col_cons:
                st.markdown("**❌ Cons:**")
                for con in strategy.cons:
                    st.markdown(f"• {con}")
            
            # Strategy parameters
            st.markdown("**⚙️ Strategy Parameters:**")
            if strategy.parameters:
                # Convert all values to strings to avoid PyArrow serialization issues
                params_data = []
                for k, v in strategy.parameters.items():
                    # Convert complex objects to strings
                    if isinstance(v, (list, dict)):
                        value_str = str(v)
                    elif isinstance(v, float):
                        value_str = f"{v:.2f}"
                    else:
                        value_str = str(v)
                    
                    params_data.append({
                        "Parameter": k.replace('_', ' ').title(),
                        "Value": value_str
                    })
                
                params_df = pd.DataFrame(params_data)
                st.dataframe(params_df, use_container_width=True)
            else:
                st.info("No specific parameters for this strategy")
            
            # Recommended symbols
            st.markdown(f"**📊 Recommended Trading Pairs:** {', '.join(strategy.symbols)}")

def display_portfolio_optimization(profile: RiskProfile, strategies: List[StrategyRecommendation]):
    """Display portfolio optimization results"""
    st.markdown("## 🎯 Portfolio Optimization")
    
    # Get diversified symbols based on risk profile
    symbols = get_diversified_symbols(profile)
    
    if not symbols:
        st.warning("No symbols available for optimization.")
        return
    
    # Show selected symbols for optimization
    st.info(f"**Selected Assets for Optimization:** {', '.join(symbols)}")
    
    # Optimization method selection
    st.markdown("### 🔧 Optimization Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        optimization_method = st.selectbox(
            "Optimization Method",
            options=[method.value for method in OptimizationMethod],
            format_func=lambda x: x.replace('_', ' ').title()
        )
    
    with col2:
        show_advanced = st.checkbox("Show Advanced Options")
    
    if show_advanced:
        st.markdown("**Advanced Settings:**")
        col_adv1, col_adv2 = st.columns(2)
        with col_adv1:
            rebalancing_threshold = st.slider("Rebalancing Threshold", 0.01, 0.20, 0.05, 0.01)
        with col_adv2:
            max_position_size = st.slider("Max Position Size", 0.1, 0.5, 0.3, 0.05)
    
    # Run optimization
    if st.button("🚀 Optimize Portfolio", type="primary"):
        with st.spinner("Optimizing portfolio..."):
            try:
                method = OptimizationMethod(optimization_method)
                result = portfolio_optimizer.optimize_portfolio(symbols, profile, method)
                
                # Display optimization results
                st.markdown("### 📊 Optimization Results")
                
                # Key metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Expected Return", f"{result.expected_return:.2%}")
                with col2:
                    st.metric("Volatility", f"{result.expected_volatility:.2%}")
                with col3:
                    st.metric("Sharpe Ratio", f"{result.sharpe_ratio:.2f}")
                with col4:
                    st.metric("Max Drawdown", f"{result.max_drawdown:.2%}")
                
                # Portfolio allocation chart
                st.markdown("### 💼 Optimized Portfolio Allocation")
                
                allocation_data = []
                for symbol, weight in result.optimal_weights.items():
                    if weight > 0.01:  # Only show weights > 1%
                        allocation_data.append({
                            'Symbol': symbol,
                            'Weight': weight * 100
                        })
                
                if allocation_data:
                    df_allocation = pd.DataFrame(allocation_data)
                    
                    # Bar chart
                    fig = px.bar(
                        df_allocation,
                        x='Symbol',
                        y='Weight',
                        title="Optimized Portfolio Weights",
                        color='Weight',
                        color_continuous_scale='Viridis'
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Allocation table
                    st.dataframe(
                        df_allocation.style.format({'Weight': '{:.1f}%'}),
                        use_container_width=True
                    )
                
                # Risk analysis
                st.markdown("### 📈 Risk Analysis")
                
                # Generate optimization report
                report = portfolio_optimizer.generate_optimization_report(result, profile)
                
                # Risk match assessment
                risk_match = report['risk_analysis']['risk_tolerance_match']
                st.info(f"**Risk Profile Match:** {risk_match}")
                
                # Diversification score
                div_score = report['risk_analysis']['diversification_score']
                st.metric("Diversification Score", f"{div_score:.1f}/100")
                
                # Concentration risk
                concentration = report['risk_analysis']['concentration_risk']
                st.warning(f"**Concentration Risk:** {concentration}")
                
                # Recommendations
                st.markdown("### 💡 Recommendations")
                for recommendation in report['recommendations']:
                    st.markdown(f"• {recommendation}")
                
                # Store results in session state
                st.session_state.optimization_result = result
                st.session_state.optimization_report = report
                
            except Exception as e:
                st.error(f"Optimization failed: {str(e)}")

def display_trading_plan(profile: RiskProfile, strategies: List[StrategyRecommendation]):
    """Display comprehensive trading plan"""
    st.markdown("## 📋 Your Personalized Trading Plan")
    
    # Generate trading plan
    trading_plan = strategy_recommender.generate_trading_plan(profile, strategies)
    
    # Plan overview
    st.markdown("### 🎯 Plan Overview")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Your Profile:**")
        st.markdown(f"• Risk Tolerance: {trading_plan['user_profile']['risk_tolerance'].title()}")
        st.markdown(f"• Investment Horizon: {trading_plan['user_profile']['investment_horizon'].replace('_', ' ').title()}")
        st.markdown(f"• Experience Level: {trading_plan['user_profile']['experience_level'].title()}")
        st.markdown(f"• Risk Score: {trading_plan['user_profile']['risk_score']:.0f}/100")
    
    with col2:
        st.markdown("**Expected Performance:**")
        perf = trading_plan['expected_performance']
        st.markdown(f"• Annual Return: {perf['annual_return']:.1f}%")
        st.markdown(f"• Volatility: {perf['volatility']:.1f}%")
        st.markdown(f"• Max Drawdown: {perf['max_drawdown']:.1f}%")
        st.markdown(f"• Sharpe Ratio: {perf['sharpe_ratio']:.2f}")
    
    # Strategy allocation
    st.markdown("### 📊 Strategy Allocation")
    
    strategy_data = []
    for strategy in trading_plan['recommended_strategies']:
        strategy_data.append({
            'Strategy': strategy['name'],
            'Allocation': f"{strategy['allocation']:.1%}",
            'Expected Return': f"{strategy['expected_return']:.1f}%",
            'Max Drawdown': f"{strategy['max_drawdown']:.1f}%",
            'Suitability': f"{strategy['suitability_score']:.0f}%"
        })
    
    df_strategies = pd.DataFrame(strategy_data)
    st.dataframe(df_strategies, use_container_width=True)
    
    # Implementation plan
    st.markdown("### 🚀 Implementation Plan")
    
    implementation = trading_plan['implementation_plan']
    for phase, description in implementation.items():
        st.markdown(f"**{phase.replace('_', ' ').title()}:** {description}")
    
    # Risk management
    st.markdown("### ⚠️ Risk Management")
    
    risk_mgmt = trading_plan['risk_management']
    st.markdown(f"**Rebalancing Frequency:** {risk_mgmt['rebalancing_frequency']}")
    
    st.markdown("**Risk Metrics:**")
    for metric, value in risk_mgmt['risk_metrics'].items():
        st.markdown(f"• {metric.replace('_', ' ').title()}: {value}")
    
    # Market analysis
    st.markdown("### 📈 Market Analysis")
    
    market_analysis = trading_plan['market_analysis']
    st.markdown(f"**Current Trend:** {market_analysis['current_trend']}")
    st.markdown(f"**Volatility Level:** {market_analysis['volatility_level']}")
    st.markdown(f"**Market Phase:** {market_analysis['market_phase']}")
    st.markdown(f"**Recommended Approach:** {market_analysis['recommended_approach']}")
    
    # Download plan
    st.markdown("### 💾 Download Your Plan")
    
    plan_json = json.dumps(trading_plan, indent=2, default=str)
    
    st.download_button(
        label="📥 Download Trading Plan (JSON)",
        data=plan_json,
        file_name=f"trading_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
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
    st.markdown("Get personalized trading strategies based on your risk profile and investment goals.")
    
    # Show tutorial hints
    show_tutorial_hints()
    
    # Initialize session state
    if 'risk_profile' not in st.session_state:
        st.session_state.risk_profile = None
    if 'strategy_recommendations' not in st.session_state:
        st.session_state.strategy_recommendations = None
    if 'trading_plan' not in st.session_state:
        st.session_state.trading_plan = None
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Risk Assessment", 
        "📊 Strategy Recommendations", 
        "🎯 Portfolio Optimization",
        "📋 Trading Plan"
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
        st.markdown("### Step 2: AI Strategy Recommendations")
        
        if st.session_state.risk_profile:
            profile = st.session_state.risk_profile
            
            if st.button("🤖 Get Strategy Recommendations", type="primary"):
                with st.spinner("Analyzing strategies for your profile..."):
                    # Get strategy recommendations
                    strategies = strategy_recommender.recommend_strategies(profile, max_strategies=5)
                    st.session_state.strategy_recommendations = strategies
                    
                    # Display recommendations
                    display_strategy_recommendations(strategies)
        else:
            st.info("Please complete the risk assessment first.")
    
    with tab3:
        st.markdown("### Step 3: Portfolio Optimization")
        
        if st.session_state.risk_profile and st.session_state.strategy_recommendations:
            profile = st.session_state.risk_profile
            strategies = st.session_state.strategy_recommendations
            
            display_portfolio_optimization(profile, strategies)
        else:
            st.info("Please complete the risk assessment and get strategy recommendations first.")
    
    with tab4:
        st.markdown("### Step 4: Your Personalized Trading Plan")
        
        if st.session_state.risk_profile and st.session_state.strategy_recommendations:
            profile = st.session_state.risk_profile
            strategies = st.session_state.strategy_recommendations
            
            display_trading_plan(profile, strategies)
        else:
            st.info("Please complete all previous steps first.")
    
    # Sidebar information
    with st.sidebar:
        st.markdown("## ℹ️ About Robo Advisor")
        st.markdown("""
        Our AI-powered robo advisor analyzes your risk preferences and recommends personalized trading strategies.
        
        **Features:**
        - 🎯 Risk assessment questionnaire
        - 🤖 AI strategy matching
        - 🎯 Portfolio optimization
        - 📋 Personalized trading plans
        
        **How it works:**
        1. Complete the risk assessment
        2. Get AI strategy recommendations
        3. Optimize your portfolio
        4. Download your trading plan
        """)
        
        if st.session_state.risk_profile:
            st.markdown("## 📊 Your Current Profile")
            profile = st.session_state.risk_profile
            st.markdown(f"**Risk Tolerance:** {profile.risk_tolerance.value.title()}")
            st.markdown(f"**Risk Score:** {profile.score:.0f}/100")
            st.markdown(f"**Experience:** {profile.experience_level.value.title()}")

if __name__ == "__main__":
    main()

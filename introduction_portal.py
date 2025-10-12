import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

def show_introduction_portal():
    """Display the introduction portal for first-time users"""
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #1f77b4; font-size: 3rem; margin-bottom: 0.5rem;">🚀</h1>
        <h1 style="color: #2c3e50; margin-bottom: 1rem;">Welcome to AI Trading Platform</h1>
        <p style="font-size: 1.2rem; color: #7f8c8d; max-width: 800px; margin: 0 auto;">
            Your intelligent gateway to modern investing across all asset classes
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content
    st.markdown("---")
    
    # What is this platform section
    st.markdown("## 🎯 What is This Platform?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **AI Trading Platform** is a comprehensive investment management system that combines:
        
        - 🤖 **AI-Powered Robo Advisor** - Get personalized investment recommendations
        - 📊 **Multi-Asset Trading** - Trade stocks, crypto, forex, commodities, and more
        - 🔬 **Strategy Backtesting** - Test trading strategies with historical data
        - 📈 **Real-Time Analytics** - Monitor your portfolio with live data
        - 🎯 **Risk Assessment** - Understand your risk tolerance and investment style
        
        **Perfect for beginners** who want to start investing with professional-grade tools and guidance.
        """)
    
    with col2:
        # Create a simple demo chart
        demo_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'Portfolio Value': [10000, 10200, 10500, 10300, 10800, 11200]
        })
        
        fig = px.line(demo_data, x='Month', y='Portfolio Value', 
                     title="Sample Portfolio Growth",
                     color_discrete_sequence=['#1f77b4'])
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Value proposition section
    st.markdown("## 💎 What Value Will You Get?")
    
    value_cols = st.columns(3)
    
    with value_cols[0]:
        st.markdown("""
        ### 🎓 **Learn While You Invest**
        - Understand different asset classes
        - Learn about risk management
        - Discover trading strategies
        - Build investment knowledge
        """)
    
    with value_cols[1]:
        st.markdown("""
        ### 🤖 **AI-Powered Guidance**
        - Personalized risk assessment
        - Customized portfolio recommendations
        - Strategy suggestions based on your profile
        - Automated optimization
        """)
    
    with value_cols[2]:
        st.markdown("""
        ### 📊 **Professional Tools**
        - Real-time market data
        - Advanced charting capabilities
        - Backtesting engine
        - Portfolio analytics
        """)
    
    # Expected outcomes section
    st.markdown("## 🎯 What Can You Expect?")
    
    st.markdown("### 📈 **For Beginners (0-6 months):**")
    beginner_outcomes = [
        "✅ Complete risk assessment and understand your investment style",
        "✅ Get personalized portfolio recommendations",
        "✅ Learn about different asset classes (stocks, crypto, forex, commodities)",
        "✅ Practice with paper trading and backtesting",
        "✅ Build confidence in investment decision-making"
    ]
    
    for outcome in beginner_outcomes:
        st.markdown(outcome)
    
    st.markdown("### 🚀 **For Intermediate Users (6-12 months):**")
    intermediate_outcomes = [
        "✅ Develop and test your own trading strategies",
        "✅ Optimize portfolio allocation based on market conditions",
        "✅ Understand advanced technical indicators",
        "✅ Implement risk management techniques",
        "✅ Track and improve your investment performance"
    ]
    
    for outcome in intermediate_outcomes:
        st.markdown(outcome)
    
    st.markdown("### 💼 **For Advanced Users (12+ months):**")
    advanced_outcomes = [
        "✅ Master multi-asset portfolio management",
        "✅ Create sophisticated trading algorithms",
        "✅ Implement advanced risk management strategies",
        "✅ Optimize for different market conditions",
        "✅ Achieve consistent investment returns"
    ]
    
    for outcome in advanced_outcomes:
        st.markdown(outcome)
    
    # Platform features overview
    st.markdown("## 🛠️ Platform Features Overview")
    
    feature_cols = st.columns(2)
    
    with feature_cols[0]:
        st.markdown("""
        ### 🌍 **Trading Platform**
        - **Multi-Asset Support**: Trade stocks, crypto, forex, commodities
        - **Real-Time Data**: Live prices and market information
        - **Advanced Charts**: TradingView integration and custom charts
        - **Portfolio Management**: Track positions and performance
        """)
        
        st.markdown("""
        ### 🤖 **AI Robo Advisor**
        - **Risk Assessment**: Comprehensive questionnaire
        - **Portfolio Optimization**: AI-powered allocation
        - **Strategy Recommendations**: Personalized suggestions
        - **Performance Tracking**: Monitor your progress
        """)
    
    with feature_cols[1]:
        st.markdown("""
        ### 🔬 **Strategy Backtesting**
        - **Historical Testing**: Test strategies on past data
        - **Multiple Strategies**: MACD, RSI, Bollinger Bands, etc.
        - **Performance Metrics**: Returns, Sharpe ratio, drawdown
        - **Risk Analysis**: Understand strategy risks
        """)
        
        st.markdown("""
        ### 📊 **Analytics & Reporting**
        - **Portfolio Analytics**: Detailed performance metrics
        - **Risk Metrics**: VaR, volatility, correlation analysis
        - **Visual Reports**: Charts and graphs for insights
        - **Export Data**: Download your data for analysis
        """)
    
    # Getting started section
    st.markdown("## 🚀 Getting Started")
    
    st.markdown("""
    ### **Step 1: Complete Your Risk Assessment** 🎯
    - Take our comprehensive questionnaire
    - Understand your risk tolerance
    - Get your personalized investment profile
    
    ### **Step 2: Explore the AI Robo Advisor** 🤖
    - Review recommended strategies
    - See suggested portfolio allocations
    - Understand the reasoning behind recommendations
    
    ### **Step 3: Practice with Backtesting** 🔬
    - Test different trading strategies
    - Learn how strategies perform historically
    - Build confidence before live trading
    
    ### **Step 4: Start Trading** 📈
    - Use the trading platform
    - Monitor your positions
    - Track your performance
    """)
    
    # Safety and disclaimer
    st.markdown("## ⚠️ Important Disclaimers")
    
    st.warning("""
    **Investment Risk Warning:**
    - All investments carry risk of loss
    - Past performance does not guarantee future results
    - This platform is for educational and informational purposes
    - Always do your own research before making investment decisions
    - Consider consulting with a financial advisor
    """)
    
    # Call to action
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 10px;">
            <h3 style="color: #2c3e50; margin-bottom: 1rem;">Ready to Start Your Investment Journey?</h3>
            <p style="color: #7f8c8d; margin-bottom: 1.5rem;">
                Click on any of the tabs above to begin exploring the platform
            </p>
            <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
                <span style="background-color: #1f77b4; color: white; padding: 0.5rem 1rem; border-radius: 5px;">🤖 AI Robo Advisor</span>
                <span style="background-color: #ff7f0e; color: white; padding: 0.5rem 1rem; border-radius: 5px;">🌍 Trading Platform</span>
                <span style="background-color: #2ca02c; color: white; padding: 0.5rem 1rem; border-radius: 5px;">🔬 Strategy Backtesting</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; padding: 1rem;">
        <p>Built with ❤️ for investors of all levels</p>
        <p>Start your journey to financial independence today!</p>
    </div>
    """, unsafe_allow_html=True)

def show_quick_start_guide():
    """Show a quick start guide for new users"""
    
    st.markdown("## 🚀 Quick Start Guide")
    
    # Create tabs for different user types
    tab1, tab2, tab3 = st.tabs(["🆕 Complete Beginner", "📚 Some Experience", "💼 Experienced"])
    
    with tab1:
        st.markdown("""
        ### **I'm New to Investing - Where Do I Start?**
        
        1. **🎯 Start with Risk Assessment**
           - Go to "AI Robo Advisor" tab
           - Complete the questionnaire honestly
           - This will help you understand your risk tolerance
        
        2. **📊 Review Your Recommendations**
           - Look at the suggested portfolio allocation
           - Read about the recommended strategies
           - Understand why these recommendations were made
        
        3. **🔬 Practice with Backtesting**
           - Go to "Strategy Backtesting" tab
           - Try different strategies on historical data
           - Learn how they perform without risking real money
        
        4. **🌍 Explore the Trading Platform**
           - Look at different asset classes
           - Understand how to read charts
           - Practice with paper trading first
        """)
    
    with tab2:
        st.markdown("""
        ### **I Have Some Investment Experience**
        
        1. **🤖 Get AI Recommendations**
           - Complete the risk assessment for personalized advice
           - Compare AI suggestions with your current approach
           - Learn about new strategies you haven't tried
        
        2. **🔬 Test New Strategies**
           - Use backtesting to validate new ideas
           - Compare different approaches
           - Optimize your existing strategies
        
        3. **📈 Diversify Your Portfolio**
           - Explore multi-asset trading
           - Add new asset classes to your portfolio
           - Use the portfolio optimizer for better allocation
        """)
    
    with tab3:
        st.markdown("""
        ### **I'm an Experienced Investor**
        
        1. **🚀 Advanced Strategy Development**
           - Use the backtesting engine for complex strategies
           - Implement multi-timeframe analysis
           - Test advanced risk management techniques
        
        2. **📊 Portfolio Optimization**
           - Use AI-powered optimization tools
           - Implement dynamic rebalancing
           - Monitor correlation and risk metrics
        
        3. **🌍 Multi-Asset Trading**
           - Trade across all asset classes
           - Implement cross-asset strategies
           - Use advanced charting and analysis tools
        """)

def main():
    """Main function for the introduction portal"""
    
    # Check if user has seen introduction before
    if 'seen_introduction' not in st.session_state:
        st.session_state.seen_introduction = False
    
    # Show introduction portal
    show_introduction_portal()
    
    # Add a button to show quick start guide
    if st.button("📖 Show Quick Start Guide", type="primary"):
        show_quick_start_guide()
    
    # Mark as seen
    st.session_state.seen_introduction = True

if __name__ == "__main__":
    main()

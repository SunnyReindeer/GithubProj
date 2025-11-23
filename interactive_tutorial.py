import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

class TutorialStep:
    def __init__(self, step_id, title, description, action_type, target_element=None, 
                 code_to_run=None, success_message=None, next_step_condition=None):
        self.step_id = step_id
        self.title = title
        self.description = description
        self.action_type = action_type  # 'click', 'navigate', 'complete', 'observe'
        self.target_element = target_element
        self.code_to_run = code_to_run
        self.success_message = success_message
        self.next_step_condition = next_step_condition

class InteractiveTutorial:
    def __init__(self):
        self.steps = self._initialize_tutorial_steps()
        self.current_step = 0
        self.completed_steps = set()
        
    def _initialize_tutorial_steps(self):
        """Initialize all tutorial steps"""
        return [
            TutorialStep(
                step_id="welcome",
                title="🎉 Welcome to AI Trading Platform!",
                description="Let's take a quick tour to learn how to use this platform effectively.",
                action_type="observe",
                success_message="Great! You're ready to start your investment journey."
            ),
            TutorialStep(
                step_id="risk_assessment",
                title="🎯 Step 1: Complete Your Risk Assessment",
                description="First, let's understand your risk tolerance. This helps us give you personalized recommendations.",
                action_type="navigate",
                target_element="AI Robo Advisor",
                success_message="Perfect! You've learned about risk assessment."
            ),
            TutorialStep(
                step_id="questionnaire",
                title="📝 Step 2: Answer the Questionnaire",
                description="Click on 'Start Risk Assessment' and answer the questions honestly. This takes about 2-3 minutes.",
                action_type="complete",
                target_element="questionnaire",
                success_message="Excellent! Your risk profile has been created."
            ),
            TutorialStep(
                step_id="view_recommendations",
                title="📊 Step 3: Review Your Recommendations",
                description="Look at your personalized portfolio allocation and strategy recommendations.",
                action_type="observe",
                success_message="Great! You can see how AI personalizes recommendations for you."
            ),
            TutorialStep(
                step_id="trading_platform",
                title="🌍 Step 4: Explore Trading Platform",
                description="Now let's see the trading platform. Click on 'Trading Platform' tab.",
                action_type="navigate",
                target_element="Trading Platform",
                success_message="Excellent! You're now in the trading platform."
            ),
            TutorialStep(
                step_id="select_assets",
                title="📈 Step 7: Select Assets to Trade",
                description="Choose an asset class (like Stocks or Crypto) and select some symbols to watch.",
                action_type="complete",
                target_element="asset_selection",
                success_message="Perfect! You've learned how to select assets."
            ),
            TutorialStep(
                step_id="view_charts",
                title="📊 Step 8: View Price Charts",
                description="Scroll down to see the price charts. Try switching between Standard and TradingView charts.",
                action_type="observe",
                success_message="Great! You've learned how to analyze price data."
            ),
            TutorialStep(
                step_id="complete",
                title="🎉 Tutorial Complete!",
                description="Congratulations! You've learned the basics of the platform. You're ready to start investing!",
                action_type="observe",
                success_message="You're all set to use the platform effectively!"
            )
        ]
    
    def get_current_step(self):
        """Get the current tutorial step"""
        if self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None
    
    def next_step(self):
        """Move to the next step"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.completed_steps.add(self.current_step - 1)
    
    def previous_step(self):
        """Move to the previous step"""
        if self.current_step > 0:
            self.current_step -= 1
    
    def complete_step(self, step_id):
        """Mark a step as completed"""
        for i, step in enumerate(self.steps):
            if step.step_id == step_id:
                self.completed_steps.add(i)
                return True
        return False
    
    def get_progress(self):
        """Get tutorial progress percentage"""
        return (len(self.completed_steps) / len(self.steps)) * 100

def show_tutorial_overlay():
    """Show tutorial overlay with current step"""
    if 'tutorial' not in st.session_state:
        st.session_state.tutorial = InteractiveTutorial()
    
    tutorial = st.session_state.tutorial
    current_step = tutorial.get_current_step()
    
    if not current_step:
        return
    
    # Create overlay
    st.markdown(f"""
    <div style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.7);
        z-index: 1000;
        display: flex;
        justify-content: center;
        align-items: center;
    ">
        <div style="
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            max-width: 600px;
            margin: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
            <h2 style="color: #1f77b4; margin-bottom: 1rem;">{current_step.title}</h2>
            <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">{current_step.description}</p>
            
            <div style="margin-bottom: 1.5rem;">
                <div style="background-color: #f0f2f6; padding: 0.5rem; border-radius: 5px;">
                    <strong>Progress:</strong> {tutorial.current_step + 1} of {len(tutorial.steps)} steps
                    <div style="background-color: #1f77b4; height: 4px; width: {tutorial.get_progress()}%; border-radius: 2px; margin-top: 0.5rem;"></div>
                </div>
            </div>
            
            <div style="display: flex; gap: 1rem; justify-content: space-between;">
                <button onclick="window.parent.postMessage('tutorial_previous', '*')" 
                        style="padding: 0.5rem 1rem; background-color: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    ← Previous
                </button>
                <button onclick="window.parent.postMessage('tutorial_next', '*')" 
                        style="padding: 0.5rem 1rem; background-color: #1f77b4; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    Next →
                </button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_tutorial_sidebar():
    """Show tutorial controls in sidebar"""
    if 'tutorial' not in st.session_state:
        st.session_state.tutorial = InteractiveTutorial()
    
    tutorial = st.session_state.tutorial
    current_step = tutorial.get_current_step()
    
    st.sidebar.markdown("## 🎓 Interactive Tutorial")
    
    if current_step:
        st.sidebar.markdown(f"**Current Step:** {current_step.title}")
        st.sidebar.markdown(f"**Progress:** {tutorial.current_step + 1}/{len(tutorial.steps)}")
        
        # Progress bar
        progress = tutorial.get_progress()
        st.sidebar.progress(progress / 100)
        
        # Step description
        st.sidebar.markdown(f"**What to do:** {current_step.description}")
        
        # Action buttons
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if st.button("← Previous", disabled=tutorial.current_step == 0):
                tutorial.previous_step()
                st.rerun()
        
        with col2:
            if st.button("Next →"):
                tutorial.next_step()
                st.rerun()
        
        # Complete step button
        if current_step.action_type == "complete":
            if st.button("✅ Mark Complete", type="primary"):
                tutorial.complete_step(current_step.step_id)
                tutorial.next_step()
                st.rerun()
        
        # Skip tutorial
        if st.sidebar.button("⏭️ Skip Tutorial"):
            st.session_state.tutorial_completed = True
            st.rerun()
    
    else:
        st.sidebar.success("🎉 Tutorial Complete!")
        if st.sidebar.button("🔄 Restart Tutorial"):
            st.session_state.tutorial = InteractiveTutorial()
            st.rerun()

def show_tutorial_hints():
    """Show contextual hints based on current step"""
    if 'tutorial' not in st.session_state:
        return
    
    tutorial = st.session_state.tutorial
    current_step = tutorial.get_current_step()
    
    if not current_step:
        return
    
    # Show hints based on current step
    if current_step.step_id == "risk_assessment":
        st.info("💡 **Hint:** Look for the '🎯 AI Robo Advisor' tab in the navigation menu above!")
    
    elif current_step.step_id == "questionnaire":
        st.info("💡 **Hint:** Click the 'Start Risk Assessment' button to begin the questionnaire!")
    
    
    elif current_step.step_id == "trading_platform":
        st.info("💡 **Hint:** Click on '🌍 Trading Platform' in the navigation menu!")
    
    elif current_step.step_id == "select_assets":
        st.info("💡 **Hint:** Use the asset class selector and symbol multiselect in the sidebar!")
    
    elif current_step.step_id == "view_charts":
        st.info("💡 **Hint:** Scroll down to see the price charts section!")

def show_tutorial_completion_celebration():
    """Show celebration when tutorial is completed"""
    st.balloons()
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 10px; margin: 2rem 0;">
        <h2 style="color: #28a745;">🎉 Congratulations!</h2>
        <p style="font-size: 1.2rem; color: #6c757d;">
            You've completed the interactive tutorial! You now know how to:
        </p>
        <ul style="text-align: left; max-width: 400px; margin: 0 auto;">
            <li>✅ Complete risk assessment</li>
            <li>✅ Get AI recommendations</li>
            <li>✅ Test trading strategies</li>
            <li>✅ Use the trading platform</li>
            <li>✅ Analyze price charts</li>
        </ul>
        <p style="margin-top: 1rem; font-weight: bold; color: #1f77b4;">
            You're ready to start your investment journey! 🚀
        </p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main tutorial function"""
    
    # Initialize tutorial state
    if 'tutorial' not in st.session_state:
        st.session_state.tutorial = InteractiveTutorial()
    
    if 'tutorial_completed' not in st.session_state:
        st.session_state.tutorial_completed = False
    
    # Show tutorial controls in sidebar
    show_tutorial_sidebar()
    
    # Show main tutorial content
    tutorial = st.session_state.tutorial
    current_step = tutorial.get_current_step()
    
    if not current_step:
        show_tutorial_completion_celebration()
        return
    
    # Show current step content
    st.markdown(f"## {current_step.title}")
    st.markdown(current_step.description)
    
    # Show contextual hints
    show_tutorial_hints()
    
    # Show step-specific content
    if current_step.step_id == "welcome":
        st.markdown("""
        ### 🎯 What You'll Learn:
        - How to assess your risk tolerance
        - How to get AI-powered investment recommendations
        - How to test trading strategies with historical data
        - How to use the trading platform
        - How to analyze price charts and make informed decisions
        
        ### ⏱️ Time Required: 5-10 minutes
        ### 🎮 Interactive: Yes, we'll guide you step by step!
        """)
        
        if st.button("🚀 Start Tutorial", type="primary"):
            tutorial.next_step()
            st.rerun()
    
    elif current_step.step_id == "risk_assessment":
        st.markdown("""
        ### 🎯 Why Risk Assessment Matters:
        - **Personalized Recommendations**: AI gives you strategies that match your risk tolerance
        - **Better Decision Making**: Understanding your risk profile helps you make informed choices
        - **Portfolio Optimization**: Your portfolio allocation is tailored to your preferences
        - **Confidence Building**: You'll feel more confident about your investment decisions
        
        ### 📊 What You'll Get:
        - Your risk tolerance score (0-100)
        - Recommended portfolio allocation
        - Suitable trading strategies
        - Personalized investment advice
        """)
    
    elif current_step.step_id == "questionnaire":
        st.markdown("""
        ### 📝 The Questionnaire Covers:
        - **Investment Goals**: What you want to achieve
        - **Time Horizon**: How long you plan to invest
        - **Risk Tolerance**: How much risk you can handle
        - **Experience Level**: Your trading experience
        - **Portfolio Size**: How much you're investing
        
        ### ⚡ Quick Tips:
        - Answer honestly for best results
        - Take your time with each question
        - There are no wrong answers
        - You can always retake it later
        """)
    
    elif current_step.step_id == "trading_platform":
        st.markdown("""
        ### 🌍 Multi-Asset Trading Platform:
        - **Stocks**: Apple, Microsoft, Google, Tesla, etc.
        - **Cryptocurrencies**: Bitcoin, Ethereum, Binance Coin, etc.
        - **Forex**: EUR/USD, GBP/USD, USD/JPY, etc.
        - **Commodities**: Gold, Silver, Oil, Copper, etc.
        - **ETFs**: SPY, QQQ, VTI, etc.
        
        ### 🎯 What You Can Do:
        - View real-time prices
        - Analyze price charts
        - Track portfolio performance
        - Execute trades (simulated)
        - Monitor market data
        """)
    
    elif current_step.step_id == "select_assets":
        st.markdown("""
        ### 📈 Asset Selection Guide:
        
        **For Beginners:**
        - Start with large-cap stocks (AAPL, MSFT, GOOGL)
        - Try major cryptocurrencies (BTC, ETH)
        - Consider ETFs for diversification
        
        **For Intermediate:**
        - Explore forex pairs (EUR/USD, GBP/USD)
        - Try commodities (GOLD, SILVER)
        - Mix different asset classes
        
        **For Advanced:**
        - All asset classes
        - Exotic pairs and commodities
        - Complex multi-asset strategies
        """)
    
    elif current_step.step_id == "view_charts":
        st.markdown("""
        ### 📊 Chart Types Available:
        
        **Standard Charts:**
        - Candlestick charts
        - Multiple timeframes (1mo, 3mo, 1y, 5y)
        - Volume indicators
        - Technical overlays
        
        **TradingView Widgets:**
        - Professional-grade charts
        - Advanced technical indicators
        - Drawing tools
        - Real-time data
        """)
    
    elif current_step.step_id == "complete":
        show_tutorial_completion_celebration()

if __name__ == "__main__":
    main()

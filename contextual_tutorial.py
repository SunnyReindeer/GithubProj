import streamlit as st
import time
from typing import Dict, List, Optional

class ContextualTutorial:
    def __init__(self):
        self.tutorial_steps = self._initialize_tutorial_steps()
        self.current_step = 0
        self.current_tab = None
        self.completed_steps = set()
        
    def _initialize_tutorial_steps(self):
        """Initialize tutorial steps for each tab"""
        return {
            "analytics_dashboard": [
                {
                    "id": "dashboard_overview",
                    "title": "📊 Welcome to Analytics Dashboard",
                    "description": "This is your comprehensive analytics dashboard. Let's explore the key features!",
                    "highlight": "dashboard-header",
                    "action": "observe"
                },
                {
                    "id": "kpi_metrics",
                    "title": "🎯 Key Performance Indicators",
                    "description": "These 4 cards show your most important metrics: Portfolio Value, P&L, P&L%, and Market Sentiment.",
                    "highlight": "kpi-cards",
                    "action": "observe"
                },
                {
                    "id": "portfolio_chart",
                    "title": "📈 Portfolio Performance Chart",
                    "description": "This pie chart shows how your portfolio is allocated across different assets.",
                    "highlight": "portfolio-chart",
                    "action": "observe"
                },
                {
                    "id": "market_chart",
                    "title": "🌍 Market Overview Chart",
                    "description": "This bar chart shows the performance of different asset classes in the market.",
                    "highlight": "market-chart",
                    "action": "observe"
                },
                {
                    "id": "top_performers",
                    "title": "🏆 Top Performers",
                    "description": "Here you can see the best and worst performing assets across all markets.",
                    "highlight": "top-performers",
                    "action": "observe"
                },
                {
                    "id": "market_heatmap",
                    "title": "🔥 Market Heatmap",
                    "description": "This treemap gives you a visual overview of market performance by asset class and symbol.",
                    "highlight": "market-heatmap",
                    "action": "observe"
                },
                {
                    "id": "ai_insights",
                    "title": "💡 AI Insights & Recommendations",
                    "description": "Get AI-powered market insights and trading recommendations based on current conditions.",
                    "highlight": "ai-insights",
                    "action": "observe"
                },
                {
                    "id": "refresh_button",
                    "title": "🔄 Refresh Dashboard",
                    "description": "Click this button to refresh all data and get the latest market information.",
                    "highlight": "refresh-button",
                    "action": "click"
                }
            ],
            "price_charts": [
                {
                    "id": "charts_overview",
                    "title": "📈 Price Charts Section",
                    "description": "Here you can analyze price movements and technical indicators for your selected assets.",
                    "highlight": "charts-header",
                    "action": "observe"
                },
                {
                    "id": "chart_type_selector",
                    "title": "📊 Chart Type Selection",
                    "description": "Choose between Standard charts (candlesticks) or TradingView widgets (professional charts).",
                    "highlight": "chart-type-selector",
                    "action": "observe"
                },
                {
                    "id": "timeframe_selector",
                    "title": "⏰ Timeframe Selection",
                    "description": "Select the time period for your charts - from 1 month to 5 years of data.",
                    "highlight": "timeframe-selector",
                    "action": "observe"
                },
                {
                    "id": "chart_display",
                    "title": "📊 Chart Display",
                    "description": "This is where your selected charts will appear. You can analyze price movements and patterns here.",
                    "highlight": "chart-display",
                    "action": "observe"
                }
            ],
            "trading": [
                {
                    "id": "trading_overview",
                    "title": "💼 Trading Panel",
                    "description": "This is where you can place buy and sell orders for your selected assets.",
                    "highlight": "trading-header",
                    "action": "observe"
                },
                {
                    "id": "symbol_selector",
                    "title": "🎯 Symbol Selection",
                    "description": "Choose which asset you want to trade from your selected symbols.",
                    "highlight": "symbol-selector",
                    "action": "observe"
                },
                {
                    "id": "order_type",
                    "title": "📋 Order Type",
                    "description": "Select Market Order (immediate execution) or Limit Order (set your own price).",
                    "highlight": "order-type",
                    "action": "observe"
                },
                {
                    "id": "order_side",
                    "title": "📈 Order Side",
                    "description": "Choose Buy (purchase) or Sell (sell your holdings) for this asset.",
                    "highlight": "order-side",
                    "action": "observe"
                },
                {
                    "id": "quantity_input",
                    "title": "🔢 Quantity Input",
                    "description": "Enter how many shares/units you want to buy or sell.",
                    "highlight": "quantity-input",
                    "action": "observe"
                },
                {
                    "id": "current_price",
                    "title": "💰 Current Price Display",
                    "description": "This shows the current market price for your selected asset.",
                    "highlight": "current-price",
                    "action": "observe"
                },
                {
                    "id": "place_order_button",
                    "title": "🚀 Place Order Button",
                    "description": "Click this button to execute your trade order.",
                    "highlight": "place-order-button",
                    "action": "click"
                },
                {
                    "id": "positions_table",
                    "title": "📊 Your Positions",
                    "description": "This table shows all your current holdings and their performance.",
                    "highlight": "positions-table",
                    "action": "observe"
                },
                {
                    "id": "trades_table",
                    "title": "📝 Trade History",
                    "description": "This table shows your recent trading activity and order history.",
                    "highlight": "trades-table",
                    "action": "observe"
                }
            ]
        }
    
    def get_current_step(self, tab_name: str):
        """Get current tutorial step for a specific tab"""
        if tab_name not in self.tutorial_steps:
            return None
        
        steps = self.tutorial_steps[tab_name]
        if self.current_step < len(steps):
            return steps[self.current_step]
        return None
    
    def next_step(self):
        """Move to next step"""
        if self.current_tab and self.current_tab in self.tutorial_steps:
            steps = self.tutorial_steps[self.current_tab]
            if self.current_step < len(steps) - 1:
                self.current_step += 1
                self.completed_steps.add(self.current_step - 1)
                return True
        return False
    
    def previous_step(self):
        """Move to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            return True
        return False
    
    def set_tab(self, tab_name: str):
        """Set current tab and reset step if needed"""
        if self.current_tab != tab_name:
            self.current_tab = tab_name
            self.current_step = 0
    
    def complete_tutorial(self):
        """Mark tutorial as completed"""
        st.session_state.tutorial_completed = True

def show_tutorial_info_box(step_info: Dict, tab_name: str):
    """Show tutorial info box using Streamlit's native components"""
    if not step_info:
        return
    
    # Create a prominent info box with gradient background
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    ">
        <h3 style="margin: 0 0 1rem 0; color: white; text-align: center;">{step_info['title']}</h3>
        <p style="margin: 0 0 1rem 0; font-size: 1.1rem; line-height: 1.5; text-align: center;">{step_info['description']}</p>
        
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="background-color: rgba(255, 255, 255, 0.2); padding: 0.5rem; border-radius: 10px; display: inline-block;">
                <strong>Step {st.session_state.tutorial.current_step + 1} of {len(st.session_state.tutorial.tutorial_steps[tab_name])}</strong>
            </div>
        </div>
        
        <div style="text-align: center;">
            <span style="font-size: 2rem; animation: pulse 2s infinite;">👆</span>
            <p style="margin: 0.5rem 0 0 0; font-weight: bold;">Look for the highlighted element below!</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Previous", disabled=st.session_state.tutorial.current_step == 0, key=f"prev_{tab_name}_{st.session_state.tutorial.current_step}"):
            st.session_state.tutorial.previous_step()
            st.rerun()
    
    with col2:
        if st.button("Next →", key=f"next_{tab_name}_{st.session_state.tutorial.current_step}"):
            if st.session_state.tutorial.next_step():
                st.rerun()
            else:
                st.success("🎉 Tutorial completed for this tab!")
    
    with col3:
        if step_info['action'] == "click":
            if st.button("✅ Mark Complete", type="primary", key=f"complete_{tab_name}_{st.session_state.tutorial.current_step}"):
                st.session_state.tutorial.next_step()
                st.rerun()
    
    st.markdown("---")

def highlight_element(element_id: str):
    """Add highlighting effect to specific element using Streamlit-compatible approach"""
    # Use Streamlit's native success box for highlighting
    st.success(f"🎯 **Tutorial Focus**: Look for the element with ID '{element_id}' below!")
    
    # Add simple CSS highlighting that works better in Streamlit
    st.markdown(f"""
    <style>
    #{element_id} {{
        border: 3px solid #ff6b6b !important;
        border-radius: 10px !important;
        background-color: rgba(255, 107, 107, 0.1) !important;
        padding: 10px !important;
        margin: 5px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

def show_tutorial_controls():
    """Show tutorial controls in sidebar"""
    if 'tutorial' not in st.session_state:
        st.session_state.tutorial = ContextualTutorial()
    
    tutorial = st.session_state.tutorial
    
    st.sidebar.markdown("## 🎓 Interactive Tutorial")
    
    # Tutorial status
    if tutorial.current_tab and tutorial.current_tab in tutorial.tutorial_steps:
        current_step = tutorial.get_current_step(tutorial.current_tab)
        if current_step:
            st.sidebar.markdown(f"**Current:** {current_step['title']}")
            st.sidebar.markdown(f"**Tab:** {tutorial.current_tab.replace('_', ' ').title()}")
            
            # Progress bar
            total_steps = len(tutorial.tutorial_steps[tutorial.current_tab])
            progress = (tutorial.current_step + 1) / total_steps
            st.sidebar.progress(progress)
            
            # Step description
            st.sidebar.markdown(f"**What to do:** {current_step['description']}")
            
            # Action buttons
            col1, col2 = st.sidebar.columns(2)
            
            with col1:
                if st.button("← Previous", disabled=tutorial.current_step == 0):
                    tutorial.previous_step()
                    st.rerun()
            
            with col2:
                if st.button("Next →"):
                    if tutorial.next_step():
                        st.rerun()
                    else:
                        st.sidebar.success("🎉 Tutorial completed for this tab!")
            
            # Complete step button
            if current_step['action'] == "click":
                if st.button("✅ Mark Complete", type="primary"):
                    tutorial.next_step()
                    st.rerun()
    else:
        st.sidebar.info("🎓 Select a tab below to start the tutorial!")
    
    # Tutorial controls
    st.sidebar.markdown("### 🎮 Tutorial Controls")
    
    if st.sidebar.button("🔄 Restart Tutorial"):
        st.session_state.tutorial = ContextualTutorial()
        st.rerun()
    
    if st.sidebar.button("⏭️ Skip Tutorial"):
        st.session_state.tutorial_completed = True
        st.rerun()
    
    # Tab selection for tutorial
    st.sidebar.markdown("### 📚 Learn About:")
    tutorial_tabs = ["analytics_dashboard", "price_charts", "trading"]
    
    # Get current index safely
    current_index = 0
    if tutorial.current_tab and tutorial.current_tab in tutorial_tabs:
        current_index = tutorial_tabs.index(tutorial.current_tab)
    
    selected_tutorial_tab = st.sidebar.selectbox(
        "Select Tab to Learn",
        [tab.replace('_', ' ').title() for tab in tutorial_tabs],
        index=current_index
    )
    
    if selected_tutorial_tab:
        tab_name = selected_tutorial_tab.lower().replace(' ', '_')
        if tab_name != tutorial.current_tab:
            tutorial.set_tab(tab_name)
            st.rerun()

def show_tutorial_for_tab(tab_name: str):
    """Show tutorial for specific tab"""
    if 'tutorial' not in st.session_state:
        st.session_state.tutorial = ContextualTutorial()
    
    tutorial = st.session_state.tutorial
    
    # Check if tab_name is valid
    if tab_name not in tutorial.tutorial_steps:
        return False
    
    tutorial.set_tab(tab_name)
    
    current_step = tutorial.get_current_step(tab_name)
    
    if current_step:
        # Show tutorial info box at the top
        show_tutorial_info_box(current_step, tab_name)
        
        # Highlight the specific element
        if current_step.get('highlight'):
            highlight_element(current_step['highlight'])
        
        return True
    
    return False

def add_element_id(element_id: str, content: str):
    """Add element ID to content for tutorial highlighting"""
    return f'<div id="{element_id}">{content}</div>'

def main():
    """Main function for contextual tutorial"""
    st.markdown("# 🎓 Contextual Tutorial System")
    st.markdown("This system provides step-by-step guidance within each tab.")
    
    # Show tutorial controls
    show_tutorial_controls()
    
    # Demo of how to use
    st.markdown("## How to Use:")
    st.markdown("1. Select a tab to learn about in the sidebar")
    st.markdown("2. Follow the step-by-step instructions")
    st.markdown("3. Use Previous/Next buttons to navigate")
    st.markdown("4. Click 'Mark Complete' for action steps")

if __name__ == "__main__":
    main()

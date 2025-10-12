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

def show_tutorial_overlay(step_info: Dict, tab_name: str):
    """Show tutorial overlay with step information"""
    if not step_info:
        return
    
    # Create tutorial overlay
    st.markdown(f"""
    <div id="tutorial-overlay" style="
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
        pointer-events: none;
    ">
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 20px;
            max-width: 500px;
            margin: 1rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            pointer-events: auto;
            color: white;
        ">
            <h3 style="margin: 0 0 1rem 0; color: white;">{step_info['title']}</h3>
            <p style="margin: 0 0 1.5rem 0; font-size: 1.1rem; line-height: 1.5;">{step_info['description']}</p>
            
            <div style="margin-bottom: 1.5rem;">
                <div style="background-color: rgba(255, 255, 255, 0.2); padding: 0.5rem; border-radius: 10px;">
                    <strong>Step {st.session_state.tutorial.current_step + 1} of {len(st.session_state.tutorial.tutorial_steps[tab_name])}</strong>
                </div>
            </div>
            
            <div style="display: flex; gap: 1rem; justify-content: space-between;">
                <button onclick="window.parent.postMessage('tutorial_previous', '*')" 
                        style="padding: 0.8rem 1.5rem; background-color: rgba(255, 255, 255, 0.2); color: white; border: 2px solid rgba(255, 255, 255, 0.3); border-radius: 10px; cursor: pointer; font-weight: bold;">
                    ← Previous
                </button>
                <button onclick="window.parent.postMessage('tutorial_next', '*')" 
                        style="padding: 0.8rem 1.5rem; background-color: rgba(255, 255, 255, 0.9); color: #667eea; border: none; border-radius: 10px; cursor: pointer; font-weight: bold;">
                    Next →
                </button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def highlight_element(element_id: str):
    """Add highlighting effect to specific element"""
    st.markdown(f"""
    <style>
    #{element_id} {{
        position: relative;
        animation: pulse 2s infinite;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.8);
        border: 3px solid #667eea;
        border-radius: 10px;
    }}
    
    @keyframes pulse {{
        0% {{ box-shadow: 0 0 20px rgba(102, 126, 234, 0.8); }}
        50% {{ box-shadow: 0 0 30px rgba(102, 126, 234, 1); }}
        100% {{ box-shadow: 0 0 20px rgba(102, 126, 234, 0.8); }}
    }}
    
    #{element_id}::before {{
        content: "👆";
        position: absolute;
        top: -30px;
        right: -10px;
        font-size: 24px;
        animation: bounce 1s infinite;
    }}
    
    @keyframes bounce {{
        0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
        40% {{ transform: translateY(-10px); }}
        60% {{ transform: translateY(-5px); }}
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
    if tutorial.current_tab:
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
    selected_tutorial_tab = st.sidebar.selectbox(
        "Select Tab to Learn",
        [tab.replace('_', ' ').title() for tab in tutorial_tabs],
        index=tutorial_tabs.index(tutorial.current_tab) if tutorial.current_tab in tutorial_tabs else 0
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
    tutorial.set_tab(tab_name)
    
    current_step = tutorial.get_current_step(tab_name)
    
    if current_step:
        # Show tutorial overlay
        show_tutorial_overlay(current_step, tab_name)
        
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

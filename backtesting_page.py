"""
Unified Strategy Backtesting Page
Redirects to the unified backtesting system
"""
import streamlit as st

def main():
    # Import and run unified backtesting
    from unified_backtesting import main as unified_backtesting_main
    unified_backtesting_main()
    return

if __name__ == "__main__":
    main()
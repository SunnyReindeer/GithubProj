import streamlit as st
import requests
from datetime import datetime, timedelta

# Alpha Vantage API configuration
ALPHA_VANTAGE_API_KEY = "PA25XA5HB5ZSXHQZ"
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

def get_alpha_vantage_data(function, symbol=None):
    """Get data from Alpha Vantage API"""
    try:
        params = {
            "function": function,
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        if symbol:
            params["symbol"] = symbol
            
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params, timeout=10)
        return response.json()
    except Exception as e:
        return None

def get_real_time_price(symbol):
    """Get real-time price data for a symbol"""
    data = get_alpha_vantage_data("GLOBAL_QUOTE", symbol)
    if data and "Global Quote" in data:
        quote = data["Global Quote"]
        return {
            "price": float(quote.get("05. price", 0)),
            "change": float(quote.get("09. change", 0)),
            "change_percent": quote.get("10. change percent", "0%").replace("%", ""),
            "volume": int(quote.get("06. volume", 0))
        }
    return None

def get_economic_news():
    """Get real-time economic news from Alpha Vantage"""
    try:
        params = {
            "function": "NEWS_SENTIMENT",
            "apikey": ALPHA_VANTAGE_API_KEY,
            "limit": 10
        }
        
        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params, timeout=10)
        data = response.json()
        
        if "feed" in data:
            return data["feed"]
        return None
    except Exception as e:
        return None

def get_economic_indicators():
    """Get real-time economic indicators"""
    try:
        # Get real-time economic indicators
        indicators = []
        
        # Try to get real data from Alpha Vantage
        data = get_alpha_vantage_data("REAL_GDP", "quarterly")
        if data and "data" in data:
            latest_gdp = data["data"][0] if data["data"] else None
            if latest_gdp:
                indicators.append({
                    "indicator": "GDP Growth",
                    "value": latest_gdp.get("value", "N/A"),
                    "date": latest_gdp.get("date", "N/A"),
                    "change": "N/A"
                })
        
        return indicators
    except Exception as e:
        return []

def get_market_analysis():
    """Get real-time market analysis and sentiment"""
    try:
        # Get market sentiment
        sentiment_data = get_alpha_vantage_data("NEWS_SENTIMENT", "NEWS_SENTIMENT")
        
        analysis = {
            "market_sentiment": "Neutral",
            "fear_greed_index": 50,
            "volatility": "Normal",
            "trend": "Sideways"
        }
        
        if sentiment_data and "feed" in sentiment_data:
            # Analyze sentiment from news
            positive_count = 0
            negative_count = 0
            
            for article in sentiment_data["feed"][:5]:  # Analyze top 5 articles
                if "overall_sentiment_score" in article:
                    score = float(article["overall_sentiment_score"])
                    if score > 0.1:
                        positive_count += 1
                    elif score < -0.1:
                        negative_count += 1
            
            if positive_count > negative_count:
                analysis["market_sentiment"] = "Positive"
            elif negative_count > positive_count:
                analysis["market_sentiment"] = "Negative"
        
        return analysis
    except Exception as e:
        return {
            "market_sentiment": "Neutral",
            "fear_greed_index": 50,
            "volatility": "Normal",
            "trend": "Sideways"
        }

def create_market_overview_page():
    """Create the main market overview page - currently empty for future development"""
    
    st.markdown("# 📊 Market Overview")
    st.markdown("This page is currently under development. Content will be added soon.")
    
    # Placeholder content
    st.info("🚧 Market Overview page is being rebuilt. Check back soon for updates!")

def main():
    """Main function for market overview page"""
    create_market_overview_page()

if __name__ == "__main__":
    main()
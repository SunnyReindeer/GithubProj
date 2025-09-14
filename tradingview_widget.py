"""
TradingView Widget Component for Streamlit
"""
import streamlit.components.v1 as components
import json

def create_tradingview_widget(symbol: str, timeframe: str = "1h", height: int = 500):
    """Create a TradingView widget with the specified symbol and timeframe"""
    
    # Map our symbols to TradingView format
    symbol_mapping = {
        "BTCUSDT": "BINANCE:BTCUSDT",
        "ETHUSDT": "BINANCE:ETHUSDT",
        "BNBUSDT": "BINANCE:BNBUSDT",
        "ADAUSDT": "BINANCE:ADAUSDT",
        "SOLUSDT": "BINANCE:SOLUSDT",
        "XRPUSDT": "BINANCE:XRPUSDT",
        "DOTUSDT": "BINANCE:DOTUSDT",
        "DOGEUSDT": "BINANCE:DOGEUSDT",
        "AVAXUSDT": "BINANCE:AVAXUSDT",
        "MATICUSDT": "BINANCE:MATICUSDT"
    }
    
    # Map timeframes to TradingView format
    timeframe_mapping = {
        "1m": "1",
        "5m": "5",
        "15m": "15",
        "30m": "30",
        "1h": "60",
        "4h": "240",
        "1d": "1D",
        "1w": "1W",
        "1M": "1M"
    }
    
    tv_symbol = symbol_mapping.get(symbol, "BINANCE:BTCUSDT")
    tv_timeframe = timeframe_mapping.get(timeframe, "60")
    
    # TradingView widget HTML
    widget_html = f"""
    <div class="tradingview-widget-container">
        <div id="tradingview_widget"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
            "width": "100%",
            "height": {height},
            "symbol": "{tv_symbol}",
            "interval": "{tv_timeframe}",
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#f1f3f6",
            "enable_publishing": false,
            "hide_top_toolbar": false,
            "hide_legend": false,
            "save_image": false,
            "container_id": "tradingview_widget",
            "studies": [
                "RSI@tv-basicstudies",
                "MACD@tv-basicstudies",
                "MAExp@tv-basicstudies",
                "BB@tv-basicstudies",
                "Volume@tv-basicstudies"
            ],
            "show_popup_button": true,
            "popup_width": "1000",
            "popup_height": "650",
            "no_referral_id": true,
            "referral_id": "",
            "withdateranges": true,
            "hide_side_toolbar": false,
            "allow_symbol_change": true,
            "details": true,
            "hotlist": true,
            "calendar": true,
            "news": [
                "headlines"
            ],
            "studies_overrides": {{
                "volume.volume.color.0": "#00ff88",
                "volume.volume.color.1": "#ff4444",
                "volume.volume.transparency": 70,
                "rsi.rsi.color": "#ff6b6b",
                "rsi.levels.0.color": "#ff6b6b",
                "rsi.levels.1.color": "#4ecdc4",
                "rsi.levels.2.color": "#45b7d1",
                "macd.macd.color": "#ff6b6b",
                "macd.signal.color": "#4ecdc4",
                "macd.histogram.color": "#ff6b6b"
            }}
        }});
        </script>
    </div>
    """
    
    return components.html(widget_html, height=height + 50)

def create_tradingview_advanced_chart(symbol: str, timeframe: str = "1h", height: int = 600):
    """Create an advanced TradingView chart with more features"""
    
    symbol_mapping = {
        "BTCUSDT": "BINANCE:BTCUSDT",
        "ETHUSDT": "BINANCE:ETHUSDT",
        "BNBUSDT": "BINANCE:BNBUSDT",
        "ADAUSDT": "BINANCE:ADAUSDT",
        "SOLUSDT": "BINANCE:SOLUSDT",
        "XRPUSDT": "BINANCE:XRPUSDT",
        "DOTUSDT": "BINANCE:DOTUSDT",
        "DOGEUSDT": "BINANCE:DOGEUSDT",
        "AVAXUSDT": "BINANCE:AVAXUSDT",
        "MATICUSDT": "BINANCE:MATICUSDT"
    }
    
    timeframe_mapping = {
        "1m": "1",
        "5m": "5",
        "15m": "15",
        "30m": "30",
        "1h": "60",
        "4h": "240",
        "1d": "1D",
        "1w": "1W",
        "1M": "1M"
    }
    
    tv_symbol = symbol_mapping.get(symbol, "BINANCE:BTCUSDT")
    tv_timeframe = timeframe_mapping.get(timeframe, "60")
    
    # Advanced TradingView chart HTML
    chart_html = f"""
    <div class="tradingview-widget-container" style="width: 100%; height: {height}px;">
        <div id="tradingview_advanced_chart" style="width: 100%; height: {height}px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
            "width": "100%",
            "height": {height},
            "symbol": "{tv_symbol}",
            "interval": "{tv_timeframe}",
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#1e1e1e",
            "enable_publishing": false,
            "withdateranges": true,
            "hide_side_toolbar": false,
            "allow_symbol_change": true,
            "save_image": false,
            "container_id": "tradingview_advanced_chart",
            "studies": [
                "RSI@tv-basicstudies",
                "MACD@tv-basicstudies",
                "MAExp@tv-basicstudies",
                "BB@tv-basicstudies",
                "Volume@tv-basicstudies",
                "Stochastic@tv-basicstudies",
                "Williams%R@tv-basicstudies",
                "CCI@tv-basicstudies",
                "ATR@tv-basicstudies",
                "ADX@tv-basicstudies"
            ],
            "show_popup_button": true,
            "popup_width": "1200",
            "popup_height": "800",
            "no_referral_id": true,
            "referral_id": "",
            "details": true,
            "hotlist": true,
            "calendar": true,
            "news": [
                "headlines"
            ],
            "studies_overrides": {{
                "volume.volume.color.0": "#00ff88",
                "volume.volume.color.1": "#ff4444",
                "volume.volume.transparency": 70,
                "rsi.rsi.color": "#ff6b6b",
                "rsi.levels.0.color": "#ff6b6b",
                "rsi.levels.1.color": "#4ecdc4",
                "rsi.levels.2.color": "#45b7d1",
                "macd.macd.color": "#ff6b6b",
                "macd.signal.color": "#4ecdc4",
                "macd.histogram.color": "#ff6b6b",
                "maexp.ma.color": "#ffa500",
                "maexp.ma.linewidth": 2,
                "bb.bb.color": "#808080",
                "bb.bb.linewidth": 1,
                "bb.bb.fillcolor": "rgba(128, 128, 128, 0.1)"
            }},
            "overrides": {{
                "paneProperties.background": "#1e1e1e",
                "paneProperties.vertGridProperties.color": "#2a2a2a",
                "paneProperties.horzGridProperties.color": "#2a2a2a",
                "symbolWatermarkProperties.transparency": 90,
                "scalesProperties.textColor": "#ffffff",
                "scalesProperties.lineColor": "#2a2a2a"
            }}
        }});
        </script>
    </div>
    """
    
    return components.html(chart_html, height=height + 50)

def create_tradingview_screener():
    """Create a TradingView market screener widget"""
    
    screener_html = """
    <div class="tradingview-widget-container">
        <div id="tradingview_screener"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({
            "width": "100%",
            "height": 600,
            "symbol": "CRYPTOCAP:TOTAL",
            "interval": "1D",
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#1e1e1e",
            "enable_publishing": false,
            "withdateranges": true,
            "hide_side_toolbar": false,
            "allow_symbol_change": true,
            "save_image": false,
            "container_id": "tradingview_screener",
            "studies": [
                "Volume@tv-basicstudies"
            ],
            "show_popup_button": true,
            "popup_width": "1000",
            "popup_height": "650",
            "no_referral_id": true,
            "referral_id": "",
            "details": true,
            "hotlist": true,
            "calendar": true,
            "news": [
                "headlines"
            ]
        });
        </script>
    </div>
    """
    
    return components.html(screener_html, height=650)

def create_tradingview_crypto_heatmap():
    """Create a TradingView cryptocurrency heatmap"""
    
    heatmap_html = """
    <div class="tradingview-widget-container">
        <div id="tradingview_heatmap"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({
            "width": "100%",
            "height": 400,
            "symbol": "CRYPTOCAP:TOTAL",
            "interval": "1D",
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#1e1e1e",
            "enable_publishing": false,
            "withdateranges": true,
            "hide_side_toolbar": false,
            "allow_symbol_change": true,
            "save_image": false,
            "container_id": "tradingview_heatmap",
            "studies": [
                "Volume@tv-basicstudies"
            ],
            "show_popup_button": true,
            "popup_width": "1000",
            "popup_height": "650",
            "no_referral_id": true,
            "referral_id": "",
            "details": true,
            "hotlist": true,
            "calendar": true,
            "news": [
                "headlines"
            ]
        });
        </script>
    </div>
    """
    
    return components.html(heatmap_html, height=450)

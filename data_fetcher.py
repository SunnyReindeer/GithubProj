"""
Real-time crypto data fetcher using WebSocket connections
"""
import asyncio
import json
import websocket
import threading
import time
from typing import Dict, Callable, Optional
import requests
import pandas as pd
from datetime import datetime

class CryptoDataFetcher:
    def __init__(self):
        self.ws = None
        self.is_connected = False
        self.price_data = {}
        self.subscribers = []
        self.symbols = ["btcusdt", "ethusdt", "bnbusdt", "adausdt", "solusdt"]
        
    def add_subscriber(self, callback: Callable):
        """Add a callback function to receive price updates"""
        self.subscribers.append(callback)
    
    def remove_subscriber(self, callback: Callable):
        """Remove a callback function"""
        if callback in self.subscribers:
            self.subscribers.remove(callback)
    
    def notify_subscribers(self, data: Dict):
        """Notify all subscribers of new price data"""
        for callback in self.subscribers:
            try:
                callback(data)
            except Exception as e:
                print(f"Error in subscriber callback: {e}")
    
    def on_message(self, ws, message):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            
            if 'stream' in data and 'data' in data:
                stream_name = data['stream']
                ticker_data = data['data']
                
                symbol = ticker_data['s']
                price = float(ticker_data['c'])
                volume = float(ticker_data['v'])
                change_24h = float(ticker_data['P'])
                
                price_info = {
                    'symbol': symbol,
                    'price': price,
                    'volume': volume,
                    'change_24h': change_24h,
                    'timestamp': datetime.now()
                }
                
                self.price_data[symbol] = price_info
                self.notify_subscribers(price_info)
                
        except Exception as e:
            print(f"Error processing message: {e}")
    
    def on_error(self, ws, error):
        """Handle WebSocket errors"""
        print(f"WebSocket error: {error}")
        self.is_connected = False
    
    def on_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket close"""
        print("WebSocket connection closed")
        self.is_connected = False
    
    def on_open(self, ws):
        """Handle WebSocket open"""
        print("WebSocket connection opened")
        self.is_connected = True
    
    def start_websocket(self):
        """Start WebSocket connection in a separate thread"""
        def run_websocket():
            websocket.enableTrace(False)
            # Create stream names for individual ticker streams
            streams = [f"{symbol}@ticker" for symbol in self.symbols]
            stream_names = "/".join(streams)
            
            self.ws = websocket.WebSocketApp(
                f"wss://stream.binance.com:9443/stream?streams={stream_names}",
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            self.ws.run_forever()
        
        thread = threading.Thread(target=run_websocket, daemon=True)
        thread.start()
        return thread
    
    def get_historical_data(self, symbol: str, interval: str = "1h", limit: int = 100) -> pd.DataFrame:
        """Get historical price data"""
        try:
            url = f"https://api.binance.com/api/v3/klines"
            params = {
                'symbol': symbol.upper(),
                'interval': interval,
                'limit': limit
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            df = pd.DataFrame(data, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_volume', 'trades', 'taker_buy_base',
                'taker_buy_quote', 'ignore'
            ])
            
            # Convert to proper data types
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['open'] = df['open'].astype(float)
            df['high'] = df['high'].astype(float)
            df['low'] = df['low'].astype(float)
            df['close'] = df['close'].astype(float)
            df['volume'] = df['volume'].astype(float)
            
            return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
            
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return pd.DataFrame()
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price for a symbol"""
        symbol_upper = symbol.upper()
        if symbol_upper in self.price_data:
            return self.price_data[symbol_upper]['price']
        return None
    
    def stop(self):
        """Stop the WebSocket connection"""
        if self.ws:
            self.ws.close()
            self.is_connected = False

# Global instance
data_fetcher = CryptoDataFetcher()

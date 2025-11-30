"""
Multi-Asset Data Provider System
Handles data fetching for stocks, bonds, commodities, forex, crypto, and other assets
"""
import yfinance as yf
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import time
import random
from dataclasses import dataclass
from multi_asset_config import multi_asset_config, Asset, AssetClass

@dataclass
class PriceData:
    symbol: str
    price: float
    change: float
    change_percent: float
    volume: float
    timestamp: datetime
    high_24h: float
    low_24h: float
    open_24h: float

@dataclass
class HistoricalData:
    symbol: str
    data: pd.DataFrame
    timeframe: str
    start_date: datetime
    end_date: datetime

class MultiAssetDataProvider:
    def __init__(self):
        self.providers = {
            "yahoo": self._yahoo_provider,
            "alpha_vantage": self._alpha_vantage_provider,
            "binance": self._binance_provider,
            "federal_reserve": self._fred_provider
        }
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
        
    def get_current_prices(self, symbols: List[str]) -> Dict[str, PriceData]:
        """Get current prices for multiple symbols"""
        prices = {}
        
        # Group symbols by asset class to use appropriate provider
        symbol_groups = self._group_symbols_by_provider(symbols)
        
        for provider, provider_symbols in symbol_groups.items():
            try:
                provider_prices = self.providers[provider](provider_symbols, "current")
                prices.update(provider_prices)
            except Exception as e:
                print(f"Error fetching prices from {provider}: {e}")
                # Fallback to mock data
                for symbol in provider_symbols:
                    prices[symbol] = self._get_mock_price_data(symbol)
        
        return prices
    
    def get_historical_data(self, symbol: str, period: str = "1y", 
                          interval: str = "1d") -> HistoricalData:
        """Get historical data for a symbol"""
        cache_key = f"{symbol}_{period}_{interval}"
        
        # Check cache first
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_duration:
                return cached_data
        
        # Get asset info to determine provider
        asset = multi_asset_config.get_asset(symbol)
        if not asset:
            # Try to infer from symbol
            provider = self._infer_provider_from_symbol(symbol)
        else:
            provider = asset.data_provider
        
        try:
            historical_data = self.providers[provider]([symbol], "historical", period, interval)
            if symbol in historical_data:
                data = historical_data[symbol]
                # Cache the result
                self.cache[cache_key] = (data, time.time())
                return data
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {e}")
            return self._get_mock_historical_data(symbol, period, interval)
        
        return self._get_mock_historical_data(symbol, period, interval)
    
    def _group_symbols_by_provider(self, symbols: List[str]) -> Dict[str, List[str]]:
        """Group symbols by their data provider"""
        groups = {}
        
        for symbol in symbols:
            asset = multi_asset_config.get_asset(symbol)
            if asset:
                provider = asset.data_provider
            else:
                provider = self._infer_provider_from_symbol(symbol)
            
            if provider not in groups:
                groups[provider] = []
            groups[provider].append(symbol)
        
        return groups
    
    def _infer_provider_from_symbol(self, symbol: str) -> str:
        """Infer data provider from symbol format"""
        if symbol.endswith("=X"):
            return "yahoo"  # Forex pairs
        elif symbol.startswith("^"):
            return "yahoo"  # Indices
        elif any(crypto in symbol.upper() for crypto in ["BTC", "ETH", "BNB", "ADA", "SOL"]):
            return "yahoo"  # Crypto
        else:
            return "yahoo"  # Default to Yahoo Finance
    
    def _yahoo_provider(self, symbols: List[str], data_type: str, 
                       period: str = None, interval: str = None) -> Dict[str, Any]:
        """Yahoo Finance data provider"""
        if data_type == "current":
            return self._yahoo_current_prices(symbols)
        elif data_type == "historical":
            return self._yahoo_historical_data(symbols, period, interval)
    
    def _yahoo_current_prices(self, symbols: List[str]) -> Dict[str, PriceData]:
        """Get current prices from Yahoo Finance"""
        prices = {}
        
        try:
            # Convert crypto symbols from USDT format to -USD format for Yahoo Finance
            converted_symbols = []
            symbol_mapping = {}  # Maps Yahoo symbol -> original symbol
            
            for symbol in symbols:
                # Check if it's a crypto symbol in USDT format (e.g., BTCUSDT)
                if symbol.endswith("USDT") and len(symbol) > 4:
                    # Convert BTCUSDT -> BTC-USD
                    yahoo_symbol = symbol[:-4] + "-USD"
                    converted_symbols.append(yahoo_symbol)
                    symbol_mapping[yahoo_symbol] = symbol
                else:
                    converted_symbols.append(symbol)
                    symbol_mapping[symbol] = symbol
            
            # Create ticker objects
            tickers = yf.Tickers(" ".join(converted_symbols))
            
            for yahoo_symbol in converted_symbols:
                original_symbol = symbol_mapping[yahoo_symbol]
                try:
                    ticker = tickers.tickers.get(yahoo_symbol)
                    if not ticker:
                        # Try direct lookup if batch failed
                        ticker = yf.Ticker(yahoo_symbol)
                    
                    info = ticker.info
                    
                    current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
                    if current_price == 0:
                        # Try fast_info as fallback
                        try:
                            fast_info = ticker.fast_info
                            current_price = fast_info.get('lastPrice', 0)
                        except:
                            pass
                    
                    previous_close = info.get('previousClose', current_price)
                    change = current_price - previous_close
                    change_percent = (change / previous_close) * 100 if previous_close > 0 else 0
                    
                    prices[original_symbol] = PriceData(
                        symbol=original_symbol,
                        price=current_price,
                        change=change,
                        change_percent=change_percent,
                        volume=info.get('volume', 0),
                        timestamp=datetime.now(),
                        high_24h=info.get('dayHigh', current_price),
                        low_24h=info.get('dayLow', current_price),
                        open_24h=info.get('open', current_price)
                    )
                except Exception as e:
                    print(f"Error fetching {original_symbol} (Yahoo: {yahoo_symbol}): {e}")
                    prices[original_symbol] = self._get_mock_price_data(original_symbol)
        
        except Exception as e:
            print(f"Yahoo Finance error: {e}")
            # Fallback to mock data
            for symbol in symbols:
                prices[symbol] = self._get_mock_price_data(symbol)
        
        return prices
    
    def _yahoo_historical_data(self, symbols: List[str], period: str, interval: str) -> Dict[str, HistoricalData]:
        """Get historical data from Yahoo Finance"""
        historical_data = {}
        
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                df = ticker.history(period=period, interval=interval)
                
                if not df.empty:
                    historical_data[symbol] = HistoricalData(
                        symbol=symbol,
                        data=df,
                        timeframe=interval,
                        start_date=df.index[0],
                        end_date=df.index[-1]
                    )
                else:
                    historical_data[symbol] = self._get_mock_historical_data(symbol, period, interval)
            
            except Exception as e:
                print(f"Error fetching historical data for {symbol}: {e}")
                historical_data[symbol] = self._get_mock_historical_data(symbol, period, interval)
        
        return historical_data
    
    def _alpha_vantage_provider(self, symbols: List[str], data_type: str, 
                               period: str = None, interval: str = None) -> Dict[str, Any]:
        """Alpha Vantage data provider (requires API key)"""
        # This would require an API key from Alpha Vantage
        # For now, fallback to mock data
        if data_type == "current":
            return {symbol: self._get_mock_price_data(symbol) for symbol in symbols}
        else:
            return {symbol: self._get_mock_historical_data(symbol, period, interval) for symbol in symbols}
    
    def _binance_provider(self, symbols: List[str], data_type: str, 
                         period: str = None, interval: str = None) -> Dict[str, Any]:
        """Binance data provider for crypto"""
        if data_type == "current":
            return self._binance_current_prices(symbols)
        else:
            return {symbol: self._get_mock_historical_data(symbol, period, interval) for symbol in symbols}
    
    def _binance_current_prices(self, symbols: List[str]) -> Dict[str, PriceData]:
        """Get current prices from Binance"""
        prices = {}
        
        try:
            # Convert symbols to Binance format
            binance_symbols = []
            symbol_mapping = {}
            
            for symbol in symbols:
                if symbol.endswith("-USD"):
                    binance_symbol = symbol.replace("-USD", "USDT")
                    binance_symbols.append(binance_symbol)
                    symbol_mapping[binance_symbol] = symbol
            
            if binance_symbols:
                url = "https://api.binance.com/api/v3/ticker/24hr"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                for item in data:
                    if item['symbol'] in symbol_mapping:
                        original_symbol = symbol_mapping[item['symbol']]
                        prices[original_symbol] = PriceData(
                            symbol=original_symbol,
                            price=float(item['lastPrice']),
                            change=float(item['priceChange']),
                            change_percent=float(item['priceChangePercent']),
                            volume=float(item['volume']),
                            timestamp=datetime.now(),
                            high_24h=float(item['highPrice']),
                            low_24h=float(item['lowPrice']),
                            open_24h=float(item['openPrice'])
                        )
        
        except Exception as e:
            print(f"Binance API error: {e}")
            # Fallback to mock data
            for symbol in symbols:
                prices[symbol] = self._get_mock_price_data(symbol)
        
        return prices
    
    def _fred_provider(self, symbols: List[str], data_type: str, 
                      period: str = None, interval: str = None) -> Dict[str, Any]:
        """Federal Reserve Economic Data provider"""
        # This would require an API key from FRED
        # For now, fallback to mock data
        if data_type == "current":
            return {symbol: self._get_mock_price_data(symbol) for symbol in symbols}
        else:
            return {symbol: self._get_mock_historical_data(symbol, period, interval) for symbol in symbols}
    
    def _get_mock_price_data(self, symbol: str) -> PriceData:
        """Generate mock price data for demonstration"""
        # Base prices for different asset types
        base_prices = {
            # Stocks
            "AAPL": 175.0, "MSFT": 350.0, "GOOGL": 140.0, "AMZN": 150.0, "TSLA": 250.0,
            "META": 300.0, "NVDA": 450.0, "JPM": 150.0, "JNJ": 160.0, "V": 250.0,
            # Bonds
            "TLT": 95.0, "IEF": 105.0, "SHY": 82.0, "LQD": 110.0, "HYG": 75.0,
            # Commodities
            "GLD": 190.0, "SLV": 22.0, "USO": 70.0, "UNG": 25.0, "DBA": 20.0,
            # Forex
            "EURUSD=X": 1.08, "GBPUSD=X": 1.25, "USDJPY=X": 150.0, "USDCHF=X": 0.88,
            # Crypto
            "BTC-USD": 45000.0, "ETH-USD": 3000.0, "BNB-USD": 300.0, "ADA-USD": 0.5,
            # ETFs
            "SPY": 450.0, "QQQ": 380.0, "IWM": 200.0, "VTI": 220.0,
            # Indices
            "^GSPC": 4500.0, "^DJI": 35000.0, "^IXIC": 14000.0, "^VIX": 15.0
        }
        
        base_price = base_prices.get(symbol, 100.0)
        
        # Add random variation
        variation = random.uniform(0.95, 1.05)
        current_price = base_price * variation
        change = current_price - base_price
        change_percent = (change / base_price) * 100
        
        return PriceData(
            symbol=symbol,
            price=current_price,
            change=change,
            change_percent=change_percent,
            volume=random.uniform(1000000, 10000000),
            timestamp=datetime.now(),
            high_24h=current_price * 1.02,
            low_24h=current_price * 0.98,
            open_24h=base_price
        )
    
    def _get_mock_historical_data(self, symbol: str, period: str, interval: str) -> HistoricalData:
        """Generate mock historical data"""
        # Determine number of data points based on period and interval
        period_days = {
            "1d": 1, "5d": 5, "1mo": 30, "3mo": 90, "6mo": 180, "1y": 365, "2y": 730, "5y": 1825
        }
        
        interval_minutes = {
            "1m": 1, "5m": 5, "15m": 15, "30m": 30, "1h": 60, "1d": 1440
        }
        
        days = period_days.get(period, 365)
        minutes = interval_minutes.get(interval, 1440)
        
        # Calculate number of data points
        total_minutes = days * 24 * 60
        num_points = total_minutes // minutes
        
        # Generate timestamps
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        timestamps = pd.date_range(start=start_time, end=end_time, periods=num_points)
        
        # Get base price
        mock_price = self._get_mock_price_data(symbol)
        base_price = mock_price.price
        
        # Generate price data with random walk
        prices = []
        current_price = base_price
        
        for i in range(num_points):
            # Random walk with some trend
            change = random.uniform(-0.02, 0.02)  # ±2% change
            current_price *= (1 + change)
            prices.append(current_price)
        
        # Create OHLC data
        data = []
        for i, (timestamp, close_price) in enumerate(zip(timestamps, prices)):
            high = close_price * random.uniform(1.0, 1.01)
            low = close_price * random.uniform(0.99, 1.0)
            open_price = prices[i-1] if i > 0 else close_price
            volume = random.uniform(1000000, 10000000)
            
            data.append({
                'Open': open_price,
                'High': high,
                'Low': low,
                'Close': close_price,
                'Volume': volume
            })
        
        df = pd.DataFrame(data, index=timestamps)
        
        return HistoricalData(
            symbol=symbol,
            data=df,
            timeframe=interval,
            start_date=start_time,
            end_date=end_time
        )
    
    def get_market_overview(self) -> Dict[str, Any]:
        """Get market overview for different asset classes"""
        # Sample symbols for each asset class
        sample_symbols = {
            "stocks": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"],
            "bonds": ["TLT", "IEF", "SHY", "LQD", "HYG"],
            "commodities": ["GLD", "SLV", "USO", "UNG", "DBA"],
            "forex": ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "USDCHF=X"],
            "crypto": ["BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD"],
            "etfs": ["SPY", "QQQ", "IWM", "VTI", "VEA"],
            "indices": ["^GSPC", "^DJI", "^IXIC", "^VIX"]
        }
        
        overview = {}
        
        for asset_class, symbols in sample_symbols.items():
            try:
                prices = self.get_current_prices(symbols)
                
                # Calculate class metrics
                total_change = sum(price.change_percent for price in prices.values())
                avg_change = total_change / len(prices) if prices else 0
                
                overview[asset_class] = {
                    "average_change": avg_change,
                    "symbols_count": len(prices),
                    "top_gainers": sorted(prices.values(), key=lambda x: x.change_percent, reverse=True)[:3],
                    "top_losers": sorted(prices.values(), key=lambda x: x.change_percent)[:3]
                }
            except Exception as e:
                print(f"Error getting overview for {asset_class}: {e}")
                overview[asset_class] = {
                    "average_change": 0,
                    "symbols_count": 0,
                    "top_gainers": [],
                    "top_losers": []
                }
        
        return overview
    
    def search_assets(self, query: str, asset_class: str = None) -> List[Dict[str, Any]]:
        """Search for assets by query"""
        results = multi_asset_config.search_assets(query)
        
        # Filter by asset class if specified
        if asset_class:
            results = [asset for asset in results if asset.asset_class.value == asset_class]
        
        # Convert to dictionary format for API response
        search_results = []
        for asset in results:
            try:
                # Get current price
                price_data = self.get_current_prices([asset.symbol])
                current_price = price_data.get(asset.symbol, self._get_mock_price_data(asset.symbol))
                
                search_results.append({
                    "symbol": asset.symbol,
                    "name": asset.name,
                    "asset_class": asset.asset_class.value,
                    "region": asset.region.value,
                    "sector": asset.sector.value if asset.sector else None,
                    "currency": asset.currency,
                    "current_price": current_price.price,
                    "change_percent": current_price.change_percent,
                    "risk_level": asset.risk_level,
                    "volatility_level": asset.volatility_level,
                    "liquidity_level": asset.liquidity_level,
                    "description": asset.description
                })
            except Exception as e:
                print(f"Error processing {asset.symbol}: {e}")
        
        return search_results

# Global multi-asset data provider instance
multi_asset_data_provider = MultiAssetDataProvider()

"""
Multi-Asset Trading Strategies
Asset-specific trading strategies for stocks, bonds, commodities, forex, crypto, and other assets
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from multi_asset_config import AssetClass, AssetRegion, AssetSector
from multi_asset_data_provider import multi_asset_data_provider, HistoricalData

class StrategyCategory(Enum):
    TREND_FOLLOWING = "trend_following"
    MEAN_REVERSION = "mean_reversion"
    MOMENTUM = "momentum"
    ARBITRAGE = "arbitrage"
    SCALPING = "scalping"
    SWING_TRADING = "swing_trading"
    POSITION_TRADING = "position_trading"
    PAIRS_TRADING = "pairs_trading"
    SECTOR_ROTATION = "sector_rotation"
    DIVIDEND_CAPTURE = "dividend_capture"

class AssetSpecificStrategy:
    def __init__(self, name: str, description: str, asset_classes: List[AssetClass], 
                 category: StrategyCategory, risk_level: int, complexity: str):
        self.name = name
        self.description = description
        self.asset_classes = asset_classes
        self.category = category
        self.risk_level = risk_level
        self.complexity = complexity
        self.parameters = {}
        self.signals = {}
        
    def calculate_signals(self, data: HistoricalData, **params) -> pd.DataFrame:
        """Calculate trading signals for the strategy"""
        raise NotImplementedError("Subclasses must implement calculate_signals")
    
    def get_parameters(self) -> Dict[str, Any]:
        """Get strategy parameters"""
        return self.parameters
    
    def set_parameters(self, **params):
        """Set strategy parameters"""
        self.parameters.update(params)

class StockStrategies:
    """Stock-specific trading strategies"""
    
    @staticmethod
    def moving_average_crossover(data: HistoricalData, fast_period: int = 20, 
                               slow_period: int = 50) -> pd.DataFrame:
        """Moving Average Crossover Strategy for Stocks"""
        df = data.data.copy()
        
        # Calculate moving averages
        df['MA_Fast'] = df['Close'].rolling(window=fast_period).mean()
        df['MA_Slow'] = df['Close'].rolling(window=slow_period).mean()
        
        # Generate signals
        df['Signal'] = 0
        df['Signal'][fast_period:] = np.where(
            df['MA_Fast'][fast_period:] > df['MA_Slow'][fast_period:], 1, 0
        )
        df['Position'] = df['Signal'].diff()
        
        return df
    
    @staticmethod
    def rsi_mean_reversion(data: HistoricalData, period: int = 14, 
                          oversold: float = 30, overbought: float = 70) -> pd.DataFrame:
        """RSI Mean Reversion Strategy for Stocks"""
        df = data.data.copy()
        
        # Calculate RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Generate signals
        df['Signal'] = 0
        df['Signal'] = np.where(df['RSI'] < oversold, 1, 
                               np.where(df['RSI'] > overbought, -1, 0))
        df['Position'] = df['Signal'].diff()
        
        return df
    
    @staticmethod
    def bollinger_bands_strategy(data: HistoricalData, period: int = 20, 
                               std_dev: float = 2) -> pd.DataFrame:
        """Bollinger Bands Strategy for Stocks"""
        df = data.data.copy()
        
        # Calculate Bollinger Bands
        df['MA'] = df['Close'].rolling(window=period).mean()
        df['STD'] = df['Close'].rolling(window=period).std()
        df['Upper_Band'] = df['MA'] + (df['STD'] * std_dev)
        df['Lower_Band'] = df['MA'] - (df['STD'] * std_dev)
        
        # Generate signals
        df['Signal'] = 0
        df['Signal'] = np.where(df['Close'] < df['Lower_Band'], 1,
                               np.where(df['Close'] > df['Upper_Band'], -1, 0))
        df['Position'] = df['Signal'].diff()
        
        return df

class BondStrategies:
    """Bond-specific trading strategies"""
    
    @staticmethod
    def yield_curve_strategy(data: HistoricalData, short_term: int = 2, 
                           long_term: int = 10) -> pd.DataFrame:
        """Yield Curve Strategy for Bonds"""
        df = data.data.copy()
        
        # Calculate yield spread (simplified)
        df['Yield_Spread'] = df['Close'].rolling(window=long_term).mean() - df['Close'].rolling(window=short_term).mean()
        
        # Generate signals based on yield curve steepening/flattening
        df['Signal'] = 0
        df['Signal'] = np.where(df['Yield_Spread'] > df['Yield_Spread'].rolling(window=20).mean(), 1,
                               np.where(df['Yield_Spread'] < df['Yield_Spread'].rolling(window=20).mean(), -1, 0))
        df['Position'] = df['Signal'].diff()
        
        return df
    
    @staticmethod
    def duration_hedging(data: HistoricalData, target_duration: float = 5.0) -> pd.DataFrame:
        """Duration Hedging Strategy for Bonds"""
        df = data.data.copy()
        
        # Calculate modified duration (simplified)
        df['Duration'] = df['Close'].rolling(window=20).std() / df['Close'].rolling(window=20).mean()
        
        # Generate signals based on duration mismatch
        df['Signal'] = 0
        df['Signal'] = np.where(df['Duration'] > target_duration, -1,
                               np.where(df['Duration'] < target_duration, 1, 0))
        df['Position'] = df['Signal'].diff()
        
        return df

class CommodityStrategies:
    """Commodity-specific trading strategies"""
    
    @staticmethod
    def seasonal_strategy(data: HistoricalData, seasonal_period: int = 252) -> pd.DataFrame:
        """Seasonal Strategy for Commodities"""
        df = data.data.copy()
        
        # Calculate seasonal patterns
        df['DayOfYear'] = df.index.dayofyear
        df['Seasonal_Avg'] = df.groupby('DayOfYear')['Close'].transform('mean')
        df['Seasonal_Deviation'] = (df['Close'] - df['Seasonal_Avg']) / df['Seasonal_Avg']
        
        # Generate signals based on seasonal deviations
        df['Signal'] = 0
        df['Signal'] = np.where(df['Seasonal_Deviation'] > 0.05, 1,
                               np.where(df['Seasonal_Deviation'] < -0.05, -1, 0))
        df['Position'] = df['Signal'].diff()
        
        return df
    
    @staticmethod
    def inventory_cycle_strategy(data: HistoricalData, inventory_period: int = 60) -> pd.DataFrame:
        """Inventory Cycle Strategy for Commodities"""
        df = data.data.copy()
        
        # Calculate inventory cycle (simplified using volume as proxy)
        df['Volume_MA'] = df['Volume'].rolling(window=inventory_period).mean()
        df['Inventory_Cycle'] = df['Volume'] / df['Volume_MA']
        
        # Generate signals based on inventory levels
        df['Signal'] = 0
        df['Signal'] = np.where(df['Inventory_Cycle'] > 1.2, -1,
                               np.where(df['Inventory_Cycle'] < 0.8, 1, 0))
        df['Position'] = df['Signal'].diff()
        
        return df

class ForexStrategies:
    """Forex-specific trading strategies"""
    
    @staticmethod
    def carry_trade_strategy(data: HistoricalData, interest_rate_diff: float = 0.02) -> pd.DataFrame:
        """Carry Trade Strategy for Forex"""
        df = data.data.copy()
        
        # Calculate interest rate differential (simplified)
        df['Interest_Diff'] = interest_rate_diff  # Would be actual rate difference
        
        # Generate signals based on carry trade conditions
        df['Signal'] = 0
        df['Signal'] = np.where(df['Interest_Diff'] > 0.01, 1,
                               np.where(df['Interest_Diff'] < -0.01, -1, 0))
        df['Position'] = df['Signal'].diff()
        
        return df
    
    @staticmethod
    def momentum_breakout(data: HistoricalData, breakout_period: int = 20) -> pd.DataFrame:
        """Momentum Breakout Strategy for Forex"""
        df = data.data.copy()
        
        # Calculate breakout levels
        df['High_MA'] = df['High'].rolling(window=breakout_period).mean()
        df['Low_MA'] = df['Low'].rolling(window=breakout_period).mean()
        
        # Generate signals on breakouts
        df['Signal'] = 0
        df['Signal'] = np.where(df['Close'] > df['High_MA'], 1,
                               np.where(df['Close'] < df['Low_MA'], -1, 0))
        df['Position'] = df['Signal'].diff()
        
        return df

class CryptoStrategies:
    """Cryptocurrency-specific trading strategies"""
    
    @staticmethod
    def volatility_breakout(data: HistoricalData, volatility_period: int = 20) -> pd.DataFrame:
        """Volatility Breakout Strategy for Crypto"""
        df = data.data.copy()
        
        # Calculate volatility
        df['Returns'] = df['Close'].pct_change()
        df['Volatility'] = df['Returns'].rolling(window=volatility_period).std()
        
        # Generate signals on volatility spikes
        df['Signal'] = 0
        df['Signal'] = np.where(df['Volatility'] > df['Volatility'].rolling(window=50).quantile(0.8), 1,
                               np.where(df['Volatility'] < df['Volatility'].rolling(window=50).quantile(0.2), -1, 0))
        df['Position'] = df['Signal'].diff()
        
        return df
    
    @staticmethod
    def fear_greed_strategy(data: HistoricalData, fear_threshold: float = 20, 
                          greed_threshold: float = 80) -> pd.DataFrame:
        """Fear & Greed Strategy for Crypto"""
        df = data.data.copy()
        
        # Calculate fear/greed indicator (simplified using RSI)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['Fear_Greed'] = 100 - (100 / (1 + rs))
        
        # Generate signals based on fear/greed levels
        df['Signal'] = 0
        df['Signal'] = np.where(df['Fear_Greed'] < fear_threshold, 1,
                               np.where(df['Fear_Greed'] > greed_threshold, -1, 0))
        df['Position'] = df['Signal'].diff()
        
        return df

class REITStrategies:
    """REIT-specific trading strategies"""
    
    @staticmethod
    def dividend_capture_strategy(data: HistoricalData, dividend_threshold: float = 0.03) -> pd.DataFrame:
        """Dividend Capture Strategy for REITs"""
        df = data.data.copy()
        
        # Calculate dividend yield (simplified)
        df['Dividend_Yield'] = df['Close'].rolling(window=252).mean() * dividend_threshold / df['Close']
        
        # Generate signals based on dividend yield
        df['Signal'] = 0
        df['Signal'] = np.where(df['Dividend_Yield'] > dividend_threshold, 1, 0)
        df['Position'] = df['Signal'].diff()
        
        return df
    
    @staticmethod
    def interest_rate_sensitivity(data: HistoricalData, rate_sensitivity: float = -0.5) -> pd.DataFrame:
        """Interest Rate Sensitivity Strategy for REITs"""
        df = data.data.copy()
        
        # Calculate interest rate sensitivity (simplified)
        df['Rate_Sensitivity'] = df['Close'].rolling(window=20).std() * rate_sensitivity
        
        # Generate signals based on rate sensitivity
        df['Signal'] = 0
        df['Signal'] = np.where(df['Rate_Sensitivity'] > 0, -1,
                               np.where(df['Rate_Sensitivity'] < 0, 1, 0))
        df['Position'] = df['Signal'].diff()
        
        return df

class ETFStrategies:
    """ETF-specific trading strategies"""
    
    @staticmethod
    def sector_rotation_strategy(data: HistoricalData, rotation_period: int = 60) -> pd.DataFrame:
        """Sector Rotation Strategy for ETFs"""
        df = data.data.copy()
        
        # Calculate relative strength
        df['RS'] = df['Close'] / df['Close'].rolling(window=rotation_period).mean()
        
        # Generate signals based on relative strength
        df['Signal'] = 0
        df['Signal'] = np.where(df['RS'] > 1.1, 1,
                               np.where(df['RS'] < 0.9, -1, 0))
        df['Position'] = df['Signal'].diff()
        
        return df
    
    @staticmethod
    def rebalancing_strategy(data: HistoricalData, rebalance_period: int = 90) -> pd.DataFrame:
        """Rebalancing Strategy for ETFs"""
        df = data.data.copy()
        
        # Calculate target allocation deviation
        df['Target_Allocation'] = 0.1  # 10% target allocation
        df['Current_Allocation'] = df['Close'] / df['Close'].rolling(window=252).sum()
        df['Allocation_Deviation'] = df['Current_Allocation'] - df['Target_Allocation']
        
        # Generate rebalancing signals
        df['Signal'] = 0
        df['Signal'] = np.where(df['Allocation_Deviation'] > 0.02, -1,
                               np.where(df['Allocation_Deviation'] < -0.02, 1, 0))
        df['Position'] = df['Signal'].diff()
        
        return df

class MultiAssetStrategyManager:
    """Manager for multi-asset trading strategies"""
    
    def __init__(self):
        self.strategies = {
            # Stock strategies
            "stock_ma_crossover": {
                "name": "Stock Moving Average Crossover",
                "description": "Trend following strategy using moving average crossovers",
                "asset_classes": [AssetClass.STOCKS],
                "category": StrategyCategory.TREND_FOLLOWING,
                "risk_level": 5,
                "complexity": "Intermediate",
                "function": StockStrategies.moving_average_crossover
            },
            "stock_rsi_mean_reversion": {
                "name": "Stock RSI Mean Reversion",
                "description": "Mean reversion strategy using RSI indicator",
                "asset_classes": [AssetClass.STOCKS],
                "category": StrategyCategory.MEAN_REVERSION,
                "risk_level": 4,
                "complexity": "Intermediate",
                "function": StockStrategies.rsi_mean_reversion
            },
            "stock_bollinger_bands": {
                "name": "Stock Bollinger Bands",
                "description": "Mean reversion strategy using Bollinger Bands",
                "asset_classes": [AssetClass.STOCKS],
                "category": StrategyCategory.MEAN_REVERSION,
                "risk_level": 4,
                "complexity": "Intermediate",
                "function": StockStrategies.bollinger_bands_strategy
            },
            
            # Bond strategies
            "bond_yield_curve": {
                "name": "Bond Yield Curve Strategy",
                "description": "Strategy based on yield curve steepening/flattening",
                "asset_classes": [AssetClass.BONDS],
                "category": StrategyCategory.TREND_FOLLOWING,
                "risk_level": 3,
                "complexity": "Advanced",
                "function": BondStrategies.yield_curve_strategy
            },
            "bond_duration_hedging": {
                "name": "Bond Duration Hedging",
                "description": "Duration hedging strategy for interest rate risk",
                "asset_classes": [AssetClass.BONDS],
                "category": StrategyCategory.ARBITRAGE,
                "risk_level": 2,
                "complexity": "Advanced",
                "function": BondStrategies.duration_hedging
            },
            
            # Commodity strategies
            "commodity_seasonal": {
                "name": "Commodity Seasonal Strategy",
                "description": "Seasonal pattern trading for commodities",
                "asset_classes": [AssetClass.COMMODITIES],
                "category": StrategyCategory.POSITION_TRADING,
                "risk_level": 6,
                "complexity": "Advanced",
                "function": CommodityStrategies.seasonal_strategy
            },
            "commodity_inventory_cycle": {
                "name": "Commodity Inventory Cycle",
                "description": "Strategy based on inventory cycle patterns",
                "asset_classes": [AssetClass.COMMODITIES],
                "category": StrategyCategory.MEAN_REVERSION,
                "risk_level": 5,
                "complexity": "Advanced",
                "function": CommodityStrategies.inventory_cycle_strategy
            },
            
            # Forex strategies
            "forex_carry_trade": {
                "name": "Forex Carry Trade",
                "description": "Interest rate differential trading",
                "asset_classes": [AssetClass.FOREX],
                "category": StrategyCategory.POSITION_TRADING,
                "risk_level": 7,
                "complexity": "Advanced",
                "function": ForexStrategies.carry_trade_strategy
            },
            "forex_momentum_breakout": {
                "name": "Forex Momentum Breakout",
                "description": "Momentum breakout strategy for forex pairs",
                "asset_classes": [AssetClass.FOREX],
                "category": StrategyCategory.MOMENTUM,
                "risk_level": 6,
                "complexity": "Intermediate",
                "function": ForexStrategies.momentum_breakout
            },
            
            # Crypto strategies
            "crypto_volatility_breakout": {
                "name": "Crypto Volatility Breakout",
                "description": "Volatility-based breakout strategy for crypto",
                "asset_classes": [AssetClass.CRYPTO],
                "category": StrategyCategory.MOMENTUM,
                "risk_level": 8,
                "complexity": "Intermediate",
                "function": CryptoStrategies.volatility_breakout
            },
            "crypto_fear_greed": {
                "name": "Crypto Fear & Greed",
                "description": "Fear and greed sentiment strategy for crypto",
                "asset_classes": [AssetClass.CRYPTO],
                "category": StrategyCategory.MEAN_REVERSION,
                "risk_level": 7,
                "complexity": "Intermediate",
                "function": CryptoStrategies.fear_greed_strategy
            },
            "crypto_moving_average": {
                "name": "Crypto Moving Average Crossover",
                "description": "Trend following strategy using moving average crossovers for crypto",
                "asset_classes": [AssetClass.CRYPTO],
                "category": StrategyCategory.TREND_FOLLOWING,
                "risk_level": 5,
                "complexity": "Beginner",
                "function": None  # Will use backtesting engine
            },
            "crypto_rsi": {
                "name": "Crypto RSI Strategy",
                "description": "Mean reversion strategy using RSI indicator for crypto",
                "asset_classes": [AssetClass.CRYPTO],
                "category": StrategyCategory.MEAN_REVERSION,
                "risk_level": 4,
                "complexity": "Beginner",
                "function": None  # Will use backtesting engine
            },
            "crypto_bollinger_bands": {
                "name": "Crypto Bollinger Bands",
                "description": "Mean reversion strategy using Bollinger Bands for crypto",
                "asset_classes": [AssetClass.CRYPTO],
                "category": StrategyCategory.MEAN_REVERSION,
                "risk_level": 4,
                "complexity": "Beginner",
                "function": None  # Will use backtesting engine
            },
            "crypto_macd": {
                "name": "Crypto MACD Strategy",
                "description": "Momentum strategy using MACD indicator for crypto",
                "asset_classes": [AssetClass.CRYPTO],
                "category": StrategyCategory.MOMENTUM,
                "risk_level": 5,
                "complexity": "Intermediate",
                "function": None  # Will use backtesting engine
            },
            
            # REIT strategies
            "reit_dividend_capture": {
                "name": "REIT Dividend Capture",
                "description": "Dividend capture strategy for REITs",
                "asset_classes": [AssetClass.REITS],
                "category": StrategyCategory.DIVIDEND_CAPTURE,
                "risk_level": 3,
                "complexity": "Beginner",
                "function": REITStrategies.dividend_capture_strategy
            },
            "reit_interest_rate_sensitivity": {
                "name": "REIT Interest Rate Sensitivity",
                "description": "Interest rate sensitivity strategy for REITs",
                "asset_classes": [AssetClass.REITS],
                "category": StrategyCategory.TREND_FOLLOWING,
                "risk_level": 4,
                "complexity": "Intermediate",
                "function": REITStrategies.interest_rate_sensitivity
            },
            
            # ETF strategies
            "etf_sector_rotation": {
                "name": "ETF Sector Rotation",
                "description": "Sector rotation strategy for ETFs",
                "asset_classes": [AssetClass.ETFS],
                "category": StrategyCategory.SECTOR_ROTATION,
                "risk_level": 5,
                "complexity": "Advanced",
                "function": ETFStrategies.sector_rotation_strategy
            },
            "etf_rebalancing": {
                "name": "ETF Rebalancing Strategy",
                "description": "Portfolio rebalancing strategy for ETFs",
                "asset_classes": [AssetClass.ETFS],
                "category": StrategyCategory.POSITION_TRADING,
                "risk_level": 3,
                "complexity": "Beginner",
                "function": ETFStrategies.rebalancing_strategy
            }
        }
    
    def get_strategies_by_asset_class(self, asset_class: AssetClass) -> List[Dict[str, Any]]:
        """Get strategies suitable for a specific asset class"""
        return [strategy for strategy in self.strategies.values() 
                if asset_class in strategy["asset_classes"]]
    
    def get_strategies_by_category(self, category: StrategyCategory) -> List[Dict[str, Any]]:
        """Get strategies by category"""
        return [strategy for strategy in self.strategies.values() 
                if strategy["category"] == category]
    
    def get_strategies_by_risk_level(self, min_risk: int, max_risk: int) -> List[Dict[str, Any]]:
        """Get strategies within a risk level range"""
        return [strategy for strategy in self.strategies.values() 
                if min_risk <= strategy["risk_level"] <= max_risk]
    
    def get_strategy(self, strategy_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific strategy by ID"""
        return self.strategies.get(strategy_id)
    
    def run_strategy(self, strategy_id: str, data: HistoricalData, **params) -> pd.DataFrame:
        """Run a specific strategy on historical data"""
        strategy = self.get_strategy(strategy_id)
        if not strategy:
            raise ValueError(f"Strategy {strategy_id} not found")
        
        return strategy["function"](data, **params)
    
    def get_all_strategies(self) -> Dict[str, Dict[str, Any]]:
        """Get all available strategies"""
        return self.strategies
    
    def get_strategy_recommendations(self, asset_classes: List[AssetClass], 
                                   risk_level: int, complexity: str = None) -> List[Dict[str, Any]]:
        """Get strategy recommendations based on criteria"""
        recommendations = []
        
        for strategy in self.strategies.values():
            # Check asset class compatibility
            if not any(ac in strategy["asset_classes"] for ac in asset_classes):
                continue
            
            # Check risk level compatibility
            if abs(strategy["risk_level"] - risk_level) > 2:
                continue
            
            # Check complexity if specified
            if complexity and strategy["complexity"] != complexity:
                continue
            
            recommendations.append(strategy)
        
        # Sort by risk level proximity
        recommendations.sort(key=lambda x: abs(x["risk_level"] - risk_level))
        
        return recommendations

# Global multi-asset strategy manager instance
multi_asset_strategy_manager = MultiAssetStrategyManager()

"""
Multi-Asset Configuration System
Supports stocks, bonds, commodities, forex, crypto, and other investment assets
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum
import yfinance as yf
import requests
import pandas as pd
from datetime import datetime, timedelta

class AssetClass(Enum):
    STOCKS = "stocks"
    BONDS = "bonds"
    COMMODITIES = "commodities"
    FOREX = "forex"
    CRYPTO = "crypto"
    REITS = "reits"
    ETFS = "etfs"
    INDICES = "indices"
    COMMODITY_FUTURES = "commodity_futures"
    CURRENCY_FUTURES = "currency_futures"

class AssetRegion(Enum):
    US = "us"
    EUROPE = "europe"
    ASIA = "asia"
    EMERGING_MARKETS = "emerging_markets"
    GLOBAL = "global"

class AssetSector(Enum):
    TECHNOLOGY = "technology"
    HEALTHCARE = "healthcare"
    FINANCIAL = "financial"
    ENERGY = "energy"
    CONSUMER_DISCRETIONARY = "consumer_discretionary"
    CONSUMER_STAPLES = "consumer_staples"
    INDUSTRIALS = "industrials"
    MATERIALS = "materials"
    UTILITIES = "utilities"
    REAL_ESTATE = "real_estate"
    COMMUNICATION = "communication"

@dataclass
class Asset:
    symbol: str
    name: str
    asset_class: AssetClass
    region: AssetRegion
    sector: Optional[AssetSector]
    currency: str
    exchange: str
    data_provider: str
    min_trade_size: float
    trading_hours: str
    volatility_level: str  # low, medium, high
    liquidity_level: str   # low, medium, high
    risk_level: int        # 1-10 scale
    description: str
    metadata: Dict[str, Any]

class MultiAssetConfig:
    def __init__(self):
        self.assets = self._initialize_assets()
        self.data_providers = self._initialize_data_providers()
        self.asset_allocations = self._initialize_asset_allocations()
        
    def _initialize_assets(self) -> Dict[str, Asset]:
        """Initialize comprehensive asset database"""
        assets = {}
        
        # US Stocks
        us_stocks = [
            ("AAPL", "Apple Inc.", AssetSector.TECHNOLOGY),
            ("MSFT", "Microsoft Corporation", AssetSector.TECHNOLOGY),
            ("GOOGL", "Alphabet Inc.", AssetSector.TECHNOLOGY),
            ("AMZN", "Amazon.com Inc.", AssetSector.CONSUMER_DISCRETIONARY),
            ("TSLA", "Tesla Inc.", AssetSector.CONSUMER_DISCRETIONARY),
            ("META", "Meta Platforms Inc.", AssetSector.COMMUNICATION),
            ("NVDA", "NVIDIA Corporation", AssetSector.TECHNOLOGY),
            ("JPM", "JPMorgan Chase & Co.", AssetSector.FINANCIAL),
            ("JNJ", "Johnson & Johnson", AssetSector.HEALTHCARE),
            ("V", "Visa Inc.", AssetSector.FINANCIAL),
            ("PG", "Procter & Gamble Co.", AssetSector.CONSUMER_STAPLES),
            ("UNH", "UnitedHealth Group Inc.", AssetSector.HEALTHCARE),
            ("HD", "Home Depot Inc.", AssetSector.CONSUMER_DISCRETIONARY),
            ("MA", "Mastercard Inc.", AssetSector.FINANCIAL),
            ("DIS", "Walt Disney Co.", AssetSector.COMMUNICATION)
        ]
        
        for symbol, name, sector in us_stocks:
            assets[symbol] = Asset(
                symbol=symbol,
                name=name,
                asset_class=AssetClass.STOCKS,
                region=AssetRegion.US,
                sector=sector,
                currency="USD",
                exchange="NASDAQ/NYSE",
                data_provider="yahoo",
                min_trade_size=1.0,
                trading_hours="09:30-16:00 EST",
                volatility_level="medium",
                liquidity_level="high",
                risk_level=6,
                description=f"US {sector.value} stock",
                metadata={"market_cap": "large", "dividend_yield": "varies"}
            )
        
        # International Stocks
        intl_stocks = [
            ("ASML", "ASML Holding N.V.", AssetRegion.EUROPE, AssetSector.TECHNOLOGY),
            ("TSM", "Taiwan Semiconductor", AssetRegion.ASIA, AssetSector.TECHNOLOGY),
            ("SAP", "SAP SE", AssetRegion.EUROPE, AssetSector.TECHNOLOGY),
            ("TM", "Toyota Motor Corp", AssetRegion.ASIA, AssetSector.CONSUMER_DISCRETIONARY),
            ("NVO", "Novo Nordisk A/S", AssetRegion.EUROPE, AssetSector.HEALTHCARE)
        ]
        
        for symbol, name, region, sector in intl_stocks:
            assets[symbol] = Asset(
                symbol=symbol,
                name=name,
                asset_class=AssetClass.STOCKS,
                region=region,
                sector=sector,
                currency="USD",
                exchange="International",
                data_provider="yahoo",
                min_trade_size=1.0,
                trading_hours="varies",
                volatility_level="medium",
                liquidity_level="high",
                risk_level=6,
                description=f"International {sector.value} stock",
                metadata={"market_cap": "large"}
            )
        
        # Bonds
        bonds = [
            ("TLT", "iShares 20+ Year Treasury Bond ETF", "USD", 3),
            ("IEF", "iShares 7-10 Year Treasury Bond ETF", "USD", 2),
            ("SHY", "iShares 1-3 Year Treasury Bond ETF", "USD", 1),
            ("LQD", "iShares iBoxx $ Investment Grade Corporate Bond ETF", "USD", 4),
            ("HYG", "iShares iBoxx $ High Yield Corporate Bond ETF", "USD", 6)
        ]
        
        for symbol, name, currency, risk_level in bonds:
            assets[symbol] = Asset(
                symbol=symbol,
                name=name,
                asset_class=AssetClass.BONDS,
                region=AssetRegion.US,
                sector=None,
                currency=currency,
                exchange="NYSE",
                data_provider="yahoo",
                min_trade_size=1.0,
                trading_hours="09:30-16:00 EST",
                volatility_level="low",
                liquidity_level="high",
                risk_level=risk_level,
                description="Bond ETF",
                metadata={"bond_type": "treasury", "duration": "varies"}
            )
        
        # Commodities
        commodities = [
            ("GLD", "SPDR Gold Trust", "USD", 4),
            ("SLV", "iShares Silver Trust", "USD", 5),
            ("USO", "United States Oil Fund", "USD", 7),
            ("UNG", "United States Natural Gas Fund", "USD", 8),
            ("DBA", "Invesco DB Agriculture Fund", "USD", 6),
            ("CORN", "Teucrium Corn Fund", "USD", 6),
            ("WEAT", "Teucrium Wheat Fund", "USD", 6)
        ]
        
        for symbol, name, currency, risk_level in commodities:
            assets[symbol] = Asset(
                symbol=symbol,
                name=name,
                asset_class=AssetClass.COMMODITIES,
                region=AssetRegion.GLOBAL,
                sector=None,
                currency=currency,
                exchange="NYSE",
                data_provider="yahoo",
                min_trade_size=1.0,
                trading_hours="09:30-16:00 EST",
                volatility_level="high",
                liquidity_level="medium",
                risk_level=risk_level,
                description="Commodity ETF",
                metadata={"commodity_type": "varies"}
            )
        
        # Forex
        forex_pairs = [
            ("EURUSD=X", "Euro/US Dollar", "USD", 5),
            ("GBPUSD=X", "British Pound/US Dollar", "USD", 6),
            ("USDJPY=X", "US Dollar/Japanese Yen", "USD", 4),
            ("USDCHF=X", "US Dollar/Swiss Franc", "USD", 4),
            ("AUDUSD=X", "Australian Dollar/US Dollar", "USD", 6),
            ("USDCAD=X", "US Dollar/Canadian Dollar", "USD", 4),
            ("NZDUSD=X", "New Zealand Dollar/US Dollar", "USD", 6)
        ]
        
        for symbol, name, currency, risk_level in forex_pairs:
            assets[symbol] = Asset(
                symbol=symbol,
                name=name,
                asset_class=AssetClass.FOREX,
                region=AssetRegion.GLOBAL,
                sector=None,
                currency=currency,
                exchange="Forex",
                data_provider="yahoo",
                min_trade_size=1000.0,
                trading_hours="24/5",
                volatility_level="medium",
                liquidity_level="high",
                risk_level=risk_level,
                description="Forex pair",
                metadata={"base_currency": "varies", "quote_currency": "USD"}
            )
        
        # REITs
        reits = [
            ("VNQ", "Vanguard Real Estate ETF", "USD", 5),
            ("IYR", "iShares U.S. Real Estate ETF", "USD", 5),
            ("SCHH", "Schwab U.S. REIT ETF", "USD", 5),
            ("XLRE", "Real Estate Select Sector SPDR Fund", "USD", 5)
        ]
        
        for symbol, name, currency, risk_level in reits:
            assets[symbol] = Asset(
                symbol=symbol,
                name=name,
                asset_class=AssetClass.REITS,
                region=AssetRegion.US,
                sector=AssetSector.REAL_ESTATE,
                currency=currency,
                exchange="NYSE",
                data_provider="yahoo",
                min_trade_size=1.0,
                trading_hours="09:30-16:00 EST",
                volatility_level="medium",
                liquidity_level="high",
                risk_level=risk_level,
                description="Real Estate Investment Trust ETF",
                metadata={"dividend_yield": "high"}
            )
        
        # ETFs
        etfs = [
            ("SPY", "SPDR S&P 500 ETF Trust", "USD", 4),
            ("QQQ", "Invesco QQQ Trust", "USD", 5),
            ("IWM", "iShares Russell 2000 ETF", "USD", 6),
            ("VTI", "Vanguard Total Stock Market ETF", "USD", 4),
            ("VEA", "Vanguard FTSE Developed Markets ETF", "USD", 5),
            ("VWO", "Vanguard FTSE Emerging Markets ETF", "USD", 7),
            ("BND", "Vanguard Total Bond Market ETF", "USD", 2)
        ]
        
        for symbol, name, currency, risk_level in etfs:
            assets[symbol] = Asset(
                symbol=symbol,
                name=name,
                asset_class=AssetClass.ETFS,
                region=AssetRegion.GLOBAL,
                sector=None,
                currency=currency,
                exchange="NYSE",
                data_provider="yahoo",
                min_trade_size=1.0,
                trading_hours="09:30-16:00 EST",
                volatility_level="medium",
                liquidity_level="high",
                risk_level=risk_level,
                description="Exchange Traded Fund",
                metadata={"expense_ratio": "low"}
            )
        
        # Indices
        indices = [
            ("^GSPC", "S&P 500", "USD", 4),
            ("^DJI", "Dow Jones Industrial Average", "USD", 4),
            ("^IXIC", "NASDAQ Composite", "USD", 5),
            ("^VIX", "CBOE Volatility Index", "USD", 8),
            ("^TNX", "10-Year Treasury Note", "USD", 2)
        ]
        
        for symbol, name, currency, risk_level in indices:
            assets[symbol] = Asset(
                symbol=symbol,
                name=name,
                asset_class=AssetClass.INDICES,
                region=AssetRegion.US,
                sector=None,
                currency=currency,
                exchange="CBOE",
                data_provider="yahoo",
                min_trade_size=1.0,
                trading_hours="09:30-16:00 EST",
                volatility_level="medium",
                liquidity_level="high",
                risk_level=risk_level,
                description="Market Index",
                metadata={"index_type": "market"}
            )
        
        # Cryptocurrencies (existing)
        crypto_assets = [
            ("BTC-USD", "Bitcoin", "USD", 7),
            ("ETH-USD", "Ethereum", "USD", 8),
            ("BNB-USD", "Binance Coin", "USD", 8),
            ("ADA-USD", "Cardano", "USD", 8),
            ("SOL-USD", "Solana", "USD", 9),
            ("XRP-USD", "XRP", "USD", 8),
            ("DOT-USD", "Polkadot", "USD", 8),
            ("DOGE-USD", "Dogecoin", "USD", 9),
            ("AVAX-USD", "Avalanche", "USD", 9),
            ("MATIC-USD", "Polygon", "USD", 8)
        ]
        
        for symbol, name, currency, risk_level in crypto_assets:
            assets[symbol] = Asset(
                symbol=symbol,
                name=name,
                asset_class=AssetClass.CRYPTO,
                region=AssetRegion.GLOBAL,
                sector=None,
                currency=currency,
                exchange="Crypto Exchanges",
                data_provider="yahoo",
                min_trade_size=0.001,
                trading_hours="24/7",
                volatility_level="very_high",
                liquidity_level="high",
                risk_level=risk_level,
                description="Cryptocurrency",
                metadata={"blockchain": "varies", "market_cap": "varies"}
            )
        
        return assets
    
    def _initialize_data_providers(self) -> Dict[str, Dict[str, Any]]:
        """Initialize data provider configurations"""
        return {
            "yahoo": {
                "name": "Yahoo Finance",
                "api_url": "https://query1.finance.yahoo.com/v8/finance/chart/",
                "rate_limit": 2000,  # requests per hour
                "supported_assets": [AssetClass.STOCKS, AssetClass.BONDS, AssetClass.COMMODITIES, 
                                   AssetClass.FOREX, AssetClass.REITS, AssetClass.ETFS, 
                                   AssetClass.INDICES, AssetClass.CRYPTO],
                "real_time": True,
                "historical": True
            },
            "alpha_vantage": {
                "name": "Alpha Vantage",
                "api_url": "https://www.alphavantage.co/query",
                "rate_limit": 5,  # requests per minute
                "supported_assets": [AssetClass.STOCKS, AssetClass.FOREX, AssetClass.CRYPTO],
                "real_time": True,
                "historical": True,
                "api_key_required": True
            },
            "binance": {
                "name": "Binance",
                "api_url": "https://api.binance.com/api/v3/",
                "rate_limit": 1200,  # requests per minute
                "supported_assets": [AssetClass.CRYPTO],
                "real_time": True,
                "historical": True
            },
            "federal_reserve": {
                "name": "Federal Reserve Economic Data",
                "api_url": "https://api.stlouisfed.org/fred/",
                "rate_limit": 120,  # requests per minute
                "supported_assets": [AssetClass.BONDS, AssetClass.INDICES],
                "real_time": False,
                "historical": True,
                "api_key_required": True
            }
        }
    
    def _initialize_asset_allocations(self) -> Dict[str, Dict[str, float]]:
        """Initialize recommended asset allocations for different risk profiles"""
        return {
            "conservative": {
                "stocks": 0.30,
                "bonds": 0.50,
                "commodities": 0.05,
                "reits": 0.10,
                "cash": 0.05
            },
            "moderate": {
                "stocks": 0.50,
                "bonds": 0.30,
                "commodities": 0.10,
                "reits": 0.05,
                "crypto": 0.03,
                "cash": 0.02
            },
            "aggressive": {
                "stocks": 0.60,
                "bonds": 0.15,
                "commodities": 0.10,
                "crypto": 0.10,
                "reits": 0.03,
                "cash": 0.02
            },
            "very_aggressive": {
                "stocks": 0.40,
                "crypto": 0.30,
                "commodities": 0.15,
                "bonds": 0.10,
                "reits": 0.03,
                "cash": 0.02
            }
        }
    
    def get_assets_by_class(self, asset_class: AssetClass) -> List[Asset]:
        """Get all assets of a specific class"""
        return [asset for asset in self.assets.values() if asset.asset_class == asset_class]
    
    def get_assets_by_region(self, region: AssetRegion) -> List[Asset]:
        """Get all assets from a specific region"""
        return [asset for asset in self.assets.values() if asset.region == region]
    
    def get_assets_by_sector(self, sector: AssetSector) -> List[Asset]:
        """Get all assets from a specific sector"""
        return [asset for asset in self.assets.values() if asset.sector == sector]
    
    def get_assets_by_risk_level(self, min_risk: int, max_risk: int) -> List[Asset]:
        """Get assets within a specific risk level range"""
        return [asset for asset in self.assets.values() if min_risk <= asset.risk_level <= max_risk]
    
    def get_asset(self, symbol: str) -> Optional[Asset]:
        """Get a specific asset by symbol"""
        return self.assets.get(symbol)
    
    def get_supported_asset_classes(self) -> List[AssetClass]:
        """Get all supported asset classes"""
        return list(AssetClass)
    
    def get_asset_allocation(self, risk_profile: str) -> Dict[str, float]:
        """Get recommended asset allocation for a risk profile"""
        return self.asset_allocations.get(risk_profile, self.asset_allocations["moderate"])
    
    def search_assets(self, query: str) -> List[Asset]:
        """Search assets by name or symbol"""
        query = query.lower()
        results = []
        for asset in self.assets.values():
            if (query in asset.symbol.lower() or 
                query in asset.name.lower() or 
                query in asset.asset_class.value.lower()):
                results.append(asset)
        return results

# Global multi-asset configuration instance
multi_asset_config = MultiAssetConfig()

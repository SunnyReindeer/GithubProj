"""
Fund-Based Portfolio Manager (Like Syfe)
Creates themed portfolios instead of strategy-based recommendations
Uses AI labeling for sectors and themes
"""
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime
import yfinance as yf

from risk_assessment_engine import RiskProfile, RiskTolerance

class PortfolioTheme(Enum):
    """Portfolio themes (like Syfe's portfolios)"""
    CORE = "Core Portfolio"  # Balanced, diversified
    GROWTH = "Growth Portfolio"  # Tech, growth stocks
    DIVIDEND = "Dividend Portfolio"  # Income-focused
    ESG = "ESG Portfolio"  # Sustainable investing
    REITS = "REITs Portfolio"  # Real estate
    EMERGING = "Emerging Markets"  # Emerging economies
    TECH = "Tech Focus"  # Technology sector
    DEFENSIVE = "Defensive Portfolio"  # Safe, stable
    AGGRESSIVE = "Aggressive Growth"  # High risk, high return

class AILabel(Enum):
    """AI-generated labels for investments"""
    # Sector Labels
    TECHNOLOGY = "Technology"
    HEALTHCARE = "Healthcare"
    FINANCIAL = "Financial Services"
    ENERGY = "Energy"
    CONSUMER = "Consumer Goods"
    INDUSTRIAL = "Industrial"
    MATERIALS = "Materials"
    UTILITIES = "Utilities"
    REAL_ESTATE = "Real Estate"
    COMMUNICATION = "Communication Services"
    
    # Theme Labels
    GROWTH_STOCK = "Growth Stock"
    VALUE_STOCK = "Value Stock"
    DIVIDEND_STOCK = "Dividend Stock"
    BLUE_CHIP = "Blue Chip"
    SMALL_CAP = "Small Cap"
    LARGE_CAP = "Large Cap"
    MID_CAP = "Mid Cap"
    
    # Geographic Labels
    US_MARKET = "US Market"
    EMERGING_MARKET = "Emerging Market"
    DEVELOPED_MARKET = "Developed Market"
    ASIA_PACIFIC = "Asia Pacific"
    EUROPE = "Europe"
    
    # Risk Labels
    LOW_RISK = "Low Risk"
    MEDIUM_RISK = "Medium Risk"
    HIGH_RISK = "High Risk"
    
    # Style Labels
    ESG_COMPLIANT = "ESG Compliant"
    SUSTAINABLE = "Sustainable"
    INCOME_FOCUSED = "Income Focused"
    CAPITAL_APPRECIATION = "Capital Appreciation"

@dataclass
class FundHolding:
    """A single holding in a fund portfolio"""
    symbol: str
    name: str
    sector: str
    ai_labels: List[AILabel]  # AI-generated labels
    allocation: float  # Percentage allocation (0-1)
    asset_class: str  # Stock, ETF, Bond, Crypto, etc.
    description: str

@dataclass
class FundPortfolio:
    """A fund portfolio (like Syfe's portfolios)"""
    theme: PortfolioTheme
    name: str
    description: str
    risk_level: int  # 1-10
    expected_return: float  # Annual %
    expected_volatility: float
    holdings: List[FundHolding]
    total_allocation: float  # Should sum to 1.0
    rebalancing_frequency: str  # Monthly, Quarterly, etc.
    suitability_score: float  # Match with user profile (0-100)

class AILabeler:
    """AI system to label investments with sectors, themes, and characteristics"""
    
    # Sector mapping for stocks
    SECTOR_MAP = {
        # Technology
        "AAPL": "Technology", "MSFT": "Technology", "GOOGL": "Technology",
        "META": "Technology", "NVDA": "Technology", "AMD": "Technology",
        "INTC": "Technology", "CRM": "Technology", "ORCL": "Technology",
        "TSM": "Technology", "ASML": "Technology",
        
        # Healthcare
        "JNJ": "Healthcare", "PFE": "Healthcare", "UNH": "Healthcare",
        "ABBV": "Healthcare", "TMO": "Healthcare", "ABT": "Healthcare",
        "DHR": "Healthcare", "BMY": "Healthcare",
        
        # Financial
        "JPM": "Financial Services", "BAC": "Financial Services",
        "WFC": "Financial Services", "GS": "Financial Services",
        "MS": "Financial Services", "C": "Financial Services",
        "V": "Financial Services", "MA": "Financial Services",
        
        # Energy
        "XOM": "Energy", "CVX": "Energy", "SLB": "Energy",
        "COP": "Energy", "EOG": "Energy",
        
        # Consumer
        "AMZN": "Consumer Discretionary", "TSLA": "Consumer Discretionary",
        "HD": "Consumer Discretionary", "NKE": "Consumer Discretionary",
        "SBUX": "Consumer Discretionary", "MCD": "Consumer Staples",
        "KO": "Consumer Staples", "PEP": "Consumer Staples",
        "WMT": "Consumer Staples", "PG": "Consumer Staples",
        
        # Industrial
        "BA": "Industrial", "CAT": "Industrial", "GE": "Industrial",
        "HON": "Industrial", "LMT": "Industrial",
        
        # Communication
        "DIS": "Communication Services", "NFLX": "Communication Services",
        "CMCSA": "Communication Services", "VZ": "Communication Services",
        "T": "Communication Services",
    }
    
    # ETF Theme mapping
    ETF_THEMES = {
        "SPY": ["US Market", "Large Cap", "Broad Market"],
        "QQQ": ["Technology", "Growth Stock", "US Market"],
        "VTI": ["US Market", "Total Market", "Diversified"],
        "VEA": ["Developed Market", "International", "Europe"],
        "VWO": ["Emerging Market", "International", "Asia Pacific"],
        "IWM": ["US Market", "Small Cap", "Growth Stock"],
        "XLK": ["Technology", "Sector", "Growth Stock"],
        "XLV": ["Healthcare", "Sector", "Defensive"],
        "XLF": ["Financial Services", "Sector", "Value Stock"],
        "XLE": ["Energy", "Sector", "Cyclical"],
        "XLY": ["Consumer Discretionary", "Sector", "Growth Stock"],
        "XLP": ["Consumer Staples", "Sector", "Defensive"],
        "XLI": ["Industrial", "Sector", "Cyclical"],
        "XLB": ["Materials", "Sector", "Cyclical"],
        "XLU": ["Utilities", "Sector", "Defensive", "Dividend Stock"],
        "XLRE": ["Real Estate", "Sector", "Income Focused"],
        "VYM": ["Dividend Stock", "Value Stock", "Income Focused"],
        "SCHD": ["Dividend Stock", "Value Stock", "Income Focused"],
        "VNQ": ["Real Estate", "REITs", "Income Focused"],
    }
    
    def label_investment(self, symbol: str, asset_class: str = "Stock") -> List[AILabel]:
        """Generate AI labels for an investment"""
        labels = []
        
        # Get sector label
        if asset_class == "Stock" and symbol in self.SECTOR_MAP:
            sector = self.SECTOR_MAP[symbol]
            # Map sector to AILabel enum
            sector_map = {
                "Technology": AILabel.TECHNOLOGY,
                "Healthcare": AILabel.HEALTHCARE,
                "Financial Services": AILabel.FINANCIAL,
                "Energy": AILabel.ENERGY,
                "Consumer Discretionary": AILabel.CONSUMER,
                "Consumer Staples": AILabel.CONSUMER,
                "Industrial": AILabel.INDUSTRIAL,
                "Materials": AILabel.MATERIALS,
                "Utilities": AILabel.UTILITIES,
                "Real Estate": AILabel.REAL_ESTATE,
                "Communication Services": AILabel.COMMUNICATION,
            }
            if sector in sector_map:
                labels.append(sector_map[sector])
        
        # Get ETF theme labels
        if asset_class == "ETF" and symbol in self.ETF_THEMES:
            themes = self.ETF_THEMES[symbol]
            theme_map = {
                "Technology": AILabel.TECHNOLOGY,
                "Healthcare": AILabel.HEALTHCARE,
                "Financial Services": AILabel.FINANCIAL,
                "Energy": AILabel.ENERGY,
                "Consumer Discretionary": AILabel.CONSUMER,
                "Consumer Staples": AILabel.CONSUMER,
                "Industrial": AILabel.INDUSTRIAL,
                "Materials": AILabel.MATERIALS,
                "Utilities": AILabel.UTILITIES,
                "Real Estate": AILabel.REAL_ESTATE,
                "US Market": AILabel.US_MARKET,
                "Emerging Market": AILabel.EMERGING_MARKET,
                "Developed Market": AILabel.DEVELOPED_MARKET,
                "Asia Pacific": AILabel.ASIA_PACIFIC,
                "Europe": AILabel.EUROPE,
                "Growth Stock": AILabel.GROWTH_STOCK,
                "Value Stock": AILabel.VALUE_STOCK,
                "Dividend Stock": AILabel.DIVIDEND_STOCK,
                "Large Cap": AILabel.LARGE_CAP,
                "Small Cap": AILabel.SMALL_CAP,
                "Mid Cap": AILabel.MID_CAP,
                "Income Focused": AILabel.INCOME_FOCUSED,
                "REITs": AILabel.REAL_ESTATE,
            }
            for theme in themes:
                if theme in theme_map:
                    labels.append(theme_map[theme])
        
        # Add risk labels based on volatility (would need real data)
        # For now, use heuristics
        if asset_class == "Crypto":
            labels.append(AILabel.HIGH_RISK)
        elif asset_class == "Bond":
            labels.append(AILabel.LOW_RISK)
        else:
            labels.append(AILabel.MEDIUM_RISK)
        
        return labels
    
    def get_investment_name(self, symbol: str) -> str:
        """Get human-readable name for investment"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return info.get("longName", symbol) or info.get("shortName", symbol) or symbol
        except:
            return symbol

class FundPortfolioManager:
    """Manages fund-based portfolios (like Syfe)"""
    
    def __init__(self):
        self.labeler = AILabeler()
        self.portfolios = self._initialize_portfolios()
    
    def _initialize_portfolios(self) -> List[FundPortfolio]:
        """Initialize fund portfolios (like Syfe's offerings)"""
        return [
            # Core Portfolio - Balanced, diversified
            FundPortfolio(
                theme=PortfolioTheme.CORE,
                name="Core Portfolio",
                description="A balanced, diversified portfolio suitable for most investors. Mix of stocks, ETFs, and bonds.",
                risk_level=5,
                expected_return=8.5,
                expected_volatility=12.0,
                holdings=[
                    FundHolding("SPY", "S&P 500 ETF", "ETF", 
                               [AILabel.US_MARKET, AILabel.LARGE_CAP, AILabel.MEDIUM_RISK], 0.30, "ETF", "Broad US market exposure"),
                    FundHolding("VTI", "Total Stock Market ETF", "ETF",
                               [AILabel.US_MARKET, AILabel.LARGE_CAP, AILabel.MEDIUM_RISK], 0.25, "ETF", "Total US market"),
                    FundHolding("VEA", "Developed Markets ETF", "ETF",
                               [AILabel.DEVELOPED_MARKET, AILabel.EUROPE, AILabel.MEDIUM_RISK], 0.20, "ETF", "International developed markets"),
                    FundHolding("VWO", "Emerging Markets ETF", "ETF",
                               [AILabel.EMERGING_MARKET, AILabel.ASIA_PACIFIC, AILabel.HIGH_RISK], 0.15, "ETF", "Emerging markets exposure"),
                    FundHolding("TLT", "20+ Year Treasury Bond ETF", "ETF",
                               [AILabel.LOW_RISK, AILabel.INCOME_FOCUSED], 0.10, "Bond", "Long-term bonds for stability"),
                ],
                total_allocation=1.0,
                rebalancing_frequency="Quarterly",
                suitability_score=0.0
            ),
            
            # Growth Portfolio - Tech and growth stocks
            FundPortfolio(
                theme=PortfolioTheme.GROWTH,
                name="Growth Portfolio",
                description="Focus on technology and growth companies with high potential returns.",
                risk_level=7,
                expected_return=12.0,
                expected_volatility=18.0,
                holdings=[
                    FundHolding("QQQ", "NASDAQ 100 ETF", "ETF",
                               [AILabel.TECHNOLOGY, AILabel.GROWTH_STOCK, AILabel.US_MARKET], 0.35, "ETF", "Tech-heavy growth"),
                    FundHolding("AAPL", "Apple Inc", "Stock",
                               [AILabel.TECHNOLOGY, AILabel.LARGE_CAP, AILabel.GROWTH_STOCK], 0.15, "Stock", "Tech giant"),
                    FundHolding("MSFT", "Microsoft Corporation", "Stock",
                               [AILabel.TECHNOLOGY, AILabel.LARGE_CAP, AILabel.GROWTH_STOCK], 0.15, "Stock", "Cloud and software leader"),
                    FundHolding("NVDA", "NVIDIA Corporation", "Stock",
                               [AILabel.TECHNOLOGY, AILabel.GROWTH_STOCK, AILabel.HIGH_RISK], 0.15, "Stock", "AI and GPU leader"),
                    FundHolding("TSLA", "Tesla Inc", "Stock",
                               [AILabel.CONSUMER, AILabel.GROWTH_STOCK, AILabel.HIGH_RISK], 0.10, "Stock", "Electric vehicle leader"),
                    FundHolding("AMZN", "Amazon.com Inc", "Stock",
                               [AILabel.CONSUMER, AILabel.GROWTH_STOCK, AILabel.LARGE_CAP], 0.10, "Stock", "E-commerce and cloud"),
                ],
                total_allocation=1.0,
                rebalancing_frequency="Monthly",
                suitability_score=0.0
            ),
            
            # Dividend Portfolio - Income-focused
            FundPortfolio(
                theme=PortfolioTheme.DIVIDEND,
                name="Dividend Portfolio",
                description="Focus on dividend-paying stocks and income-generating assets for regular cash flow.",
                risk_level=4,
                expected_return=6.5,
                expected_volatility=10.0,
                holdings=[
                    FundHolding("VYM", "High Dividend Yield ETF", "ETF",
                               [AILabel.DIVIDEND_STOCK, AILabel.INCOME_FOCUSED, AILabel.VALUE_STOCK], 0.30, "ETF", "High dividend yield"),
                    FundHolding("SCHD", "Dividend Equity ETF", "ETF",
                               [AILabel.DIVIDEND_STOCK, AILabel.INCOME_FOCUSED, AILabel.VALUE_STOCK], 0.25, "ETF", "Quality dividend stocks"),
                    FundHolding("JNJ", "Johnson & Johnson", "Stock",
                               [AILabel.HEALTHCARE, AILabel.DIVIDEND_STOCK, AILabel.BLUE_CHIP], 0.15, "Stock", "Healthcare dividend aristocrat"),
                    FundHolding("KO", "Coca-Cola Company", "Stock",
                               [AILabel.CONSUMER, AILabel.DIVIDEND_STOCK, AILabel.BLUE_CHIP], 0.10, "Stock", "Consumer staples dividend"),
                    FundHolding("PG", "Procter & Gamble", "Stock",
                               [AILabel.CONSUMER, AILabel.DIVIDEND_STOCK, AILabel.BLUE_CHIP], 0.10, "Stock", "Consumer goods dividend"),
                    FundHolding("XLU", "Utilities Sector ETF", "ETF",
                               [AILabel.UTILITIES, AILabel.DIVIDEND_STOCK, AILabel.DEFENSIVE], 0.10, "ETF", "Utilities for income"),
                ],
                total_allocation=1.0,
                rebalancing_frequency="Quarterly",
                suitability_score=0.0
            ),
            
            # ESG Portfolio - Sustainable investing
            FundPortfolio(
                theme=PortfolioTheme.ESG,
                name="ESG Portfolio",
                description="Environmentally and socially responsible investments aligned with sustainability goals.",
                risk_level=5,
                expected_return=9.0,
                expected_volatility=13.0,
                holdings=[
                    FundHolding("ESG", "ESG ETF", "ETF",
                               [AILabel.ESG_COMPLIANT, AILabel.SUSTAINABLE, AILabel.US_MARKET], 0.40, "ETF", "ESG-focused companies"),
                    FundHolding("TSLA", "Tesla Inc", "Stock",
                               [AILabel.ESG_COMPLIANT, AILabel.SUSTAINABLE, AILabel.TECHNOLOGY], 0.20, "Stock", "Electric vehicles"),
                    FundHolding("ENPH", "Enphase Energy", "Stock",
                               [AILabel.ENERGY, AILabel.ESG_COMPLIANT, AILabel.SUSTAINABLE], 0.15, "Stock", "Solar energy"),
                    FundHolding("XLU", "Utilities Sector ETF", "ETF",
                               [AILabel.UTILITIES, AILabel.ESG_COMPLIANT, AILabel.DEFENSIVE], 0.15, "ETF", "Clean utilities"),
                    FundHolding("VEA", "Developed Markets ETF", "ETF",
                               [AILabel.DEVELOPED_MARKET, AILabel.ESG_COMPLIANT], 0.10, "ETF", "International ESG"),
                ],
                total_allocation=1.0,
                rebalancing_frequency="Quarterly",
                suitability_score=0.0
            ),
            
            # REITs Portfolio - Real estate
            FundPortfolio(
                theme=PortfolioTheme.REITS,
                name="REITs Portfolio",
                description="Real Estate Investment Trusts for real estate exposure and income generation.",
                risk_level=5,
                expected_return=7.5,
                expected_volatility=14.0,
                holdings=[
                    FundHolding("VNQ", "Real Estate ETF", "ETF",
                               [AILabel.REAL_ESTATE, AILabel.INCOME_FOCUSED, AILabel.US_MARKET], 0.50, "ETF", "US real estate"),
                    FundHolding("XLRE", "Real Estate Sector ETF", "ETF",
                               [AILabel.REAL_ESTATE, AILabel.INCOME_FOCUSED], 0.30, "ETF", "Real estate sector"),
                    FundHolding("SCHH", "US REIT ETF", "ETF",
                               [AILabel.REAL_ESTATE, AILabel.INCOME_FOCUSED], 0.20, "ETF", "Diversified REITs"),
                ],
                total_allocation=1.0,
                rebalancing_frequency="Quarterly",
                suitability_score=0.0
            ),
            
            # Defensive Portfolio - Safe, stable
            FundPortfolio(
                theme=PortfolioTheme.DEFENSIVE,
                name="Defensive Portfolio",
                description="Low-risk portfolio focused on stability and capital preservation.",
                risk_level=3,
                expected_return=5.5,
                expected_volatility=8.0,
                holdings=[
                    FundHolding("TLT", "20+ Year Treasury Bond ETF", "ETF",
                               [AILabel.LOW_RISK, AILabel.INCOME_FOCUSED], 0.40, "Bond", "Long-term bonds"),
                    FundHolding("XLP", "Consumer Staples ETF", "ETF",
                               [AILabel.CONSUMER, AILabel.DEFENSIVE, AILabel.LOW_RISK], 0.25, "ETF", "Stable consumer goods"),
                    FundHolding("XLU", "Utilities Sector ETF", "ETF",
                               [AILabel.UTILITIES, AILabel.DEFENSIVE, AILabel.DIVIDEND_STOCK], 0.20, "ETF", "Defensive utilities"),
                    FundHolding("XLV", "Healthcare Sector ETF", "ETF",
                               [AILabel.HEALTHCARE, AILabel.DEFENSIVE, AILabel.MEDIUM_RISK], 0.15, "ETF", "Healthcare stability"),
                ],
                total_allocation=1.0,
                rebalancing_frequency="Semi-Annually",
                suitability_score=0.0
            ),
        ]
    
    def recommend_portfolios(self, profile: RiskProfile, max_portfolios: int = 3) -> List[FundPortfolio]:
        """Recommend fund portfolios based on risk profile"""
        # Calculate suitability scores
        for portfolio in self.portfolios:
            portfolio.suitability_score = self._calculate_suitability(portfolio, profile)
        
        # Sort by suitability
        sorted_portfolios = sorted(self.portfolios, key=lambda x: x.suitability_score, reverse=True)
        
        # Filter suitable portfolios (score >= 60)
        suitable = [p for p in sorted_portfolios if p.suitability_score >= 60]
        
        return suitable[:max_portfolios]
    
    def _calculate_suitability(self, portfolio: FundPortfolio, profile: RiskProfile) -> float:
        """Calculate how well a portfolio matches the user's risk profile"""
        score = 100.0
        
        # Risk level matching
        risk_diff = abs(portfolio.risk_level - profile.score / 10)
        score -= risk_diff * 10  # Penalize risk mismatch
        
        # Risk tolerance matching
        if profile.risk_tolerance == RiskTolerance.CONSERVATIVE and portfolio.risk_level > 5:
            score -= 20
        elif profile.risk_tolerance == RiskTolerance.AGGRESSIVE and portfolio.risk_level < 5:
            score -= 20
        elif profile.risk_tolerance == RiskTolerance.VERY_AGGRESSIVE and portfolio.risk_level < 7:
            score -= 30
        
        return max(0, min(100, score))

# Global instance
fund_manager = FundPortfolioManager()


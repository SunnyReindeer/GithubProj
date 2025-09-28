"""
AI Strategy Recommender for Robo Advisor
Matches risk profiles to suitable trading strategies and provides recommendations
"""
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum
import json
from datetime import datetime, timedelta
from risk_assessment_engine import RiskProfile, RiskTolerance, InvestmentHorizon, ExperienceLevel

class StrategyType(Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"
    VERY_AGGRESSIVE = "very_aggressive"

class StrategyCategory(Enum):
    TREND_FOLLOWING = "trend_following"
    MEAN_REVERSION = "mean_reversion"
    MOMENTUM = "momentum"
    ARBITRAGE = "arbitrage"
    SCALPING = "scalping"
    SWING_TRADING = "swing_trading"
    POSITION_TRADING = "position_trading"

@dataclass
class StrategyRecommendation:
    strategy_name: str
    strategy_type: StrategyType
    category: StrategyCategory
    description: str
    risk_level: int  # 1-10 scale
    expected_return: float  # Annual percentage
    max_drawdown: float  # Maximum expected drawdown
    volatility: float  # Expected volatility
    time_horizon: str  # Short/Medium/Long term
    capital_requirement: str  # Low/Medium/High
    complexity: str  # Beginner/Intermediate/Advanced
    suitability_score: float  # 0-100 match with user profile
    parameters: Dict[str, any]
    pros: List[str]
    cons: List[str]
    market_conditions: List[str]  # Best market conditions
    symbols: List[str]  # Recommended trading pairs

@dataclass
class PortfolioRecommendation:
    total_allocation: Dict[str, float]  # Asset allocation
    strategy_allocations: Dict[str, float]  # Strategy allocation
    expected_annual_return: float
    expected_volatility: float
    max_drawdown: float
    sharpe_ratio: float
    rebalancing_frequency: str
    risk_metrics: Dict[str, float]

class StrategyRecommender:
    def __init__(self):
        self.strategies = self._initialize_strategies()
        self.market_conditions = self._initialize_market_conditions()
        self.asset_categories = self._initialize_asset_categories()
        
    def _initialize_strategies(self) -> List[StrategyRecommendation]:
        """Initialize available trading strategies"""
        return [
            # Conservative Strategies
            StrategyRecommendation(
                strategy_name="DCA (Dollar Cost Averaging)",
                strategy_type=StrategyType.CONSERVATIVE,
                category=StrategyCategory.POSITION_TRADING,
                description="Regular purchases of fixed amounts regardless of price, reducing impact of volatility",
                risk_level=2,
                expected_return=8.0,
                max_drawdown=15.0,
                volatility=0.20,
                time_horizon="Long term",
                capital_requirement="Low",
                complexity="Beginner",
                suitability_score=0.0,  # Will be calculated
                parameters={
                    "frequency": "weekly",
                    "amount": 100,
                    "assets": ["BTCUSDT", "ETHUSDT"]
                },
                pros=[
                    "Reduces timing risk",
                    "Simple to implement",
                    "Low emotional stress",
                    "Good for beginners"
                ],
                cons=[
                    "Lower potential returns",
                    "No market timing advantage",
                    "Requires discipline"
                ],
                market_conditions=["Bull market", "Sideways market", "Volatile market"],
                symbols=["BTCUSDT", "ETHUSDT", "BNBUSDT", "AAPL", "MSFT", "GOOGL"]
            ),
            
            StrategyRecommendation(
                strategy_name="Conservative RSI Mean Reversion",
                strategy_type=StrategyType.CONSERVATIVE,
                category=StrategyCategory.MEAN_REVERSION,
                description="Buy when RSI is oversold (30) and sell when overbought (70) with conservative position sizing",
                risk_level=3,
                expected_return=12.0,
                max_drawdown=20.0,
                volatility=0.25,
                time_horizon="Medium term",
                capital_requirement="Medium",
                complexity="Intermediate",
                suitability_score=0.0,
                parameters={
                    "rsi_period": 14,
                    "oversold": 30,
                    "overbought": 70,
                    "position_size": 0.05,
                    "stop_loss": 0.10
                },
                pros=[
                    "Works well in ranging markets",
                    "Clear entry/exit signals",
                    "Risk management built-in"
                ],
                cons=[
                    "Poor performance in strong trends",
                    "Can generate false signals",
                    "Requires market monitoring"
                ],
                market_conditions=["Sideways market", "Ranging market"],
                symbols=["BTCUSDT", "ETHUSDT", "ADAUSDT", "DOTUSDT", "AAPL", "TSLA", "NVDA"]
            ),
            
            # Moderate Strategies
            StrategyRecommendation(
                strategy_name="EMA Crossover Strategy",
                strategy_type=StrategyType.MODERATE,
                category=StrategyCategory.TREND_FOLLOWING,
                description="Buy when fast EMA crosses above slow EMA, sell when it crosses below",
                risk_level=5,
                expected_return=18.0,
                max_drawdown=25.0,
                volatility=0.30,
                time_horizon="Medium term",
                capital_requirement="Medium",
                complexity="Intermediate",
                suitability_score=0.0,
                parameters={
                    "fast_ema": 12,
                    "slow_ema": 26,
                    "position_size": 0.10,
                    "stop_loss": 0.15
                },
                pros=[
                    "Good trend following",
                    "Clear signals",
                    "Works in trending markets"
                ],
                cons=[
                    "Lagging indicator",
                    "Whipsaws in sideways markets",
                    "Late entries/exits"
                ],
                market_conditions=["Bull market", "Bear market", "Strong trends"],
                symbols=["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "SPY", "QQQ", "IWM"]
            ),
            
            StrategyRecommendation(
                strategy_name="Bollinger Bands Mean Reversion",
                strategy_type=StrategyType.MODERATE,
                category=StrategyCategory.MEAN_REVERSION,
                description="Buy when price touches lower band, sell when it touches upper band",
                risk_level=4,
                expected_return=15.0,
                max_drawdown=22.0,
                volatility=0.28,
                time_horizon="Short to medium term",
                capital_requirement="Medium",
                complexity="Intermediate",
                suitability_score=0.0,
                parameters={
                    "period": 20,
                    "std_dev": 2,
                    "position_size": 0.08,
                    "stop_loss": 0.12
                },
                pros=[
                    "Adapts to volatility",
                    "Good risk/reward ratio",
                    "Works in ranging markets"
                ],
                cons=[
                    "Poor in strong trends",
                    "Can break out of bands",
                    "Requires volatility"
                ],
                market_conditions=["Sideways market", "Volatile market"],
                symbols=["BTCUSDT", "ETHUSDT", "XRPUSDT", "ADAUSDT", "EURUSD", "GBPUSD", "USDJPY"]
            ),
            
            # Aggressive Strategies
            StrategyRecommendation(
                strategy_name="MACD Momentum Strategy",
                strategy_type=StrategyType.AGGRESSIVE,
                category=StrategyCategory.MOMENTUM,
                description="Buy when MACD line crosses above signal line, sell when it crosses below",
                risk_level=7,
                expected_return=25.0,
                max_drawdown=35.0,
                volatility=0.40,
                time_horizon="Short to medium term",
                capital_requirement="High",
                complexity="Advanced",
                suitability_score=0.0,
                parameters={
                    "fast": 12,
                    "slow": 26,
                    "signal": 9,
                    "position_size": 0.15,
                    "stop_loss": 0.20
                },
                pros=[
                    "Good momentum capture",
                    "Trend confirmation",
                    "High profit potential"
                ],
                cons=[
                    "High volatility",
                    "False signals possible",
                    "Requires active management"
                ],
                market_conditions=["Bull market", "Strong momentum"],
                symbols=["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "GOLD", "SILVER", "OIL"]
            ),
            
            StrategyRecommendation(
                strategy_name="Multi-Timeframe Analysis",
                strategy_type=StrategyType.AGGRESSIVE,
                category=StrategyCategory.TREND_FOLLOWING,
                description="Combine multiple timeframes for trend confirmation and entry timing",
                risk_level=6,
                expected_return=22.0,
                max_drawdown=30.0,
                volatility=0.35,
                time_horizon="Medium term",
                capital_requirement="High",
                complexity="Advanced",
                suitability_score=0.0,
                parameters={
                    "timeframes": ["1h", "4h", "1d"],
                    "position_size": 0.12,
                    "stop_loss": 0.18
                },
                pros=[
                    "Better trend confirmation",
                    "Reduced false signals",
                    "Higher accuracy"
                ],
                cons=[
                    "Complex analysis",
                    "More time consuming",
                    "Requires experience"
                ],
                market_conditions=["Trending market", "Clear direction"],
                symbols=["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "SPY", "QQQ", "IWM", "EURUSD"]
            ),
            
            # Very Aggressive Strategies
            StrategyRecommendation(
                strategy_name="Scalping Strategy",
                strategy_type=StrategyType.VERY_AGGRESSIVE,
                category=StrategyCategory.SCALPING,
                description="Quick trades based on short-term price movements and order book analysis",
                risk_level=9,
                expected_return=35.0,
                max_drawdown=50.0,
                volatility=0.60,
                time_horizon="Very short term",
                capital_requirement="Very high",
                complexity="Expert",
                suitability_score=0.0,
                parameters={
                    "timeframe": "1m",
                    "position_size": 0.20,
                    "stop_loss": 0.05,
                    "take_profit": 0.03
                },
                pros=[
                    "High profit potential",
                    "Quick results",
                    "Active trading"
                ],
                cons=[
                    "Very high risk",
                    "Requires constant attention",
                    "High transaction costs",
                    "Stressful"
                ],
                market_conditions=["High volatility", "Liquid markets"],
                symbols=["BTCUSDT", "ETHUSDT", "EURUSD", "GBPUSD", "SPY", "QQQ"]
            ),
            
            StrategyRecommendation(
                strategy_name="Leverage Trading Strategy",
                strategy_type=StrategyType.VERY_AGGRESSIVE,
                category=StrategyCategory.MOMENTUM,
                description="Use leverage to amplify returns on strong trend signals",
                risk_level=10,
                expected_return=50.0,
                max_drawdown=80.0,
                volatility=0.80,
                time_horizon="Short term",
                capital_requirement="Very high",
                complexity="Expert",
                suitability_score=0.0,
                parameters={
                    "leverage": 3,
                    "position_size": 0.25,
                    "stop_loss": 0.10,
                    "max_exposure": 0.75
                },
                pros=[
                    "Maximum profit potential",
                    "Capital efficiency",
                    "Quick gains"
                ],
                cons=[
                    "Maximum risk",
                    "Can lose entire capital",
                    "Requires expert knowledge",
                    "High stress"
                ],
                market_conditions=["Strong trends", "High conviction"],
                symbols=["BTCUSDT", "ETHUSDT", "SPY", "QQQ", "EURUSD", "GOLD"]
            )
        ]
    
    def _initialize_market_conditions(self) -> Dict[str, Dict]:
        """Initialize market condition definitions"""
        return {
            "bull_market": {
                "description": "Sustained upward price movement",
                "characteristics": ["Rising prices", "High volume", "Positive sentiment"],
                "best_strategies": ["trend_following", "momentum"]
            },
            "bear_market": {
                "description": "Sustained downward price movement",
                "characteristics": ["Falling prices", "High volatility", "Negative sentiment"],
                "best_strategies": ["mean_reversion", "short_selling"]
            },
            "sideways_market": {
                "description": "Price moving within a range",
                "characteristics": ["Range-bound prices", "Low volatility", "Uncertain direction"],
                "best_strategies": ["mean_reversion", "scalping"]
            },
            "volatile_market": {
                "description": "High price volatility with uncertain direction",
                "characteristics": ["Large price swings", "High volume", "Mixed signals"],
                "best_strategies": ["mean_reversion", "arbitrage"]
            }
        }
    
    def _initialize_asset_categories(self) -> Dict[str, List[str]]:
        """Initialize asset categories for portfolio allocation"""
        return {
            "stable_coins": ["USDT", "USDC", "BUSD"],
            "blue_chip_crypto": ["BTCUSDT", "ETHUSDT", "BNBUSDT"],
            "defi_tokens": ["UNIUSDT", "AAVEUSDT", "COMPUSDT", "SUSHIUSDT"],
            "alt_coins": ["ADAUSDT", "DOTUSDT", "LINKUSDT", "MATICUSDT"],
            "new_tokens": ["SOLUSDT", "AVAXUSDT", "FTMUSDT", "NEARUSDT"]
        }
    
    def calculate_strategy_suitability(self, strategy: StrategyRecommendation, profile: RiskProfile) -> float:
        """Calculate how well a strategy matches the user's risk profile"""
        suitability_score = 0.0
        
        # Risk tolerance matching (40% weight)
        risk_tolerance_scores = {
            RiskTolerance.CONSERVATIVE: 1,
            RiskTolerance.MODERATE: 3,
            RiskTolerance.AGGRESSIVE: 5,
            RiskTolerance.VERY_AGGRESSIVE: 7
        }
        
        user_risk_score = risk_tolerance_scores[profile.risk_tolerance]
        strategy_risk_score = strategy.risk_level
        
        # Calculate risk compatibility (closer scores = higher suitability)
        risk_compatibility = 1.0 - abs(user_risk_score - strategy_risk_score) / 9.0
        suitability_score += risk_compatibility * 0.40
        
        # Experience level matching (25% weight)
        experience_scores = {
            ExperienceLevel.BEGINNER: 1,
            ExperienceLevel.INTERMEDIATE: 2,
            ExperienceLevel.ADVANCED: 3,
            ExperienceLevel.EXPERT: 4
        }
        
        complexity_scores = {
            "Beginner": 1,
            "Intermediate": 2,
            "Advanced": 3,
            "Expert": 4
        }
        
        user_experience = experience_scores[profile.experience_level]
        strategy_complexity = complexity_scores[strategy.complexity]
        
        # Experience compatibility (user should have equal or higher experience)
        if user_experience >= strategy_complexity:
            experience_compatibility = 1.0
        else:
            experience_compatibility = user_experience / strategy_complexity
        
        suitability_score += experience_compatibility * 0.25
        
        # Investment horizon matching (20% weight)
        horizon_scores = {
            InvestmentHorizon.SHORT_TERM: 1,
            InvestmentHorizon.MEDIUM_TERM: 2,
            InvestmentHorizon.LONG_TERM: 3
        }
        
        time_horizon_scores = {
            "Very short term": 1,
            "Short term": 1,
            "Short to medium term": 2,
            "Medium term": 2,
            "Long term": 3
        }
        
        user_horizon = horizon_scores[profile.investment_horizon]
        strategy_horizon = time_horizon_scores[strategy.time_horizon]
        
        # Horizon compatibility (strategy should match or be shorter than user horizon)
        if strategy_horizon <= user_horizon:
            horizon_compatibility = 1.0
        else:
            horizon_compatibility = user_horizon / strategy_horizon
        
        suitability_score += horizon_compatibility * 0.20
        
        # Volatility tolerance matching (15% weight)
        user_volatility_tolerance = profile.volatility_tolerance
        strategy_volatility = strategy.volatility
        
        # Volatility compatibility (user should tolerate strategy volatility)
        if user_volatility_tolerance >= strategy_volatility:
            volatility_compatibility = 1.0
        else:
            volatility_compatibility = user_volatility_tolerance / strategy_volatility
        
        suitability_score += volatility_compatibility * 0.15
        
        return min(100, max(0, suitability_score * 100))
    
    def recommend_strategies(self, profile: RiskProfile, max_strategies: int = 5) -> List[StrategyRecommendation]:
        """Recommend strategies based on risk profile"""
        # Calculate suitability scores for all strategies
        for strategy in self.strategies:
            strategy.suitability_score = self.calculate_strategy_suitability(strategy, profile)
        
        # Sort by suitability score
        sorted_strategies = sorted(self.strategies, key=lambda x: x.suitability_score, reverse=True)
        
        # Filter strategies that meet minimum suitability threshold
        suitable_strategies = [s for s in sorted_strategies if s.suitability_score >= 60]
        
        # Return top recommendations
        return suitable_strategies[:max_strategies]
    
    def create_portfolio_recommendation(self, profile: RiskProfile, strategies: List[StrategyRecommendation]) -> PortfolioRecommendation:
        """Create portfolio recommendation based on risk profile and selected strategies"""
        # Get asset allocation from risk profile
        asset_allocation = profile.recommended_asset_allocation
        
        # Calculate strategy allocations based on suitability scores
        total_suitability = sum(s.suitability_score for s in strategies)
        strategy_allocations = {}
        
        for strategy in strategies:
            allocation = (strategy.suitability_score / total_suitability) * 0.8  # 80% to strategies
            strategy_allocations[strategy.strategy_name] = allocation
        
        # Add cash allocation (20%)
        strategy_allocations["Cash Reserve"] = 0.20
        
        # Calculate expected portfolio metrics
        expected_return = sum(s.expected_return * strategy_allocations.get(s.strategy_name, 0) for s in strategies)
        expected_volatility = sum(s.volatility * strategy_allocations.get(s.strategy_name, 0) for s in strategies)
        max_drawdown = max(s.max_drawdown for s in strategies)  # Conservative estimate
        
        # Calculate Sharpe ratio (assuming 2% risk-free rate)
        sharpe_ratio = (expected_return - 2.0) / expected_volatility if expected_volatility > 0 else 0
        
        # Determine rebalancing frequency based on risk tolerance
        rebalancing_frequency = {
            RiskTolerance.CONSERVATIVE: "Monthly",
            RiskTolerance.MODERATE: "Bi-weekly",
            RiskTolerance.AGGRESSIVE: "Weekly",
            RiskTolerance.VERY_AGGRESSIVE: "Daily"
        }[profile.risk_tolerance]
        
        # Calculate risk metrics
        risk_metrics = {
            "var_95": max_drawdown * 0.8,  # 95% Value at Risk
            "expected_shortfall": max_drawdown * 0.9,  # Expected shortfall
            "max_consecutive_losses": 5 if profile.risk_tolerance in [RiskTolerance.CONSERVATIVE, RiskTolerance.MODERATE] else 3,
            "correlation_threshold": 0.7 if profile.diversification_preference > 0.5 else 0.9
        }
        
        return PortfolioRecommendation(
            total_allocation=asset_allocation,
            strategy_allocations=strategy_allocations,
            expected_annual_return=expected_return,
            expected_volatility=expected_volatility,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe_ratio,
            rebalancing_frequency=rebalancing_frequency,
            risk_metrics=risk_metrics
        )
    
    def get_market_analysis(self) -> Dict[str, any]:
        """Get current market analysis for strategy recommendations"""
        # This would typically connect to market data APIs
        # For now, return mock analysis
        return {
            "current_trend": "Bullish",
            "volatility_level": "Medium",
            "market_phase": "Accumulation",
            "recommended_approach": "Trend following with mean reversion backup",
            "key_levels": {
                "support": 45000,
                "resistance": 50000,
                "current_price": 47500
            },
            "market_sentiment": "Positive",
            "risk_events": ["Fed meeting next week", "Earnings season approaching"]
        }
    
    def generate_trading_plan(self, profile: RiskProfile, strategies: List[StrategyRecommendation]) -> Dict[str, any]:
        """Generate a comprehensive trading plan"""
        portfolio_rec = self.create_portfolio_recommendation(profile, strategies)
        market_analysis = self.get_market_analysis()
        
        return {
            "user_profile": {
                "risk_tolerance": profile.risk_tolerance.value,
                "investment_horizon": profile.investment_horizon.value,
                "experience_level": profile.experience_level.value,
                "risk_score": profile.score
            },
            "recommended_strategies": [
                {
                    "name": s.strategy_name,
                    "suitability_score": s.suitability_score,
                    "allocation": portfolio_rec.strategy_allocations.get(s.strategy_name, 0),
                    "expected_return": s.expected_return,
                    "max_drawdown": s.max_drawdown,
                    "complexity": s.complexity
                }
                for s in strategies
            ],
            "portfolio_allocation": portfolio_rec.total_allocation,
            "expected_performance": {
                "annual_return": portfolio_rec.expected_annual_return,
                "volatility": portfolio_rec.expected_volatility,
                "max_drawdown": portfolio_rec.max_drawdown,
                "sharpe_ratio": portfolio_rec.sharpe_ratio
            },
            "risk_management": {
                "rebalancing_frequency": portfolio_rec.rebalancing_frequency,
                "risk_metrics": portfolio_rec.risk_metrics,
                "risk_factors": profile.risk_factors
            },
            "market_analysis": market_analysis,
            "implementation_plan": {
                "phase_1": "Start with 1-2 strategies",
                "phase_2": "Add more strategies after 1 month",
                "phase_3": "Optimize based on performance",
                "monitoring": "Daily performance review"
            }
        }

# Global strategy recommender instance
strategy_recommender = StrategyRecommender()

"""
Portfolio Optimizer for Robo Advisor
Optimizes portfolio allocation based on risk tolerance, market conditions, and performance metrics
"""
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum
import json
from datetime import datetime, timedelta
from scipy.optimize import minimize
from risk_assessment_engine import RiskProfile, RiskTolerance
from strategy_recommender import StrategyRecommendation, PortfolioRecommendation

class OptimizationMethod(Enum):
    MEAN_VARIANCE = "mean_variance"
    RISK_PARITY = "risk_parity"
    MAXIMUM_SHARPE = "maximum_sharpe"
    MINIMUM_VARIANCE = "minimum_variance"
    EQUAL_WEIGHT = "equal_weight"

@dataclass
class OptimizationResult:
    optimal_weights: Dict[str, float]
    expected_return: float
    expected_volatility: float
    sharpe_ratio: float
    max_drawdown: float
    var_95: float  # 95% Value at Risk
    optimization_method: OptimizationMethod
    constraints_satisfied: bool
    optimization_metrics: Dict[str, float]

@dataclass
class MarketData:
    symbol: str
    price: float
    volatility: float
    expected_return: float
    correlation_matrix: pd.DataFrame
    historical_returns: pd.Series

class PortfolioOptimizer:
    def __init__(self):
        self.risk_free_rate = 0.02  # 2% annual risk-free rate
        self.optimization_methods = {
            OptimizationMethod.MEAN_VARIANCE: self._mean_variance_optimization,
            OptimizationMethod.RISK_PARITY: self._risk_parity_optimization,
            OptimizationMethod.MAXIMUM_SHARPE: self._maximum_sharpe_optimization,
            OptimizationMethod.MINIMUM_VARIANCE: self._minimum_variance_optimization,
            OptimizationMethod.EQUAL_WEIGHT: self._equal_weight_optimization
        }
        
    def _get_market_data(self, symbols: List[str]) -> Dict[str, MarketData]:
        """Get market data for optimization (mock implementation)"""
        # In a real implementation, this would fetch data from APIs
        market_data = {}
        
        # Mock data for demonstration - Multi-asset
        base_volatilities = {
            # Crypto
            "BTCUSDT": 0.35,
            "ETHUSDT": 0.40,
            "BNBUSDT": 0.45,
            "ADAUSDT": 0.50,
            "SOLUSDT": 0.55,
            "XRPUSDT": 0.45,
            "DOTUSDT": 0.50,
            "DOGEUSDT": 0.60,
            "AVAXUSDT": 0.55,
            "MATICUSDT": 0.50,
            # Stocks
            "AAPL": 0.25,
            "MSFT": 0.22,
            "GOOGL": 0.28,
            "TSLA": 0.45,
            "AMZN": 0.30,
            "META": 0.35,
            "NVDA": 0.40,
            "SPY": 0.18,
            "QQQ": 0.20,
            "IWM": 0.25,
            # Forex
            "EURUSD": 0.08,
            "GBPUSD": 0.10,
            "USDJPY": 0.09,
            "USDCHF": 0.08,
            "AUDUSD": 0.12,
            "USDCAD": 0.09,
            "NZDUSD": 0.13,
            # Commodities
            "GOLD": 0.15,
            "SILVER": 0.25,
            "OIL": 0.30,
            "COPPER": 0.20,
            "NATURAL_GAS": 0.40
        }
        
        base_returns = {
            # Crypto
            "BTCUSDT": 0.15,
            "ETHUSDT": 0.18,
            "BNBUSDT": 0.20,
            "ADAUSDT": 0.12,
            "SOLUSDT": 0.25,
            "XRPUSDT": 0.10,
            "DOTUSDT": 0.14,
            "DOGEUSDT": 0.08,
            "AVAXUSDT": 0.22,
            "MATICUSDT": 0.16,
            # Stocks
            "AAPL": 0.12,
            "MSFT": 0.14,
            "GOOGL": 0.16,
            "TSLA": 0.25,
            "AMZN": 0.13,
            "META": 0.18,
            "NVDA": 0.22,
            "SPY": 0.10,
            "QQQ": 0.12,
            "IWM": 0.11,
            # Forex
            "EURUSD": 0.02,
            "GBPUSD": 0.03,
            "USDJPY": 0.02,
            "USDCHF": 0.02,
            "AUDUSD": 0.04,
            "USDCAD": 0.03,
            "NZDUSD": 0.04,
            # Commodities
            "GOLD": 0.06,
            "SILVER": 0.08,
            "OIL": 0.10,
            "COPPER": 0.07,
            "NATURAL_GAS": 0.15
        }
        
        base_prices = {
            # Crypto
            "BTCUSDT": 45000,
            "ETHUSDT": 3000,
            "BNBUSDT": 300,
            "ADAUSDT": 0.5,
            "SOLUSDT": 100,
            "XRPUSDT": 0.6,
            "DOTUSDT": 7,
            "DOGEUSDT": 0.08,
            "AVAXUSDT": 25,
            "MATICUSDT": 0.8,
            # Stocks
            "AAPL": 150,
            "MSFT": 300,
            "GOOGL": 2500,
            "TSLA": 200,
            "AMZN": 3000,
            "META": 250,
            "NVDA": 400,
            "SPY": 400,
            "QQQ": 350,
            "IWM": 200,
            # Forex
            "EURUSD": 1.05,
            "GBPUSD": 1.25,
            "USDJPY": 150,
            "USDCHF": 0.90,
            "AUDUSD": 0.65,
            "USDCAD": 1.35,
            "NZDUSD": 0.60,
            # Commodities
            "GOLD": 2000,
            "SILVER": 25,
            "OIL": 80,
            "COPPER": 4.5,
            "NATURAL_GAS": 3.5
        }
        
        for symbol in symbols:
            # Generate mock correlation matrix
            np.random.seed(42)  # For reproducible results
            n_assets = len(symbols)
            correlation_matrix = np.random.uniform(0.3, 0.8, (n_assets, n_assets))
            correlation_matrix = (correlation_matrix + correlation_matrix.T) / 2
            np.fill_diagonal(correlation_matrix, 1.0)
            
            # Generate mock historical returns
            n_days = 252  # 1 year of trading days
            returns = np.random.normal(
                base_returns.get(symbol, 0.15),
                base_volatilities.get(symbol, 0.40),
                n_days
            )
            
            market_data[symbol] = MarketData(
                symbol=symbol,
                price=base_prices.get(symbol, 100),
                volatility=base_volatilities.get(symbol, 0.40),
                expected_return=base_returns.get(symbol, 0.15),
                correlation_matrix=pd.DataFrame(correlation_matrix, index=symbols, columns=symbols),
                historical_returns=pd.Series(returns)
            )
        
        return market_data
    
    def _mean_variance_optimization(self, market_data: Dict[str, MarketData], 
                                  risk_tolerance: float) -> OptimizationResult:
        """Mean-variance optimization with risk tolerance"""
        symbols = list(market_data.keys())
        n_assets = len(symbols)
        
        # Expected returns
        expected_returns = np.array([market_data[symbol].expected_return for symbol in symbols])
        
        # Covariance matrix
        volatilities = np.array([market_data[symbol].volatility for symbol in symbols])
        correlation_matrix = market_data[symbols[0]].correlation_matrix.values
        covariance_matrix = np.outer(volatilities, volatilities) * correlation_matrix
        
        # Objective function: maximize return - risk_penalty * variance
        def objective(weights):
            portfolio_return = np.dot(weights, expected_returns)
            portfolio_variance = np.dot(weights, np.dot(covariance_matrix, weights))
            return -(portfolio_return - risk_tolerance * portfolio_variance)
        
        # Constraints
        constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]  # Weights sum to 1
        
        # Bounds: no short selling
        bounds = [(0, 1) for _ in range(n_assets)]
        
        # Initial guess
        x0 = np.ones(n_assets) / n_assets
        
        # Optimize
        result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
        
        if result.success:
            optimal_weights = dict(zip(symbols, result.x))
            portfolio_return = np.dot(result.x, expected_returns)
            portfolio_variance = np.dot(result.x, np.dot(covariance_matrix, result.x))
            portfolio_volatility = np.sqrt(portfolio_variance)
            sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility
            
            return OptimizationResult(
                optimal_weights=optimal_weights,
                expected_return=portfolio_return,
                expected_volatility=portfolio_volatility,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=self._estimate_max_drawdown(portfolio_volatility),
                var_95=self._calculate_var_95(portfolio_return, portfolio_volatility),
                optimization_method=OptimizationMethod.MEAN_VARIANCE,
                constraints_satisfied=True,
                optimization_metrics={
                    "objective_value": -result.fun,
                    "iterations": result.nit,
                    "success": result.success
                }
            )
        else:
            # Fallback to equal weights
            return self._equal_weight_optimization(market_data, risk_tolerance)
    
    def _risk_parity_optimization(self, market_data: Dict[str, MarketData], 
                                risk_tolerance: float) -> OptimizationResult:
        """Risk parity optimization - equal risk contribution"""
        symbols = list(market_data.keys())
        n_assets = len(symbols)
        
        # Covariance matrix
        volatilities = np.array([market_data[symbol].volatility for symbol in symbols])
        correlation_matrix = market_data[symbols[0]].correlation_matrix.values
        covariance_matrix = np.outer(volatilities, volatilities) * correlation_matrix
        
        # Objective function: minimize sum of squared differences from equal risk contribution
        def objective(weights):
            portfolio_variance = np.dot(weights, np.dot(covariance_matrix, weights))
            risk_contributions = (weights * np.dot(covariance_matrix, weights)) / portfolio_variance
            target_contribution = 1.0 / n_assets
            return np.sum((risk_contributions - target_contribution) ** 2)
        
        # Constraints
        constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
        bounds = [(0, 1) for _ in range(n_assets)]
        x0 = np.ones(n_assets) / n_assets
        
        result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
        
        if result.success:
            optimal_weights = dict(zip(symbols, result.x))
            expected_returns = np.array([market_data[symbol].expected_return for symbol in symbols])
            portfolio_return = np.dot(result.x, expected_returns)
            portfolio_variance = np.dot(result.x, np.dot(covariance_matrix, result.x))
            portfolio_volatility = np.sqrt(portfolio_variance)
            sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility
            
            return OptimizationResult(
                optimal_weights=optimal_weights,
                expected_return=portfolio_return,
                expected_volatility=portfolio_volatility,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=self._estimate_max_drawdown(portfolio_volatility),
                var_95=self._calculate_var_95(portfolio_return, portfolio_volatility),
                optimization_method=OptimizationMethod.RISK_PARITY,
                constraints_satisfied=True,
                optimization_metrics={
                    "objective_value": result.fun,
                    "iterations": result.nit,
                    "success": result.success
                }
            )
        else:
            return self._equal_weight_optimization(market_data, risk_tolerance)
    
    def _maximum_sharpe_optimization(self, market_data: Dict[str, MarketData], 
                                   risk_tolerance: float) -> OptimizationResult:
        """Maximum Sharpe ratio optimization"""
        symbols = list(market_data.keys())
        n_assets = len(symbols)
        
        expected_returns = np.array([market_data[symbol].expected_return for symbol in symbols])
        volatilities = np.array([market_data[symbol].volatility for symbol in symbols])
        correlation_matrix = market_data[symbols[0]].correlation_matrix.values
        covariance_matrix = np.outer(volatilities, volatilities) * correlation_matrix
        
        # Objective function: minimize negative Sharpe ratio
        def objective(weights):
            portfolio_return = np.dot(weights, expected_returns)
            portfolio_variance = np.dot(weights, np.dot(covariance_matrix, weights))
            portfolio_volatility = np.sqrt(portfolio_variance)
            sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility
            return -sharpe_ratio
        
        constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
        bounds = [(0, 1) for _ in range(n_assets)]
        x0 = np.ones(n_assets) / n_assets
        
        result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
        
        if result.success:
            optimal_weights = dict(zip(symbols, result.x))
            portfolio_return = np.dot(result.x, expected_returns)
            portfolio_variance = np.dot(result.x, np.dot(covariance_matrix, result.x))
            portfolio_volatility = np.sqrt(portfolio_variance)
            sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility
            
            return OptimizationResult(
                optimal_weights=optimal_weights,
                expected_return=portfolio_return,
                expected_volatility=portfolio_volatility,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=self._estimate_max_drawdown(portfolio_volatility),
                var_95=self._calculate_var_95(portfolio_return, portfolio_volatility),
                optimization_method=OptimizationMethod.MAXIMUM_SHARPE,
                constraints_satisfied=True,
                optimization_metrics={
                    "objective_value": -result.fun,
                    "iterations": result.nit,
                    "success": result.success
                }
            )
        else:
            return self._equal_weight_optimization(market_data, risk_tolerance)
    
    def _minimum_variance_optimization(self, market_data: Dict[str, MarketData], 
                                     risk_tolerance: float) -> OptimizationResult:
        """Minimum variance optimization"""
        symbols = list(market_data.keys())
        n_assets = len(symbols)
        
        volatilities = np.array([market_data[symbol].volatility for symbol in symbols])
        correlation_matrix = market_data[symbols[0]].correlation_matrix.values
        covariance_matrix = np.outer(volatilities, volatilities) * correlation_matrix
        
        # Objective function: minimize portfolio variance
        def objective(weights):
            return np.dot(weights, np.dot(covariance_matrix, weights))
        
        constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
        bounds = [(0, 1) for _ in range(n_assets)]
        x0 = np.ones(n_assets) / n_assets
        
        result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
        
        if result.success:
            optimal_weights = dict(zip(symbols, result.x))
            expected_returns = np.array([market_data[symbol].expected_return for symbol in symbols])
            portfolio_return = np.dot(result.x, expected_returns)
            portfolio_variance = np.dot(result.x, np.dot(covariance_matrix, result.x))
            portfolio_volatility = np.sqrt(portfolio_variance)
            sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility
            
            return OptimizationResult(
                optimal_weights=optimal_weights,
                expected_return=portfolio_return,
                expected_volatility=portfolio_volatility,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=self._estimate_max_drawdown(portfolio_volatility),
                var_95=self._calculate_var_95(portfolio_return, portfolio_volatility),
                optimization_method=OptimizationMethod.MINIMUM_VARIANCE,
                constraints_satisfied=True,
                optimization_metrics={
                    "objective_value": result.fun,
                    "iterations": result.nit,
                    "success": result.success
                }
            )
        else:
            return self._equal_weight_optimization(market_data, risk_tolerance)
    
    def _equal_weight_optimization(self, market_data: Dict[str, MarketData], 
                                 risk_tolerance: float) -> OptimizationResult:
        """Equal weight optimization (fallback method)"""
        symbols = list(market_data.keys())
        n_assets = len(symbols)
        equal_weights = {symbol: 1.0 / n_assets for symbol in symbols}
        
        expected_returns = np.array([market_data[symbol].expected_return for symbol in symbols])
        volatilities = np.array([market_data[symbol].volatility for symbol in symbols])
        correlation_matrix = market_data[symbols[0]].correlation_matrix.values
        covariance_matrix = np.outer(volatilities, volatilities) * correlation_matrix
        
        weights_array = np.array([equal_weights[symbol] for symbol in symbols])
        portfolio_return = np.dot(weights_array, expected_returns)
        portfolio_variance = np.dot(weights_array, np.dot(covariance_matrix, weights_array))
        portfolio_volatility = np.sqrt(portfolio_variance)
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility
        
        return OptimizationResult(
            optimal_weights=equal_weights,
            expected_return=portfolio_return,
            expected_volatility=portfolio_volatility,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=self._estimate_max_drawdown(portfolio_volatility),
            var_95=self._calculate_var_95(portfolio_return, portfolio_volatility),
            optimization_method=OptimizationMethod.EQUAL_WEIGHT,
            constraints_satisfied=True,
            optimization_metrics={
                "objective_value": portfolio_variance,
                "iterations": 0,
                "success": True
            }
        )
    
    def _estimate_max_drawdown(self, volatility: float) -> float:
        """Estimate maximum drawdown based on volatility"""
        # Rough approximation: max drawdown ≈ 2 * volatility
        return min(0.8, 2.0 * volatility)
    
    def _calculate_var_95(self, expected_return: float, volatility: float) -> float:
        """Calculate 95% Value at Risk"""
        # VaR = expected_return - 1.645 * volatility (95% confidence)
        return max(0, expected_return - 1.645 * volatility)
    
    def optimize_portfolio(self, symbols: List[str], profile: RiskProfile, 
                          method: OptimizationMethod = None) -> OptimizationResult:
        """Optimize portfolio based on risk profile"""
        # Get market data
        market_data = self._get_market_data(symbols)
        
        # Determine optimization method based on risk tolerance
        if method is None:
            method = self._select_optimization_method(profile)
        
        # Apply risk tolerance scaling
        risk_tolerance = self._calculate_risk_tolerance_parameter(profile)
        
        # Run optimization
        optimizer_func = self.optimization_methods[method]
        result = optimizer_func(market_data, risk_tolerance)
        
        return result
    
    def _select_optimization_method(self, profile: RiskProfile) -> OptimizationMethod:
        """Select optimization method based on risk profile"""
        if profile.risk_tolerance == RiskTolerance.CONSERVATIVE:
            return OptimizationMethod.MINIMUM_VARIANCE
        elif profile.risk_tolerance == RiskTolerance.MODERATE:
            return OptimizationMethod.RISK_PARITY
        elif profile.risk_tolerance == RiskTolerance.AGGRESSIVE:
            return OptimizationMethod.MAXIMUM_SHARPE
        else:  # VERY_AGGRESSIVE
            return OptimizationMethod.MEAN_VARIANCE
    
    def _calculate_risk_tolerance_parameter(self, profile: RiskProfile) -> float:
        """Calculate risk tolerance parameter for optimization"""
        risk_tolerance_map = {
            RiskTolerance.CONSERVATIVE: 0.5,
            RiskTolerance.MODERATE: 1.0,
            RiskTolerance.AGGRESSIVE: 2.0,
            RiskTolerance.VERY_AGGRESSIVE: 3.0
        }
        return risk_tolerance_map[profile.risk_tolerance]
    
    def rebalance_portfolio(self, current_weights: Dict[str, float], 
                          target_weights: Dict[str, float], 
                          current_prices: Dict[str, float],
                          rebalancing_threshold: float = 0.05) -> Dict[str, float]:
        """Calculate rebalancing trades needed"""
        rebalancing_trades = {}
        
        for symbol in target_weights:
            if symbol in current_weights and symbol in current_prices:
                current_weight = current_weights[symbol]
                target_weight = target_weights[symbol]
                weight_diff = target_weight - current_weight
                
                # Only rebalance if difference exceeds threshold
                if abs(weight_diff) > rebalancing_threshold:
                    rebalancing_trades[symbol] = {
                        "current_weight": current_weight,
                        "target_weight": target_weight,
                        "weight_difference": weight_diff,
                        "action": "buy" if weight_diff > 0 else "sell",
                        "priority": abs(weight_diff)  # Higher priority for larger differences
                    }
        
        return rebalancing_trades
    
    def calculate_portfolio_metrics(self, weights: Dict[str, float], 
                                  market_data: Dict[str, MarketData]) -> Dict[str, float]:
        """Calculate comprehensive portfolio metrics"""
        symbols = list(weights.keys())
        weights_array = np.array([weights[symbol] for symbol in symbols])
        
        expected_returns = np.array([market_data[symbol].expected_return for symbol in symbols])
        volatilities = np.array([market_data[symbol].volatility for symbol in symbols])
        correlation_matrix = market_data[symbols[0]].correlation_matrix.values
        covariance_matrix = np.outer(volatilities, volatilities) * correlation_matrix
        
        portfolio_return = np.dot(weights_array, expected_returns)
        portfolio_variance = np.dot(weights_array, np.dot(covariance_matrix, weights_array))
        portfolio_volatility = np.sqrt(portfolio_variance)
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility
        
        # Calculate risk contributions
        risk_contributions = (weights_array * np.dot(covariance_matrix, weights_array)) / portfolio_variance
        
        # Calculate diversification ratio
        weighted_volatility = np.dot(weights_array, volatilities)
        diversification_ratio = weighted_volatility / portfolio_volatility
        
        return {
            "expected_return": portfolio_return,
            "volatility": portfolio_volatility,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": self._estimate_max_drawdown(portfolio_volatility),
            "var_95": self._calculate_var_95(portfolio_return, portfolio_volatility),
            "diversification_ratio": diversification_ratio,
            "risk_contributions": dict(zip(symbols, risk_contributions)),
            "concentration_risk": np.sum(weights_array ** 2)  # Herfindahl index
        }
    
    def generate_optimization_report(self, result: OptimizationResult, 
                                   profile: RiskProfile) -> Dict[str, any]:
        """Generate comprehensive optimization report"""
        return {
            "optimization_summary": {
                "method": result.optimization_method.value,
                "expected_return": f"{result.expected_return:.2%}",
                "volatility": f"{result.expected_volatility:.2%}",
                "sharpe_ratio": f"{result.sharpe_ratio:.2f}",
                "max_drawdown": f"{result.max_drawdown:.2%}",
                "var_95": f"{result.var_95:.2%}"
            },
            "portfolio_allocation": {
                symbol: f"{weight:.1%}"
                for symbol, weight in result.optimal_weights.items()
            },
            "risk_analysis": {
                "risk_tolerance_match": self._assess_risk_match(result, profile),
                "diversification_score": self._calculate_diversification_score(result.optimal_weights),
                "concentration_risk": self._calculate_concentration_risk(result.optimal_weights)
            },
            "recommendations": self._generate_recommendations(result, profile),
            "optimization_details": result.optimization_metrics
        }
    
    def _assess_risk_match(self, result: OptimizationResult, profile: RiskProfile) -> str:
        """Assess how well the optimization matches the risk profile"""
        if result.expected_volatility <= profile.volatility_tolerance:
            return "Excellent match"
        elif result.expected_volatility <= profile.volatility_tolerance * 1.2:
            return "Good match"
        elif result.expected_volatility <= profile.volatility_tolerance * 1.5:
            return "Acceptable match"
        else:
            return "Poor match - consider lower risk strategies"
    
    def _calculate_diversification_score(self, weights: Dict[str, float]) -> float:
        """Calculate diversification score (0-100)"""
        weights_array = np.array(list(weights.values()))
        # Use entropy as diversification measure
        entropy = -np.sum(weights_array * np.log(weights_array + 1e-10))
        max_entropy = np.log(len(weights_array))
        return (entropy / max_entropy) * 100
    
    def _calculate_concentration_risk(self, weights: Dict[str, float]) -> str:
        """Calculate concentration risk level"""
        max_weight = max(weights.values())
        if max_weight > 0.4:
            return "High concentration risk"
        elif max_weight > 0.25:
            return "Medium concentration risk"
        else:
            return "Low concentration risk"
    
    def _generate_recommendations(self, result: OptimizationResult, 
                                profile: RiskProfile) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        # Risk level recommendations
        if result.expected_volatility > profile.volatility_tolerance * 1.2:
            recommendations.append("Consider reducing position sizes to lower portfolio volatility")
        
        # Diversification recommendations
        max_weight = max(result.optimal_weights.values())
        if max_weight > 0.3:
            recommendations.append("Portfolio is concentrated - consider diversifying across more assets")
        
        # Performance recommendations
        if result.sharpe_ratio < 1.0:
            recommendations.append("Sharpe ratio is low - consider reviewing strategy selection")
        
        # Rebalancing recommendations
        recommendations.append(f"Rebalance portfolio {self._get_rebalancing_frequency(profile)}")
        
        return recommendations
    
    def _get_rebalancing_frequency(self, profile: RiskProfile) -> str:
        """Get recommended rebalancing frequency"""
        frequency_map = {
            RiskTolerance.CONSERVATIVE: "monthly",
            RiskTolerance.MODERATE: "bi-weekly",
            RiskTolerance.AGGRESSIVE: "weekly",
            RiskTolerance.VERY_AGGRESSIVE: "daily"
        }
        return frequency_map[profile.risk_tolerance]

# Global portfolio optimizer instance
portfolio_optimizer = PortfolioOptimizer()

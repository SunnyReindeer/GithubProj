"""
Risk Assessment Engine for Robo Advisor
Evaluates user risk preferences and generates risk profiles
"""
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum
import json
from datetime import datetime

class RiskTolerance(Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"
    VERY_AGGRESSIVE = "very_aggressive"

class InvestmentHorizon(Enum):
    SHORT_TERM = "short_term"  # < 1 year
    MEDIUM_TERM = "medium_term"  # 1-5 years
    LONG_TERM = "long_term"  # > 5 years

class ExperienceLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

@dataclass
class RiskProfile:
    risk_tolerance: RiskTolerance
    investment_horizon: InvestmentHorizon
    experience_level: ExperienceLevel
    max_drawdown_tolerance: float  # Maximum acceptable loss percentage
    volatility_tolerance: float  # Acceptable volatility level
    diversification_preference: float  # 0-1 scale
    liquidity_needs: float  # 0-1 scale (0 = can lock funds, 1 = need immediate access)
    score: float  # Overall risk score (0-100)
    recommended_asset_allocation: Dict[str, float]
    risk_factors: List[str]

class RiskAssessmentEngine:
    def __init__(self):
        self.questions = self._initialize_questions()
        self.scoring_weights = self._initialize_scoring_weights()
        self.asset_allocations = self._initialize_asset_allocations()
        
    def _initialize_questions(self) -> List[Dict]:
        """Initialize risk assessment questionnaire"""
        return [
            {
                "id": "investment_goal",
                "question": "What is your primary investment goal?",
                "type": "single_choice",
                "options": [
                    {"text": "Preserve capital with modest growth", "score": 1, "risk": "conservative"},
                    {"text": "Steady growth with some risk", "score": 2, "risk": "moderate"},
                    {"text": "Aggressive growth with higher risk", "score": 3, "risk": "aggressive"},
                    {"text": "Maximum returns regardless of risk", "score": 4, "risk": "very_aggressive"}
                ]
            },
            {
                "id": "investment_horizon",
                "question": "What is your investment time horizon?",
                "type": "single_choice",
                "options": [
                    {"text": "Less than 1 year", "score": 1, "horizon": "short_term"},
                    {"text": "1-3 years", "score": 2, "horizon": "medium_term"},
                    {"text": "3-5 years", "score": 3, "horizon": "medium_term"},
                    {"text": "More than 5 years", "score": 4, "horizon": "long_term"}
                ]
            },
            {
                "id": "loss_tolerance",
                "question": "How would you react to a 20% portfolio decline?",
                "type": "single_choice",
                "options": [
                    {"text": "Sell everything immediately", "score": 1, "tolerance": "low"},
                    {"text": "Sell some positions", "score": 2, "tolerance": "medium"},
                    {"text": "Hold and wait for recovery", "score": 3, "tolerance": "high"},
                    {"text": "Buy more at lower prices", "score": 4, "tolerance": "very_high"}
                ]
            },
            {
                "id": "experience_level",
                "question": "How would you describe your trading experience?",
                "type": "single_choice",
                "options": [
                    {"text": "New to trading", "score": 1, "experience": "beginner"},
                    {"text": "Some experience with basic strategies", "score": 2, "experience": "intermediate"},
                    {"text": "Experienced with advanced strategies", "score": 3, "experience": "advanced"},
                    {"text": "Professional trader", "score": 4, "experience": "expert"}
                ]
            },
            {
                "id": "portfolio_size",
                "question": "What percentage of your total wealth is this investment?",
                "type": "single_choice",
                "options": [
                    {"text": "More than 50%", "score": 1, "size": "large"},
                    {"text": "25-50%", "score": 2, "size": "medium"},
                    {"text": "10-25%", "score": 3, "size": "small"},
                    {"text": "Less than 10%", "score": 4, "size": "very_small"}
                ]
            },
            {
                "id": "volatility_comfort",
                "question": "How comfortable are you with daily price fluctuations?",
                "type": "single_choice",
                "options": [
                    {"text": "Very uncomfortable with any volatility", "score": 1, "volatility": "low"},
                    {"text": "Comfortable with small daily changes", "score": 2, "volatility": "medium"},
                    {"text": "Comfortable with moderate volatility", "score": 3, "volatility": "high"},
                    {"text": "Thrive on high volatility", "score": 4, "volatility": "very_high"}
                ]
            },
            {
                "id": "diversification_preference",
                "question": "How important is portfolio diversification to you?",
                "type": "single_choice",
                "options": [
                    {"text": "Extremely important - spread risk widely", "score": 4, "diversification": "high"},
                    {"text": "Important - some diversification", "score": 3, "diversification": "medium"},
                    {"text": "Somewhat important", "score": 2, "diversification": "low"},
                    {"text": "Not important - focus on best opportunities", "score": 1, "diversification": "very_low"}
                ]
            },
            {
                "id": "liquidity_needs",
                "question": "How quickly might you need to access your funds?",
                "type": "single_choice",
                "options": [
                    {"text": "Immediately - emergency fund", "score": 1, "liquidity": "high"},
                    {"text": "Within a few months", "score": 2, "liquidity": "medium"},
                    {"text": "Within a year", "score": 3, "liquidity": "low"},
                    {"text": "Not for several years", "score": 4, "liquidity": "very_low"}
                ]
            },
            {
                "id": "risk_scenarios",
                "question": "Which scenario best describes your risk preference?",
                "type": "single_choice",
                "options": [
                    {"text": "I prefer guaranteed small returns over uncertain large returns", "score": 1, "scenario": "conservative"},
                    {"text": "I prefer moderate returns with some risk", "score": 2, "scenario": "moderate"},
                    {"text": "I prefer higher returns with higher risk", "score": 3, "scenario": "aggressive"},
                    {"text": "I prefer maximum returns with maximum risk", "score": 4, "scenario": "very_aggressive"}
                ]
            },
            {
                "id": "market_conditions",
                "question": "How do you typically react to market downturns?",
                "type": "single_choice",
                "options": [
                    {"text": "Panic and sell everything", "score": 1, "reaction": "panic"},
                    {"text": "Reduce positions significantly", "score": 2, "reaction": "reduce"},
                    {"text": "Hold current positions", "score": 3, "reaction": "hold"},
                    {"text": "Increase positions (buy the dip)", "score": 4, "reaction": "buy"}
                ]
            }
        ]
    
    def _initialize_scoring_weights(self) -> Dict[str, float]:
        """Initialize weights for different risk factors"""
        return {
            "investment_goal": 0.20,
            "loss_tolerance": 0.15,
            "volatility_comfort": 0.15,
            "risk_scenarios": 0.15,
            "market_conditions": 0.10,
            "portfolio_size": 0.10,
            "experience_level": 0.10,
            "diversification_preference": 0.05
        }
    
    def _initialize_asset_allocations(self) -> Dict[RiskTolerance, Dict[str, float]]:
        """Initialize recommended asset allocations for different risk profiles"""
        return {
            RiskTolerance.CONSERVATIVE: {
                "bonds": 0.35,  # Government and corporate bonds
                "etfs": 0.30,   # Broad market ETFs
                "stocks": 0.20, # Blue chip stocks
                "commodities": 0.10,  # Gold, silver
                "crypto": 0.05  # Bitcoin, stablecoins
            },
            RiskTolerance.MODERATE: {
                "stocks": 0.35, # Diversified stock portfolio
                "etfs": 0.25,   # Market ETFs
                "crypto": 0.20, # Bitcoin, Ethereum
                "commodities": 0.15,  # Gold, silver, oil
                "bonds": 0.05   # Some bond exposure
            },
            RiskTolerance.AGGRESSIVE: {
                "crypto": 0.35, # Bitcoin, Ethereum, altcoins
                "stocks": 0.30, # Growth stocks
                "commodities": 0.20,  # Gold, silver, oil
                "etfs": 0.10,   # Sector ETFs
                "forex": 0.05   # Currency trading
            },
            RiskTolerance.VERY_AGGRESSIVE: {
                "crypto": 0.45, # High allocation to crypto
                "stocks": 0.25, # High-growth stocks
                "commodities": 0.20,  # Volatile commodities
                "forex": 0.10   # Currency speculation
            }
        }
    
    def calculate_risk_score(self, answers: Dict[str, any]) -> float:
        """Calculate overall risk score from questionnaire answers"""
        total_score = 0.0
        total_weight = 0.0
        
        for question_id, answer in answers.items():
            if question_id in self.scoring_weights:
                weight = self.scoring_weights[question_id]
                total_score += answer * weight
                total_weight += weight
        
        # Normalize to 0-100 scale
        if total_weight > 0:
            normalized_score = (total_score / (4 * total_weight)) * 100
            return min(100, max(0, normalized_score))
        
        return 50.0  # Default moderate risk
    
    def determine_risk_tolerance(self, score: float) -> RiskTolerance:
        """Determine risk tolerance level from score"""
        if score <= 25:
            return RiskTolerance.CONSERVATIVE
        elif score <= 50:
            return RiskTolerance.MODERATE
        elif score <= 75:
            return RiskTolerance.AGGRESSIVE
        else:
            return RiskTolerance.VERY_AGGRESSIVE
    
    def determine_investment_horizon(self, answers: Dict[str, any]) -> InvestmentHorizon:
        """Determine investment horizon from answers"""
        horizon_answer = answers.get("investment_horizon", 2)
        if horizon_answer <= 1:
            return InvestmentHorizon.SHORT_TERM
        elif horizon_answer <= 3:
            return InvestmentHorizon.MEDIUM_TERM
        else:
            return InvestmentHorizon.LONG_TERM
    
    def determine_experience_level(self, answers: Dict[str, any]) -> ExperienceLevel:
        """Determine experience level from answers"""
        experience_answer = answers.get("experience_level", 2)
        if experience_answer <= 1:
            return ExperienceLevel.BEGINNER
        elif experience_answer <= 2:
            return ExperienceLevel.INTERMEDIATE
        elif experience_answer <= 3:
            return ExperienceLevel.ADVANCED
        else:
            return ExperienceLevel.EXPERT
    
    def calculate_risk_metrics(self, answers: Dict[str, any], risk_tolerance: RiskTolerance) -> Tuple[float, float, float, float]:
        """Calculate specific risk metrics"""
        # Max drawdown tolerance based on risk tolerance and loss tolerance
        loss_tolerance = answers.get("loss_tolerance", 2)
        base_drawdown = {
            RiskTolerance.CONSERVATIVE: 0.10,
            RiskTolerance.MODERATE: 0.20,
            RiskTolerance.AGGRESSIVE: 0.35,
            RiskTolerance.VERY_AGGRESSIVE: 0.50
        }
        max_drawdown = base_drawdown[risk_tolerance] * (loss_tolerance / 4)
        
        # Volatility tolerance
        volatility_comfort = answers.get("volatility_comfort", 2)
        volatility_tolerance = (volatility_comfort / 4) * 0.5  # 0-0.5 scale
        
        # Diversification preference
        diversification = answers.get("diversification_preference", 2)
        diversification_preference = diversification / 4  # 0-1 scale
        
        # Liquidity needs
        liquidity = answers.get("liquidity_needs", 2)
        liquidity_needs = (5 - liquidity) / 4  # Inverted scale (0-1)
        
        return max_drawdown, volatility_tolerance, diversification_preference, liquidity_needs
    
    def identify_risk_factors(self, answers: Dict[str, any], risk_tolerance: RiskTolerance) -> List[str]:
        """Identify specific risk factors based on answers"""
        risk_factors = []
        
        # Portfolio size risk
        portfolio_size = answers.get("portfolio_size", 2)
        if portfolio_size <= 2:
            risk_factors.append("High portfolio concentration risk")
        
        # Liquidity risk
        liquidity = answers.get("liquidity_needs", 2)
        if liquidity <= 2:
            risk_factors.append("High liquidity needs may limit investment options")
        
        # Experience risk
        experience = answers.get("experience_level", 2)
        if experience <= 2:
            risk_factors.append("Limited trading experience")
        
        # Market reaction risk
        market_reaction = answers.get("market_conditions", 2)
        if market_reaction <= 2:
            risk_factors.append("Tendency to panic sell during downturns")
        
        # Diversification risk
        diversification = answers.get("diversification_preference", 2)
        if diversification <= 2:
            risk_factors.append("Low diversification preference increases concentration risk")
        
        # Risk tolerance specific factors
        if risk_tolerance == RiskTolerance.VERY_AGGRESSIVE:
            risk_factors.append("Very high risk tolerance may lead to significant losses")
        elif risk_tolerance == RiskTolerance.CONSERVATIVE:
            risk_factors.append("Conservative approach may limit growth potential")
        
        return risk_factors
    
    def generate_risk_profile(self, answers: Dict[str, any]) -> RiskProfile:
        """Generate comprehensive risk profile from questionnaire answers"""
        # Calculate risk score
        risk_score = self.calculate_risk_score(answers)
        
        # Determine risk tolerance
        risk_tolerance = self.determine_risk_tolerance(risk_score)
        
        # Determine other profile components
        investment_horizon = self.determine_investment_horizon(answers)
        experience_level = self.determine_experience_level(answers)
        
        # Calculate risk metrics
        max_drawdown, volatility_tolerance, diversification_preference, liquidity_needs = self.calculate_risk_metrics(answers, risk_tolerance)
        
        # Get recommended asset allocation
        recommended_asset_allocation = self.asset_allocations[risk_tolerance]
        
        # Identify risk factors
        risk_factors = self.identify_risk_factors(answers, risk_tolerance)
        
        return RiskProfile(
            risk_tolerance=risk_tolerance,
            investment_horizon=investment_horizon,
            experience_level=experience_level,
            max_drawdown_tolerance=max_drawdown,
            volatility_tolerance=volatility_tolerance,
            diversification_preference=diversification_preference,
            liquidity_needs=liquidity_needs,
            score=risk_score,
            recommended_asset_allocation=recommended_asset_allocation,
            risk_factors=risk_factors
        )
    
    def get_questions(self) -> List[Dict]:
        """Get the risk assessment questionnaire"""
        return self.questions
    
    def save_risk_profile(self, profile: RiskProfile, user_id: str = "default") -> str:
        """Save risk profile to file"""
        filename = f"risk_profile_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        profile_data = {
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "risk_tolerance": profile.risk_tolerance.value,
            "investment_horizon": profile.investment_horizon.value,
            "experience_level": profile.experience_level.value,
            "max_drawdown_tolerance": profile.max_drawdown_tolerance,
            "volatility_tolerance": profile.volatility_tolerance,
            "diversification_preference": profile.diversification_preference,
            "liquidity_needs": profile.liquidity_needs,
            "score": profile.score,
            "recommended_asset_allocation": profile.recommended_asset_allocation,
            "risk_factors": profile.risk_factors
        }
        
        with open(filename, 'w') as f:
            json.dump(profile_data, f, indent=2)
        
        return filename
    
    def load_risk_profile(self, filename: str) -> RiskProfile:
        """Load risk profile from file"""
        with open(filename, 'r') as f:
            profile_data = json.load(f)
        
        return RiskProfile(
            risk_tolerance=RiskTolerance(profile_data["risk_tolerance"]),
            investment_horizon=InvestmentHorizon(profile_data["investment_horizon"]),
            experience_level=ExperienceLevel(profile_data["experience_level"]),
            max_drawdown_tolerance=profile_data["max_drawdown_tolerance"],
            volatility_tolerance=profile_data["volatility_tolerance"],
            diversification_preference=profile_data["diversification_preference"],
            liquidity_needs=profile_data["liquidity_needs"],
            score=profile_data["score"],
            recommended_asset_allocation=profile_data["recommended_asset_allocation"],
            risk_factors=profile_data["risk_factors"]
        )

# Global risk assessment engine instance
risk_engine = RiskAssessmentEngine()

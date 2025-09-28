"""
Demo script for the AI Robo Advisor system
Shows how the risk assessment, strategy recommendation, and portfolio optimization work together
"""
import json
from datetime import datetime
from risk_assessment_engine import risk_engine, RiskProfile
from strategy_recommender import strategy_recommender
from portfolio_optimizer import portfolio_optimizer, OptimizationMethod

def demo_risk_assessment():
    """Demo the risk assessment functionality"""
    print("🎯 Risk Assessment Demo")
    print("=" * 50)
    
    # Sample answers for different risk profiles
    sample_profiles = {
        "Conservative": {
            "investment_goal": 1,
            "investment_horizon": 4,
            "loss_tolerance": 1,
            "experience_level": 1,
            "portfolio_size": 1,
            "volatility_comfort": 1,
            "diversification_preference": 4,
            "liquidity_needs": 2,
            "risk_scenarios": 1,
            "market_conditions": 1
        },
        "Moderate": {
            "investment_goal": 2,
            "investment_horizon": 3,
            "loss_tolerance": 2,
            "experience_level": 2,
            "portfolio_size": 2,
            "volatility_comfort": 2,
            "diversification_preference": 3,
            "liquidity_needs": 2,
            "risk_scenarios": 2,
            "market_conditions": 2
        },
        "Aggressive": {
            "investment_goal": 3,
            "investment_horizon": 2,
            "loss_tolerance": 3,
            "experience_level": 3,
            "portfolio_size": 3,
            "volatility_comfort": 3,
            "diversification_preference": 2,
            "liquidity_needs": 3,
            "risk_scenarios": 3,
            "market_conditions": 3
        },
        "Very Aggressive": {
            "investment_goal": 4,
            "investment_horizon": 1,
            "loss_tolerance": 4,
            "experience_level": 4,
            "portfolio_size": 4,
            "volatility_comfort": 4,
            "diversification_preference": 1,
            "liquidity_needs": 4,
            "risk_scenarios": 4,
            "market_conditions": 4
        }
    }
    
    profiles = {}
    
    for profile_name, answers in sample_profiles.items():
        print(f"\n📊 {profile_name} Profile:")
        profile = risk_engine.generate_risk_profile(answers)
        profiles[profile_name] = profile
        
        print(f"  Risk Score: {profile.score:.0f}/100")
        print(f"  Risk Tolerance: {profile.risk_tolerance.value}")
        print(f"  Investment Horizon: {profile.investment_horizon.value}")
        print(f"  Experience Level: {profile.experience_level.value}")
        print(f"  Max Drawdown Tolerance: {profile.max_drawdown_tolerance:.1%}")
        print(f"  Volatility Tolerance: {profile.volatility_tolerance:.1%}")
        print(f"  Diversification Preference: {profile.diversification_preference:.1%}")
        print(f"  Liquidity Needs: {profile.liquidity_needs:.1%}")
        
        print(f"  Risk Factors: {len(profile.risk_factors)}")
        for factor in profile.risk_factors:
            print(f"    • {factor}")
        
        print(f"  Asset Allocation:")
        for category, percentage in profile.recommended_asset_allocation.items():
            print(f"    • {category}: {percentage:.1%}")
    
    return profiles

def demo_strategy_recommendations(profiles):
    """Demo the strategy recommendation functionality"""
    print("\n\n🤖 Strategy Recommendations Demo")
    print("=" * 50)
    
    for profile_name, profile in profiles.items():
        print(f"\n📈 {profile_name} Profile Recommendations:")
        
        strategies = strategy_recommender.recommend_strategies(profile, max_strategies=3)
        
        for i, strategy in enumerate(strategies, 1):
            print(f"\n  {i}. {strategy.strategy_name}")
            print(f"     Suitability Score: {strategy.suitability_score:.0f}%")
            print(f"     Expected Return: {strategy.expected_return:.1f}%")
            print(f"     Max Drawdown: {strategy.max_drawdown:.1f}%")
            print(f"     Volatility: {strategy.volatility:.1%}")
            print(f"     Complexity: {strategy.complexity}")
            print(f"     Time Horizon: {strategy.time_horizon}")
            print(f"     Category: {strategy.category.value}")
            print(f"     Risk Level: {strategy.risk_level}/10")

def demo_portfolio_optimization(profiles):
    """Demo the portfolio optimization functionality"""
    print("\n\n🎯 Portfolio Optimization Demo")
    print("=" * 50)
    
    # Sample symbols for optimization
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT"]
    
    for profile_name, profile in profiles.items():
        print(f"\n📊 {profile_name} Profile Optimization:")
        
        # Test different optimization methods
        methods = [
            OptimizationMethod.MINIMUM_VARIANCE,
            OptimizationMethod.RISK_PARITY,
            OptimizationMethod.MAXIMUM_SHARPE,
            OptimizationMethod.MEAN_VARIANCE
        ]
        
        for method in methods:
            try:
                result = portfolio_optimizer.optimize_portfolio(symbols, profile, method)
                
                print(f"\n  {method.value.replace('_', ' ').title()}:")
                print(f"    Expected Return: {result.expected_return:.2%}")
                print(f"    Volatility: {result.expected_volatility:.2%}")
                print(f"    Sharpe Ratio: {result.sharpe_ratio:.2f}")
                print(f"    Max Drawdown: {result.max_drawdown:.2%}")
                print(f"    VaR (95%): {result.var_95:.2%}")
                
                # Show top allocations
                sorted_weights = sorted(result.optimal_weights.items(), key=lambda x: x[1], reverse=True)
                print(f"    Top Allocations:")
                for symbol, weight in sorted_weights[:3]:
                    if weight > 0.01:  # Only show weights > 1%
                        print(f"      • {symbol}: {weight:.1%}")
                
            except Exception as e:
                print(f"    Error with {method.value}: {str(e)}")

def demo_trading_plan_generation(profiles):
    """Demo the trading plan generation functionality"""
    print("\n\n📋 Trading Plan Generation Demo")
    print("=" * 50)
    
    for profile_name, profile in profiles.items():
        print(f"\n📋 {profile_name} Profile Trading Plan:")
        
        # Get strategy recommendations
        strategies = strategy_recommender.recommend_strategies(profile, max_strategies=3)
        
        if strategies:
            # Generate trading plan
            trading_plan = strategy_recommender.generate_trading_plan(profile, strategies)
            
            print(f"  User Profile:")
            print(f"    Risk Tolerance: {trading_plan['user_profile']['risk_tolerance']}")
            print(f"    Investment Horizon: {trading_plan['user_profile']['investment_horizon']}")
            print(f"    Experience Level: {trading_plan['user_profile']['experience_level']}")
            print(f"    Risk Score: {trading_plan['user_profile']['risk_score']:.0f}/100")
            
            print(f"  Expected Performance:")
            perf = trading_plan['expected_performance']
            print(f"    Annual Return: {perf['annual_return']:.1f}%")
            print(f"    Volatility: {perf['volatility']:.1f}%")
            print(f"    Max Drawdown: {perf['max_drawdown']:.1f}%")
            print(f"    Sharpe Ratio: {perf['sharpe_ratio']:.2f}")
            
            print(f"  Recommended Strategies:")
            for strategy in trading_plan['recommended_strategies']:
                print(f"    • {strategy['name']}: {strategy['allocation']:.1%} allocation")
            
            print(f"  Risk Management:")
            risk_mgmt = trading_plan['risk_management']
            print(f"    Rebalancing Frequency: {risk_mgmt['rebalancing_frequency']}")
            print(f"    Risk Factors: {len(profile.risk_factors)} identified")
            
            print(f"  Implementation Plan:")
            implementation = trading_plan['implementation_plan']
            for phase, description in implementation.items():
                print(f"    • {phase.replace('_', ' ').title()}: {description}")

def demo_comprehensive_workflow():
    """Demo the complete robo advisor workflow"""
    print("\n\n🚀 Complete Robo Advisor Workflow Demo")
    print("=" * 60)
    
    # Step 1: Risk Assessment
    print("\n1️⃣ Risk Assessment")
    profiles = demo_risk_assessment()
    
    # Step 2: Strategy Recommendations
    print("\n2️⃣ Strategy Recommendations")
    demo_strategy_recommendations(profiles)
    
    # Step 3: Portfolio Optimization
    print("\n3️⃣ Portfolio Optimization")
    demo_portfolio_optimization(profiles)
    
    # Step 4: Trading Plan Generation
    print("\n4️⃣ Trading Plan Generation")
    demo_trading_plan_generation(profiles)
    
    # Step 5: Save Results
    print("\n5️⃣ Save Results")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for profile_name, profile in profiles.items():
        filename = f"demo_profile_{profile_name.lower()}_{timestamp}.json"
        risk_engine.save_risk_profile(profile, f"demo_{profile_name.lower()}")
        print(f"  ✅ {profile_name} profile saved as {filename}")
    
    print(f"\n🎉 Demo completed successfully!")
    print(f"📁 Check the generated JSON files for detailed results")

def main():
    """Main demo function"""
    print("🤖 AI Robo Advisor System Demo")
    print("=" * 60)
    print("This demo showcases the complete robo advisor functionality:")
    print("• Risk assessment and profiling")
    print("• AI-powered strategy recommendations")
    print("• Portfolio optimization")
    print("• Personalized trading plan generation")
    print("=" * 60)
    
    try:
        demo_comprehensive_workflow()
    except Exception as e:
        print(f"❌ Demo failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

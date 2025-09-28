"""
Multi-Asset Trading Platform Demo
Demonstrates the comprehensive multi-asset trading capabilities
"""
import json
from datetime import datetime
from multi_asset_config import multi_asset_config, AssetClass, AssetRegion, AssetSector
from multi_asset_data_provider import multi_asset_data_provider
from multi_asset_portfolio import multi_asset_portfolio, OrderSide, OrderType
from multi_asset_strategies import multi_asset_strategy_manager

def demo_asset_configuration():
    """Demo the multi-asset configuration system"""
    print("🌍 Multi-Asset Configuration Demo")
    print("=" * 60)
    
    # Show supported asset classes
    print("\n📊 Supported Asset Classes:")
    asset_classes = multi_asset_config.get_supported_asset_classes()
    for i, asset_class in enumerate(asset_classes, 1):
        print(f"  {i}. {asset_class.value.replace('_', ' ').title()}")
    
    # Show assets by class
    print("\n📈 Assets by Class:")
    for asset_class in [AssetClass.STOCKS, AssetClass.BONDS, AssetClass.COMMODITIES, AssetClass.CRYPTO]:
        assets = multi_asset_config.get_assets_by_class(asset_class)
        print(f"\n  {asset_class.value.replace('_', ' ').title()} ({len(assets)} assets):")
        for asset in assets[:5]:  # Show first 5
            print(f"    • {asset.symbol} - {asset.name}")
        if len(assets) > 5:
            print(f"    ... and {len(assets) - 5} more")
    
    # Show assets by region
    print("\n🌎 Assets by Region:")
    for region in [AssetRegion.US, AssetRegion.EUROPE, AssetRegion.ASIA]:
        assets = multi_asset_config.get_assets_by_region(region)
        print(f"  {region.value.replace('_', ' ').title()}: {len(assets)} assets")
    
    # Show assets by sector
    print("\n🏭 Assets by Sector:")
    for sector in [AssetSector.TECHNOLOGY, AssetSector.HEALTHCARE, AssetSector.FINANCIAL]:
        assets = multi_asset_config.get_assets_by_sector(sector)
        print(f"  {sector.value.replace('_', ' ').title()}: {len(assets)} assets")
    
    # Show risk-based asset allocation
    print("\n⚖️ Risk-Based Asset Allocations:")
    for risk_profile in ["conservative", "moderate", "aggressive", "very_aggressive"]:
        allocation = multi_asset_config.get_asset_allocation(risk_profile)
        print(f"\n  {risk_profile.title()}:")
        for asset_class, percentage in allocation.items():
            print(f"    • {asset_class.replace('_', ' ').title()}: {percentage:.1%}")

def demo_data_providers():
    """Demo the multi-asset data provider system"""
    print("\n\n📡 Data Provider Demo")
    print("=" * 60)
    
    # Test different asset classes
    test_symbols = {
        "stocks": ["AAPL", "MSFT", "GOOGL"],
        "bonds": ["TLT", "IEF", "SHY"],
        "commodities": ["GLD", "SLV", "USO"],
        "forex": ["EURUSD=X", "GBPUSD=X", "USDJPY=X"],
        "crypto": ["BTC-USD", "ETH-USD", "BNB-USD"],
        "etfs": ["SPY", "QQQ", "VTI"]
    }
    
    for asset_type, symbols in test_symbols.items():
        print(f"\n📊 {asset_type.title()} Data:")
        try:
            prices = multi_asset_data_provider.get_current_prices(symbols)
            for symbol, price_data in prices.items():
                print(f"  {symbol}: ${price_data.price:.2f} ({price_data.change_percent:+.2f}%)")
        except Exception as e:
            print(f"  Error fetching {asset_type} data: {e}")
    
    # Test market overview
    print("\n📈 Market Overview:")
    try:
        overview = multi_asset_data_provider.get_market_overview()
        for asset_class, data in overview.items():
            print(f"  {asset_class.title()}: Avg Change {data['average_change']:.2f}%")
    except Exception as e:
        print(f"  Error fetching market overview: {e}")
    
    # Test asset search
    print("\n🔍 Asset Search Demo:")
    search_queries = ["Apple", "Gold", "Bitcoin", "S&P"]
    for query in search_queries:
        try:
            results = multi_asset_data_provider.search_assets(query)
            print(f"  '{query}': {len(results)} results")
            for result in results[:2]:  # Show first 2 results
                print(f"    • {result['symbol']} - {result['name']} ({result['asset_class']})")
        except Exception as e:
            print(f"  Error searching for '{query}': {e}")

def demo_portfolio_management():
    """Demo the multi-asset portfolio management system"""
    print("\n\n💼 Portfolio Management Demo")
    print("=" * 60)
    
    # Initialize portfolio
    portfolio = multi_asset_portfolio
    portfolio.__init__(100000.0)  # $100,000 initial balance
    
    print(f"Initial Portfolio Balance: ${portfolio.initial_balance:,.2f}")
    
    # Create sample orders
    sample_orders = [
        ("AAPL", OrderSide.BUY, 10),      # Buy 10 Apple shares
        ("TLT", OrderSide.BUY, 50),       # Buy 50 TLT shares
        ("GLD", OrderSide.BUY, 20),       # Buy 20 GLD shares
        ("BTC-USD", OrderSide.BUY, 0.1),  # Buy 0.1 Bitcoin
        ("SPY", OrderSide.BUY, 25),       # Buy 25 SPY shares
    ]
    
    print("\n📝 Creating Sample Orders:")
    for symbol, side, quantity in sample_orders:
        order = portfolio.create_order(
            symbol=symbol,
            side=side,
            order_type=OrderType.MARKET,
            quantity=quantity
        )
        print(f"  Created {side.value} order for {quantity} {symbol}")
    
    # Execute orders
    print("\n⚡ Executing Orders:")
    symbols = [order[0] for order in sample_orders]
    current_prices = multi_asset_data_provider.get_current_prices(symbols)
    
    for order in portfolio.orders:
        if order.status.value == "pending":
            current_price = current_prices.get(order.symbol)
            if current_price:
                success = portfolio.execute_order(order, current_price.price)
                status = "✅ Executed" if success else "❌ Failed"
                print(f"  {order.symbol}: {status}")
            else:
                print(f"  {order.symbol}: ❌ No price data")
    
    # Display portfolio metrics
    print("\n📊 Portfolio Metrics:")
    metrics = portfolio.get_portfolio_metrics(current_prices)
    print(f"  Total Value: ${metrics.total_value:,.2f}")
    print(f"  Total P&L: ${metrics.total_pnl:,.2f}")
    print(f"  P&L %: {metrics.total_pnl_percent:.2f}%")
    print(f"  Positions: {len(portfolio.positions)}")
    
    # Display asset class allocation
    print("\n📈 Asset Class Allocation:")
    for asset_class, percentage in metrics.asset_class_allocation.items():
        print(f"  {asset_class.replace('_', ' ').title()}: {percentage:.1f}%")
    
    # Display positions
    print("\n💼 Current Positions:")
    positions_df = portfolio.get_positions_dataframe(current_prices)
    if not positions_df.empty:
        for _, position in positions_df.iterrows():
            print(f"  {position['Symbol']}: {position['Quantity']:.3f} @ ${position['Average Price']:.2f}")
            print(f"    Market Value: ${position['Market Value']:,.2f}")
            print(f"    Unrealized P&L: ${position['Unrealized PnL']:,.2f} ({position['Unrealized PnL %']:.2f}%)")
    
    # Display trades
    print("\n📋 Recent Trades:")
    trades_df = portfolio.get_trades_dataframe()
    if not trades_df.empty:
        for _, trade in trades_df.iterrows():
            print(f"  {trade['Side'].upper()} {trade['Quantity']:.3f} {trade['Symbol']} @ ${trade['Price']:.2f}")
            print(f"    Fee: ${trade['Fees']:.2f} | Time: {trade['Timestamp']}")

def demo_trading_strategies():
    """Demo the multi-asset trading strategies"""
    print("\n\n🤖 Trading Strategies Demo")
    print("=" * 60)
    
    # Show strategies by asset class
    print("📊 Strategies by Asset Class:")
    for asset_class in [AssetClass.STOCKS, AssetClass.BONDS, AssetClass.COMMODITIES, AssetClass.CRYPTO]:
        strategies = multi_asset_strategy_manager.get_strategies_by_asset_class(asset_class)
        print(f"\n  {asset_class.value.replace('_', ' ').title()} ({len(strategies)} strategies):")
        for strategy in strategies:
            print(f"    • {strategy['name']}")
            print(f"      Category: {strategy['category'].value.replace('_', ' ').title()}")
            print(f"      Risk Level: {strategy['risk_level']}/10")
            print(f"      Complexity: {strategy['complexity']}")
    
    # Show strategies by category
    print("\n📈 Strategies by Category:")
    for category in [StrategyCategory.TREND_FOLLOWING, StrategyCategory.MEAN_REVERSION, StrategyCategory.MOMENTUM]:
        strategies = multi_asset_strategy_manager.get_strategies_by_category(category)
        print(f"\n  {category.value.replace('_', ' ').title()} ({len(strategies)} strategies):")
        for strategy in strategies[:3]:  # Show first 3
            print(f"    • {strategy['name']} - {strategy['asset_classes'][0].value}")
    
    # Show strategies by risk level
    print("\n⚖️ Strategies by Risk Level:")
    for risk_level in [3, 5, 7]:
        strategies = multi_asset_strategy_manager.get_strategies_by_risk_level(risk_level, risk_level)
        print(f"\n  Risk Level {risk_level} ({len(strategies)} strategies):")
        for strategy in strategies[:2]:  # Show first 2
            print(f"    • {strategy['name']} - {strategy['asset_classes'][0].value}")
    
    # Test strategy recommendations
    print("\n🎯 Strategy Recommendations:")
    test_cases = [
        ([AssetClass.STOCKS], 5, "Intermediate"),
        ([AssetClass.BONDS], 3, "Advanced"),
        ([AssetClass.CRYPTO], 8, "Intermediate"),
        ([AssetClass.STOCKS, AssetClass.ETFS], 6, None)
    ]
    
    for asset_classes, risk_level, complexity in test_cases:
        recommendations = multi_asset_strategy_manager.get_strategy_recommendations(
            asset_classes, risk_level, complexity
        )
        print(f"\n  Asset Classes: {[ac.value for ac in asset_classes]}")
        print(f"  Risk Level: {risk_level}, Complexity: {complexity or 'Any'}")
        print(f"  Recommendations ({len(recommendations)}):")
        for rec in recommendations[:3]:  # Show first 3
            print(f"    • {rec['name']} (Risk: {rec['risk_level']}, Complexity: {rec['complexity']})")

def demo_comprehensive_workflow():
    """Demo the complete multi-asset trading workflow"""
    print("\n\n🚀 Complete Multi-Asset Trading Workflow Demo")
    print("=" * 70)
    
    # Step 1: Asset Configuration
    print("\n1️⃣ Asset Configuration")
    demo_asset_configuration()
    
    # Step 2: Data Providers
    print("\n2️⃣ Data Providers")
    demo_data_providers()
    
    # Step 3: Portfolio Management
    print("\n3️⃣ Portfolio Management")
    demo_portfolio_management()
    
    # Step 4: Trading Strategies
    print("\n4️⃣ Trading Strategies")
    demo_trading_strategies()
    
    # Step 5: Save Results
    print("\n5️⃣ Save Results")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save portfolio
    portfolio_filename = f"multi_asset_portfolio_{timestamp}.json"
    multi_asset_portfolio.save_portfolio(portfolio_filename)
    print(f"  ✅ Portfolio saved as {portfolio_filename}")
    
    # Save configuration summary
    config_summary = {
        "timestamp": timestamp,
        "supported_asset_classes": [ac.value for ac in multi_asset_config.get_supported_asset_classes()],
        "total_assets": len(multi_asset_config.assets),
        "data_providers": list(multi_asset_config.data_providers.keys()),
        "trading_strategies": len(multi_asset_strategy_manager.get_all_strategies()),
        "portfolio_balance": multi_asset_portfolio.initial_balance,
        "portfolio_positions": len(multi_asset_portfolio.positions),
        "portfolio_trades": len(multi_asset_portfolio.trades)
    }
    
    config_filename = f"multi_asset_config_summary_{timestamp}.json"
    with open(config_filename, 'w') as f:
        json.dump(config_summary, f, indent=2)
    print(f"  ✅ Configuration summary saved as {config_filename}")
    
    print(f"\n🎉 Multi-Asset Trading Platform Demo completed successfully!")
    print(f"📁 Check the generated JSON files for detailed results")
    print(f"🌍 The platform now supports trading across {len(multi_asset_config.get_supported_asset_classes())} asset classes!")
    print(f"📊 Total assets available: {len(multi_asset_config.assets)}")
    print(f"🤖 Trading strategies available: {len(multi_asset_strategy_manager.get_all_strategies())}")

def main():
    """Main demo function"""
    print("🌍 Multi-Asset Trading Platform Demo")
    print("=" * 70)
    print("This demo showcases the comprehensive multi-asset trading capabilities:")
    print("• Multi-asset configuration and management")
    print("• Real-time data providers for all asset classes")
    print("• Advanced portfolio management with multi-currency support")
    print("• Asset-specific trading strategies")
    print("• Risk management and performance analytics")
    print("=" * 70)
    
    try:
        demo_comprehensive_workflow()
    except Exception as e:
        print(f"❌ Demo failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

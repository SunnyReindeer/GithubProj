"""
Demo script to test the crypto trading simulator components
"""
import time
import pandas as pd
from datetime import datetime
from data_fetcher import data_fetcher
from trading_engine import portfolio, OrderSide, OrderType

def test_data_fetcher():
    """Test the data fetcher functionality"""
    print("🔍 Testing Data Fetcher...")
    
    # Test historical data
    print("📊 Fetching historical data for BTCUSDT...")
    historical_data = data_fetcher.get_historical_data("BTCUSDT", "1h", 10)
    
    if not historical_data.empty:
        print("✅ Historical data fetched successfully!")
        print(f"Data shape: {historical_data.shape}")
        print(f"Latest price: ${historical_data['close'].iloc[-1]:,.2f}")
        print(f"Price range: ${historical_data['low'].min():,.2f} - ${historical_data['high'].max():,.2f}")
    else:
        print("❌ Failed to fetch historical data")
    
    print("\n" + "="*50 + "\n")

def test_trading_engine():
    """Test the trading engine functionality"""
    print("🎯 Testing Trading Engine...")
    
    # Initialize portfolio
    portfolio.__init__(10000)  # Start with $10,000
    
    print(f"💰 Initial balance: ${portfolio.cash_balance:,.2f}")
    
    # Create some test orders
    print("\n📝 Creating test orders...")
    
    # Buy order
    buy_order = portfolio.create_order(
        symbol="BTCUSDT",
        side=OrderSide.BUY,
        order_type=OrderType.MARKET,
        quantity=0.1
    )
    print(f"✅ Created buy order: {buy_order.id}")
    
    # Sell order
    sell_order = portfolio.create_order(
        symbol="ETHUSDT",
        side=OrderSide.SELL,
        order_type=OrderType.MARKET,
        quantity=0.5
    )
    print(f"✅ Created sell order: {sell_order.id}")
    
    # Simulate executing orders with mock prices
    mock_prices = {
        "BTCUSDT": 45000.0,
        "ETHUSDT": 3000.0
    }
    
    print(f"\n💱 Executing orders with mock prices...")
    print(f"BTC Price: ${mock_prices['BTCUSDT']:,.2f}")
    print(f"ETH Price: ${mock_prices['ETHUSDT']:,.2f}")
    
    # Execute buy order
    buy_success = portfolio.execute_order(buy_order, mock_prices["BTCUSDT"])
    if buy_success:
        print("✅ Buy order executed successfully!")
    else:
        print("❌ Buy order failed")
    
    # Execute sell order (should fail - no position)
    sell_success = portfolio.execute_order(sell_order, mock_prices["ETHUSDT"])
    if sell_success:
        print("✅ Sell order executed successfully!")
    else:
        print("❌ Sell order failed (no position to sell)")
    
    # Show portfolio summary
    print(f"\n📊 Portfolio Summary:")
    summary = portfolio.get_portfolio_summary(mock_prices)
    print(f"Total Value: ${summary['total_value']:,.2f}")
    print(f"Cash Balance: ${summary['cash_balance']:,.2f}")
    print(f"Total P&L: ${summary['total_pnl']:,.2f}")
    print(f"P&L Percentage: {summary['pnl_percentage']:.2f}%")
    print(f"Positions: {summary['positions_count']}")
    
    # Show positions
    positions_df = portfolio.get_positions_dataframe(mock_prices)
    if not positions_df.empty:
        print(f"\n💼 Current Positions:")
        print(positions_df.to_string(index=False))
    
    # Show trades
    trades_df = portfolio.get_trades_dataframe()
    if not trades_df.empty:
        print(f"\n📋 Trade History:")
        print(trades_df.to_string(index=False))
    
    print("\n" + "="*50 + "\n")

def test_websocket_connection():
    """Test WebSocket connection (brief test)"""
    print("🌐 Testing WebSocket Connection...")
    
    price_updates = []
    
    def price_callback(price_data):
        price_updates.append(price_data)
        print(f"📈 {price_data['symbol']}: ${price_data['price']:,.2f}")
    
    # Add callback and start WebSocket
    data_fetcher.add_subscriber(price_callback)
    thread = data_fetcher.start_websocket()
    
    print("⏳ Waiting for price updates (10 seconds)...")
    time.sleep(10)
    
    if price_updates:
        print(f"✅ Received {len(price_updates)} price updates!")
        print("🎉 WebSocket connection working!")
    else:
        print("❌ No price updates received")
        print("💡 This might be due to network issues or API limits")
    
    # Clean up
    data_fetcher.stop()
    print("\n" + "="*50 + "\n")

def main():
    """Run all tests"""
    print("🚀 Crypto Trading Simulator - Demo & Test Suite")
    print("=" * 60)
    
    # Test data fetcher
    test_data_fetcher()
    
    # Test trading engine
    test_trading_engine()
    
    # Test WebSocket (optional - comment out if you don't want to wait)
    print("⚠️  WebSocket test will take 10 seconds...")
    user_input = input("Run WebSocket test? (y/n): ").lower().strip()
    if user_input == 'y':
        test_websocket_connection()
    else:
        print("⏭️  Skipping WebSocket test")
    
    print("🎉 Demo completed!")
    print("\n📝 To run the full Streamlit app:")
    print("   streamlit run app.py")

if __name__ == "__main__":
    main()

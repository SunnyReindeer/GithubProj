# Crypto Trading Simulator with AI Robo Advisor 📈🤖

A comprehensive cryptocurrency trading simulation application built with Streamlit, featuring live market data, portfolio management, interactive trading interface, and an AI-powered robo advisor for personalized trading strategies.

## Features

### Core Trading Features
- **Real-time Market Data**: Live cryptocurrency prices via Binance WebSocket API
- **Trading Simulation**: Place buy/sell orders with realistic trading fees
- **Portfolio Management**: Track positions, P&L, and portfolio performance
- **Interactive Charts**: Candlestick charts with historical price data
- **Order Management**: Market and limit orders with order history
- **Performance Analytics**: Real-time portfolio metrics and performance tracking

### AI Robo Advisor Features
- **🎯 Risk Assessment**: Comprehensive questionnaire to evaluate your risk preferences
- **🤖 AI Strategy Recommendations**: Personalized trading strategies based on your risk profile
- **🎯 Portfolio Optimization**: Advanced portfolio optimization using multiple methods
- **📋 Trading Plans**: Complete personalized trading plans with implementation guidance
- **📊 Risk Analysis**: Detailed risk metrics and portfolio analysis
- **💾 Export Functionality**: Download your risk profile and trading plan

## Supported Cryptocurrencies

- Bitcoin (BTC/USDT)
- Ethereum (ETH/USDT)
- Binance Coin (BNB/USDT)
- Cardano (ADA/USDT)
- Solana (SOL/USDT)
- XRP (XRP/USDT)
- Polkadot (DOT/USDT)
- Dogecoin (DOGE/USDT)
- Avalanche (AVAX/USDT)
- Polygon (MATIC/USDT)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd crypto-trading-simulator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

### Starting the App
1. Run `streamlit run app.py` in your terminal
2. The app will open in your browser at `http://localhost:8501`
3. Wait for the WebSocket connection to establish (you'll see "Connecting to market data...")

### Using the AI Robo Advisor
1. Navigate to the "🎯 AI Robo Advisor" tab in the sidebar
2. Complete the risk assessment questionnaire (10 questions)
3. Review your personalized risk profile
4. Get AI-powered strategy recommendations
5. Optimize your portfolio allocation
6. Download your complete trading plan

### Demo the Robo Advisor
Run the demo script to see the robo advisor in action:
```bash
python robo_advisor_demo.py
```

### Trading
1. **Select a Cryptocurrency**: Choose from the dropdown in the sidebar
2. **Place Orders**: 
   - Select Buy/Sell
   - Choose Market or Limit order
   - Enter quantity
   - For limit orders, set your desired price
3. **Monitor Portfolio**: View your positions, P&L, and performance metrics

### Features Overview
- **Real-time Prices**: Live price updates every second
- **Portfolio Tracking**: Monitor your total value, cash balance, and P&L
- **Position Management**: View all open positions with unrealized P&L
- **Trade History**: Complete record of all executed trades
- **Order History**: Track all placed orders and their status
- **Performance Charts**: Visual representation of portfolio performance

## Configuration

Edit `config.py` to customize:
- Initial balance (default: $10,000)
- Trading fees (default: 0.1%)
- Supported cryptocurrencies
- API endpoints

## Technical Details

### Architecture
- **Frontend**: Streamlit for interactive web interface
- **Data Source**: Binance WebSocket API for real-time data
- **Backend**: Python with pandas for data processing
- **Charts**: Plotly for interactive visualizations

### Key Components
- `data_fetcher.py`: WebSocket connection and data management
- `trading_engine.py`: Portfolio and order management system
- `app.py`: Main Streamlit application
- `config.py`: Configuration settings

### AI Robo Advisor Components
- `risk_assessment_engine.py`: Risk profiling and questionnaire system
- `strategy_recommender.py`: AI strategy matching and recommendations
- `portfolio_optimizer.py`: Advanced portfolio optimization algorithms
- `robo_advisor_page.py`: User interface for the robo advisor
- `robo_advisor_demo.py`: Demo script showcasing all features

### Data Flow
1. WebSocket connects to Binance API
2. Real-time price data flows to the trading engine
3. Streamlit UI updates automatically with new data
4. User interactions trigger portfolio updates

## Deployment on Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy the app

### Environment Variables (if needed)
Create a `.env` file for any API keys or configuration:
```
# Add any environment variables here
```

## Troubleshooting

### Common Issues
1. **No price data**: Check internet connection and Binance API status
2. **WebSocket connection failed**: Try refreshing the page
3. **Orders not executing**: Ensure sufficient balance for buy orders or sufficient position for sell orders

### Performance Tips
- The app auto-refreshes every second for real-time updates
- Large portfolios may take longer to load
- Close unused browser tabs to improve performance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes. Please ensure compliance with Binance API terms of service when using real market data.

## Disclaimer

This is a simulation application for educational purposes only. It does not involve real money or actual trading. Always do your own research before making any real investment decisions.

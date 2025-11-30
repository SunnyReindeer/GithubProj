# Multi-Asset Trading Platform with AI Robo Advisor 🌍📈🤖

A comprehensive multi-asset trading simulation application built with Streamlit, featuring live market data, portfolio management, interactive trading interface, and an AI-powered robo advisor for personalized trading strategies across stocks, bonds, commodities, forex, crypto, and other investment assets.

## Features

### Core Trading Features
- **🌍 Multi-Asset Support**: Trade stocks, bonds, commodities, forex, crypto, REITs, ETFs, and indices
- **Real-time Market Data**: Live prices via Yahoo Finance, Binance, and other data providers
- **Trading Simulation**: Place buy/sell orders with realistic trading fees for each asset class
- **Portfolio Management**: Track positions, P&L, and portfolio performance across all asset classes
- **Interactive Charts**: Candlestick charts with historical price data for all assets
- **Order Management**: Market, limit, stop, and stop-limit orders with order history
- **Performance Analytics**: Real-time portfolio metrics and performance tracking
- **Multi-Currency Support**: Handle different currencies and exchange rates

### AI Robo Advisor Features
- **🎯 Risk Assessment**: Comprehensive questionnaire to evaluate your risk preferences
- **💼 Fund Portfolio Recommendations**: Pre-defined fund portfolios (Core, Growth, Dividend, ESG, REITs, Defensive) matched to your risk profile
- **🤖 AI Labeling**: Automatic labeling of investments with sectors, themes, geography, and risk characteristics
- **📊 Portfolio Details**: Real-time price data, allocation charts, and AI label breakdowns
- **📋 Investment Plans**: Complete personalized investment plans with implementation guidance
- **📈 Portfolio Allocation**: Full portfolio allocation and detailed stock allocation breakdown
- **💾 Export Functionality**: Download your risk profile and investment plan

### Market Overview Features
- **🌍 Global Market Indices**: Interactive world map showing market performance by region
- **📊 Market Details**: Real-time data for major indices (S&P 500, NASDAQ, Dow Jones, etc.)
- **🏆 Top Performers & Losers**: Best and worst performing markets and assets
- **📅 Economic Events**: Calendar of upcoming economic events and indicators (90-day view)
- **📰 News**: Real-time financial news with direct article links
- **📈 Market Analysis**: Fear & Greed Index, key market indicators, bond yields, sector performance
- **💼 Overview of Assets**: Real-time data for stocks and cryptocurrencies with sparkline charts

## Supported Assets

### 🌍 Trading Platform Assets
- **📈 Stocks**: Apple, Microsoft, Google, Amazon, Tesla, and 50+ more
- **🏦 Bonds**: Treasury bonds, corporate bonds, high-yield bonds
- **🥇 Commodities**: Gold, silver, oil, natural gas, agriculture
- **💱 Forex**: EUR/USD, GBP/USD, USD/JPY, and major currency pairs
- **₿ Cryptocurrencies**: Bitcoin, Ethereum, Binance Coin, and 10+ more
- **🏢 REITs**: Real estate investment trusts and REIT ETFs
- **📊 ETFs**: S&P 500, NASDAQ, sector ETFs, and index funds
- **📈 Indices**: S&P 500, Dow Jones, NASDAQ, VIX

### 🌎 Market Overview Coverage
- **🇺🇸 US Markets**: S&P 500, NASDAQ, Dow Jones, Russell 2000
- **🇪🇺 European Markets**: FTSE 100, DAX, CAC 40, Euro Stoxx 50
- **🇦🇸 Asian Markets**: Nikkei 225, Hang Seng, Shanghai Composite, Taiwan Weighted
- **🌍 Global Markets**: MSCI World, Emerging Markets, South American indices (Brazil, Argentina, Chile)

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
3. Navigate between pages using the sidebar navigation

### Using the Market Overview
1. Navigate to the "📊 Market Overview" tab in the sidebar
2. View global market indices on an interactive world map
3. Check economic events calendar (90-day view)
4. Read real-time financial news
5. Analyze market sentiment with Fear & Greed Index
6. Review sector performance and key market indicators

### Using the Trading Platform
1. Navigate to the "🌍 Trading Platform" tab in the sidebar
2. Select an asset class (stocks, bonds, commodities, forex, crypto, etc.)
3. Choose specific symbols to trade
4. View real-time market data and charts
5. Place orders with appropriate order types
6. Monitor your multi-asset portfolio performance

### Using the AI Robo Advisor
1. Navigate to the "🎯 AI Robo Advisor" tab in the sidebar
2. Complete the risk assessment questionnaire (10 questions)
3. Review your personalized risk profile and recommended asset allocation
4. Get fund portfolio recommendations (Core, Growth, Dividend, ESG, REITs, Defensive)
5. View detailed portfolio holdings with AI labels and real-time prices
6. Review your personalized investment plan
7. Download your risk profile and investment plan

### Demo the Multi-Asset Platform
Run the demo script to see the multi-asset platform in action:
```bash
python multi_asset_demo.py
```

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
- **Data Sources**: 
  - Yahoo Finance (yfinance) for stocks, ETFs, indices, and market data
  - Fear & Greed Index API for market sentiment
  - Real-time economic events and news
- **Backend**: Python with pandas for data processing
- **Charts**: Plotly for interactive visualizations (maps, charts, sparklines)

### Key Components
- `app.py`: Main Streamlit application with navigation
- `market_overview_page.py`: Market overview, economic events, news, and analysis
- `unified_trading_platform.py`: Multi-asset trading interface
- `robo_advisor_page.py`: AI robo advisor interface
- `data_fetcher.py`: WebSocket connection and data management
- `trading_engine.py`: Portfolio and order management system
- `config.py`: Configuration settings

### AI Robo Advisor Components
- `risk_assessment_engine.py`: Risk profiling and questionnaire system
- `fund_portfolio_manager.py`: Fund-based portfolio management with AI labeling
- `robo_advisor_page.py`: User interface for the robo advisor
- `robo_advisor_demo.py`: Demo script showcasing all features

### Market Overview Components
- `market_overview_page.py`: Market overview, economic events, news, and market analysis

### Trading Platform Components
- `unified_trading_platform.py`: Unified trading interface for all asset classes
- `trading_engine.py`: Portfolio and order management
- `data_fetcher.py`: Real-time data fetching
- `tradingview_widget.py`: TradingView chart integration

### Data Flow
1. Market data fetched from Yahoo Finance (yfinance) for stocks, ETFs, indices
2. Real-time price data flows to trading engine and market overview
3. Streamlit UI updates automatically with new data
4. User interactions trigger portfolio updates and recommendations

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
1. **No price data**: Check internet connection and Yahoo Finance API status
2. **Market data not loading**: Try refreshing the page or check API rate limits
3. **Orders not executing**: Ensure sufficient balance for buy orders or sufficient position for sell orders
4. **Fear & Greed Index showing 0**: This is a fallback value; the system will retry fetching real data

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

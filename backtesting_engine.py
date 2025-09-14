"""
Algorithmic Trading Strategies Backtesting Engine
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

@dataclass
class BacktestResult:
    total_return: float
    annual_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    total_trades: int
    profit_factor: float
    trades: List[Dict]
    equity_curve: pd.DataFrame

class TechnicalIndicators:
    @staticmethod
    def sma(data: pd.Series, period: int) -> pd.Series:
        """Simple Moving Average"""
        return data.rolling(window=period).mean()
    
    @staticmethod
    def ema(data: pd.Series, period: int) -> pd.Series:
        """Exponential Moving Average"""
        return data.ewm(span=period).mean()
    
    @staticmethod
    def rsi(data: pd.Series, period: int = 14) -> pd.Series:
        """Relative Strength Index"""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    @staticmethod
    def macd(data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """MACD Indicator"""
        ema_fast = TechnicalIndicators.ema(data, fast)
        ema_slow = TechnicalIndicators.ema(data, slow)
        macd_line = ema_fast - ema_slow
        signal_line = TechnicalIndicators.ema(macd_line, signal)
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram
    
    @staticmethod
    def bollinger_bands(data: pd.Series, period: int = 20, std_dev: float = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Bollinger Bands"""
        sma = TechnicalIndicators.sma(data, period)
        std = data.rolling(window=period).std()
        upper = sma + (std * std_dev)
        lower = sma - (std * std_dev)
        return upper, sma, lower

class TradingStrategies:
    @staticmethod
    def macd_strategy(data: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """MACD Crossover Strategy"""
        df = data.copy()
        macd_line, signal_line, histogram = TechnicalIndicators.macd(df['close'], fast, slow, signal)
        
        df['macd'] = macd_line
        df['macd_signal'] = signal_line
        df['macd_histogram'] = histogram
        
        # Generate signals
        df['macd_signal_buy'] = (df['macd'] > df['macd_signal']) & (df['macd'].shift(1) <= df['macd_signal'].shift(1))
        df['macd_signal_sell'] = (df['macd'] < df['macd_signal']) & (df['macd'].shift(1) >= df['macd_signal'].shift(1))
        
        return df
    
    @staticmethod
    def rsi_strategy(data: pd.DataFrame, period: int = 14, oversold: float = 30, overbought: float = 70) -> pd.DataFrame:
        """RSI Mean Reversion Strategy"""
        df = data.copy()
        df['rsi'] = TechnicalIndicators.rsi(df['close'], period)
        
        # Generate signals
        df['rsi_signal_buy'] = (df['rsi'] < oversold) & (df['rsi'].shift(1) >= oversold)
        df['rsi_signal_sell'] = (df['rsi'] > overbought) & (df['rsi'].shift(1) <= overbought)
        
        return df
    
    @staticmethod
    def ema_cross_strategy(data: pd.DataFrame, fast: int = 12, slow: int = 26) -> pd.DataFrame:
        """EMA Crossover Strategy"""
        df = data.copy()
        df['ema_fast'] = TechnicalIndicators.ema(df['close'], fast)
        df['ema_slow'] = TechnicalIndicators.ema(df['close'], slow)
        
        # Generate signals
        df['ema_signal_buy'] = (df['ema_fast'] > df['ema_slow']) & (df['ema_fast'].shift(1) <= df['ema_slow'].shift(1))
        df['ema_signal_sell'] = (df['ema_fast'] < df['ema_slow']) & (df['ema_fast'].shift(1) >= df['ema_slow'].shift(1))
        
        return df
    
    @staticmethod
    def bollinger_bands_strategy(data: pd.DataFrame, period: int = 20, std_dev: float = 2) -> pd.DataFrame:
        """Bollinger Bands Mean Reversion Strategy"""
        df = data.copy()
        upper, middle, lower = TechnicalIndicators.bollinger_bands(df['close'], period, std_dev)
        
        df['bb_upper'] = upper
        df['bb_middle'] = middle
        df['bb_lower'] = lower
        
        # Generate signals
        df['bb_signal_buy'] = (df['close'] < df['bb_lower']) & (df['close'].shift(1) >= df['bb_lower'].shift(1))
        df['bb_signal_sell'] = (df['close'] > df['bb_upper']) & (df['close'].shift(1) <= df['bb_upper'].shift(1))
        
        return df
    
    @staticmethod
    def combined_strategy(data: pd.DataFrame) -> pd.DataFrame:
        """Combined Strategy using multiple indicators"""
        df = data.copy()
        
        # Get individual strategy signals
        df = TradingStrategies.macd_strategy(df)
        df = TradingStrategies.rsi_strategy(df)
        df = TradingStrategies.ema_cross_strategy(df)
        df = TradingStrategies.bollinger_bands_strategy(df)
        
        # Combine signals (buy when at least 2 strategies agree)
        buy_signals = df[['macd_signal_buy', 'rsi_signal_buy', 'ema_signal_buy', 'bb_signal_buy']].sum(axis=1)
        sell_signals = df[['macd_signal_sell', 'rsi_signal_sell', 'ema_signal_sell', 'bb_signal_sell']].sum(axis=1)
        
        df['combined_signal_buy'] = buy_signals >= 2
        df['combined_signal_sell'] = sell_signals >= 2
        
        return df

class Backtester:
    def __init__(self, initial_capital: float = 10000, commission: float = 0.001):
        self.initial_capital = initial_capital
        self.commission = commission
    
    def run_backtest(self, data: pd.DataFrame, strategy_name: str, **strategy_params) -> BacktestResult:
        """Run backtest for a given strategy"""
        
        # Apply strategy
        if strategy_name == "MACD":
            df = TradingStrategies.macd_strategy(data, **strategy_params)
            buy_signal = 'macd_signal_buy'
            sell_signal = 'macd_signal_sell'
        elif strategy_name == "RSI":
            df = TradingStrategies.rsi_strategy(data, **strategy_params)
            buy_signal = 'rsi_signal_buy'
            sell_signal = 'rsi_signal_sell'
        elif strategy_name == "EMA Cross":
            df = TradingStrategies.ema_cross_strategy(data, **strategy_params)
            buy_signal = 'ema_signal_buy'
            sell_signal = 'ema_signal_sell'
        elif strategy_name == "Bollinger Bands":
            df = TradingStrategies.bollinger_bands_strategy(data, **strategy_params)
            buy_signal = 'bb_signal_buy'
            sell_signal = 'bb_signal_sell'
        elif strategy_name == "Combined":
            df = TradingStrategies.combined_strategy(data)
            buy_signal = 'combined_signal_buy'
            sell_signal = 'combined_signal_sell'
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")
        
        # Execute trades
        trades = self._execute_trades(df, buy_signal, sell_signal)
        
        # Calculate performance metrics
        result = self._calculate_metrics(trades, df)
        
        return result
    
    def _execute_trades(self, df: pd.DataFrame, buy_signal: str, sell_signal: str) -> List[Dict]:
        """Execute trades based on signals"""
        trades = []
        position = 0  # 0 = no position, 1 = long position
        entry_price = 0
        entry_time = None
        
        for i, row in df.iterrows():
            if position == 0 and row[buy_signal]:
                # Enter long position
                position = 1
                entry_price = row['close']
                entry_time = row['timestamp']
                
            elif position == 1 and row[sell_signal]:
                # Exit long position
                exit_price = row['close']
                exit_time = row['timestamp']
                
                # Calculate trade result
                pnl = (exit_price - entry_price) / entry_price
                commission_cost = self.commission * 2  # Entry + exit
                net_pnl = pnl - commission_cost
                
                trades.append({
                    'entry_time': entry_time,
                    'exit_time': exit_time,
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'pnl': pnl,
                    'net_pnl': net_pnl,
                    'duration': (exit_time - entry_time).total_seconds() / 3600  # hours
                })
                
                position = 0
        
        return trades
    
    def _calculate_metrics(self, trades: List[Dict], df: pd.DataFrame) -> BacktestResult:
        """Calculate performance metrics"""
        if not trades:
            return BacktestResult(
                total_return=0, annual_return=0, sharpe_ratio=0,
                max_drawdown=0, win_rate=0, total_trades=0,
                profit_factor=0, trades=[], equity_curve=pd.DataFrame()
            )
        
        # Calculate equity curve
        equity_curve = self._calculate_equity_curve(trades, df)
        
        # Calculate returns
        total_return = (equity_curve['equity'].iloc[-1] / self.initial_capital) - 1
        
        # Annual return
        days = (df['timestamp'].iloc[-1] - df['timestamp'].iloc[0]).days
        annual_return = (1 + total_return) ** (365 / days) - 1 if days > 0 else 0
        
        # Sharpe ratio
        returns = equity_curve['equity'].pct_change().dropna()
        sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0
        
        # Maximum drawdown
        rolling_max = equity_curve['equity'].expanding().max()
        drawdown = (equity_curve['equity'] - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        
        # Win rate
        winning_trades = [t for t in trades if t['net_pnl'] > 0]
        win_rate = len(winning_trades) / len(trades) if trades else 0
        
        # Profit factor
        gross_profit = sum(t['net_pnl'] for t in trades if t['net_pnl'] > 0)
        gross_loss = abs(sum(t['net_pnl'] for t in trades if t['net_pnl'] < 0))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        return BacktestResult(
            total_return=total_return,
            annual_return=annual_return,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            win_rate=win_rate,
            total_trades=len(trades),
            profit_factor=profit_factor,
            trades=trades,
            equity_curve=equity_curve
        )
    
    def _calculate_equity_curve(self, trades: List[Dict], df: pd.DataFrame) -> pd.DataFrame:
        """Calculate equity curve over time"""
        equity_curve = df[['timestamp', 'close']].copy()
        equity_curve['equity'] = self.initial_capital
        
        current_equity = self.initial_capital
        trade_index = 0
        
        for i, row in equity_curve.iterrows():
            # Check if there are trades that should be executed at this time
            while (trade_index < len(trades) and 
                   trades[trade_index]['exit_time'] <= row['timestamp']):
                trade = trades[trade_index]
                current_equity *= (1 + trade['net_pnl'])
                trade_index += 1
            
            equity_curve.at[i, 'equity'] = current_equity
        
        return equity_curve

def get_sample_data(symbol: str = "BTCUSDT", days: int = 365) -> pd.DataFrame:
    """Get sample data for backtesting"""
    # Generate sample data (in real app, this would fetch from API)
    dates = pd.date_range(start=datetime.now() - timedelta(days=days), 
                         end=datetime.now(), freq='1H')
    
    # Generate realistic price data with trend and volatility
    np.random.seed(42)
    base_price = 45000 if symbol == "BTCUSDT" else 3000
    returns = np.random.normal(0.0001, 0.02, len(dates))  # 0.01% mean return, 2% volatility
    
    prices = [base_price]
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    # Add some trend
    trend = np.linspace(0, 0.1, len(dates))  # 10% upward trend over period
    prices = [p * (1 + t) for p, t in zip(prices, trend)]
    
    # Create OHLC data
    data = []
    for i, (date, price) in enumerate(zip(dates, prices)):
        volatility = 0.01
        high = price * (1 + np.random.uniform(0, volatility))
        low = price * (1 - np.random.uniform(0, volatility))
        open_price = prices[i-1] if i > 0 else price
        close_price = price
        volume = np.random.uniform(1000, 10000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close_price,
            'volume': volume
        })
    
    return pd.DataFrame(data)

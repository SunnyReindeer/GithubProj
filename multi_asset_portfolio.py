"""
Multi-Asset Portfolio Management System
Handles portfolio management for stocks, bonds, commodities, forex, crypto, and other assets
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import json
from dataclasses import dataclass, asdict
from enum import Enum
from multi_asset_config import multi_asset_config, Asset, AssetClass, AssetRegion, AssetSector
from multi_asset_data_provider import multi_asset_data_provider, PriceData

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

class OrderStatus(Enum):
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    PARTIALLY_FILLED = "partially_filled"
    REJECTED = "rejected"

@dataclass
class MultiAssetOrder:
    id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float]
    stop_price: Optional[float]
    status: OrderStatus
    timestamp: datetime
    filled_quantity: float = 0.0
    average_price: float = 0.0
    asset_class: str = ""
    currency: str = "USD"
    fees: float = 0.0

@dataclass
class MultiAssetPosition:
    symbol: str
    quantity: float
    average_price: float
    current_price: float
    unrealized_pnl: float
    realized_pnl: float = 0.0
    asset_class: str = ""
    currency: str = "USD"
    market_value: float = 0.0
    cost_basis: float = 0.0

@dataclass
class MultiAssetTrade:
    id: str
    order_id: str
    symbol: str
    side: OrderSide
    quantity: float
    price: float
    timestamp: datetime
    fees: float
    asset_class: str = ""
    currency: str = "USD"

@dataclass
class PortfolioMetrics:
    total_value: float
    total_cost_basis: float
    total_pnl: float
    total_pnl_percent: float
    daily_pnl: float
    daily_pnl_percent: float
    asset_class_allocation: Dict[str, float]
    region_allocation: Dict[str, float]
    sector_allocation: Dict[str, float]
    risk_metrics: Dict[str, float]
    performance_metrics: Dict[str, float]

class MultiAssetPortfolio:
    def __init__(self, initial_balance: float = 100000.0, base_currency: str = "USD"):
        self.initial_balance = initial_balance
        self.base_currency = base_currency
        self.cash_balances = {base_currency: initial_balance}  # Support multiple currencies
        self.positions: Dict[str, MultiAssetPosition] = {}
        self.orders: List[MultiAssetOrder] = []
        self.trades: List[MultiAssetTrade] = []
        self.order_counter = 0
        self.trade_counter = 0
        self.trading_fees = {
            "stocks": 0.001,      # 0.1%
            "bonds": 0.0005,      # 0.05%
            "commodities": 0.001, # 0.1%
            "forex": 0.0001,      # 0.01%
            "crypto": 0.001,      # 0.1%
            "reits": 0.001,       # 0.1%
            "etfs": 0.0005,       # 0.05%
            "indices": 0.0001,    # 0.01%
            "default": 0.001      # 0.1%
        }
        
    def get_asset_info(self, symbol: str) -> Optional[Asset]:
        """Get asset information from configuration"""
        return multi_asset_config.get_asset(symbol)
    
    def get_trading_fee(self, symbol: str) -> float:
        """Get trading fee for a specific symbol"""
        asset = self.get_asset_info(symbol)
        if asset:
            return self.trading_fees.get(asset.asset_class.value, self.trading_fees["default"])
        return self.trading_fees["default"]
    
    def get_current_prices(self, symbols: List[str]) -> Dict[str, PriceData]:
        """Get current prices for symbols"""
        return multi_asset_data_provider.get_current_prices(symbols)
    
    def create_order(self, symbol: str, side: OrderSide, order_type: OrderType, 
                    quantity: float, price: Optional[float] = None, 
                    stop_price: Optional[float] = None) -> MultiAssetOrder:
        """Create a new order"""
        self.order_counter += 1
        
        # Get asset information
        asset = self.get_asset_info(symbol)
        asset_class = asset.asset_class.value if asset else "unknown"
        currency = asset.currency if asset else "USD"
        
        order = MultiAssetOrder(
            id=f"order_{self.order_counter}",
            symbol=symbol.upper(),
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price,
            status=OrderStatus.PENDING,
            timestamp=datetime.now(),
            asset_class=asset_class,
            currency=currency
        )
        
        self.orders.append(order)
        return order
    
    def execute_order(self, order: MultiAssetOrder, current_price: float) -> bool:
        """Execute an order at current market price"""
        if order.status != OrderStatus.PENDING:
            return False
        
        symbol = order.symbol
        asset = self.get_asset_info(symbol)
        
        if not asset:
            order.status = OrderStatus.REJECTED
            return False
        
        # Get trading fee
        fee_rate = self.get_trading_fee(symbol)
        
        if order.side == OrderSide.BUY:
            # Calculate total cost including fees
            total_cost = order.quantity * current_price
            fees = total_cost * fee_rate
            total_required = total_cost + fees
            
            # Check if we have enough cash in the required currency
            if self.cash_balances.get(asset.currency, 0) >= total_required:
                # Execute buy order
                self.cash_balances[asset.currency] -= total_required
                
                # Update or create position
                if symbol in self.positions:
                    position = self.positions[symbol]
                    total_quantity = position.quantity + order.quantity
                    total_cost_basis = (position.average_price * position.quantity) + total_cost
                    position.average_price = total_cost_basis / total_quantity
                    position.quantity = total_quantity
                    position.cost_basis = total_cost_basis
                else:
                    self.positions[symbol] = MultiAssetPosition(
                        symbol=symbol,
                        quantity=order.quantity,
                        average_price=current_price,
                        current_price=current_price,
                        unrealized_pnl=0.0,
                        asset_class=asset.asset_class.value,
                        currency=asset.currency,
                        cost_basis=total_cost
                    )
                
                # Create trade record
                self.trade_counter += 1
                trade = MultiAssetTrade(
                    id=f"trade_{self.trade_counter}",
                    order_id=order.id,
                    symbol=symbol,
                    side=order.side,
                    quantity=order.quantity,
                    price=current_price,
                    timestamp=datetime.now(),
                    fees=fees,
                    asset_class=asset.asset_class.value,
                    currency=asset.currency
                )
                self.trades.append(trade)
                
                # Update order
                order.status = OrderStatus.FILLED
                order.filled_quantity = order.quantity
                order.average_price = current_price
                order.fees = fees
                
                return True
            else:
                order.status = OrderStatus.REJECTED
                return False
                
        elif order.side == OrderSide.SELL:
            if symbol in self.positions and self.positions[symbol].quantity >= order.quantity:
                # Execute sell order
                position = self.positions[symbol]
                
                # Calculate proceeds and fees
                proceeds = order.quantity * current_price
                fees = proceeds * fee_rate
                net_proceeds = proceeds - fees
                
                self.cash_balances[asset.currency] += net_proceeds
                
                # Calculate realized P&L
                cost_basis = (order.quantity / position.quantity) * position.cost_basis
                realized_pnl = proceeds - cost_basis - fees
                position.realized_pnl += realized_pnl
                
                # Update position
                position.quantity -= order.quantity
                position.cost_basis -= cost_basis
                if position.quantity == 0:
                    del self.positions[symbol]
                
                # Create trade record
                self.trade_counter += 1
                trade = MultiAssetTrade(
                    id=f"trade_{self.trade_counter}",
                    order_id=order.id,
                    symbol=symbol,
                    side=order.side,
                    quantity=order.quantity,
                    price=current_price,
                    timestamp=datetime.now(),
                    fees=fees,
                    asset_class=asset.asset_class.value,
                    currency=asset.currency
                )
                self.trades.append(trade)
                
                # Update order
                order.status = OrderStatus.FILLED
                order.filled_quantity = order.quantity
                order.average_price = current_price
                order.fees = fees
                
                return True
            else:
                order.status = OrderStatus.REJECTED
                return False
        
        return False
    
    def get_total_value(self, current_prices: Dict[str, PriceData]) -> float:
        """Calculate total portfolio value in base currency"""
        total_value = 0.0
        
        # Add cash balances (convert to base currency)
        for currency, balance in self.cash_balances.items():
            if currency == self.base_currency:
                total_value += balance
            else:
                # Convert to base currency (simplified - would need real exchange rates)
                total_value += balance * 1.0  # Assume 1:1 for demo
        
        # Add position values
        for symbol, position in self.positions.items():
            if symbol in current_prices:
                price_data = current_prices[symbol]
                position.current_price = price_data.price
                position.market_value = position.quantity * price_data.price
                position.unrealized_pnl = position.market_value - position.cost_basis
                
                # Convert to base currency if needed
                if position.currency == self.base_currency:
                    total_value += position.market_value
                else:
                    total_value += position.market_value * 1.0  # Assume 1:1 for demo
        
        return total_value
    
    def get_total_cost_basis(self) -> float:
        """Calculate total cost basis (initial investment)"""
        # Cost basis is the initial balance - this is what we started with
        # When we buy positions, cash decreases but cost basis stays the same
        # P&L = Current Value - Initial Balance
        return self.initial_balance
    
    def get_portfolio_metrics(self, current_prices: Dict[str, PriceData]) -> PortfolioMetrics:
        """Calculate comprehensive portfolio metrics"""
        total_value = self.get_total_value(current_prices)
        # P&L = Current Total Value - Initial Balance
        # This way, when you buy at market price, P&L = 0 initially
        # P&L only changes when prices move
        total_pnl = total_value - self.initial_balance
        total_pnl_percent = (total_pnl / self.initial_balance) * 100 if self.initial_balance > 0 else 0
        
        # Calculate asset class allocation
        asset_class_allocation = {}
        region_allocation = {}
        sector_allocation = {}
        
        for symbol, position in self.positions.items():
            if symbol in current_prices:
                asset = self.get_asset_info(symbol)
                if asset:
                    # Asset class allocation
                    asset_class = asset.asset_class.value
                    if asset_class not in asset_class_allocation:
                        asset_class_allocation[asset_class] = 0
                    asset_class_allocation[asset_class] += position.market_value
                    
                    # Region allocation
                    region = asset.region.value
                    if region not in region_allocation:
                        region_allocation[region] = 0
                    region_allocation[region] += position.market_value
                    
                    # Sector allocation
                    if asset.sector:
                        sector = asset.sector.value
                        if sector not in sector_allocation:
                            sector_allocation[sector] = 0
                        sector_allocation[sector] += position.market_value
        
        # Convert to percentages
        for allocation in [asset_class_allocation, region_allocation, sector_allocation]:
            total_allocation = sum(allocation.values())
            if total_allocation > 0:
                for key in allocation:
                    allocation[key] = (allocation[key] / total_allocation) * 100
        
        # Calculate risk metrics
        risk_metrics = self._calculate_risk_metrics(current_prices)
        
        # Calculate performance metrics
        performance_metrics = self._calculate_performance_metrics()
        
        return PortfolioMetrics(
            total_value=total_value,
            total_cost_basis=total_cost_basis,
            total_pnl=total_pnl,
            total_pnl_percent=total_pnl_percent,
            daily_pnl=0.0,  # Would need historical data
            daily_pnl_percent=0.0,
            asset_class_allocation=asset_class_allocation,
            region_allocation=region_allocation,
            sector_allocation=sector_allocation,
            risk_metrics=risk_metrics,
            performance_metrics=performance_metrics
        )
    
    def _calculate_risk_metrics(self, current_prices: Dict[str, PriceData]) -> Dict[str, float]:
        """Calculate portfolio risk metrics"""
        if not self.positions:
            return {"portfolio_volatility": 0.0, "max_drawdown": 0.0, "var_95": 0.0}
        
        # Get position weights
        total_value = self.get_total_value(current_prices)
        weights = {}
        volatilities = {}
        
        for symbol, position in self.positions.items():
            if symbol in current_prices and total_value > 0:
                weight = position.market_value / total_value
                weights[symbol] = weight
                
                # Get asset volatility (simplified)
                asset = self.get_asset_info(symbol)
                if asset:
                    volatility_map = {"low": 0.15, "medium": 0.25, "high": 0.40, "very_high": 0.60}
                    volatilities[symbol] = volatility_map.get(asset.volatility_level, 0.25)
        
        # Calculate portfolio volatility (simplified)
        portfolio_variance = 0.0
        for symbol, weight in weights.items():
            portfolio_variance += (weight ** 2) * (volatilities.get(symbol, 0.25) ** 2)
        
        portfolio_volatility = np.sqrt(portfolio_variance)
        
        # Estimate max drawdown (simplified)
        max_drawdown = portfolio_volatility * 2.0
        
        # Calculate VaR (95%)
        var_95 = portfolio_volatility * 1.645
        
        return {
            "portfolio_volatility": portfolio_volatility,
            "max_drawdown": max_drawdown,
            "var_95": var_95,
            "concentration_risk": max(weights.values()) if weights else 0.0
        }
    
    def _calculate_performance_metrics(self) -> Dict[str, float]:
        """Calculate portfolio performance metrics"""
        if not self.trades:
            return {"total_trades": 0, "win_rate": 0.0, "avg_trade_return": 0.0}
        
        # Calculate trade returns
        trade_returns = []
        winning_trades = 0
        
        for trade in self.trades:
            # This is simplified - would need to track entry/exit pairs
            if trade.side == OrderSide.SELL:
                # Find corresponding buy trade
                buy_trades = [t for t in self.trades if t.symbol == trade.symbol and t.side == OrderSide.BUY]
                if buy_trades:
                    avg_buy_price = sum(t.price for t in buy_trades) / len(buy_trades)
                    trade_return = (trade.price - avg_buy_price) / avg_buy_price
                    trade_returns.append(trade_return)
                    if trade_return > 0:
                        winning_trades += 1
        
        total_trades = len(trade_returns)
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        avg_trade_return = np.mean(trade_returns) * 100 if trade_returns else 0
        
        return {
            "total_trades": total_trades,
            "win_rate": win_rate,
            "avg_trade_return": avg_trade_return,
            "total_fees": sum(trade.fees for trade in self.trades)
        }
    
    def get_positions_dataframe(self, current_prices: Dict[str, PriceData]) -> pd.DataFrame:
        """Get positions as DataFrame"""
        if not self.positions:
            return pd.DataFrame()
        
        data = []
        for symbol, position in self.positions.items():
            if symbol in current_prices:
                price_data = current_prices[symbol]
                position.current_price = price_data.price
                position.market_value = position.quantity * price_data.price
                position.unrealized_pnl = position.market_value - position.cost_basis
                
                asset = self.get_asset_info(symbol)
                
                data.append({
                    'Symbol': symbol,
                    'Name': asset.name if asset else symbol,
                    'Asset Class': asset.asset_class.value if asset else 'Unknown',
                    'Quantity': position.quantity,
                    'Average Price': position.average_price,
                    'Current Price': position.current_price,
                    'Market Value': position.market_value,
                    'Unrealized PnL': position.unrealized_pnl,
                    'Unrealized PnL %': (position.unrealized_pnl / position.cost_basis) * 100 if position.cost_basis > 0 else 0,
                    'Realized PnL': position.realized_pnl,
                    'Currency': position.currency
                })
        
        return pd.DataFrame(data)
    
    def get_trades_dataframe(self) -> pd.DataFrame:
        """Get trades as DataFrame"""
        if not self.trades:
            return pd.DataFrame()
        
        data = []
        for trade in self.trades:
            asset = self.get_asset_info(trade.symbol)
            data.append({
                'ID': trade.id,
                'Symbol': trade.symbol,
                'Name': asset.name if asset else trade.symbol,
                'Asset Class': trade.asset_class,
                'Side': trade.side.value,
                'Quantity': trade.quantity,
                'Price': trade.price,
                'Fees': trade.fees,
                'Currency': trade.currency,
                'Timestamp': trade.timestamp
            })
        
        return pd.DataFrame(data)
    
    def get_orders_dataframe(self) -> pd.DataFrame:
        """Get orders as DataFrame"""
        if not self.orders:
            return pd.DataFrame()
        
        data = []
        for order in self.orders:
            asset = self.get_asset_info(order.symbol)
            data.append({
                'ID': order.id,
                'Symbol': order.symbol,
                'Name': asset.name if asset else order.symbol,
                'Asset Class': order.asset_class,
                'Side': order.side.value,
                'Type': order.order_type.value,
                'Quantity': order.quantity,
                'Price': order.price,
                'Status': order.status.value,
                'Filled': order.filled_quantity,
                'Fees': order.fees,
                'Currency': order.currency,
                'Timestamp': order.timestamp
            })
        
        return pd.DataFrame(data)
    
    def save_portfolio(self, filename: str):
        """Save portfolio state to file"""
        portfolio_data = {
            'initial_balance': self.initial_balance,
            'base_currency': self.base_currency,
            'cash_balances': self.cash_balances,
            'positions': {symbol: asdict(pos) for symbol, pos in self.positions.items()},
            'orders': [asdict(order) for order in self.orders],
            'trades': [asdict(trade) for trade in self.trades],
            'order_counter': self.order_counter,
            'trade_counter': self.trade_counter
        }
        
        with open(filename, 'w') as f:
            json.dump(portfolio_data, f, indent=2, default=str)
    
    def load_portfolio(self, filename: str):
        """Load portfolio state from file"""
        try:
            with open(filename, 'r') as f:
                portfolio_data = json.load(f)
            
            self.initial_balance = portfolio_data['initial_balance']
            self.base_currency = portfolio_data['base_currency']
            self.cash_balances = portfolio_data['cash_balances']
            self.order_counter = portfolio_data['order_counter']
            self.trade_counter = portfolio_data['trade_counter']
            
            # Load positions
            self.positions = {}
            for symbol, pos_data in portfolio_data['positions'].items():
                self.positions[symbol] = MultiAssetPosition(**pos_data)
            
            # Load orders
            self.orders = []
            for order_data in portfolio_data['orders']:
                order_data['side'] = OrderSide(order_data['side'])
                order_data['order_type'] = OrderType(order_data['order_type'])
                order_data['status'] = OrderStatus(order_data['status'])
                order_data['timestamp'] = datetime.fromisoformat(order_data['timestamp'])
                self.orders.append(MultiAssetOrder(**order_data))
            
            # Load trades
            self.trades = []
            for trade_data in portfolio_data['trades']:
                trade_data['side'] = OrderSide(trade_data['side'])
                trade_data['timestamp'] = datetime.fromisoformat(trade_data['timestamp'])
                self.trades.append(MultiAssetTrade(**trade_data))
                
        except Exception as e:
            print(f"Error loading portfolio: {e}")

# Global multi-asset portfolio instance
multi_asset_portfolio = MultiAssetPortfolio()

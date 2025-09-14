"""
Trading simulation engine with portfolio management
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
from dataclasses import dataclass, asdict
from enum import Enum

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

class OrderStatus(Enum):
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    PARTIALLY_FILLED = "partially_filled"

@dataclass
class Order:
    id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float]
    status: OrderStatus
    timestamp: datetime
    filled_quantity: float = 0.0
    average_price: float = 0.0

@dataclass
class Position:
    symbol: str
    quantity: float
    average_price: float
    current_price: float
    unrealized_pnl: float
    realized_pnl: float = 0.0

@dataclass
class Trade:
    id: str
    order_id: str
    symbol: str
    side: OrderSide
    quantity: float
    price: float
    timestamp: datetime
    fee: float

class Portfolio:
    def __init__(self, initial_balance: float = 10000.0):
        self.initial_balance = initial_balance
        self.cash_balance = initial_balance
        self.positions: Dict[str, Position] = {}
        self.orders: List[Order] = []
        self.trades: List[Trade] = []
        self.order_counter = 0
        self.trade_counter = 0
        self.trading_fee = 0.001  # 0.1%
        
    def get_total_value(self, current_prices: Dict[str, float]) -> float:
        """Calculate total portfolio value"""
        total_value = self.cash_balance
        
        for symbol, position in self.positions.items():
            if symbol in current_prices:
                position.current_price = current_prices[symbol]
                position.unrealized_pnl = (position.current_price - position.average_price) * position.quantity
                total_value += position.quantity * position.current_price
        
        return total_value
    
    def get_total_pnl(self, current_prices: Dict[str, float]) -> float:
        """Calculate total profit/loss"""
        total_value = self.get_total_value(current_prices)
        return total_value - self.initial_balance
    
    def get_portfolio_summary(self, current_prices: Dict[str, float]) -> Dict:
        """Get portfolio summary"""
        total_value = self.get_total_value(current_prices)
        total_pnl = self.get_total_pnl(current_prices)
        
        return {
            'total_value': total_value,
            'cash_balance': self.cash_balance,
            'total_pnl': total_pnl,
            'pnl_percentage': (total_pnl / self.initial_balance) * 100,
            'positions_count': len(self.positions),
            'active_orders': len([o for o in self.orders if o.status == OrderStatus.PENDING])
        }
    
    def create_order(self, symbol: str, side: OrderSide, order_type: OrderType, 
                    quantity: float, price: Optional[float] = None) -> Order:
        """Create a new order"""
        self.order_counter += 1
        order = Order(
            id=f"order_{self.order_counter}",
            symbol=symbol.upper(),
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            status=OrderStatus.PENDING,
            timestamp=datetime.now()
        )
        
        self.orders.append(order)
        return order
    
    def execute_order(self, order: Order, current_price: float) -> bool:
        """Execute an order at current market price"""
        if order.status != OrderStatus.PENDING:
            return False
        
        symbol = order.symbol
        
        if order.side == OrderSide.BUY:
            # Calculate total cost including fees
            total_cost = order.quantity * current_price
            fee = total_cost * self.trading_fee
            total_required = total_cost + fee
            
            if self.cash_balance >= total_required:
                # Execute buy order
                self.cash_balance -= total_required
                
                # Update or create position
                if symbol in self.positions:
                    position = self.positions[symbol]
                    total_quantity = position.quantity + order.quantity
                    total_cost_basis = (position.average_price * position.quantity) + total_cost
                    position.average_price = total_cost_basis / total_quantity
                    position.quantity = total_quantity
                else:
                    self.positions[symbol] = Position(
                        symbol=symbol,
                        quantity=order.quantity,
                        average_price=current_price,
                        current_price=current_price,
                        unrealized_pnl=0.0
                    )
                
                # Create trade record
                self.trade_counter += 1
                trade = Trade(
                    id=f"trade_{self.trade_counter}",
                    order_id=order.id,
                    symbol=symbol,
                    side=order.side,
                    quantity=order.quantity,
                    price=current_price,
                    timestamp=datetime.now(),
                    fee=fee
                )
                self.trades.append(trade)
                
                # Update order
                order.status = OrderStatus.FILLED
                order.filled_quantity = order.quantity
                order.average_price = current_price
                
                return True
            else:
                order.status = OrderStatus.CANCELLED
                return False
                
        elif order.side == OrderSide.SELL:
            if symbol in self.positions and self.positions[symbol].quantity >= order.quantity:
                # Execute sell order
                position = self.positions[symbol]
                
                # Calculate proceeds and fees
                proceeds = order.quantity * current_price
                fee = proceeds * self.trading_fee
                net_proceeds = proceeds - fee
                
                self.cash_balance += net_proceeds
                
                # Update position
                position.quantity -= order.quantity
                if position.quantity == 0:
                    del self.positions[symbol]
                
                # Create trade record
                self.trade_counter += 1
                trade = Trade(
                    id=f"trade_{self.trade_counter}",
                    order_id=order.id,
                    symbol=symbol,
                    side=order.side,
                    quantity=order.quantity,
                    price=current_price,
                    timestamp=datetime.now(),
                    fee=fee
                )
                self.trades.append(trade)
                
                # Update order
                order.status = OrderStatus.FILLED
                order.filled_quantity = order.quantity
                order.average_price = current_price
                
                return True
            else:
                order.status = OrderStatus.CANCELLED
                return False
        
        return False
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel a pending order"""
        for order in self.orders:
            if order.id == order_id and order.status == OrderStatus.PENDING:
                order.status = OrderStatus.CANCELLED
                return True
        return False
    
    def get_positions_dataframe(self, current_prices: Dict[str, float]) -> pd.DataFrame:
        """Get positions as DataFrame"""
        if not self.positions:
            return pd.DataFrame()
        
        data = []
        for symbol, position in self.positions.items():
            if symbol in current_prices:
                position.current_price = current_prices[symbol]
                position.unrealized_pnl = (position.current_price - position.average_price) * position.quantity
                
                data.append({
                    'Symbol': symbol,
                    'Quantity': position.quantity,
                    'Average Price': position.average_price,
                    'Current Price': position.current_price,
                    'Unrealized PnL': position.unrealized_pnl,
                    'Unrealized PnL %': (position.unrealized_pnl / (position.average_price * position.quantity)) * 100
                })
        
        return pd.DataFrame(data)
    
    def get_trades_dataframe(self) -> pd.DataFrame:
        """Get trades as DataFrame"""
        if not self.trades:
            return pd.DataFrame()
        
        data = []
        for trade in self.trades:
            data.append({
                'ID': trade.id,
                'Symbol': trade.symbol,
                'Side': trade.side.value,
                'Quantity': trade.quantity,
                'Price': trade.price,
                'Fee': trade.fee,
                'Timestamp': trade.timestamp
            })
        
        return pd.DataFrame(data)
    
    def get_orders_dataframe(self) -> pd.DataFrame:
        """Get orders as DataFrame"""
        if not self.orders:
            return pd.DataFrame()
        
        data = []
        for order in self.orders:
            data.append({
                'ID': order.id,
                'Symbol': order.symbol,
                'Side': order.side.value,
                'Type': order.order_type.value,
                'Quantity': order.quantity,
                'Price': order.price,
                'Status': order.status.value,
                'Filled': order.filled_quantity,
                'Timestamp': order.timestamp
            })
        
        return pd.DataFrame(data)
    
    def save_portfolio(self, filename: str):
        """Save portfolio state to file"""
        portfolio_data = {
            'initial_balance': self.initial_balance,
            'cash_balance': self.cash_balance,
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
            self.cash_balance = portfolio_data['cash_balance']
            self.order_counter = portfolio_data['order_counter']
            self.trade_counter = portfolio_data['trade_counter']
            
            # Load positions
            self.positions = {}
            for symbol, pos_data in portfolio_data['positions'].items():
                self.positions[symbol] = Position(**pos_data)
            
            # Load orders
            self.orders = []
            for order_data in portfolio_data['orders']:
                order_data['side'] = OrderSide(order_data['side'])
                order_data['order_type'] = OrderType(order_data['order_type'])
                order_data['status'] = OrderStatus(order_data['status'])
                order_data['timestamp'] = datetime.fromisoformat(order_data['timestamp'])
                self.orders.append(Order(**order_data))
            
            # Load trades
            self.trades = []
            for trade_data in portfolio_data['trades']:
                trade_data['side'] = OrderSide(trade_data['side'])
                trade_data['timestamp'] = datetime.fromisoformat(trade_data['timestamp'])
                self.trades.append(Trade(**trade_data))
                
        except Exception as e:
            print(f"Error loading portfolio: {e}")

# Global portfolio instance
portfolio = Portfolio()

"""
Position Management Module
Handles position opening, closing, and management
"""

import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class Position:
    """Data class for position information"""
    symbol: str
    side: str  # LONG, SHORT
    size: float
    entry_price: float
    current_price: float
    unrealized_pnl: float
    realized_pnl: float = 0.0
    
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    trailing_stop: Optional[float] = None
    
    leverage: int = 1
    margin_used: float = 0.0
    
    entry_time: datetime = field(default_factory=datetime.now)
    last_update: datetime = field(default_factory=datetime.now)
    
    strategy: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

class PositionManager:
    """Advanced Position Management System"""
    
    def __init__(self, binance_client, risk_manager):
        """Initialize position manager"""
        self.binance_client = binance_client
        self.risk_manager = risk_manager
        
        self.positions = {}  # symbol -> Position
        self.order_history = []
        self.pnl_history = []
        
        logger.info("Position Manager initialized")
    
    async def get_position(self, symbol: str) -> Optional[Position]:
        """Get current position for a symbol"""
        try:
            # Get position from exchange
            exchange_position = await self.binance_client.get_position(symbol)
            
            if not exchange_position or float(exchange_position.get('positionAmt', 0)) == 0:
                # No position exists
                if symbol in self.positions:
                    del self.positions[symbol]
                return None
            
            # Convert exchange position to our Position object
            position_amt = float(exchange_position.get('positionAmt', 0))
            entry_price = float(exchange_position.get('entryPrice', 0))
            current_price = float(exchange_position.get('markPrice', entry_price))
            unrealized_pnl = float(exchange_position.get('unRealizedProfit', 0))
            
            side = 'LONG' if position_amt > 0 else 'SHORT'
            size = abs(position_amt)
            
            # Update or create position
            if symbol in self.positions:
                position = self.positions[symbol]
                position.current_price = current_price
                position.unrealized_pnl = unrealized_pnl
                position.last_update = datetime.now()
            else:
                position = Position(
                    symbol=symbol,
                    side=side,
                    size=size,
                    entry_price=entry_price,
                    current_price=current_price,
                    unrealized_pnl=unrealized_pnl,
                    leverage=int(exchange_position.get('leverage', 1)),
                    margin_used=size * entry_price / int(exchange_position.get('leverage', 1))
                )
                self.positions[symbol] = position
            
            return position
            
        except Exception as e:
            logger.error(f"Error getting position for {symbol}: {e}")
            return None
    
    async def open_long_position(self, symbol: str, signals: Dict[str, Any],
                               risk_assessment: Dict[str, Any]) -> bool:
        """Open a long position"""
        try:
            logger.info(f"Opening long position for {symbol}")
            
            # Check if we already have a position
            current_position = await self.get_position(symbol)
            if current_position and current_position.side == 'LONG':
                logger.warning(f"Already have long position for {symbol}")
                return False
            
            # Close opposite position if exists
            if current_position and current_position.side == 'SHORT':
                await self.close_position(symbol)
            
            # Calculate position size
            position_size = risk_assessment.get('position_size', 0)
            if position_size <= 0:
                logger.warning(f"Invalid position size for {symbol}: {position_size}")
                return False
            
            # Set leverage
            leverage = risk_assessment.get('leverage', 10)
            await self.binance_client.change_leverage(symbol, leverage)
            
            # Place market buy order
            order_result = await self.binance_client.market_buy(symbol, position_size)
            
            if order_result.get('status') == 'FILLED':
                # Set stop loss and take profit
                if risk_assessment.get('stop_loss'):
                    await self._set_stop_loss(symbol, 'SELL', position_size, 
                                            risk_assessment['stop_loss'])
                
                if risk_assessment.get('take_profit'):
                    await self._set_take_profit(symbol, 'SELL', position_size,
                                              risk_assessment['take_profit'])
                
                # Update position tracking
                await self.get_position(symbol)  # Refresh position data
                
                logger.info(f"✅ Long position opened for {symbol}: {position_size} @ {order_result.get('avgPrice')}")
                return True
            else:
                logger.error(f"❌ Failed to open long position for {symbol}: {order_result}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error opening long position for {symbol}: {e}")
            return False
    
    async def open_short_position(self, symbol: str, signals: Dict[str, Any],
                                risk_assessment: Dict[str, Any]) -> bool:
        """Open a short position"""
        try:
            logger.info(f"Opening short position for {symbol}")
            
            # Check if we already have a position
            current_position = await self.get_position(symbol)
            if current_position and current_position.side == 'SHORT':
                logger.warning(f"Already have short position for {symbol}")
                return False
            
            # Close opposite position if exists
            if current_position and current_position.side == 'LONG':
                await self.close_position(symbol)
            
            # Calculate position size
            position_size = risk_assessment.get('position_size', 0)
            if position_size <= 0:
                logger.warning(f"Invalid position size for {symbol}: {position_size}")
                return False
            
            # Set leverage
            leverage = risk_assessment.get('leverage', 10)
            await self.binance_client.change_leverage(symbol, leverage)
            
            # Place market sell order
            order_result = await self.binance_client.market_sell(symbol, position_size)
            
            if order_result.get('status') == 'FILLED':
                # Set stop loss and take profit
                if risk_assessment.get('stop_loss'):
                    await self._set_stop_loss(symbol, 'BUY', position_size,
                                            risk_assessment['stop_loss'])
                
                if risk_assessment.get('take_profit'):
                    await self._set_take_profit(symbol, 'BUY', position_size,
                                              risk_assessment['take_profit'])
                
                # Update position tracking
                await self.get_position(symbol)  # Refresh position data
                
                logger.info(f"✅ Short position opened for {symbol}: {position_size} @ {order_result.get('avgPrice')}")
                return True
            else:
                logger.error(f"❌ Failed to open short position for {symbol}: {order_result}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error opening short position for {symbol}: {e}")
            return False
    
    async def close_position(self, symbol: str, reason: str = "Manual close") -> bool:
        """Close position for a symbol"""
        try:
            position = await self.get_position(symbol)
            if not position:
                logger.warning(f"No position to close for {symbol}")
                return False
            
            logger.info(f"Closing {position.side} position for {symbol}: {reason}")
            
            # Cancel all open orders for the symbol
            await self.binance_client.cancel_all_orders(symbol)
            
            # Place opposite market order to close position
            if position.side == 'LONG':
                order_result = await self.binance_client.market_sell(symbol, position.size)
            else:  # SHORT
                order_result = await self.binance_client.market_buy(symbol, position.size)
            
            if order_result.get('status') == 'FILLED':
                # Calculate realized PnL
                exit_price = float(order_result.get('avgPrice', 0))
                if position.side == 'LONG':
                    realized_pnl = (exit_price - position.entry_price) * position.size
                else:
                    realized_pnl = (position.entry_price - exit_price) * position.size
                
                logger.info(f"✅ Position closed for {symbol}: PnL = ${realized_pnl:.2f}")
                
                # Record PnL history
                self.pnl_history.append({
                    'symbol': symbol,
                    'side': position.side,
                    'entry_price': position.entry_price,
                    'exit_price': exit_price,
                    'size': position.size,
                    'realized_pnl': realized_pnl,
                    'entry_time': position.entry_time,
                    'exit_time': datetime.now(),
                    'reason': reason
                })
                
                # Remove from positions
                if symbol in self.positions:
                    del self.positions[symbol]
                
                return True
            else:
                logger.error(f"❌ Failed to close position for {symbol}: {order_result}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error closing position for {symbol}: {e}")
            return False
    
    async def close_all_positions(self) -> int:
        """Close all open positions"""
        closed_count = 0
        
        try:
            # Get all positions from exchange
            exchange_positions = await self.binance_client.get_positions()
            
            for pos in exchange_positions:
                position_amt = float(pos.get('positionAmt', 0))
                if position_amt != 0:  # Has open position
                    symbol = pos['symbol']
                    if await self.close_position(symbol, "Bot shutdown"):
                        closed_count += 1
            
            logger.info(f"Closed {closed_count} positions")
            return closed_count
            
        except Exception as e:
            logger.error(f"Error closing all positions: {e}")
            return closed_count
    
    async def update_trailing_stops(self):
        """Update trailing stops for all positions"""
        try:
            for symbol, position in self.positions.items():
                # Get current price
                ticker = await self.binance_client.get_ticker_price(symbol)
                current_price = float(ticker['price'])
                
                # Check if we need to update trailing stop
                new_stop = await self.risk_manager.update_trailing_stop(
                    symbol, current_price, position.__dict__
                )
                
                if new_stop:
                    # Cancel existing stop loss orders
                    open_orders = await self.binance_client.get_open_orders(symbol)
                    for order in open_orders:
                        if order['type'] == 'STOP_MARKET':
                            await self.binance_client.cancel_order(symbol, order['orderId'])
                    
                    # Place new trailing stop
                    side = 'SELL' if position.side == 'LONG' else 'BUY'
                    await self.binance_client.stop_loss_order(
                        symbol, side, position.size, new_stop
                    )
                    
                    position.trailing_stop = new_stop
                    logger.info(f"Updated trailing stop for {symbol}: {new_stop}")
                
        except Exception as e:
            logger.error(f"Error updating trailing stops: {e}")
    
    async def check_position_exits(self):
        """Check all positions for stop loss and take profit triggers"""
        try:
            for symbol, position in list(self.positions.items()):
                # Get current price
                ticker = await self.binance_client.get_ticker_price(symbol)
                current_price = float(ticker['price'])
                
                # Update position current price
                position.current_price = current_price
                position.last_update = datetime.now()
                
                # Check stop loss
                if await self.risk_manager.check_stop_loss(
                    symbol, current_price, position.__dict__
                ):
                    await self.close_position(symbol, "Stop loss triggered")
                    continue
                
                # Check take profit
                if await self.risk_manager.check_take_profit(
                    symbol, current_price, position.__dict__
                ):
                    await self.close_position(symbol, "Take profit triggered")
                    continue
                
        except Exception as e:
            logger.error(f"Error checking position exits: {e}")
    
    async def _set_stop_loss(self, symbol: str, side: str, quantity: float,
                           stop_price: float) -> bool:
        """Set stop loss order"""
        try:
            order_result = await self.binance_client.stop_loss_order(
                symbol, side, quantity, stop_price
            )
            
            if order_result.get('status') in ['NEW', 'PENDING']:
                logger.info(f"Stop loss set for {symbol}: {stop_price}")
                return True
            else:
                logger.error(f"Failed to set stop loss for {symbol}: {order_result}")
                return False
                
        except Exception as e:
            logger.error(f"Error setting stop loss for {symbol}: {e}")
            return False
    
    async def _set_take_profit(self, symbol: str, side: str, quantity: float,
                             price: float) -> bool:
        """Set take profit order"""
        try:
            order_result = await self.binance_client.limit_buy(symbol, quantity, price) \
                          if side == 'BUY' else \
                          await self.binance_client.limit_sell(symbol, quantity, price)
            
            if order_result.get('status') in ['NEW', 'PENDING']:
                logger.info(f"Take profit set for {symbol}: {price}")
                return True
            else:
                logger.error(f"Failed to set take profit for {symbol}: {order_result}")
                return False
                
        except Exception as e:
            logger.error(f"Error setting take profit for {symbol}: {e}")
            return False
    
    def get_all_positions(self) -> List[Position]:
        """Get all current positions"""
        return list(self.positions.values())
    
    def get_position_summary(self) -> Dict[str, Any]:
        """Get summary of all positions"""
        total_unrealized_pnl = sum(pos.unrealized_pnl for pos in self.positions.values())
        total_margin_used = sum(pos.margin_used for pos in self.positions.values())
        
        return {
            'position_count': len(self.positions),
            'symbols': list(self.positions.keys()),
            'total_unrealized_pnl': total_unrealized_pnl,
            'total_margin_used': total_margin_used,
            'positions': [
                {
                    'symbol': pos.symbol,
                    'side': pos.side,
                    'size': pos.size,
                    'entry_price': pos.entry_price,
                    'current_price': pos.current_price,
                    'unrealized_pnl': pos.unrealized_pnl,
                    'entry_time': pos.entry_time.isoformat()
                }
                for pos in self.positions.values()
            ]
        }
    
    def get_pnl_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get PnL history"""
        return self.pnl_history[-limit:] if self.pnl_history else []
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        if not self.pnl_history:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'total_pnl': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'profit_factor': 0.0
            }
        
        winning_trades = [trade for trade in self.pnl_history if trade['realized_pnl'] > 0]
        losing_trades = [trade for trade in self.pnl_history if trade['realized_pnl'] < 0]
        
        total_pnl = sum(trade['realized_pnl'] for trade in self.pnl_history)
        total_wins = sum(trade['realized_pnl'] for trade in winning_trades)
        total_losses = abs(sum(trade['realized_pnl'] for trade in losing_trades))
        
        return {
            'total_trades': len(self.pnl_history),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': len(winning_trades) / len(self.pnl_history) * 100,
            'total_pnl': total_pnl,
            'avg_win': total_wins / len(winning_trades) if winning_trades else 0,
            'avg_loss': total_losses / len(losing_trades) if losing_trades else 0,
            'profit_factor': total_wins / total_losses if total_losses > 0 else float('inf'),
            'best_trade': max(self.pnl_history, key=lambda x: x['realized_pnl'])['realized_pnl'],
            'worst_trade': min(self.pnl_history, key=lambda x: x['realized_pnl'])['realized_pnl']
        }

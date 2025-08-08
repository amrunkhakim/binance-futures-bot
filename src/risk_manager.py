"""
Risk Management Module
Provides comprehensive risk assessment and management for trading operations
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class RiskMetrics:
    """Data class for risk metrics"""
    account_balance: float = 0.0
    unrealized_pnl: float = 0.0
    daily_pnl: float = 0.0
    total_exposure: float = 0.0
    margin_ratio: float = 0.0
    
    daily_trades: int = 0
    consecutive_losses: int = 0
    max_drawdown: float = 0.0
    
    risk_score: float = 0.0  # 0-100
    risk_level: str = 'LOW'  # LOW, MEDIUM, HIGH, CRITICAL
    
    violations: List[str] = field(default_factory=list)

@dataclass
class PositionRisk:
    """Data class for individual position risk"""
    symbol: str
    position_size: float
    entry_price: float
    current_price: float
    unrealized_pnl: float
    position_value: float
    
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    
    risk_percent: float = 0.0
    max_loss_amount: float = 0.0
    
    leverage: int = 1
    margin_used: float = 0.0

class RiskManager:
    """Advanced Risk Management System"""
    
    def __init__(self, config):
        """Initialize risk manager"""
        self.config = config
        self.risk_limits = self._load_risk_limits()
        self.daily_stats = {}
        self.position_history = []
        
        # Risk state
        self.emergency_stop = False
        self.trading_paused = False
        self.last_risk_check = datetime.now()
        
        logger.info("Risk Manager initialized")
    
    def _load_risk_limits(self) -> Dict[str, Any]:
        """Load risk management limits from config"""
        return {
            'max_position_size_percent': self.config.MAX_POSITION_SIZE_PERCENT,
            'max_daily_loss_percent': self.config.MAX_DAILY_LOSS_PERCENT,
            'max_drawdown_percent': self.config.MAX_DRAWDOWN_PERCENT,
            'stop_loss_percent': self.config.STOP_LOSS_PERCENT,
            'take_profit_percent': self.config.TAKE_PROFIT_PERCENT,
            'trailing_stop_percent': self.config.TRAILING_STOP_PERCENT,
            'max_open_positions': 5,
            'max_daily_trades': 20,
            'max_consecutive_losses': 3,
            'min_risk_reward_ratio': 1.5,
            'max_correlation': 0.7,
            'max_leverage': self.config.LEVERAGE
        }
    
    async def assess_risk(self, symbol: str, signals: Dict[str, Any], 
                         current_position: Optional[Dict] = None) -> Dict[str, Any]:
        """Comprehensive risk assessment for trading decision"""
        try:
            # Get current account metrics
            account_metrics = await self._get_account_metrics()
            
            # Calculate position risk
            position_risk = await self._calculate_position_risk(
                symbol, signals, current_position, account_metrics
            )
            
            # Perform risk checks
            risk_assessment = await self._perform_risk_checks(
                symbol, signals, position_risk, account_metrics
            )
            
            # Update risk history
            await self._update_risk_history(symbol, risk_assessment)
            
            logger.debug(f"Risk assessment for {symbol}: {risk_assessment['risk_level']}")
            return risk_assessment
            
        except Exception as e:
            logger.error(f"Risk assessment error for {symbol}: {e}")
            return {
                'approved': False,
                'risk_level': 'CRITICAL',
                'violations': [f"Risk assessment failed: {e}"],
                'position_size': 0,
                'stop_loss': None,
                'take_profit': None
            }
    
    async def _get_account_metrics(self) -> RiskMetrics:
        """Get current account risk metrics"""
        # This would typically fetch real data from the exchange
        # For now, returning mock data
        return RiskMetrics(
            account_balance=10000.0,  # Mock balance
            unrealized_pnl=0.0,
            daily_pnl=0.0,
            total_exposure=0.0,
            margin_ratio=0.1,
            daily_trades=0,
            consecutive_losses=0,
            max_drawdown=0.0
        )
    
    async def _calculate_position_risk(self, symbol: str, signals: Dict[str, Any],
                                     current_position: Optional[Dict],
                                     account_metrics: RiskMetrics) -> PositionRisk:
        """Calculate risk metrics for a potential position"""
        
        # Get current price (mock)
        current_price = 50000.0  # This should come from market data
        
        # Calculate position size based on risk limits
        max_risk_amount = account_metrics.account_balance * (self.risk_limits['max_position_size_percent'] / 100)
        stop_loss_percent = self.risk_limits['stop_loss_percent'] / 100
        
        # Calculate position size based on stop loss
        if signals.get('action') in ['BUY', 'SELL']:
            stop_distance = current_price * stop_loss_percent
            position_size = max_risk_amount / stop_distance
            
            # Apply leverage
            leverage = min(self.risk_limits['max_leverage'], 10)
            position_value = position_size * current_price
            margin_used = position_value / leverage
            
            # Calculate stop loss and take profit levels
            if signals.get('action') == 'BUY':
                stop_loss = current_price * (1 - stop_loss_percent)
                take_profit = current_price * (1 + (self.risk_limits['take_profit_percent'] / 100))
            else:  # SELL
                stop_loss = current_price * (1 + stop_loss_percent)
                take_profit = current_price * (1 - (self.risk_limits['take_profit_percent'] / 100))
            
        else:
            position_size = 0
            position_value = 0
            margin_used = 0
            stop_loss = None
            take_profit = None
        
        return PositionRisk(
            symbol=symbol,
            position_size=position_size,
            entry_price=current_price,
            current_price=current_price,
            unrealized_pnl=0.0,
            position_value=position_value,
            stop_loss=stop_loss,
            take_profit=take_profit,
            risk_percent=(margin_used / account_metrics.account_balance) * 100,
            max_loss_amount=max_risk_amount,
            leverage=leverage,
            margin_used=margin_used
        )
    
    async def _perform_risk_checks(self, symbol: str, signals: Dict[str, Any],
                                 position_risk: PositionRisk, 
                                 account_metrics: RiskMetrics) -> Dict[str, Any]:
        """Perform comprehensive risk checks"""
        
        violations = []
        approved = True
        risk_score = 0
        
        # Check 1: Position size limit
        if position_risk.risk_percent > self.risk_limits['max_position_size_percent']:
            violations.append(f"Position size exceeds limit: {position_risk.risk_percent:.2f}%")
            approved = False
            risk_score += 30
        
        # Check 2: Daily loss limit
        if account_metrics.daily_pnl < -(account_metrics.account_balance * self.risk_limits['max_daily_loss_percent'] / 100):
            violations.append("Daily loss limit exceeded")
            approved = False
            risk_score += 40
        
        # Check 3: Maximum drawdown
        if account_metrics.max_drawdown > self.risk_limits['max_drawdown_percent']:
            violations.append(f"Maximum drawdown exceeded: {account_metrics.max_drawdown:.2f}%")
            approved = False
            risk_score += 50
        
        # Check 4: Consecutive losses
        if account_metrics.consecutive_losses >= self.risk_limits['max_consecutive_losses']:
            violations.append(f"Too many consecutive losses: {account_metrics.consecutive_losses}")
            approved = False
            risk_score += 25
        
        # Check 5: Daily trade limit
        if account_metrics.daily_trades >= self.risk_limits['max_daily_trades']:
            violations.append("Daily trade limit reached")
            approved = False
            risk_score += 20
        
        # Check 6: Signal strength
        signal_strength = signals.get('signal_strength', 0)
        min_signal_strength = self.config.MIN_SIGNAL_STRENGTH
        if signal_strength < min_signal_strength:
            violations.append(f"Signal strength too low: {signal_strength:.2f}")
            approved = False
            risk_score += 15
        
        # Check 7: Emergency stop
        if self.emergency_stop:
            violations.append("Emergency stop activated")
            approved = False
            risk_score = 100
        
        # Check 8: Trading paused
        if self.trading_paused:
            violations.append("Trading is paused")
            approved = False
            risk_score += 100
        
        # Check 9: Market conditions
        volatility = signals.get('volatility', 'MEDIUM')
        if volatility == 'HIGH':
            risk_score += 15
            # Reduce position size in high volatility
            position_risk.position_size *= 0.7
            position_risk.position_value *= 0.7
            position_risk.margin_used *= 0.7
        
        # Check 10: Risk-reward ratio
        if position_risk.stop_loss and position_risk.take_profit:
            risk_amount = abs(position_risk.entry_price - position_risk.stop_loss)
            reward_amount = abs(position_risk.take_profit - position_risk.entry_price)
            risk_reward_ratio = reward_amount / risk_amount if risk_amount > 0 else 0
            
            if risk_reward_ratio < self.risk_limits['min_risk_reward_ratio']:
                violations.append(f"Poor risk-reward ratio: {risk_reward_ratio:.2f}")
                risk_score += 20
        
        # Determine risk level
        if risk_score >= 80:
            risk_level = 'CRITICAL'
            approved = False
        elif risk_score >= 60:
            risk_level = 'HIGH'
        elif risk_score >= 30:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        return {
            'approved': approved,
            'risk_level': risk_level,
            'risk_score': risk_score,
            'violations': violations,
            'position_size': position_risk.position_size if approved else 0,
            'position_value': position_risk.position_value if approved else 0,
            'margin_used': position_risk.margin_used if approved else 0,
            'stop_loss': position_risk.stop_loss,
            'take_profit': position_risk.take_profit,
            'leverage': position_risk.leverage,
            'max_loss_amount': position_risk.max_loss_amount
        }
    
    async def _update_risk_history(self, symbol: str, risk_assessment: Dict[str, Any]):
        """Update risk history and statistics"""
        current_time = datetime.now()
        
        # Update daily stats
        today_key = current_time.strftime('%Y-%m-%d')
        if today_key not in self.daily_stats:
            self.daily_stats[today_key] = {
                'trades': 0,
                'approved_trades': 0,
                'rejected_trades': 0,
                'violations': []
            }
        
        self.daily_stats[today_key]['trades'] += 1
        
        if risk_assessment['approved']:
            self.daily_stats[today_key]['approved_trades'] += 1
        else:
            self.daily_stats[today_key]['rejected_trades'] += 1
            self.daily_stats[today_key]['violations'].extend(risk_assessment['violations'])
        
        # Clean old history (keep last 30 days)
        cutoff_date = current_time - timedelta(days=30)
        cutoff_key = cutoff_date.strftime('%Y-%m-%d')
        
        keys_to_remove = [key for key in self.daily_stats.keys() if key < cutoff_key]
        for key in keys_to_remove:
            del self.daily_stats[key]
    
    async def update_position_pnl(self, symbol: str, unrealized_pnl: float,
                                 current_price: float):
        """Update position PnL for risk monitoring"""
        # This would update the running PnL for open positions
        # and check for any risk limit violations
        pass
    
    async def check_stop_loss(self, symbol: str, current_price: float,
                            position: Dict[str, Any]) -> bool:
        """Check if stop loss should be triggered"""
        if not position or 'stop_loss' not in position:
            return False
        
        stop_loss = position['stop_loss']
        side = position.get('side', 'LONG')
        
        if side == 'LONG' and current_price <= stop_loss:
            logger.warning(f"Stop loss triggered for {symbol}: {current_price} <= {stop_loss}")
            return True
        elif side == 'SHORT' and current_price >= stop_loss:
            logger.warning(f"Stop loss triggered for {symbol}: {current_price} >= {stop_loss}")
            return True
        
        return False
    
    async def check_take_profit(self, symbol: str, current_price: float,
                              position: Dict[str, Any]) -> bool:
        """Check if take profit should be triggered"""
        if not position or 'take_profit' not in position:
            return False
        
        take_profit = position['take_profit']
        side = position.get('side', 'LONG')
        
        if side == 'LONG' and current_price >= take_profit:
            logger.info(f"Take profit triggered for {symbol}: {current_price} >= {take_profit}")
            return True
        elif side == 'SHORT' and current_price <= take_profit:
            logger.info(f"Take profit triggered for {symbol}: {current_price} <= {take_profit}")
            return True
        
        return False
    
    async def update_trailing_stop(self, symbol: str, current_price: float,
                                 position: Dict[str, Any]) -> Optional[float]:
        """Update trailing stop loss"""
        if not position or 'entry_price' not in position:
            return None
        
        side = position.get('side', 'LONG')
        trailing_percent = self.risk_limits['trailing_stop_percent'] / 100
        
        if side == 'LONG':
            # For long positions, trailing stop moves up with price
            new_stop = current_price * (1 - trailing_percent)
            current_stop = position.get('stop_loss', 0)
            
            if new_stop > current_stop:
                logger.info(f"Updating trailing stop for {symbol}: {current_stop} -> {new_stop}")
                return new_stop
        
        elif side == 'SHORT':
            # For short positions, trailing stop moves down with price
            new_stop = current_price * (1 + trailing_percent)
            current_stop = position.get('stop_loss', float('inf'))
            
            if new_stop < current_stop:
                logger.info(f"Updating trailing stop for {symbol}: {current_stop} -> {new_stop}")
                return new_stop
        
        return None
    
    def activate_emergency_stop(self, reason: str):
        """Activate emergency stop"""
        self.emergency_stop = True
        logger.critical(f"🚨 EMERGENCY STOP ACTIVATED: {reason}")
    
    def deactivate_emergency_stop(self):
        """Deactivate emergency stop"""
        self.emergency_stop = False
        logger.info("Emergency stop deactivated")
    
    def pause_trading(self, reason: str):
        """Pause trading temporarily"""
        self.trading_paused = True
        logger.warning(f"⏸️ Trading paused: {reason}")
    
    def resume_trading(self):
        """Resume trading"""
        self.trading_paused = False
        logger.info("Trading resumed")
    
    def get_daily_stats(self, date: str = None) -> Dict[str, Any]:
        """Get daily trading statistics"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        return self.daily_stats.get(date, {
            'trades': 0,
            'approved_trades': 0,
            'rejected_trades': 0,
            'violations': []
        })
    
    def get_risk_summary(self) -> Dict[str, Any]:
        """Get overall risk summary"""
        return {
            'emergency_stop': self.emergency_stop,
            'trading_paused': self.trading_paused,
            'risk_limits': self.risk_limits,
            'daily_stats': self.get_daily_stats(),
            'last_risk_check': self.last_risk_check.isoformat()
        }

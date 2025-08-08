"""
Strategy Management Module
Implements multiple trading strategies with signal generation
"""

import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
from dataclasses import dataclass
from abc import ABC, abstractmethod

from .technical_analyzer import TechnicalSignals
from .ai_analyzer import AIAnalyzer

logger = logging.getLogger(__name__)

@dataclass
class TradingSignal:
    """Data class for trading signals"""
    action: str  # BUY, SELL, HOLD, CLOSE
    confidence: float  # 0-1
    entry_price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    signal_strength: float = 0.5
    reason: str = ""
    metadata: Dict[str, Any] = None

class BaseStrategy(ABC):
    """Base class for trading strategies"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.enabled = config.get('enabled', True)
        self.min_signal_strength = config.get('min_signal_strength', 0.6)
    
    @abstractmethod
    async def generate_signal(self, symbol: str, analysis: TechnicalSignals,
                            current_position: Optional[Dict] = None) -> TradingSignal:
        """Generate trading signal based on analysis"""
        pass
    
    def _calculate_confidence(self, signals: Dict[str, float]) -> float:
        """Calculate confidence score from multiple signals"""
        if not signals:
            return 0.0
        
        weights = {
            'trend': 0.3,
            'momentum': 0.25,
            'reversal': 0.2,
            'volume': 0.15,
            'volatility': 0.1
        }
        
        weighted_score = sum(signals.get(key, 0) * weight 
                           for key, weight in weights.items())
        return min(max(weighted_score, 0.0), 1.0)

class MultiIndicatorStrategy(BaseStrategy):
    """Multi-indicator strategy combining various technical signals"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("multi_indicator", config)
        self.rsi_weight = config.get('rsi_weight', 0.2)
        self.macd_weight = config.get('macd_weight', 0.3)
        self.ema_weight = config.get('ema_weight', 0.3)
        self.bb_weight = config.get('bb_weight', 0.2)
    
    async def generate_signal(self, symbol: str, analysis: TechnicalSignals,
                            current_position: Optional[Dict] = None) -> TradingSignal:
        """Generate signal using multiple technical indicators"""
        try:
            signals = {}
            reasons = []
            
            # RSI Analysis
            rsi_signal = self._analyze_rsi(analysis)
            signals['rsi'] = rsi_signal['score']
            if abs(rsi_signal['score']) > 0.3:
                reasons.append(rsi_signal['reason'])
            
            # MACD Analysis
            macd_signal = self._analyze_macd(analysis)
            signals['macd'] = macd_signal['score']
            if abs(macd_signal['score']) > 0.3:
                reasons.append(macd_signal['reason'])
            
            # EMA Analysis
            ema_signal = self._analyze_ema(analysis)
            signals['ema'] = ema_signal['score']
            if abs(ema_signal['score']) > 0.3:
                reasons.append(ema_signal['reason'])
            
            # Bollinger Bands Analysis
            bb_signal = self._analyze_bollinger_bands(analysis)
            signals['bb'] = bb_signal['score']
            if abs(bb_signal['score']) > 0.3:
                reasons.append(bb_signal['reason'])
            
            # Volume Analysis
            volume_signal = self._analyze_volume(analysis)
            signals['volume'] = volume_signal['score']
            if abs(volume_signal['score']) > 0.2:
                reasons.append(volume_signal['reason'])
            
            # Calculate overall signal
            overall_score = (
                signals['rsi'] * self.rsi_weight +
                signals['macd'] * self.macd_weight +
                signals['ema'] * self.ema_weight +
                signals['bb'] * self.bb_weight +
                signals['volume'] * 0.1
            )
            
            # Determine action
            action = self._determine_action(overall_score, current_position)
            confidence = abs(overall_score)
            signal_strength = min(confidence, 1.0)
            
            # Calculate entry, stop loss, and take profit
            entry_price = None
            stop_loss = None
            take_profit = None
            
            if action in ['BUY', 'SELL']:
                entry_price = analysis.ema_fast  # Use fast EMA as entry reference
                if action == 'BUY':
                    stop_loss = entry_price * 0.98  # 2% stop loss
                    take_profit = entry_price * 1.06  # 6% take profit
                else:  # SELL
                    stop_loss = entry_price * 1.02  # 2% stop loss
                    take_profit = entry_price * 0.94  # 6% take profit
            
            return TradingSignal(
                action=action,
                confidence=confidence,
                entry_price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                signal_strength=signal_strength,
                reason="; ".join(reasons[:3]),  # Top 3 reasons
                metadata={
                    'strategy': self.name,
                    'overall_score': overall_score,
                    'individual_signals': signals,
                    'analysis_timestamp': datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Error generating multi-indicator signal for {symbol}: {e}")
            return self._default_signal()
    
    def _analyze_rsi(self, analysis: TechnicalSignals) -> Dict[str, Any]:
        """Analyze RSI for trading signals"""
        rsi = analysis.rsi
        
        if rsi < 25:
            return {'score': 0.8, 'reason': f'RSI oversold ({rsi:.1f})'}
        elif rsi < 30:
            return {'score': 0.6, 'reason': f'RSI approaching oversold ({rsi:.1f})'}
        elif rsi > 75:
            return {'score': -0.8, 'reason': f'RSI overbought ({rsi:.1f})'}
        elif rsi > 70:
            return {'score': -0.6, 'reason': f'RSI approaching overbought ({rsi:.1f})'}
        else:
            return {'score': 0.0, 'reason': f'RSI neutral ({rsi:.1f})'}
    
    def _analyze_macd(self, analysis: TechnicalSignals) -> Dict[str, Any]:
        """Analyze MACD for trading signals"""
        if analysis.macd_signal_type == 'BULLISH':
            if analysis.macd_histogram > 0:
                return {'score': 0.9, 'reason': 'MACD bullish crossover with positive histogram'}
            else:
                return {'score': 0.7, 'reason': 'MACD bullish crossover'}
        elif analysis.macd_signal_type == 'BEARISH':
            if analysis.macd_histogram < 0:
                return {'score': -0.9, 'reason': 'MACD bearish crossover with negative histogram'}
            else:
                return {'score': -0.7, 'reason': 'MACD bearish crossover'}
        else:
            return {'score': 0.0, 'reason': 'MACD neutral'}
    
    def _analyze_ema(self, analysis: TechnicalSignals) -> Dict[str, Any]:
        """Analyze EMA for trading signals"""
        if analysis.ema_signal == 'BULLISH':
            return {'score': 0.8, 'reason': 'EMA bullish alignment'}
        elif analysis.ema_signal == 'BEARISH':
            return {'score': -0.8, 'reason': 'EMA bearish alignment'}
        else:
            return {'score': 0.0, 'reason': 'EMA neutral'}
    
    def _analyze_bollinger_bands(self, analysis: TechnicalSignals) -> Dict[str, Any]:
        """Analyze Bollinger Bands for trading signals"""
        if analysis.bb_position == 'LOWER':
            if analysis.bb_squeeze:
                return {'score': 0.7, 'reason': 'Price near lower BB during squeeze'}
            else:
                return {'score': 0.5, 'reason': 'Price near lower Bollinger Band'}
        elif analysis.bb_position == 'UPPER':
            if analysis.bb_squeeze:
                return {'score': -0.7, 'reason': 'Price near upper BB during squeeze'}
            else:
                return {'score': -0.5, 'reason': 'Price near upper Bollinger Band'}
        else:
            return {'score': 0.0, 'reason': 'Price in middle of Bollinger Bands'}
    
    def _analyze_volume(self, analysis: TechnicalSignals) -> Dict[str, Any]:
        """Analyze volume for signal confirmation"""
        if analysis.volume_ratio > 2.0:
            return {'score': 0.3, 'reason': f'High volume ({analysis.volume_ratio:.1f}x avg)'}
        elif analysis.volume_ratio > 1.5:
            return {'score': 0.2, 'reason': f'Above average volume ({analysis.volume_ratio:.1f}x avg)'}
        elif analysis.volume_ratio < 0.5:
            return {'score': -0.2, 'reason': f'Low volume ({analysis.volume_ratio:.1f}x avg)'}
        else:
            return {'score': 0.0, 'reason': f'Normal volume ({analysis.volume_ratio:.1f}x avg)'}
    
    def _determine_action(self, score: float, current_position: Optional[Dict]) -> str:
        """Determine trading action based on signal score"""
        if current_position and current_position.get('positionAmt', 0) != 0:
            # Check if we should close the current position
            current_side = 'LONG' if float(current_position.get('positionAmt', 0)) > 0 else 'SHORT'
            
            if (current_side == 'LONG' and score < -0.4) or (current_side == 'SHORT' and score > 0.4):
                return 'CLOSE'
        
        # Check for new positions
        if score > 0.6:
            return 'BUY'
        elif score < -0.6:
            return 'SELL'
        else:
            return 'HOLD'
    
    def _default_signal(self) -> TradingSignal:
        """Return default signal when analysis fails"""
        return TradingSignal(
            action='HOLD',
            confidence=0.0,
            signal_strength=0.0,
            reason='Strategy analysis failed'
        )

class ScalpingStrategy(BaseStrategy):
    """Short-term scalping strategy"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("scalping", config)
        self.profit_target = config.get('profit_target', 0.5)  # 0.5% profit target
        self.stop_loss = config.get('stop_loss', 0.3)  # 0.3% stop loss
    
    async def generate_signal(self, symbol: str, analysis: TechnicalSignals,
                            current_position: Optional[Dict] = None) -> TradingSignal:
        """Generate scalping signals for short-term trades"""
        try:
            # Focus on quick momentum changes
            score = 0
            reasons = []
            
            # Quick RSI reversals
            if analysis.rsi < 25:
                score += 0.8
                reasons.append("RSI extreme oversold")
            elif analysis.rsi > 75:
                score -= 0.8
                reasons.append("RSI extreme overbought")
            
            # MACD momentum
            if analysis.macd_signal_type == 'BULLISH' and analysis.macd_histogram > 0:
                score += 0.6
                reasons.append("MACD bullish momentum")
            elif analysis.macd_signal_type == 'BEARISH' and analysis.macd_histogram < 0:
                score -= 0.6
                reasons.append("MACD bearish momentum")
            
            # Volume confirmation
            if analysis.volume_ratio > 1.8:
                score *= 1.2  # Boost signal with high volume
                reasons.append("High volume confirmation")
            
            # Determine action
            action = 'HOLD'
            if score > 0.7:
                action = 'BUY'
            elif score < -0.7:
                action = 'SELL'
            
            confidence = abs(score)
            
            # Calculate tight stop loss and take profit for scalping
            entry_price = None
            stop_loss = None
            take_profit = None
            
            if action in ['BUY', 'SELL']:
                entry_price = analysis.ema_fast
                if action == 'BUY':
                    stop_loss = entry_price * (1 - self.stop_loss / 100)
                    take_profit = entry_price * (1 + self.profit_target / 100)
                else:
                    stop_loss = entry_price * (1 + self.stop_loss / 100)
                    take_profit = entry_price * (1 - self.profit_target / 100)
            
            return TradingSignal(
                action=action,
                confidence=confidence,
                entry_price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                signal_strength=confidence,
                reason="; ".join(reasons[:2]),
                metadata={
                    'strategy': self.name,
                    'score': score,
                    'volume_ratio': analysis.volume_ratio
                }
            )
            
        except Exception as e:
            logger.error(f"Error generating scalping signal for {symbol}: {e}")
            return self._default_signal()

class SwingStrategy(BaseStrategy):
    """Medium-term swing trading strategy"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("swing", config)
        self.profit_target = config.get('profit_target', 8.0)  # 8% profit target
        self.stop_loss = config.get('stop_loss', 4.0)  # 4% stop loss
    
    async def generate_signal(self, symbol: str, analysis: TechnicalSignals,
                            current_position: Optional[Dict] = None) -> TradingSignal:
        """Generate swing trading signals for medium-term positions"""
        try:
            score = 0
            reasons = []
            
            # Trend following with EMA
            if analysis.ema_signal == 'BULLISH':
                score += 0.7
                reasons.append("Bullish EMA trend")
            elif analysis.ema_signal == 'BEARISH':
                score -= 0.7
                reasons.append("Bearish EMA trend")
            
            # Support and resistance levels
            current_price = analysis.ema_fast  # Approximate current price
            if current_price <= analysis.support_level * 1.02:  # Near support
                score += 0.5
                reasons.append("Near support level")
            elif current_price >= analysis.resistance_level * 0.98:  # Near resistance
                score -= 0.5
                reasons.append("Near resistance level")
            
            # MACD trend confirmation
            if analysis.macd_signal_type == 'BULLISH':
                score += 0.4
                reasons.append("MACD bullish")
            elif analysis.macd_signal_type == 'BEARISH':
                score -= 0.4
                reasons.append("MACD bearish")
            
            # RSI for entries (not extremes)
            if 30 < analysis.rsi < 40:  # RSI recovering from oversold
                score += 0.3
                reasons.append("RSI recovering")
            elif 60 < analysis.rsi < 70:  # RSI weakening from overbought
                score -= 0.3
                reasons.append("RSI weakening")
            
            # Determine action
            action = 'HOLD'
            if score > 0.8:
                action = 'BUY'
            elif score < -0.8:
                action = 'SELL'
            
            confidence = abs(score)
            
            # Calculate wider stop loss and take profit for swing trading
            entry_price = None
            stop_loss = None
            take_profit = None
            
            if action in ['BUY', 'SELL']:
                entry_price = analysis.ema_fast
                if action == 'BUY':
                    stop_loss = entry_price * (1 - self.stop_loss / 100)
                    take_profit = entry_price * (1 + self.profit_target / 100)
                else:
                    stop_loss = entry_price * (1 + self.stop_loss / 100)
                    take_profit = entry_price * (1 - self.profit_target / 100)
            
            return TradingSignal(
                action=action,
                confidence=confidence,
                entry_price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                signal_strength=confidence,
                reason="; ".join(reasons[:3]),
                metadata={
                    'strategy': self.name,
                    'score': score,
                    'support': analysis.support_level,
                    'resistance': analysis.resistance_level
                }
            )
            
        except Exception as e:
            logger.error(f"Error generating swing signal for {symbol}: {e}")
            return self._default_signal()

class AIEnhancedStrategy(BaseStrategy):
    """AI-enhanced strategy using Gemini AI for analysis"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("ai_enhanced", config)
        self.ai_analyzer = AIAnalyzer()
        self.ai_weight = config.get('ai_weight', 0.6)  # Weight for AI analysis
        self.technical_weight = config.get('technical_weight', 0.4)  # Weight for technical analysis
        self.profit_target = config.get('profit_target', 4.0)  # 4% profit target
        self.stop_loss = config.get('stop_loss', 2.0)  # 2% stop loss
    
    async def generate_signal(self, symbol: str, analysis: TechnicalSignals,
                            current_position: Optional[Dict] = None) -> TradingSignal:
        """Generate AI-enhanced trading signal"""
        try:
            # Get traditional technical analysis signal
            technical_signal = await self._get_technical_signal(analysis)
            
            # Get AI analysis if available
            ai_signal = None
            if self.ai_analyzer.is_available():
                try:
                    # Prepare market data for AI
                    market_data = {
                        "price": analysis.ema_fast,  # Use EMA as price reference
                        "volume": analysis.volume_ratio,
                        "price_change_24h": 0,  # Would need actual price change data
                        "price_change_percent": 0,
                        "high_24h": analysis.resistance_level,
                        "low_24h": analysis.support_level
                    }
                    
                    # Prepare technical analysis data
                    tech_data = {
                        "rsi": {"value": analysis.rsi},
                        "macd": {"signal": analysis.macd_signal_type},
                        "ema": {"trend": analysis.ema_signal},
                        "bollinger_bands": {"position": analysis.bb_position},
                        "support_resistance": {
                            "support": analysis.support_level,
                            "resistance": analysis.resistance_level
                        },
                        "volume": {"ratio": analysis.volume_ratio}
                    }
                    
                    # Get AI sentiment analysis
                    ai_sentiment = await self.ai_analyzer.analyze_market_sentiment(
                        symbol, market_data, tech_data
                    )
                    
                    # Convert AI analysis to signal score
                    ai_signal = self._convert_ai_to_signal(ai_sentiment)
                    
                except Exception as e:
                    logger.warning(f"AI analysis failed for {symbol}: {e}")
                    ai_signal = None
            
            # Combine signals
            final_signal = self._combine_signals(technical_signal, ai_signal, current_position)
            
            return final_signal
            
        except Exception as e:
            logger.error(f"Error generating AI-enhanced signal for {symbol}: {e}")
            return self._default_signal()
    
    async def _get_technical_signal(self, analysis: TechnicalSignals) -> Dict[str, Any]:
        """Get traditional technical analysis signal"""
        score = 0
        reasons = []
        
        # RSI Analysis
        if analysis.rsi < 30:
            score += 0.7
            reasons.append(f"RSI oversold ({analysis.rsi:.1f})")
        elif analysis.rsi > 70:
            score -= 0.7
            reasons.append(f"RSI overbought ({analysis.rsi:.1f})")
        
        # MACD Analysis
        if analysis.macd_signal_type == 'BULLISH':
            score += 0.6
            reasons.append("MACD bullish")
        elif analysis.macd_signal_type == 'BEARISH':
            score -= 0.6
            reasons.append("MACD bearish")
        
        # EMA Trend
        if analysis.ema_signal == 'BULLISH':
            score += 0.5
            reasons.append("Bullish EMA trend")
        elif analysis.ema_signal == 'BEARISH':
            score -= 0.5
            reasons.append("Bearish EMA trend")
        
        # Volume confirmation
        if analysis.volume_ratio > 1.5:
            score *= 1.2
            reasons.append("Volume confirmation")
        
        return {
            "score": score,
            "confidence": abs(score),
            "reasons": reasons
        }
    
    def _convert_ai_to_signal(self, ai_sentiment: Dict[str, Any]) -> Dict[str, Any]:
        """Convert AI sentiment to trading signal"""
        sentiment = ai_sentiment.get("ai_sentiment", "NEUTRAL")
        confidence = ai_sentiment.get("confidence", 0.5)
        
        # Convert sentiment to score
        if sentiment == "BULLISH":
            score = confidence
        elif sentiment == "BEARISH":
            score = -confidence
        else:
            score = 0
        
        return {
            "score": score,
            "confidence": confidence,
            "reasons": [ai_sentiment.get("reasoning", "AI analysis")],
            "recommendation": ai_sentiment.get("recommendation", "HOLD"),
            "risk_level": ai_sentiment.get("risk_level", "MEDIUM")
        }
    
    def _combine_signals(self, technical_signal: Dict[str, Any], 
                        ai_signal: Optional[Dict[str, Any]], 
                        current_position: Optional[Dict]) -> TradingSignal:
        """Combine technical and AI signals"""
        
        if ai_signal:
            # Weighted combination of signals
            combined_score = (
                technical_signal["score"] * self.technical_weight +
                ai_signal["score"] * self.ai_weight
            )
            combined_confidence = (
                technical_signal["confidence"] * self.technical_weight +
                ai_signal["confidence"] * self.ai_weight
            )
            reasons = technical_signal["reasons"] + ai_signal["reasons"]
        else:
            # Use only technical signal
            combined_score = technical_signal["score"]
            combined_confidence = technical_signal["confidence"]
            reasons = technical_signal["reasons"] + ["AI analysis unavailable"]
        
        # Determine action
        action = self._determine_action(combined_score, current_position)
        
        # Calculate entry, stop loss, and take profit
        entry_price = None
        stop_loss = None
        take_profit = None
        
        if action in ['BUY', 'SELL']:
            # Use a reference price (would need actual market price in real implementation)
            entry_price = 50000  # Placeholder - should use actual current price
            
            if action == 'BUY':
                stop_loss = entry_price * (1 - self.stop_loss / 100)
                take_profit = entry_price * (1 + self.profit_target / 100)
            else:  # SELL
                stop_loss = entry_price * (1 + self.stop_loss / 100)
                take_profit = entry_price * (1 - self.profit_target / 100)
        
        return TradingSignal(
            action=action,
            confidence=combined_confidence,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            signal_strength=combined_confidence,
            reason="; ".join(reasons[:3]),  # Top 3 reasons
            metadata={
                'strategy': self.name,
                'technical_score': technical_signal["score"],
                'ai_score': ai_signal["score"] if ai_signal else None,
                'combined_score': combined_score,
                'ai_available': ai_signal is not None,
                'ai_recommendation': ai_signal.get("recommendation") if ai_signal else None,
                'risk_level': ai_signal.get("risk_level") if ai_signal else "MEDIUM"
            }
        )
    
    def _determine_action(self, score: float, current_position: Optional[Dict]) -> str:
        """Determine trading action based on combined signal score"""
        if current_position and current_position.get('positionAmt', 0) != 0:
            # Check if we should close the current position
            current_side = 'LONG' if float(current_position.get('positionAmt', 0)) > 0 else 'SHORT'
            
            if (current_side == 'LONG' and score < -0.5) or (current_side == 'SHORT' and score > 0.5):
                return 'CLOSE'
        
        # Check for new positions with AI-enhanced thresholds
        if score > 0.6:
            return 'BUY'
        elif score < -0.6:
            return 'SELL'
        else:
            return 'HOLD'

class StrategyManager:
    """Manages multiple trading strategies"""
    
    def __init__(self, config):
        """Initialize strategy manager"""
        self.config = config
        self.strategies = {}
        self.active_strategy = config.STRATEGY_NAME
        
        # Initialize AI analyzer for AI-enhanced features
        self.ai_analyzer = AIAnalyzer()
        
        # Initialize strategies
        self._initialize_strategies()
        
        logger.info(f"Strategy Manager initialized with {len(self.strategies)} strategies")
        logger.info(f"Active strategy: {self.active_strategy}")
        logger.info(f"AI Analyzer available: {self.ai_analyzer.is_available()}")
    
    def _initialize_strategies(self):
        """Initialize all available strategies"""
        strategy_config = self.config.get_strategy_config()
        
        # Multi-indicator strategy
        self.strategies['multi_indicator'] = MultiIndicatorStrategy({
            'enabled': True,
            'min_signal_strength': self.config.MIN_SIGNAL_STRENGTH,
            **strategy_config
        })
        
        # Scalping strategy
        self.strategies['scalping'] = ScalpingStrategy({
            'enabled': True,
            'min_signal_strength': 0.7,
            'profit_target': 0.5,
            'stop_loss': 0.3,
            **strategy_config
        })
        
        # Swing strategy
        self.strategies['swing'] = SwingStrategy({
            'enabled': True,
            'min_signal_strength': 0.6,
            'profit_target': 8.0,
            'stop_loss': 4.0,
            **strategy_config
        })
        
        # AI-Enhanced strategy
        self.strategies['ai_enhanced'] = AIEnhancedStrategy({
            'enabled': True,
            'min_signal_strength': 0.5,
            'ai_weight': 0.6,
            'technical_weight': 0.4,
            'profit_target': 4.0,
            'stop_loss': 2.0,
            **strategy_config
        })
    
    async def generate_signals(self, symbol: str, analysis: TechnicalSignals,
                             current_position: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate trading signals using the active strategy"""
        try:
            if self.active_strategy not in self.strategies:
                logger.error(f"Strategy '{self.active_strategy}' not found")
                return self._default_signals()
            
            strategy = self.strategies[self.active_strategy]
            
            if not strategy.enabled:
                logger.warning(f"Strategy '{self.active_strategy}' is disabled")
                return self._default_signals()
            
            # Generate signal using active strategy
            signal = await strategy.generate_signal(symbol, analysis, current_position)
            
            # Filter by minimum signal strength
            if signal.signal_strength < strategy.min_signal_strength:
                signal.action = 'HOLD'
                signal.reason += " (signal strength too low)"
            
            return {
                'action': signal.action,
                'confidence': signal.confidence,
                'entry_price': signal.entry_price,
                'stop_loss': signal.stop_loss,
                'take_profit': signal.take_profit,
                'signal_strength': signal.signal_strength,
                'reason': signal.reason,
                'strategy': self.active_strategy,
                'metadata': signal.metadata or {}
            }
            
        except Exception as e:
            logger.error(f"Error generating signals for {symbol}: {e}")
            return self._default_signals()
    
    def switch_strategy(self, strategy_name: str) -> bool:
        """Switch to a different strategy"""
        if strategy_name in self.strategies:
            self.active_strategy = strategy_name
            logger.info(f"Switched to strategy: {strategy_name}")
            return True
        else:
            logger.error(f"Strategy '{strategy_name}' not found")
            return False
    
    def get_strategy_status(self) -> Dict[str, Any]:
        """Get status of all strategies"""
        return {
            'active_strategy': self.active_strategy,
            'available_strategies': list(self.strategies.keys()),
            'strategy_details': {
                name: {
                    'enabled': strategy.enabled,
                    'min_signal_strength': strategy.min_signal_strength
                }
                for name, strategy in self.strategies.items()
            }
        }
    
    def _default_signals(self) -> Dict[str, Any]:
        """Return default signals when strategy fails"""
        return {
            'action': 'HOLD',
            'confidence': 0.0,
            'entry_price': None,
            'stop_loss': None,
            'take_profit': None,
            'signal_strength': 0.0,
            'reason': 'Strategy error or disabled',
            'strategy': 'none',
            'metadata': {}
        }

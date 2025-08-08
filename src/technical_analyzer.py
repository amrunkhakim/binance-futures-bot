"""
Technical Analysis Module
Provides comprehensive technical analysis with multiple indicators
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class TechnicalSignals:
    """Data class for technical analysis signals"""
    rsi: float
    rsi_signal: str  # OVERSOLD, OVERBOUGHT, NEUTRAL
    
    macd_line: float
    macd_signal: float
    macd_histogram: float
    macd_signal_type: str  # BULLISH, BEARISH, NEUTRAL
    
    bb_upper: float
    bb_middle: float
    bb_lower: float
    bb_position: str  # UPPER, MIDDLE, LOWER
    bb_squeeze: bool
    
    ema_fast: float
    ema_slow: float
    ema_trend: float
    ema_signal: str  # BULLISH, BEARISH, NEUTRAL
    
    support_level: float
    resistance_level: float
    
    volume_sma: float
    volume_ratio: float
    
    atr: float
    volatility: str  # HIGH, MEDIUM, LOW
    
    overall_signal: str  # STRONG_BUY, BUY, HOLD, SELL, STRONG_SELL
    signal_strength: float  # 0-1

class TechnicalAnalyzer:
    """Technical Analysis Engine"""
    
    def __init__(self):
        """Initialize technical analyzer"""
        self.indicators = {}
    
    async def analyze(self, symbol: str, klines: List[List]) -> TechnicalSignals:
        """Perform comprehensive technical analysis"""
        try:
            # Convert klines to DataFrame
            df = self._klines_to_dataframe(klines)
            
            if df.empty or len(df) < 50:
                logger.warning(f"Insufficient data for {symbol}")
                return self._default_signals()
            
            # Calculate all indicators
            rsi_data = self._calculate_rsi(df, period=14)
            macd_data = self._calculate_macd(df)
            bb_data = self._calculate_bollinger_bands(df)
            ema_data = self._calculate_emas(df)
            support_resistance = self._calculate_support_resistance(df)
            volume_data = self._calculate_volume_indicators(df)
            atr_data = self._calculate_atr(df)
            
            # Generate signals
            signals = TechnicalSignals(
                rsi=rsi_data['rsi'],
                rsi_signal=rsi_data['signal'],
                
                macd_line=macd_data['macd'],
                macd_signal=macd_data['signal'],
                macd_histogram=macd_data['histogram'],
                macd_signal_type=macd_data['signal_type'],
                
                bb_upper=bb_data['upper'],
                bb_middle=bb_data['middle'],
                bb_lower=bb_data['lower'],
                bb_position=bb_data['position'],
                bb_squeeze=bb_data['squeeze'],
                
                ema_fast=ema_data['fast'],
                ema_slow=ema_data['slow'],
                ema_trend=ema_data['trend'],
                ema_signal=ema_data['signal'],
                
                support_level=support_resistance['support'],
                resistance_level=support_resistance['resistance'],
                
                volume_sma=volume_data['sma'],
                volume_ratio=volume_data['ratio'],
                
                atr=atr_data['atr'],
                volatility=atr_data['volatility'],
                
                overall_signal='HOLD',
                signal_strength=0.5
            )
            
            # Generate overall signal
            signals.overall_signal, signals.signal_strength = self._generate_overall_signal(signals)
            
            logger.debug(f"Analysis complete for {symbol}: {signals.overall_signal}")
            return signals
            
        except Exception as e:
            logger.error(f"Technical analysis error for {symbol}: {e}")
            return self._default_signals()
    
    def _klines_to_dataframe(self, klines: List[List]) -> pd.DataFrame:
        """Convert klines data to pandas DataFrame"""
        columns = [
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ]
        
        df = pd.DataFrame(klines, columns=columns)
        
        # Convert to numeric
        numeric_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        return df
    
    def _calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> Dict[str, Any]:
        """Calculate RSI indicator"""
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current_rsi = float(rsi.iloc[-1])
        
        # Generate signal
        if current_rsi < 30:
            signal = 'OVERSOLD'
        elif current_rsi > 70:
            signal = 'OVERBOUGHT'
        else:
            signal = 'NEUTRAL'
        
        return {
            'rsi': current_rsi,
            'signal': signal
        }
    
    def _calculate_macd(self, df: pd.DataFrame, fast: int = 12, 
                       slow: int = 26, signal: int = 9) -> Dict[str, Any]:
        """Calculate MACD indicator"""
        ema_fast = df['close'].ewm(span=fast).mean()
        ema_slow = df['close'].ewm(span=slow).mean()
        
        macd_line = ema_fast - ema_slow
        macd_signal = macd_line.ewm(span=signal).mean()
        macd_histogram = macd_line - macd_signal
        
        current_macd = float(macd_line.iloc[-1])
        current_signal = float(macd_signal.iloc[-1])
        current_histogram = float(macd_histogram.iloc[-1])
        
        # Generate signal
        if current_macd > current_signal and macd_histogram.iloc[-2] < macd_histogram.iloc[-1]:
            signal_type = 'BULLISH'
        elif current_macd < current_signal and macd_histogram.iloc[-2] > macd_histogram.iloc[-1]:
            signal_type = 'BEARISH'
        else:
            signal_type = 'NEUTRAL'
        
        return {
            'macd': current_macd,
            'signal': current_signal,
            'histogram': current_histogram,
            'signal_type': signal_type
        }
    
    def _calculate_bollinger_bands(self, df: pd.DataFrame, period: int = 20, 
                                 std_dev: float = 2) -> Dict[str, Any]:
        """Calculate Bollinger Bands"""
        sma = df['close'].rolling(window=period).mean()
        std = df['close'].rolling(window=period).std()
        
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        current_price = float(df['close'].iloc[-1])
        current_upper = float(upper_band.iloc[-1])
        current_middle = float(sma.iloc[-1])
        current_lower = float(lower_band.iloc[-1])
        
        # Determine position
        if current_price > current_upper * 0.95:
            position = 'UPPER'
        elif current_price < current_lower * 1.05:
            position = 'LOWER'
        else:
            position = 'MIDDLE'
        
        # Check for squeeze
        band_width = (current_upper - current_lower) / current_middle
        avg_width = ((upper_band - lower_band) / sma).rolling(window=20).mean().iloc[-1]
        squeeze = band_width < avg_width * 0.8
        
        return {
            'upper': current_upper,
            'middle': current_middle,
            'lower': current_lower,
            'position': position,
            'squeeze': squeeze
        }
    
    def _calculate_emas(self, df: pd.DataFrame, fast: int = 9, 
                       slow: int = 21, trend: int = 50) -> Dict[str, Any]:
        """Calculate EMA indicators"""
        ema_fast = df['close'].ewm(span=fast).mean()
        ema_slow = df['close'].ewm(span=slow).mean()
        ema_trend = df['close'].ewm(span=trend).mean()
        
        current_fast = float(ema_fast.iloc[-1])
        current_slow = float(ema_slow.iloc[-1])
        current_trend = float(ema_trend.iloc[-1])
        current_price = float(df['close'].iloc[-1])
        
        # Generate signal
        if current_fast > current_slow > current_trend and current_price > current_fast:
            signal = 'BULLISH'
        elif current_fast < current_slow < current_trend and current_price < current_fast:
            signal = 'BEARISH'
        else:
            signal = 'NEUTRAL'
        
        return {
            'fast': current_fast,
            'slow': current_slow,
            'trend': current_trend,
            'signal': signal
        }
    
    def _calculate_support_resistance(self, df: pd.DataFrame, 
                                    lookback: int = 20) -> Dict[str, float]:
        """Calculate support and resistance levels"""
        highs = df['high'].rolling(window=lookback).max()
        lows = df['low'].rolling(window=lookback).min()
        
        # Find pivot points
        recent_data = df.tail(lookback * 2)
        pivot_highs = []
        pivot_lows = []
        
        for i in range(lookback, len(recent_data) - lookback):
            # Check for pivot high
            if (recent_data['high'].iloc[i] > recent_data['high'].iloc[i-lookback:i].max() and
                recent_data['high'].iloc[i] > recent_data['high'].iloc[i+1:i+lookback+1].max()):
                pivot_highs.append(recent_data['high'].iloc[i])
            
            # Check for pivot low
            if (recent_data['low'].iloc[i] < recent_data['low'].iloc[i-lookback:i].min() and
                recent_data['low'].iloc[i] < recent_data['low'].iloc[i+1:i+lookback+1].min()):
                pivot_lows.append(recent_data['low'].iloc[i])
        
        resistance = np.mean(pivot_highs) if pivot_highs else float(highs.iloc[-1])
        support = np.mean(pivot_lows) if pivot_lows else float(lows.iloc[-1])
        
        return {
            'resistance': resistance,
            'support': support
        }
    
    def _calculate_volume_indicators(self, df: pd.DataFrame, 
                                   period: int = 20) -> Dict[str, float]:
        """Calculate volume-based indicators"""
        volume_sma = df['volume'].rolling(window=period).mean()
        current_volume = float(df['volume'].iloc[-1])
        avg_volume = float(volume_sma.iloc[-1])
        
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
        
        return {
            'sma': avg_volume,
            'ratio': volume_ratio
        }
    
    def _calculate_atr(self, df: pd.DataFrame, period: int = 14) -> Dict[str, Any]:
        """Calculate Average True Range"""
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=period).mean()
        
        current_atr = float(atr.iloc[-1])
        current_price = float(df['close'].iloc[-1])
        
        # Determine volatility
        atr_percent = (current_atr / current_price) * 100
        
        if atr_percent > 3:
            volatility = 'HIGH'
        elif atr_percent < 1:
            volatility = 'LOW'
        else:
            volatility = 'MEDIUM'
        
        return {
            'atr': current_atr,
            'volatility': volatility
        }
    
    def _generate_overall_signal(self, signals: TechnicalSignals) -> Tuple[str, float]:
        """Generate overall trading signal based on all indicators"""
        score = 0
        weights = {
            'rsi': 0.15,
            'macd': 0.25,
            'bb': 0.15,
            'ema': 0.25,
            'volume': 0.10,
            'volatility': 0.10
        }
        
        # RSI scoring
        if signals.rsi_signal == 'OVERSOLD':
            score += weights['rsi'] * 0.8  # Bullish
        elif signals.rsi_signal == 'OVERBOUGHT':
            score -= weights['rsi'] * 0.8  # Bearish
        
        # MACD scoring
        if signals.macd_signal_type == 'BULLISH':
            score += weights['macd'] * 1.0
        elif signals.macd_signal_type == 'BEARISH':
            score -= weights['macd'] * 1.0
        
        # Bollinger Bands scoring
        if signals.bb_position == 'LOWER':
            score += weights['bb'] * 0.6
        elif signals.bb_position == 'UPPER':
            score -= weights['bb'] * 0.6
        
        # EMA scoring
        if signals.ema_signal == 'BULLISH':
            score += weights['ema'] * 1.0
        elif signals.ema_signal == 'BEARISH':
            score -= weights['ema'] * 1.0
        
        # Volume scoring
        if signals.volume_ratio > 1.5:
            score += weights['volume'] * 0.5  # High volume supports trend
        elif signals.volume_ratio < 0.5:
            score -= weights['volume'] * 0.3  # Low volume weakens signal
        
        # Volatility adjustment
        if signals.volatility == 'HIGH':
            score *= 0.8  # Reduce confidence in high volatility
        elif signals.volatility == 'LOW':
            score *= 1.1  # Increase confidence in low volatility
        
        # Normalize score to 0-1 range
        signal_strength = abs(score)
        signal_strength = min(signal_strength, 1.0)
        
        # Determine signal
        if score > 0.6:
            return 'STRONG_BUY', signal_strength
        elif score > 0.3:
            return 'BUY', signal_strength
        elif score < -0.6:
            return 'STRONG_SELL', signal_strength
        elif score < -0.3:
            return 'SELL', signal_strength
        else:
            return 'HOLD', signal_strength
    
    def _default_signals(self) -> TechnicalSignals:
        """Return default signals when analysis fails"""
        return TechnicalSignals(
            rsi=50.0,
            rsi_signal='NEUTRAL',
            macd_line=0.0,
            macd_signal=0.0,
            macd_histogram=0.0,
            macd_signal_type='NEUTRAL',
            bb_upper=0.0,
            bb_middle=0.0,
            bb_lower=0.0,
            bb_position='MIDDLE',
            bb_squeeze=False,
            ema_fast=0.0,
            ema_slow=0.0,
            ema_trend=0.0,
            ema_signal='NEUTRAL',
            support_level=0.0,
            resistance_level=0.0,
            volume_sma=0.0,
            volume_ratio=1.0,
            atr=0.0,
            volatility='MEDIUM',
            overall_signal='HOLD',
            signal_strength=0.0
        )

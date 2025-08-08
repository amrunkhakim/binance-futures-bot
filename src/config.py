"""
Configuration settings for Binance Futures Trading Bot
"""

import os
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for trading bot"""
    
    # API Configuration
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', '')
    BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET', '')
    TESTNET = os.getenv('TESTNET', 'True').lower() == 'true'
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///trading_bot.db')
    
    # Trading Configuration
    TRADING_SYMBOLS = [
        'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'DOTUSDT',
        'XRPUSDT', 'LTCUSDT', 'LINKUSDT', 'BCHUSDT', 'XLMUSDT'
    ]
    
    TIMEFRAME = '15m'  # 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d
    SCAN_INTERVAL = 60  # seconds between scans
    
    # Risk Management
    MAX_POSITION_SIZE_PERCENT = 5.0  # Max position size as % of account balance
    MAX_DAILY_LOSS_PERCENT = 2.0     # Max daily loss as % of account balance
    MAX_DRAWDOWN_PERCENT = 10.0      # Max drawdown before stopping
    
    STOP_LOSS_PERCENT = 2.0          # Stop loss as % from entry
    TAKE_PROFIT_PERCENT = 6.0        # Take profit as % from entry
    TRAILING_STOP_PERCENT = 1.5      # Trailing stop as % from peak
    
    # Position Management
    LEVERAGE = 10                    # Max leverage to use
    MIN_TRADE_AMOUNT_USDT = 10       # Minimum trade amount
    CLOSE_POSITIONS_ON_STOP = True   # Close all positions when bot stops
    
    # Technical Analysis
    RSI_OVERSOLD = 30
    RSI_OVERBOUGHT = 70
    RSI_PERIOD = 14
    
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    
    BB_PERIOD = 20
    BB_STD_DEV = 2
    
    EMA_FAST = 9
    EMA_SLOW = 21
    EMA_TREND = 50
    
    # Strategy Configuration
    STRATEGY_NAME = 'multi_indicator'  # multi_indicator, scalping, swing
    MIN_SIGNAL_STRENGTH = 0.6         # Minimum signal strength (0-1)
    
    # Notification Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', '')
    
    SEND_TRADE_ALERTS = True
    SEND_ERROR_ALERTS = True
    SEND_DAILY_REPORT = True
    
    # Backtesting Configuration
    BACKTEST_START_DATE = '2023-01-01'
    BACKTEST_END_DATE = '2024-01-01'
    BACKTEST_INITIAL_BALANCE = 10000  # USDT
    
    @classmethod
    def validate_config(cls) -> List[str]:
        """Validate configuration and return list of errors"""
        errors = []
        
        if not cls.BINANCE_API_KEY:
            errors.append("BINANCE_API_KEY is required")
        
        if not cls.BINANCE_API_SECRET:
            errors.append("BINANCE_API_SECRET is required")
        
        if cls.MAX_POSITION_SIZE_PERCENT <= 0 or cls.MAX_POSITION_SIZE_PERCENT > 100:
            errors.append("MAX_POSITION_SIZE_PERCENT must be between 0 and 100")
        
        if cls.LEVERAGE < 1 or cls.LEVERAGE > 125:
            errors.append("LEVERAGE must be between 1 and 125")
        
        if cls.MIN_SIGNAL_STRENGTH < 0 or cls.MIN_SIGNAL_STRENGTH > 1:
            errors.append("MIN_SIGNAL_STRENGTH must be between 0 and 1")
        
        return errors
    
    @classmethod
    def get_strategy_config(cls) -> Dict[str, Any]:
        """Get strategy-specific configuration"""
        return {
            'rsi': {
                'period': cls.RSI_PERIOD,
                'oversold': cls.RSI_OVERSOLD,
                'overbought': cls.RSI_OVERBOUGHT
            },
            'macd': {
                'fast': cls.MACD_FAST,
                'slow': cls.MACD_SLOW,
                'signal': cls.MACD_SIGNAL
            },
            'bollinger_bands': {
                'period': cls.BB_PERIOD,
                'std_dev': cls.BB_STD_DEV
            },
            'ema': {
                'fast': cls.EMA_FAST,
                'slow': cls.EMA_SLOW,
                'trend': cls.EMA_TREND
            }
        }
    
    @classmethod
    def get_risk_config(cls) -> Dict[str, Any]:
        """Get risk management configuration"""
        return {
            'max_position_size_percent': cls.MAX_POSITION_SIZE_PERCENT,
            'max_daily_loss_percent': cls.MAX_DAILY_LOSS_PERCENT,
            'max_drawdown_percent': cls.MAX_DRAWDOWN_PERCENT,
            'stop_loss_percent': cls.STOP_LOSS_PERCENT,
            'take_profit_percent': cls.TAKE_PROFIT_PERCENT,
            'trailing_stop_percent': cls.TRAILING_STOP_PERCENT
        }

#!/usr/bin/env python3
"""
Binance Futures Trading Bot
Bot otomatis untuk perdagangan Binance Futures dengan analisa teknikal dan manajemen risiko
"""

import asyncio
import logging
import signal
import sys
from datetime import datetime
from typing import Dict, Any
import json

from src.binance_client import BinanceClient
from src.technical_analyzer import TechnicalAnalyzer
from src.risk_manager import RiskManager
from src.strategy_manager import StrategyManager
from src.position_manager import PositionManager
from src.notification_manager import NotificationManager
from src.config import Config
from src.database import DatabaseManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/trading_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class BinanceFuturesBot:
    """Main trading bot class"""
    
    def __init__(self):
        """Initialize bot components"""
        self.config = Config()
        self.running = False
        
        # Initialize components
        self.binance_client = BinanceClient(
            api_key=self.config.BINANCE_API_KEY,
            api_secret=self.config.BINANCE_API_SECRET,
            testnet=self.config.TESTNET
        )
        
        self.technical_analyzer = TechnicalAnalyzer()
        self.risk_manager = RiskManager(self.config)
        self.strategy_manager = StrategyManager(self.config)
        self.position_manager = PositionManager(self.binance_client, self.risk_manager)
        self.notification_manager = NotificationManager(self.config)
        self.database = DatabaseManager(self.config.DATABASE_URL)
        
        logger.info("Bot initialized successfully")
    
    async def start(self):
        """Start the trading bot"""
        logger.info("Starting Binance Futures Trading Bot...")
        
        try:
            # Test API connection
            await self.binance_client.test_connection()
            logger.info("✅ Binance API connection successful")
            
            # Initialize database
            await self.database.initialize()
            logger.info("✅ Database initialized")
            
            # Start main trading loop
            self.running = True
            await self.main_loop()
            
        except Exception as e:
            logger.error(f"❌ Error starting bot: {e}")
            await self.stop()
    
    async def stop(self):
        """Stop the trading bot"""
        logger.info("Stopping trading bot...")
        self.running = False
        
        # Close all positions if configured
        if self.config.CLOSE_POSITIONS_ON_STOP:
            await self.position_manager.close_all_positions()
        
        # Close connections
        await self.binance_client.close()
        await self.database.close()
        
        logger.info("Bot stopped successfully")
    
    async def main_loop(self):
        """Main trading loop"""
        logger.info("Starting main trading loop...")
        
        while self.running:
            try:
                # Get watchlist symbols
                symbols = self.config.TRADING_SYMBOLS
                
                for symbol in symbols:
                    await self.process_symbol(symbol)
                
                # Wait before next cycle
                await asyncio.sleep(self.config.SCAN_INTERVAL)
                
            except Exception as e:
                logger.error(f"❌ Error in main loop: {e}")
                await asyncio.sleep(10)  # Wait before retry
    
    async def process_symbol(self, symbol: str):
        """Process trading signals for a symbol"""
        try:
            # Get market data
            klines = await self.binance_client.get_klines(
                symbol, 
                self.config.TIMEFRAME, 
                limit=500
            )
            
            if not klines:
                logger.warning(f"No data available for {symbol}")
                return
            
            # Perform technical analysis
            analysis = await self.technical_analyzer.analyze(symbol, klines)
            
            # Get current position
            current_position = await self.position_manager.get_position(symbol)
            
            # Generate trading signals
            signals = await self.strategy_manager.generate_signals(
                symbol, analysis, current_position
            )
            
            # Apply risk management
            risk_assessment = await self.risk_manager.assess_risk(
                symbol, signals, current_position
            )
            
            # Execute trades if approved
            if risk_assessment['approved']:
                await self.execute_trades(symbol, signals, risk_assessment)
            
            # Log analysis results
            logger.info(f"📊 {symbol}: Signal={signals.get('action', 'HOLD')}, "
                       f"Risk={risk_assessment['risk_level']}")
            
        except Exception as e:
            logger.error(f"❌ Error processing {symbol}: {e}")
    
    async def execute_trades(self, symbol: str, signals: Dict[str, Any], 
                           risk_assessment: Dict[str, Any]):
        """Execute trading orders"""
        try:
            action = signals.get('action')
            
            if action == 'BUY':
                await self.position_manager.open_long_position(
                    symbol, signals, risk_assessment
                )
            elif action == 'SELL':
                await self.position_manager.open_short_position(
                    symbol, signals, risk_assessment
                )
            elif action == 'CLOSE':
                await self.position_manager.close_position(symbol)
            
        except Exception as e:
            logger.error(f"❌ Error executing trade for {symbol}: {e}")
            await self.notification_manager.send_error_alert(
                f"Trade execution error for {symbol}: {e}"
            )

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info("Received shutdown signal")
    sys.exit(0)

async def main():
    """Main entry point"""
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and start bot
    bot = BinanceFuturesBot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    finally:
        await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())

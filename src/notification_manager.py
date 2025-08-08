"""
Notification Management Module
Handles Telegram, Discord, and other notification services
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class NotificationManager:
    """Centralized notification management"""
    
    def __init__(self, config):
        """Initialize notification manager"""
        self.config = config
        
        # Telegram configuration
        self.telegram_token = config.TELEGRAM_BOT_TOKEN
        self.telegram_chat_id = config.TELEGRAM_CHAT_ID
        
        # Discord configuration
        self.discord_webhook_url = config.DISCORD_WEBHOOK_URL
        
        # Notification settings
        self.send_trade_alerts = config.SEND_TRADE_ALERTS
        self.send_error_alerts = config.SEND_ERROR_ALERTS
        self.send_daily_report = config.SEND_DAILY_REPORT
        
        # Session for HTTP requests
        self.session = None
        
        logger.info("Notification Manager initialized")
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10)
            )
        return self.session
    
    async def close(self):
        """Close notification manager"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def send_trade_alert(self, symbol: str, action: str, 
                             details: Dict[str, Any]):
        """Send trading alert notification"""
        if not self.send_trade_alerts:
            return
        
        try:
            # Format trade message
            message = self._format_trade_message(symbol, action, details)
            
            # Send to all configured channels
            await asyncio.gather(
                self._send_telegram_message(message),
                self._send_discord_message(message, "TRADE"),
                return_exceptions=True
            )
            
        except Exception as e:
            logger.error(f"Error sending trade alert: {e}")
    
    async def send_error_alert(self, error_message: str, context: str = ""):
        """Send error alert notification"""
        if not self.send_error_alerts:
            return
        
        try:
            message = f"🚨 **ERROR ALERT** 🚨\n\n"
            message += f"**Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            message += f"**Context**: {context}\n" if context else ""
            message += f"**Error**: {error_message}"
            
            await asyncio.gather(
                self._send_telegram_message(message),
                self._send_discord_message(message, "ERROR"),
                return_exceptions=True
            )
            
        except Exception as e:
            logger.error(f"Error sending error alert: {e}")
    
    async def send_daily_report(self, report_data: Dict[str, Any]):
        """Send daily trading report"""
        if not self.send_daily_report:
            return
        
        try:
            message = self._format_daily_report(report_data)
            
            await asyncio.gather(
                self._send_telegram_message(message),
                self._send_discord_message(message, "REPORT"),
                return_exceptions=True
            )
            
        except Exception as e:
            logger.error(f"Error sending daily report: {e}")
    
    async def send_position_update(self, symbol: str, position_data: Dict[str, Any]):
        """Send position update notification"""
        try:
            message = self._format_position_message(symbol, position_data)
            
            await asyncio.gather(
                self._send_telegram_message(message),
                self._send_discord_message(message, "POSITION"),
                return_exceptions=True
            )
            
        except Exception as e:
            logger.error(f"Error sending position update: {e}")
    
    async def send_risk_alert(self, alert_type: str, message: str):
        """Send risk management alert"""
        try:
            formatted_message = f"⚠️ **RISK ALERT** ⚠️\n\n"
            formatted_message += f"**Type**: {alert_type}\n"
            formatted_message += f"**Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            formatted_message += f"**Message**: {message}"
            
            await asyncio.gather(
                self._send_telegram_message(formatted_message),
                self._send_discord_message(formatted_message, "RISK"),
                return_exceptions=True
            )
            
        except Exception as e:
            logger.error(f"Error sending risk alert: {e}")
    
    def _format_trade_message(self, symbol: str, action: str, 
                            details: Dict[str, Any]) -> str:
        """Format trade message"""
        emojis = {
            'BUY': '📈',
            'SELL': '📉',
            'CLOSE': '🔒'
        }
        
        emoji = emojis.get(action, '🔄')
        
        message = f"{emoji} **{action} {symbol}** {emoji}\n\n"
        message += f"**Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        if details.get('entry_price'):
            message += f"**Entry Price**: ${details['entry_price']:.4f}\n"
        
        if details.get('position_size'):
            message += f"**Size**: {details['position_size']:.4f}\n"
        
        if details.get('stop_loss'):
            message += f"**Stop Loss**: ${details['stop_loss']:.4f}\n"
        
        if details.get('take_profit'):
            message += f"**Take Profit**: ${details['take_profit']:.4f}\n"
        
        if details.get('leverage'):
            message += f"**Leverage**: {details['leverage']}x\n"
        
        if details.get('reason'):
            message += f"**Reason**: {details['reason']}\n"
        
        if details.get('strategy'):
            message += f"**Strategy**: {details['strategy']}\n"
        
        if details.get('signal_strength'):
            strength_bars = "█" * int(details['signal_strength'] * 10)
            message += f"**Signal Strength**: {strength_bars} ({details['signal_strength']:.2f})"
        
        return message
    
    def _format_position_message(self, symbol: str, 
                               position_data: Dict[str, Any]) -> str:
        """Format position update message"""
        side_emoji = "📈" if position_data.get('side') == 'LONG' else "📉"
        
        message = f"{side_emoji} **Position Update - {symbol}**\n\n"
        message += f"**Side**: {position_data.get('side', 'N/A')}\n"
        message += f"**Size**: {position_data.get('size', 0):.4f}\n"
        message += f"**Entry Price**: ${position_data.get('entry_price', 0):.4f}\n"
        message += f"**Current Price**: ${position_data.get('current_price', 0):.4f}\n"
        
        pnl = position_data.get('unrealized_pnl', 0)
        pnl_emoji = "💚" if pnl >= 0 else "❤️"
        message += f"**Unrealized PnL**: {pnl_emoji} ${pnl:.2f}\n"
        
        if position_data.get('stop_loss'):
            message += f"**Stop Loss**: ${position_data['stop_loss']:.4f}\n"
        
        if position_data.get('take_profit'):
            message += f"**Take Profit**: ${position_data['take_profit']:.4f}\n"
        
        return message
    
    def _format_daily_report(self, report_data: Dict[str, Any]) -> str:
        """Format daily report message"""
        message = "📊 **DAILY TRADING REPORT** 📊\n\n"
        message += f"**Date**: {datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        # Trading statistics
        stats = report_data.get('stats', {})
        message += "**📈 Trading Stats:**\n"
        message += f"• Total Trades: {stats.get('total_trades', 0)}\n"
        message += f"• Winning Trades: {stats.get('winning_trades', 0)}\n"
        message += f"• Losing Trades: {stats.get('losing_trades', 0)}\n"
        message += f"• Win Rate: {stats.get('win_rate', 0):.1f}%\n\n"
        
        # PnL information
        total_pnl = stats.get('total_pnl', 0)
        pnl_emoji = "💚" if total_pnl >= 0 else "❤️"
        message += f"**💰 PnL Summary:**\n"
        message += f"• Total PnL: {pnl_emoji} ${total_pnl:.2f}\n"
        message += f"• Best Trade: ${stats.get('best_trade', 0):.2f}\n"
        message += f"• Worst Trade: ${stats.get('worst_trade', 0):.2f}\n\n"
        
        # Risk metrics
        risk = report_data.get('risk', {})
        message += "**🛡️ Risk Metrics:**\n"
        message += f"• Max Drawdown: {risk.get('max_drawdown', 0):.2f}%\n"
        message += f"• Risk Score: {risk.get('risk_score', 0)}/100\n"
        message += f"• Active Positions: {risk.get('active_positions', 0)}\n\n"
        
        # Performance rating
        performance = self._calculate_performance_rating(stats)
        message += f"**⭐ Performance Rating: {performance}**"
        
        return message
    
    def _calculate_performance_rating(self, stats: Dict[str, Any]) -> str:
        """Calculate performance rating based on stats"""
        win_rate = stats.get('win_rate', 0)
        total_pnl = stats.get('total_pnl', 0)
        profit_factor = stats.get('profit_factor', 0)
        
        score = 0
        
        # Win rate scoring
        if win_rate >= 70:
            score += 3
        elif win_rate >= 50:
            score += 2
        elif win_rate >= 30:
            score += 1
        
        # PnL scoring
        if total_pnl > 0:
            score += 2
        elif total_pnl >= -50:
            score += 1
        
        # Profit factor scoring
        if profit_factor >= 2.0:
            score += 2
        elif profit_factor >= 1.5:
            score += 1
        
        # Rating based on total score
        if score >= 6:
            return "⭐⭐⭐⭐⭐ EXCELLENT"
        elif score >= 5:
            return "⭐⭐⭐⭐ GOOD"
        elif score >= 3:
            return "⭐⭐⭐ AVERAGE"
        elif score >= 2:
            return "⭐⭐ POOR"
        else:
            return "⭐ VERY POOR"
    
    async def _send_telegram_message(self, message: str) -> bool:
        """Send message via Telegram"""
        if not self.telegram_token or not self.telegram_chat_id:
            return False
        
        try:
            session = await self._get_session()
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            
            data = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'Markdown'
            }
            
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    logger.debug("Telegram message sent successfully")
                    return True
                else:
                    logger.error(f"Telegram API error: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
    
    async def _send_discord_message(self, message: str, 
                                  message_type: str = "INFO") -> bool:
        """Send message via Discord webhook"""
        if not self.discord_webhook_url:
            return False
        
        try:
            session = await self._get_session()
            
            # Color mapping for different message types
            colors = {
                'TRADE': 0x00FF00,    # Green
                'ERROR': 0xFF0000,    # Red
                'RISK': 0xFF8C00,     # Orange
                'REPORT': 0x0080FF,   # Blue
                'POSITION': 0x8B00FF   # Purple
            }
            
            embed = {
                'title': f"{message_type} - Binance Futures Bot",
                'description': message,
                'color': colors.get(message_type, 0x808080),
                'timestamp': datetime.now().isoformat(),
                'footer': {
                    'text': 'Binance Futures Trading Bot'
                }
            }
            
            data = {
                'embeds': [embed]
            }
            
            async with session.post(
                self.discord_webhook_url,
                data=json.dumps(data),
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status == 204:  # Discord webhook success code
                    logger.debug("Discord message sent successfully")
                    return True
                else:
                    logger.error(f"Discord webhook error: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error sending Discord message: {e}")
            return False
    
    async def send_startup_message(self):
        """Send bot startup notification"""
        message = "🚀 **TRADING BOT STARTED** 🚀\n\n"
        message += f"**Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        message += "**Status**: Bot is now active and monitoring markets\n"
        message += "**Mode**: Testnet" if self.config.TESTNET else "**Mode**: Live Trading"
        
        await asyncio.gather(
            self._send_telegram_message(message),
            self._send_discord_message(message, "INFO"),
            return_exceptions=True
        )
    
    async def send_shutdown_message(self):
        """Send bot shutdown notification"""
        message = "🛑 **TRADING BOT STOPPED** 🛑\n\n"
        message += f"**Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        message += "**Status**: Bot has been shut down"
        
        await asyncio.gather(
            self._send_telegram_message(message),
            self._send_discord_message(message, "INFO"),
            return_exceptions=True
        )

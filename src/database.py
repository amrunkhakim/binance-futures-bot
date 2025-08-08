"""
Database Management Module
Handles data persistence for trading bot
"""

import asyncio
import aiosqlite
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Database management for trading bot data"""
    
    def __init__(self, database_url: str):
        """Initialize database manager"""
        self.database_path = database_url.replace('sqlite:///', '')
        self.connection = None
        
        logger.info(f"Database Manager initialized: {self.database_path}")
    
    async def initialize(self):
        """Initialize database schema"""
        try:
            self.connection = await aiosqlite.connect(self.database_path)
            await self._create_tables()
            logger.info("✅ Database initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            raise
    
    async def close(self):
        """Close database connection"""
        if self.connection:
            await self.connection.close()
            logger.info("Database connection closed")
    
    async def _create_tables(self):
        """Create database tables"""
        
        # Trades table
        await self.connection.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                side TEXT NOT NULL,
                entry_price REAL NOT NULL,
                exit_price REAL,
                quantity REAL NOT NULL,
                leverage INTEGER,
                entry_time TIMESTAMP NOT NULL,
                exit_time TIMESTAMP,
                realized_pnl REAL,
                unrealized_pnl REAL,
                stop_loss REAL,
                take_profit REAL,
                strategy TEXT,
                reason TEXT,
                status TEXT DEFAULT 'OPEN',
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Orders table
        await self.connection.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trade_id INTEGER,
                symbol TEXT NOT NULL,
                order_id TEXT UNIQUE,
                side TEXT NOT NULL,
                order_type TEXT NOT NULL,
                quantity REAL NOT NULL,
                price REAL,
                status TEXT NOT NULL,
                filled_quantity REAL DEFAULT 0,
                avg_price REAL DEFAULT 0,
                commission REAL DEFAULT 0,
                order_time TIMESTAMP NOT NULL,
                update_time TIMESTAMP,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (trade_id) REFERENCES trades (id)
            )
        ''')
        
        # Signals table
        await self.connection.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                action TEXT NOT NULL,
                signal_strength REAL NOT NULL,
                confidence REAL NOT NULL,
                entry_price REAL,
                stop_loss REAL,
                take_profit REAL,
                strategy TEXT NOT NULL,
                reason TEXT,
                rsi REAL,
                macd_line REAL,
                macd_signal REAL,
                macd_histogram REAL,
                bb_position TEXT,
                ema_signal TEXT,
                volume_ratio REAL,
                volatility TEXT,
                executed BOOLEAN DEFAULT FALSE,
                signal_time TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Risk events table
        await self.connection.execute('''
            CREATE TABLE IF NOT EXISTS risk_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                symbol TEXT,
                risk_level TEXT NOT NULL,
                risk_score REAL,
                description TEXT,
                action_taken TEXT,
                event_time TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Daily stats table
        await self.connection.execute('''
            CREATE TABLE IF NOT EXISTS daily_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE NOT NULL,
                total_trades INTEGER DEFAULT 0,
                winning_trades INTEGER DEFAULT 0,
                losing_trades INTEGER DEFAULT 0,
                total_pnl REAL DEFAULT 0,
                max_drawdown REAL DEFAULT 0,
                win_rate REAL DEFAULT 0,
                profit_factor REAL DEFAULT 0,
                best_trade REAL DEFAULT 0,
                worst_trade REAL DEFAULT 0,
                total_volume REAL DEFAULT 0,
                account_balance REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Bot performance table
        await self.connection.execute('''
            CREATE TABLE IF NOT EXISTS bot_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP NOT NULL,
                account_balance REAL,
                total_pnl REAL,
                unrealized_pnl REAL,
                open_positions INTEGER DEFAULT 0,
                daily_pnl REAL DEFAULT 0,
                risk_score REAL DEFAULT 0,
                active_strategy TEXT,
                market_condition TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        await self.connection.commit()
        logger.info("Database tables created successfully")
    
    async def save_trade(self, trade_data: Dict[str, Any]) -> int:
        """Save trade to database"""
        try:
            query = '''
                INSERT INTO trades (
                    symbol, side, entry_price, quantity, leverage,
                    entry_time, stop_loss, take_profit, strategy,
                    reason, status, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            cursor = await self.connection.execute(query, (
                trade_data['symbol'],
                trade_data['side'],
                trade_data['entry_price'],
                trade_data['quantity'],
                trade_data.get('leverage', 1),
                trade_data.get('entry_time', datetime.now()),
                trade_data.get('stop_loss'),
                trade_data.get('take_profit'),
                trade_data.get('strategy', ''),
                trade_data.get('reason', ''),
                'OPEN',
                json.dumps(trade_data.get('metadata', {}))
            ))
            
            await self.connection.commit()
            trade_id = cursor.lastrowid
            
            logger.debug(f"Trade saved with ID: {trade_id}")
            return trade_id
            
        except Exception as e:
            logger.error(f"Error saving trade: {e}")
            return 0
    
    async def update_trade(self, trade_id: int, updates: Dict[str, Any]) -> bool:
        """Update existing trade"""
        try:
            # Build dynamic update query
            fields = []
            values = []
            
            for field, value in updates.items():
                if field == 'metadata':
                    fields.append(f"{field} = ?")
                    values.append(json.dumps(value))
                else:
                    fields.append(f"{field} = ?")
                    values.append(value)
            
            if not fields:
                return False
            
            query = f"UPDATE trades SET {', '.join(fields)} WHERE id = ?"
            values.append(trade_id)
            
            await self.connection.execute(query, values)
            await self.connection.commit()
            
            logger.debug(f"Trade {trade_id} updated")
            return True
            
        except Exception as e:
            logger.error(f"Error updating trade {trade_id}: {e}")
            return False
    
    async def save_signal(self, signal_data: Dict[str, Any]) -> int:
        """Save trading signal to database"""
        try:
            query = '''
                INSERT INTO signals (
                    symbol, action, signal_strength, confidence,
                    entry_price, stop_loss, take_profit, strategy,
                    reason, rsi, macd_line, macd_signal, macd_histogram,
                    bb_position, ema_signal, volume_ratio, volatility,
                    signal_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            cursor = await self.connection.execute(query, (
                signal_data['symbol'],
                signal_data['action'],
                signal_data.get('signal_strength', 0),
                signal_data.get('confidence', 0),
                signal_data.get('entry_price'),
                signal_data.get('stop_loss'),
                signal_data.get('take_profit'),
                signal_data.get('strategy', ''),
                signal_data.get('reason', ''),
                signal_data.get('rsi'),
                signal_data.get('macd_line'),
                signal_data.get('macd_signal'),
                signal_data.get('macd_histogram'),
                signal_data.get('bb_position'),
                signal_data.get('ema_signal'),
                signal_data.get('volume_ratio'),
                signal_data.get('volatility'),
                signal_data.get('signal_time', datetime.now())
            ))
            
            await self.connection.commit()
            signal_id = cursor.lastrowid
            
            logger.debug(f"Signal saved with ID: {signal_id}")
            return signal_id
            
        except Exception as e:
            logger.error(f"Error saving signal: {e}")
            return 0
    
    async def save_risk_event(self, risk_data: Dict[str, Any]) -> int:
        """Save risk management event"""
        try:
            query = '''
                INSERT INTO risk_events (
                    event_type, symbol, risk_level, risk_score,
                    description, action_taken, event_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            
            cursor = await self.connection.execute(query, (
                risk_data['event_type'],
                risk_data.get('symbol'),
                risk_data['risk_level'],
                risk_data.get('risk_score', 0),
                risk_data.get('description', ''),
                risk_data.get('action_taken', ''),
                risk_data.get('event_time', datetime.now())
            ))
            
            await self.connection.commit()
            event_id = cursor.lastrowid
            
            logger.debug(f"Risk event saved with ID: {event_id}")
            return event_id
            
        except Exception as e:
            logger.error(f"Error saving risk event: {e}")
            return 0
    
    async def update_daily_stats(self, date_str: str, stats: Dict[str, Any]) -> bool:
        """Update daily statistics"""
        try:
            # Check if record exists
            cursor = await self.connection.execute(
                "SELECT id FROM daily_stats WHERE date = ?", (date_str,)
            )
            existing = await cursor.fetchone()
            
            if existing:
                # Update existing record
                fields = []
                values = []
                
                for field, value in stats.items():
                    fields.append(f"{field} = ?")
                    values.append(value)
                
                if fields:
                    query = f"UPDATE daily_stats SET {', '.join(fields)} WHERE date = ?"
                    values.append(date_str)
                    await self.connection.execute(query, values)
            else:
                # Insert new record
                query = '''
                    INSERT INTO daily_stats (
                        date, total_trades, winning_trades, losing_trades,
                        total_pnl, max_drawdown, win_rate, profit_factor,
                        best_trade, worst_trade, total_volume, account_balance
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                
                await self.connection.execute(query, (
                    date_str,
                    stats.get('total_trades', 0),
                    stats.get('winning_trades', 0),
                    stats.get('losing_trades', 0),
                    stats.get('total_pnl', 0),
                    stats.get('max_drawdown', 0),
                    stats.get('win_rate', 0),
                    stats.get('profit_factor', 0),
                    stats.get('best_trade', 0),
                    stats.get('worst_trade', 0),
                    stats.get('total_volume', 0),
                    stats.get('account_balance', 0)
                ))
            
            await self.connection.commit()
            logger.debug(f"Daily stats updated for {date_str}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating daily stats: {e}")
            return False
    
    async def save_bot_performance(self, performance_data: Dict[str, Any]) -> int:
        """Save bot performance snapshot"""
        try:
            query = '''
                INSERT INTO bot_performance (
                    timestamp, account_balance, total_pnl, unrealized_pnl,
                    open_positions, daily_pnl, risk_score, active_strategy,
                    market_condition
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            
            cursor = await self.connection.execute(query, (
                performance_data.get('timestamp', datetime.now()),
                performance_data.get('account_balance', 0),
                performance_data.get('total_pnl', 0),
                performance_data.get('unrealized_pnl', 0),
                performance_data.get('open_positions', 0),
                performance_data.get('daily_pnl', 0),
                performance_data.get('risk_score', 0),
                performance_data.get('active_strategy', ''),
                performance_data.get('market_condition', 'NORMAL')
            ))
            
            await self.connection.commit()
            performance_id = cursor.lastrowid
            
            logger.debug(f"Bot performance saved with ID: {performance_id}")
            return performance_id
            
        except Exception as e:
            logger.error(f"Error saving bot performance: {e}")
            return 0
    
    async def get_trades(self, symbol: Optional[str] = None,
                        days: int = 30, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get trades from database"""
        try:
            query = "SELECT * FROM trades WHERE 1=1"
            params = []
            
            if symbol:
                query += " AND symbol = ?"
                params.append(symbol)
            
            if status:
                query += " AND status = ?"
                params.append(status)
            
            # Date filter
            cutoff_date = datetime.now() - timedelta(days=days)
            query += " AND entry_time >= ?"
            params.append(cutoff_date)
            
            query += " ORDER BY entry_time DESC"
            
            cursor = await self.connection.execute(query, params)
            rows = await cursor.fetchall()
            
            trades = []
            for row in rows:
                trade = dict(row)
                if trade.get('metadata'):
                    trade['metadata'] = json.loads(trade['metadata'])
                trades.append(trade)
            
            return trades
            
        except Exception as e:
            logger.error(f"Error getting trades: {e}")
            return []
    
    async def get_signals(self, symbol: Optional[str] = None,
                         days: int = 7) -> List[Dict[str, Any]]:
        """Get signals from database"""
        try:
            query = "SELECT * FROM signals WHERE 1=1"
            params = []
            
            if symbol:
                query += " AND symbol = ?"
                params.append(symbol)
            
            # Date filter
            cutoff_date = datetime.now() - timedelta(days=days)
            query += " AND signal_time >= ?"
            params.append(cutoff_date)
            
            query += " ORDER BY signal_time DESC"
            
            cursor = await self.connection.execute(query, params)
            rows = await cursor.fetchall()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Error getting signals: {e}")
            return []
    
    async def get_daily_stats(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get daily statistics"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            cutoff_str = cutoff_date.strftime('%Y-%m-%d')
            
            cursor = await self.connection.execute(
                "SELECT * FROM daily_stats WHERE date >= ? ORDER BY date DESC",
                (cutoff_str,)
            )
            rows = await cursor.fetchall()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Error getting daily stats: {e}")
            return []
    
    async def get_performance_history(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get bot performance history"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            cursor = await self.connection.execute(
                "SELECT * FROM bot_performance WHERE timestamp >= ? ORDER BY timestamp DESC",
                (cutoff_time,)
            )
            rows = await cursor.fetchall()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Error getting performance history: {e}")
            return []
    
    async def cleanup_old_data(self, days_to_keep: int = 90):
        """Clean up old data from database"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            # Clean old closed trades
            await self.connection.execute(
                "DELETE FROM trades WHERE exit_time < ? AND status = 'CLOSED'",
                (cutoff_date,)
            )
            
            # Clean old signals
            await self.connection.execute(
                "DELETE FROM signals WHERE signal_time < ?",
                (cutoff_date,)
            )
            
            # Clean old performance data
            await self.connection.execute(
                "DELETE FROM bot_performance WHERE timestamp < ?",
                (cutoff_date,)
            )
            
            await self.connection.commit()
            logger.info(f"Cleaned up data older than {days_to_keep} days")
            
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
    
    async def get_trading_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get trading summary statistics"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Get trade statistics
            cursor = await self.connection.execute('''
                SELECT 
                    COUNT(*) as total_trades,
                    SUM(CASE WHEN realized_pnl > 0 THEN 1 ELSE 0 END) as winning_trades,
                    SUM(CASE WHEN realized_pnl < 0 THEN 1 ELSE 0 END) as losing_trades,
                    SUM(realized_pnl) as total_pnl,
                    AVG(realized_pnl) as avg_pnl,
                    MAX(realized_pnl) as best_trade,
                    MIN(realized_pnl) as worst_trade
                FROM trades 
                WHERE exit_time >= ? AND status = 'CLOSED'
            ''', (cutoff_date,))
            
            stats = dict(await cursor.fetchone())
            
            # Calculate additional metrics
            if stats['total_trades'] > 0:
                stats['win_rate'] = (stats['winning_trades'] / stats['total_trades']) * 100
            else:
                stats['win_rate'] = 0
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting trading summary: {e}")
            return {}

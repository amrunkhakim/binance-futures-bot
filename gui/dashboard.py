"""
Dashboard Panel for Bot Overview
Shows key metrics, bot status, and performance summary
"""

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from datetime import datetime
from typing import Dict, Any
import threading
import time

class DashboardFrame(ctk.CTkFrame):
    """Main dashboard showing bot overview and key metrics"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.metrics_data = {
            'total_trades': 0,
            'winning_trades': 0,
            'total_pnl': 0.0,
            'daily_pnl': 0.0,
            'active_positions': 0,
            'account_balance': 0.0,
            'win_rate': 0.0
        }
        
        self.create_dashboard()
        
        # Start auto-refresh
        self.start_refresh_timer()
    
    def create_dashboard(self):
        """Create dashboard layout"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="📊 Trading Dashboard",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        # Create sections
        self.create_status_section()
        self.create_metrics_section()
        self.create_quick_stats_section()
    
    def create_status_section(self):
        """Create bot status section"""
        status_frame = ctk.CTkFrame(self)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        # Section title
        status_title = ctk.CTkLabel(
            status_frame,
            text="🤖 Bot Status",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        status_title.pack(pady=10)
        
        # Status cards container
        cards_frame = ctk.CTkFrame(status_frame)
        cards_frame.pack(fill="x", padx=10, pady=10)
        
        # Bot Status Card
        self.create_status_card(
            cards_frame, "Bot Status", "🔴 Stopped", "red", 0
        )
        
        # Trading Mode Card
        self.create_status_card(
            cards_frame, "Trading Mode", "🧪 Testnet", "yellow", 1
        )
        
        # Active Strategy Card
        self.create_status_card(
            cards_frame, "Strategy", "📊 Multi-Indicator", "blue", 2
        )
        
        # Last Update Card
        self.create_status_card(
            cards_frame, "Last Update", "⏰ Never", "gray", 3
        )
    
    def create_status_card(self, parent, title, value, color, column):
        """Create a status card"""
        card = ctk.CTkFrame(parent)
        card.grid(row=0, column=column, padx=5, pady=5, sticky="ew")
        parent.grid_columnconfigure(column, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        title_label.pack(pady=(10, 5))
        
        # Value
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=14),
            text_color=color
        )
        value_label.pack(pady=(0, 10))
        
        # Store reference for updates
        setattr(self, f"status_{column}_value", value_label)
    
    def create_metrics_section(self):
        """Create performance metrics section"""
        metrics_frame = ctk.CTkFrame(self)
        metrics_frame.pack(fill="x", padx=20, pady=10)
        
        # Section title
        metrics_title = ctk.CTkLabel(
            metrics_frame,
            text="📈 Performance Metrics",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        metrics_title.pack(pady=10)
        
        # Metrics grid
        grid_frame = ctk.CTkFrame(metrics_frame)
        grid_frame.pack(fill="x", padx=10, pady=10)
        
        # Row 1
        self.create_metric_card(grid_frame, "Total Trades", "0", 0, 0)
        self.create_metric_card(grid_frame, "Winning Trades", "0", 0, 1)
        self.create_metric_card(grid_frame, "Win Rate", "0.0%", 0, 2)
        self.create_metric_card(grid_frame, "Active Positions", "0", 0, 3)
        
        # Row 2  
        self.create_metric_card(grid_frame, "Total PnL", "$0.00", 1, 0)
        self.create_metric_card(grid_frame, "Daily PnL", "$0.00", 1, 1)
        self.create_metric_card(grid_frame, "Account Balance", "$0.00", 1, 2)
        self.create_metric_card(grid_frame, "Risk Score", "0/100", 1, 3)
    
    def create_metric_card(self, parent, title, value, row, column):
        """Create a metric card"""
        card = ctk.CTkFrame(parent)
        card.grid(row=row, column=column, padx=5, pady=5, sticky="ew")
        parent.grid_columnconfigure(column, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        title_label.pack(pady=(8, 2))
        
        # Value
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        value_label.pack(pady=(2, 8))
        
        # Store reference for updates
        metric_key = title.lower().replace(" ", "_")
        setattr(self, f"metric_{metric_key}", value_label)
    
    def create_quick_stats_section(self):
        """Create quick statistics section"""
        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Section title
        stats_title = ctk.CTkLabel(
            stats_frame,
            text="⚡ Quick Stats",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        stats_title.pack(pady=10)
        
        # Create two columns
        columns_frame = ctk.CTkFrame(stats_frame)
        columns_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left column - Recent Activity
        left_column = ctk.CTkFrame(columns_frame)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        activity_title = ctk.CTkLabel(
            left_column,
            text="📋 Recent Activity",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        activity_title.pack(pady=(10, 5))
        
        # Activity list
        self.activity_text = ctk.CTkTextbox(
            left_column,
            height=200,
            font=ctk.CTkFont(size=11)
        )
        self.activity_text.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        # Add initial message
        self.activity_text.insert("1.0", "No recent activity...\n")
        self.activity_text.configure(state="disabled")
        
        # Right column - Market Overview
        right_column = ctk.CTkFrame(columns_frame)
        right_column.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        market_title = ctk.CTkLabel(
            right_column,
            text="🌍 Market Overview",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        market_title.pack(pady=(10, 5))
        
        # Market data
        self.market_text = ctk.CTkTextbox(
            right_column,
            height=200,
            font=ctk.CTkFont(size=11)
        )
        self.market_text.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        # Add initial message
        self.market_text.insert("1.0", "Loading market data...\n")
        self.market_text.configure(state="disabled")
    
    def update_status(self, bot_running=False, trading_mode="Testnet", 
                     strategy="Multi-Indicator", last_update=None):
        """Update status section"""
        try:
            # Bot Status
            status = "🟢 Running" if bot_running else "🔴 Stopped"
            color = "green" if bot_running else "red"
            self.status_0_value.configure(text=status, text_color=color)
            
            # Trading Mode
            mode_emoji = "🧪" if trading_mode == "Testnet" else "🔥"
            self.status_1_value.configure(text=f"{mode_emoji} {trading_mode}")
            
            # Strategy
            self.status_2_value.configure(text=f"📊 {strategy}")
            
            # Last Update
            if last_update:
                time_str = last_update.strftime("%H:%M:%S")
                self.status_3_value.configure(text=f"⏰ {time_str}")
            
        except AttributeError:
            pass  # Labels may not be created yet
    
    def update_metrics(self, metrics_data: Dict[str, Any]):
        """Update performance metrics"""
        try:
            # Update stored data
            self.metrics_data.update(metrics_data)
            
            # Update UI labels
            self.metric_total_trades.configure(text=str(self.metrics_data['total_trades']))
            self.metric_winning_trades.configure(text=str(self.metrics_data['winning_trades']))
            
            win_rate = self.metrics_data['win_rate']
            self.metric_win_rate.configure(text=f"{win_rate:.1f}%")
            
            self.metric_active_positions.configure(text=str(self.metrics_data['active_positions']))
            
            # PnL with colors
            total_pnl = self.metrics_data['total_pnl']
            pnl_color = "green" if total_pnl >= 0 else "red"
            self.metric_total_pnl.configure(
                text=f"${total_pnl:.2f}", 
                text_color=pnl_color
            )
            
            daily_pnl = self.metrics_data['daily_pnl']
            daily_color = "green" if daily_pnl >= 0 else "red"
            self.metric_daily_pnl.configure(
                text=f"${daily_pnl:.2f}",
                text_color=daily_color
            )
            
            balance = self.metrics_data['account_balance']
            self.metric_account_balance.configure(text=f"${balance:.2f}")
            
            # Risk Score
            risk_score = self.metrics_data.get('risk_score', 0)
            risk_color = "green" if risk_score < 30 else "yellow" if risk_score < 70 else "red"
            self.metric_risk_score.configure(
                text=f"{risk_score}/100",
                text_color=risk_color
            )
            
        except AttributeError:
            pass  # Labels may not be created yet
    
    def add_activity(self, message: str):
        """Add activity to recent activity log"""
        try:
            current_time = datetime.now().strftime("%H:%M:%S")
            activity_message = f"[{current_time}] {message}\n"
            
            # Enable text widget, add message, disable again
            self.activity_text.configure(state="normal")
            
            # Add to beginning
            self.activity_text.insert("1.0", activity_message)
            
            # Keep only last 20 lines
            lines = self.activity_text.get("1.0", "end").split("\n")
            if len(lines) > 21:  # 20 + 1 for empty line at end
                self.activity_text.delete("21.0", "end")
            
            self.activity_text.configure(state="disabled")
            
        except AttributeError:
            pass
    
    def update_market_overview(self, market_data: Dict[str, Any]):
        """Update market overview"""
        try:
            self.market_text.configure(state="normal")
            self.market_text.delete("1.0", "end")
            
            # Add market data
            for symbol, data in market_data.items():
                price = data.get('price', 0)
                change = data.get('change_24h', 0)
                change_color = "📈" if change >= 0 else "📉"
                
                line = f"{symbol}: ${price:.2f} {change_color} {change:+.2f}%\n"
                self.market_text.insert("end", line)
            
            self.market_text.configure(state="disabled")
            
        except AttributeError:
            pass
    
    def start_refresh_timer(self):
        """Start auto-refresh timer"""
        def refresh_loop():
            while True:
                try:
                    # Update last update time
                    self.update_status(last_update=datetime.now())
                    time.sleep(1)
                except:
                    break
        
        refresh_thread = threading.Thread(target=refresh_loop, daemon=True)
        refresh_thread.start()
    
    def update_data(self, symbol: str, signals: Dict[str, Any], 
                   risk_assessment: Dict[str, Any]):
        """Update dashboard with latest trading data"""
        # Add trading activity
        action = signals.get('action', 'HOLD')
        if action != 'HOLD':
            signal_strength = signals.get('signal_strength', 0)
            message = f"{action} signal for {symbol} (strength: {signal_strength:.2f})"
            self.add_activity(message)
        
        # Update risk score
        risk_score = risk_assessment.get('risk_score', 0)
        self.update_metrics({'risk_score': risk_score})

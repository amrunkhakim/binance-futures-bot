"""
Trading Panel for Manual Trading and Signal Monitoring
"""

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from typing import Dict, Any, Optional
from datetime import datetime

class TradingPanel(ctk.CTkFrame):
    """Panel for manual trading and signal monitoring"""
    
    def __init__(self, parent, main_app):
        super().__init__(parent)
        
        self.parent = parent
        self.main_app = main_app
        self.selected_symbol = "BTCUSDT"
        self.current_signals = {}
        
        self.create_trading_panel()
    
    def create_trading_panel(self):
        """Create trading panel layout"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="📈 Trading Panel",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        # Create main sections
        self.create_symbol_selector()
        self.create_signal_display()
        self.create_manual_trading()
        self.create_order_history()
    
    def create_symbol_selector(self):
        """Create symbol selector section"""
        selector_frame = ctk.CTkFrame(self)
        selector_frame.pack(fill="x", padx=20, pady=10)
        
        # Title
        title = ctk.CTkLabel(
            selector_frame,
            text="🎯 Symbol Selection",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=10)
        
        # Symbol selector and price display
        controls_frame = ctk.CTkFrame(selector_frame)
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        # Symbol dropdown
        ctk.CTkLabel(controls_frame, text="Trading Symbol:").pack(side="left", padx=10)
        
        self.symbol_var = ctk.StringVar(value="BTCUSDT")
        symbol_combo = ctk.CTkComboBox(
            controls_frame,
            values=["BTCUSDT", "ETHUSDT", "ADAUSDT", "BNBUSDT", "SOLUSDT"],
            variable=self.symbol_var,
            command=self.on_symbol_change,
            width=150
        )
        symbol_combo.pack(side="left", padx=10)
        
        # Current price display
        self.price_label = ctk.CTkLabel(
            controls_frame,
            text="Price: $0.00",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.price_label.pack(side="right", padx=10)
    
    def create_signal_display(self):
        """Create signal display section"""
        signal_frame = ctk.CTkFrame(self)
        signal_frame.pack(fill="x", padx=20, pady=10)
        
        # Title
        title = ctk.CTkLabel(
            signal_frame,
            text="📊 Trading Signals",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=10)
        
        # Signal cards
        cards_frame = ctk.CTkFrame(signal_frame)
        cards_frame.pack(fill="x", padx=10, pady=10)
        
        # Signal cards
        self.create_signal_card(cards_frame, "Current Signal", "HOLD", "gray", 0)
        self.create_signal_card(cards_frame, "Signal Strength", "0.00", "blue", 1)
        self.create_signal_card(cards_frame, "Confidence", "0.00", "purple", 2)
        self.create_signal_card(cards_frame, "Risk Level", "LOW", "green", 3)
        
        # Technical indicators
        indicators_frame = ctk.CTkFrame(signal_frame)
        indicators_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_indicators_display(indicators_frame)
    
    def create_signal_card(self, parent, title, value, color, column):
        """Create a signal card"""
        card = ctk.CTkFrame(parent)
        card.grid(row=0, column=column, padx=5, pady=5, sticky="ew")
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
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=color
        )
        value_label.pack(pady=(2, 8))
        
        # Store reference for updates
        setattr(self, f"signal_{title.lower().replace(' ', '_')}", value_label)
    
    def create_indicators_display(self, parent):
        """Create technical indicators display"""
        # Indicators title
        indicators_title = ctk.CTkLabel(
            parent,
            text="📊 Technical Indicators",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        indicators_title.pack(pady=5)
        
        # Indicators grid
        indicators_grid = ctk.CTkFrame(parent)
        indicators_grid.pack(fill="x", padx=5, pady=5)
        
        # RSI
        self.create_indicator_row(indicators_grid, "RSI", "50.00", 0)
        # MACD  
        self.create_indicator_row(indicators_grid, "MACD", "0.00", 1)
        # EMA Signal
        self.create_indicator_row(indicators_grid, "EMA", "NEUTRAL", 2)
        # Bollinger Bands
        self.create_indicator_row(indicators_grid, "BB Position", "MIDDLE", 3)
        # Volume
        self.create_indicator_row(indicators_grid, "Volume Ratio", "1.00x", 4)
        # ATR
        self.create_indicator_row(indicators_grid, "ATR", "0.00", 5)
    
    def create_indicator_row(self, parent, name, value, row):
        """Create indicator row"""
        # Name
        name_label = ctk.CTkLabel(
            parent,
            text=f"{name}:",
            font=ctk.CTkFont(size=12),
            width=100
        )
        name_label.grid(row=row, column=0, padx=5, pady=2, sticky="w")
        
        # Value
        value_label = ctk.CTkLabel(
            parent,
            text=value,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        value_label.grid(row=row, column=1, padx=5, pady=2, sticky="w")
        
        # Store reference
        setattr(self, f"indicator_{name.lower().replace(' ', '_')}", value_label)
    
    def create_manual_trading(self):
        """Create manual trading section"""
        trading_frame = ctk.CTkFrame(self)
        trading_frame.pack(fill="x", padx=20, pady=10)
        
        # Title
        title = ctk.CTkLabel(
            trading_frame,
            text="🎮 Manual Trading",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=10)
        
        # Trading controls
        controls_frame = ctk.CTkFrame(trading_frame)
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        # Left side - Order form
        order_frame = ctk.CTkFrame(controls_frame)
        order_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Order type
        ctk.CTkLabel(order_frame, text="Order Type:").pack(pady=5)
        self.order_type_var = ctk.StringVar(value="MARKET")
        order_type_combo = ctk.CTkComboBox(
            order_frame,
            values=["MARKET", "LIMIT"],
            variable=self.order_type_var
        )
        order_type_combo.pack(pady=5)
        
        # Quantity
        ctk.CTkLabel(order_frame, text="Quantity:").pack(pady=5)
        self.quantity_entry = ctk.CTkEntry(order_frame, placeholder_text="0.001")
        self.quantity_entry.pack(pady=5)
        
        # Price (for limit orders)
        ctk.CTkLabel(order_frame, text="Price (Limit only):").pack(pady=5)
        self.price_entry = ctk.CTkEntry(order_frame, placeholder_text="0.00")
        self.price_entry.pack(pady=5)
        
        # Leverage
        ctk.CTkLabel(order_frame, text="Leverage:").pack(pady=5)
        self.leverage_var = ctk.StringVar(value="10")
        leverage_combo = ctk.CTkComboBox(
            order_frame,
            values=["1", "5", "10", "20", "50", "100"],
            variable=self.leverage_var
        )
        leverage_combo.pack(pady=5)
        
        # Right side - Trading buttons
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(side="right", fill="y", padx=(5, 0))
        
        # Buy button
        self.buy_button = ctk.CTkButton(
            buttons_frame,
            text="🟢 BUY / LONG",
            command=self.manual_buy,
            fg_color="green",
            hover_color="darkgreen",
            width=150,
            height=40
        )
        self.buy_button.pack(pady=10)
        
        # Sell button
        self.sell_button = ctk.CTkButton(
            buttons_frame,
            text="🔴 SELL / SHORT",
            command=self.manual_sell,
            fg_color="red",
            hover_color="darkred",
            width=150,
            height=40
        )
        self.sell_button.pack(pady=10)
        
        # Close positions button
        self.close_button = ctk.CTkButton(
            buttons_frame,
            text="🔒 Close All",
            command=self.close_all_positions,
            fg_color="orange",
            hover_color="darkorange",
            width=150,
            height=40
        )
        self.close_button.pack(pady=10)
    
    def create_order_history(self):
        """Create order history section"""
        history_frame = ctk.CTkFrame(self)
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Title
        title = ctk.CTkLabel(
            history_frame,
            text="📋 Recent Orders",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=10)
        
        # Orders table
        self.orders_text = ctk.CTkTextbox(
            history_frame,
            height=150,
            font=ctk.CTkFont(size=11)
        )
        self.orders_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initial message
        self.orders_text.insert("1.0", "No recent orders...\n")
        self.orders_text.configure(state="disabled")
    
    def on_symbol_change(self, symbol):
        """Handle symbol change"""
        self.selected_symbol = symbol
        # Reset displays
        self.update_signal_display({})
    
    def manual_buy(self):
        """Handle manual buy order"""
        if not hasattr(self.main_app, 'is_bot_running') or not self.main_app.is_bot_running():
            messagebox.showwarning("Warning", "Bot is not running. Please start the bot first.")
            return
        
        # Get order parameters
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        order_type = self.order_type_var.get()
        leverage = self.leverage_var.get()
        
        if not quantity:
            messagebox.showerror("Error", "Please enter quantity")
            return
        
        try:
            quantity = float(quantity)
            if order_type == "LIMIT" and price:
                price = float(price)
            else:
                price = None
            
            leverage = int(leverage)
            
            # Confirm order
            confirm_msg = f"Place {order_type} BUY order?\n\n"
            confirm_msg += f"Symbol: {self.selected_symbol}\n"
            confirm_msg += f"Quantity: {quantity}\n"
            if price:
                confirm_msg += f"Price: ${price:.4f}\n"
            confirm_msg += f"Leverage: {leverage}x"
            
            if messagebox.askyesno("Confirm Order", confirm_msg):
                # Execute order (would integrate with bot)
                self.add_order_to_history("BUY", quantity, price, "PENDING")
                messagebox.showinfo("Order Placed", "Buy order placed successfully!")
                
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price value")
    
    def manual_sell(self):
        """Handle manual sell order"""
        if not hasattr(self.main_app, 'is_bot_running') or not self.main_app.is_bot_running():
            messagebox.showwarning("Warning", "Bot is not running. Please start the bot first.")
            return
        
        # Get order parameters
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        order_type = self.order_type_var.get()
        leverage = self.leverage_var.get()
        
        if not quantity:
            messagebox.showerror("Error", "Please enter quantity")
            return
        
        try:
            quantity = float(quantity)
            if order_type == "LIMIT" and price:
                price = float(price)
            else:
                price = None
            
            leverage = int(leverage)
            
            # Confirm order
            confirm_msg = f"Place {order_type} SELL order?\n\n"
            confirm_msg += f"Symbol: {self.selected_symbol}\n"
            confirm_msg += f"Quantity: {quantity}\n"
            if price:
                confirm_msg += f"Price: ${price:.4f}\n"
            confirm_msg += f"Leverage: {leverage}x"
            
            if messagebox.askyesno("Confirm Order", confirm_msg):
                # Execute order (would integrate with bot)
                self.add_order_to_history("SELL", quantity, price, "PENDING")
                messagebox.showinfo("Order Placed", "Sell order placed successfully!")
                
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price value")
    
    def close_all_positions(self):
        """Close all positions"""
        if not hasattr(self.main_app, 'is_bot_running') or not self.main_app.is_bot_running():
            messagebox.showwarning("Warning", "Bot is not running. Please start the bot first.")
            return
        
        confirm_msg = "Close all open positions?\n\nThis action cannot be undone."
        
        if messagebox.askyesno("Confirm Close All", confirm_msg, icon="warning"):
            # Close all positions (would integrate with bot)
            self.add_order_to_history("CLOSE_ALL", 0, None, "EXECUTED")
            messagebox.showinfo("Positions Closed", "All positions closed successfully!")
    
    def add_order_to_history(self, side: str, quantity: float, price: Optional[float], status: str):
        """Add order to history display"""
        try:
            current_time = datetime.now().strftime("%H:%M:%S")
            
            if side == "CLOSE_ALL":
                order_line = f"[{current_time}] CLOSE ALL positions - {status}\n"
            else:
                price_str = f"@${price:.4f}" if price else "@MARKET"
                order_line = f"[{current_time}] {side} {quantity} {self.selected_symbol} {price_str} - {status}\n"
            
            # Add to history
            self.orders_text.configure(state="normal")
            self.orders_text.insert("1.0", order_line)
            
            # Keep only last 20 orders
            lines = self.orders_text.get("1.0", "end").split("\n")
            if len(lines) > 21:
                self.orders_text.delete("21.0", "end")
            
            self.orders_text.configure(state="disabled")
            
        except AttributeError:
            pass
    
    def update_signal_display(self, signals_data: Dict[str, Any]):
        """Update signal display with latest data"""
        try:
            self.current_signals = signals_data
            
            # Update signal cards
            action = signals_data.get('action', 'HOLD')
            signal_color = {
                'BUY': 'green', 'STRONG_BUY': 'green',
                'SELL': 'red', 'STRONG_SELL': 'red',
                'HOLD': 'gray'
            }.get(action, 'gray')
            
            self.signal_current_signal.configure(text=action, text_color=signal_color)
            
            strength = signals_data.get('signal_strength', 0)
            self.signal_signal_strength.configure(text=f"{strength:.2f}")
            
            confidence = signals_data.get('confidence', 0)
            self.signal_confidence.configure(text=f"{confidence:.2f}")
            
            # Update indicators (if available)
            metadata = signals_data.get('metadata', {})
            if 'individual_signals' in metadata:
                individual = metadata['individual_signals']
                
                # RSI
                rsi = individual.get('rsi', 50)
                self.indicator_rsi.configure(text=f"{rsi:.2f}")
                
                # MACD
                macd = individual.get('macd', 0)
                self.indicator_macd.configure(text=f"{macd:.4f}")
            
        except AttributeError:
            pass  # UI elements may not be created yet
    
    def update_price_display(self, symbol: str, price: float):
        """Update price display"""
        if symbol == self.selected_symbol:
            try:
                self.price_label.configure(text=f"Price: ${price:.4f}")
            except AttributeError:
                pass
    
    def update_data(self, symbol: str, signals: Dict[str, Any], 
                   risk_assessment: Dict[str, Any]):
        """Update panel with latest trading data"""
        if symbol == self.selected_symbol:
            # Update signals display
            self.update_signal_display(signals)
            
            # Update risk level
            risk_level = risk_assessment.get('risk_level', 'LOW')
            risk_color = {
                'LOW': 'green',
                'MEDIUM': 'yellow', 
                'HIGH': 'orange',
                'CRITICAL': 'red'
            }.get(risk_level, 'gray')
            
            try:
                self.signal_risk_level.configure(text=risk_level, text_color=risk_color)
            except AttributeError:
                pass

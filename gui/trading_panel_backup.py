"""
Trading Panel for Manual Trading and Signal Monitoring
"""

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import datetime
from typing import Dict, Any, Optional
import asyncio
import threading

class TradingPanel(ctk.CTkFrame):
    """Trading panel for manual trading and signal monitoring"""
    
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
            text="📈 Trading Control Panel",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        # Create main sections
        self.create_symbol_selection()
        self.create_signal_monitor()
        self.create_manual_trading()
        self.create_order_history()
    
    def create_symbol_selection(self):
        """Create symbol selection section"""
        selection_frame = ctk.CTkFrame(self)
        selection_frame.pack(fill="x", padx=20, pady=10)
        
        # Title
        title = ctk.CTkLabel(
            selection_frame,
            text="🎯 Symbol Selection",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=10)
        
        # Symbol selection
        symbol_frame = ctk.CTkFrame(selection_frame)
        symbol_frame.pack(fill="x", padx=10, pady=10)
        
        # Symbol dropdown
        ctk.CTkLabel(symbol_frame, text="Select Symbol:").pack(side="left", padx=10)
        
        symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "DOTUSDT",
                  "XRPUSDT", "LTCUSDT", "LINKUSDT", "BCHUSDT", "XLMUSDT"]
        
        self.symbol_var = ctk.StringVar(value="BTCUSDT")
        self.symbol_combo = ctk.CTkComboBox(
            symbol_frame,
            values=symbols,
            variable=self.symbol_var,
            command=self.on_symbol_change
        )
        self.symbol_combo.pack(side="left", padx=10)
        
        # Current price display
        self.price_label = ctk.CTkLabel(
            symbol_frame,
            text="Price: $0.00",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.price_label.pack(side="right", padx=10)
    
    def create_signal_monitor(self):
        """Create signal monitoring section"""
        signal_frame = ctk.CTkFrame(self)
        signal_frame.pack(fill="x", padx=20, pady=10)
        
        # Title
        title = ctk.CTkLabel(
            signal_frame,
            text="🎯 Trading Signals",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=10)
        
        # Signals grid
        signals_grid = ctk.CTkFrame(signal_frame)
        signals_grid.pack(fill="x", padx=10, pady=10)
        
        # Current Signal
        self.create_signal_card(signals_grid, "Current Signal", "HOLD", "gray", 0)
        self.create_signal_card(signals_grid, "Signal Strength", "0.00", "gray", 1)
        self.create_signal_card(signals_grid, "Confidence", "0.00", "gray", 2)
        self.create_signal_card(signals_grid, "Risk Level", "LOW", "green", 3)
        
        # Technical indicators
        indicators_frame = ctk.CTkFrame(signal_frame)
        indicators_frame.pack(fill="x", padx=10, pady=10)
        
        # Create indicators display
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
        self.order_type_var = ctk.StringVar(value="MARKET")\n        order_type_combo = ctk.CTkComboBox(\n            order_frame,\n            values=[\"MARKET\", \"LIMIT\"],\n            variable=self.order_type_var\n        )\n        order_type_combo.pack(pady=5)\n        \n        # Quantity\n        ctk.CTkLabel(order_frame, text=\"Quantity:\").pack(pady=5)\n        self.quantity_entry = ctk.CTkEntry(order_frame, placeholder_text=\"0.001\")\n        self.quantity_entry.pack(pady=5)\n        \n        # Price (for limit orders)\n        ctk.CTkLabel(order_frame, text=\"Price (Limit only):\").pack(pady=5)\n        self.price_entry = ctk.CTkEntry(order_frame, placeholder_text=\"0.00\")\n        self.price_entry.pack(pady=5)\n        \n        # Leverage\n        ctk.CTkLabel(order_frame, text=\"Leverage:\").pack(pady=5)\n        self.leverage_var = ctk.StringVar(value=\"10\")\n        leverage_combo = ctk.CTkComboBox(\n            order_frame,\n            values=[\"1\", \"5\", \"10\", \"20\", \"50\", \"100\"],\n            variable=self.leverage_var\n        )\n        leverage_combo.pack(pady=5)\n        \n        # Right side - Trading buttons\n        buttons_frame = ctk.CTkFrame(controls_frame)\n        buttons_frame.pack(side=\"right\", fill=\"y\", padx=(5, 0))\n        \n        # Buy button\n        self.buy_button = ctk.CTkButton(\n            buttons_frame,\n            text=\"🟢 BUY / LONG\",\n            command=self.manual_buy,\n            fg_color=\"green\",\n            hover_color=\"darkgreen\",\n            width=150,\n            height=40\n        )\n        self.buy_button.pack(pady=10)\n        \n        # Sell button\n        self.sell_button = ctk.CTkButton(\n            buttons_frame,\n            text=\"🔴 SELL / SHORT\",\n            command=self.manual_sell,\n            fg_color=\"red\",\n            hover_color=\"darkred\",\n            width=150,\n            height=40\n        )\n        self.sell_button.pack(pady=10)\n        \n        # Close positions button\n        self.close_button = ctk.CTkButton(\n            buttons_frame,\n            text=\"🔒 Close All\",\n            command=self.close_all_positions,\n            fg_color=\"orange\",\n            hover_color=\"darkorange\",\n            width=150,\n            height=40\n        )\n        self.close_button.pack(pady=10)\n    \n    def create_order_history(self):\n        \"\"\"Create order history section\"\"\"\n        history_frame = ctk.CTkFrame(self)\n        history_frame.pack(fill=\"both\", expand=True, padx=20, pady=10)\n        \n        # Title\n        title = ctk.CTkLabel(\n            history_frame,\n            text=\"📋 Recent Orders\",\n            font=ctk.CTkFont(size=16, weight=\"bold\")\n        )\n        title.pack(pady=10)\n        \n        # Orders table\n        self.orders_text = ctk.CTkTextbox(\n            history_frame,\n            height=150,\n            font=ctk.CTkFont(size=11)\n        )\n        self.orders_text.pack(fill=\"both\", expand=True, padx=10, pady=10)\n        \n        # Initial message\n        self.orders_text.insert(\"1.0\", \"No recent orders...\\n\")\n        self.orders_text.configure(state=\"disabled\")\n    \n    def on_symbol_change(self, symbol):\n        \"\"\"Handle symbol change\"\"\"\n        self.selected_symbol = symbol\n        # Reset displays\n        self.update_signal_display({})\n    \n    def manual_buy(self):\n        \"\"\"Handle manual buy order\"\"\"\n        if not self.main_app.is_bot_running():\n            messagebox.showwarning(\"Warning\", \"Bot is not running. Please start the bot first.\")\n            return\n        \n        # Get order parameters\n        quantity = self.quantity_entry.get()\n        price = self.price_entry.get()\n        order_type = self.order_type_var.get()\n        leverage = self.leverage_var.get()\n        \n        if not quantity:\n            messagebox.showerror(\"Error\", \"Please enter quantity\")\n            return\n        \n        try:\n            quantity = float(quantity)\n            if order_type == \"LIMIT\" and price:\n                price = float(price)\n            else:\n                price = None\n            \n            leverage = int(leverage)\n            \n            # Confirm order\n            confirm_msg = f\"Place {order_type} BUY order?\\n\\n\"\n            confirm_msg += f\"Symbol: {self.selected_symbol}\\n\"\n            confirm_msg += f\"Quantity: {quantity}\\n\"\n            if price:\n                confirm_msg += f\"Price: ${price:.4f}\\n\"\n            confirm_msg += f\"Leverage: {leverage}x\"\n            \n            if messagebox.askyesno(\"Confirm Order\", confirm_msg):\n                # Execute order (would integrate with bot)\n                self.add_order_to_history(\"BUY\", quantity, price, \"PENDING\")\n                messagebox.showinfo(\"Order Placed\", \"Buy order placed successfully!\")\n                \n        except ValueError:\n            messagebox.showerror(\"Error\", \"Invalid quantity or price value\")\n    \n    def manual_sell(self):\n        \"\"\"Handle manual sell order\"\"\"\n        if not self.main_app.is_bot_running():\n            messagebox.showwarning(\"Warning\", \"Bot is not running. Please start the bot first.\")\n            return\n        \n        # Get order parameters\n        quantity = self.quantity_entry.get()\n        price = self.price_entry.get()\n        order_type = self.order_type_var.get()\n        leverage = self.leverage_var.get()\n        \n        if not quantity:\n            messagebox.showerror(\"Error\", \"Please enter quantity\")\n            return\n        \n        try:\n            quantity = float(quantity)\n            if order_type == \"LIMIT\" and price:\n                price = float(price)\n            else:\n                price = None\n            \n            leverage = int(leverage)\n            \n            # Confirm order\n            confirm_msg = f\"Place {order_type} SELL order?\\n\\n\"\n            confirm_msg += f\"Symbol: {self.selected_symbol}\\n\"\n            confirm_msg += f\"Quantity: {quantity}\\n\"\n            if price:\n                confirm_msg += f\"Price: ${price:.4f}\\n\"\n            confirm_msg += f\"Leverage: {leverage}x\"\n            \n            if messagebox.askyesno(\"Confirm Order\", confirm_msg):\n                # Execute order (would integrate with bot)\n                self.add_order_to_history(\"SELL\", quantity, price, \"PENDING\")\n                messagebox.showinfo(\"Order Placed\", \"Sell order placed successfully!\")\n                \n        except ValueError:\n            messagebox.showerror(\"Error\", \"Invalid quantity or price value\")\n    \n    def close_all_positions(self):\n        \"\"\"Close all positions\"\"\"\n        if not self.main_app.is_bot_running():\n            messagebox.showwarning(\"Warning\", \"Bot is not running. Please start the bot first.\")\n            return\n        \n        confirm_msg = \"Close all open positions?\\n\\nThis action cannot be undone.\"\n        \n        if messagebox.askyesno(\"Confirm Close All\", confirm_msg, icon=\"warning\"):\n            # Close all positions (would integrate with bot)\n            self.add_order_to_history(\"CLOSE_ALL\", 0, None, \"EXECUTED\")\n            messagebox.showinfo(\"Positions Closed\", \"All positions closed successfully!\")\n    \n    def add_order_to_history(self, side: str, quantity: float, price: Optional[float], status: str):\n        \"\"\"Add order to history display\"\"\"\n        try:\n            current_time = datetime.now().strftime(\"%H:%M:%S\")\n            \n            if side == \"CLOSE_ALL\":\n                order_line = f\"[{current_time}] CLOSE ALL positions - {status}\\n\"\n            else:\n                price_str = f\"@${price:.4f}\" if price else \"@MARKET\"\n                order_line = f\"[{current_time}] {side} {quantity} {self.selected_symbol} {price_str} - {status}\\n\"\n            \n            # Add to history\n            self.orders_text.configure(state=\"normal\")\n            self.orders_text.insert(\"1.0\", order_line)\n            \n            # Keep only last 20 orders\n            lines = self.orders_text.get(\"1.0\", \"end\").split(\"\\n\")\n            if len(lines) > 21:\n                self.orders_text.delete(\"21.0\", \"end\")\n            \n            self.orders_text.configure(state=\"disabled\")\n            \n        except AttributeError:\n            pass\n    \n    def update_signal_display(self, signals_data: Dict[str, Any]):\n        \"\"\"Update signal display with latest data\"\"\"\n        try:\n            self.current_signals = signals_data\n            \n            # Update signal cards\n            action = signals_data.get('action', 'HOLD')\n            signal_color = {\n                'BUY': 'green', 'STRONG_BUY': 'green',\n                'SELL': 'red', 'STRONG_SELL': 'red',\n                'HOLD': 'gray'\n            }.get(action, 'gray')\n            \n            self.signal_current_signal.configure(text=action, text_color=signal_color)\n            \n            strength = signals_data.get('signal_strength', 0)\n            self.signal_signal_strength.configure(text=f\"{strength:.2f}\")\n            \n            confidence = signals_data.get('confidence', 0)\n            self.signal_confidence.configure(text=f\"{confidence:.2f}\")\n            \n            # Update indicators (if available)\n            metadata = signals_data.get('metadata', {})\n            if 'individual_signals' in metadata:\n                individual = metadata['individual_signals']\n                \n                # RSI\n                rsi = individual.get('rsi', 50)\n                self.indicator_rsi.configure(text=f\"{rsi:.2f}\")\n                \n                # MACD\n                macd = individual.get('macd', 0)\n                self.indicator_macd.configure(text=f\"{macd:.4f}\")\n            \n        except AttributeError:\n            pass  # UI elements may not be created yet\n    \n    def update_price_display(self, symbol: str, price: float):\n        \"\"\"Update price display\"\"\"\n        if symbol == self.selected_symbol:\n            try:\n                self.price_label.configure(text=f\"Price: ${price:.4f}\")\n            except AttributeError:\n                pass\n    \n    def update_data(self, symbol: str, signals: Dict[str, Any], \n                   risk_assessment: Dict[str, Any]):\n        \"\"\"Update panel with latest trading data\"\"\"\n        if symbol == self.selected_symbol:\n            # Update signals display\n            self.update_signal_display(signals)\n            \n            # Update risk level\n            risk_level = risk_assessment.get('risk_level', 'LOW')\n            risk_color = {\n                'LOW': 'green',\n                'MEDIUM': 'yellow', \n                'HIGH': 'orange',\n                'CRITICAL': 'red'\n            }.get(risk_level, 'gray')\n            \n            try:\n                self.signal_risk_level.configure(text=risk_level, text_color=risk_color)\n            except AttributeError:\n                pass\n

"""
Settings Panel for Bot Configuration
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from typing import Dict, List, Any, Optional
import json
import os


class SettingsPanel(ctk.CTkFrame):
    """Panel untuk mengatur konfigurasi bot"""
    
    def __init__(self, parent, bot_interface=None):
        super().__init__(parent)
        
        self.bot_interface = bot_interface
        self.config_file = "config/bot_config.json"
        self.current_config = {}
        
        self.config_vars = {}  # Dictionary untuk menyimpan widget referensi
        
        self._setup_ui()
        self._load_config()
        
        # Load current settings from bot interface if available
        if bot_interface and hasattr(bot_interface, 'config'):
            self.load_current_settings_from_config(bot_interface.config)
    
    def _setup_ui(self):
        """Setup UI components"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self._create_header()
        
        # Main content with tabs
        self._create_content_tabs()
    
    def _create_header(self):
        """Create header with save/load buttons"""
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="⚙️ Bot Settings",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=4, pady=10)
        
        # Buttons
        load_btn = ctk.CTkButton(
            header_frame,
            text="📂 Load Config",
            width=120,
            command=self._load_config_file
        )
        load_btn.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        save_btn = ctk.CTkButton(
            header_frame,
            text="💾 Save Config",
            width=120,
            command=self._save_config
        )
        save_btn.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        export_btn = ctk.CTkButton(
            header_frame,
            text="📤 Export Config",
            width=120,
            command=self._export_config
        )
        export_btn.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        
        reset_btn = ctk.CTkButton(
            header_frame,
            text="🔄 Reset to Default",
            width=120,
            fg_color="orange",
            hover_color="darkorange",
            command=self._reset_to_default
        )
        reset_btn.grid(row=1, column=3, padx=5, pady=5, sticky="e")
    
    def _create_content_tabs(self):
        """Create tabbed content area"""
        # Tab view
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        # General tab
        self.general_tab = self.tab_view.add("General")
        self._setup_general_tab()
        
    def _setup_general_tab(self):
        """Setup general settings tab"""
        # Configure grid
        self.general_tab.grid_columnconfigure(0, weight=1)
        
        # Create scrollable frame for settings
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.general_tab,
            height=600
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create all settings sections
        self.create_api_settings()
        self.create_ai_settings()
        self.create_trading_settings()
        self.create_risk_settings()
        self.create_strategy_settings()
        self.create_notification_settings()
        self.create_control_buttons()
    
    def _load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.current_config = json.load(f)
                print("Configuration loaded successfully")
            else:
                self._set_default_config()
                print("Using default configuration")
        except Exception as e:
            print(f"Error loading config: {e}")
            self._set_default_config()
    
    def _load_config_file(self):
        """Load configuration from file dialog"""
        file_path = filedialog.askopenfilename(
            title="Load Configuration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    self.current_config = json.load(f)
                messagebox.showinfo("Success", "Configuration loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load config: {str(e)}")
    
    def _save_config(self):
        """Save current configuration"""
        try:
            # Ensure config directory exists
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                json.dump(self.current_config, f, indent=4)
            
            messagebox.showinfo("Success", "Configuration saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {str(e)}")
    
    def _export_config(self):
        """Export configuration to a file"""
        file_path = filedialog.asksaveasfilename(
            title="Export Configuration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.current_config, f, indent=4)
                messagebox.showinfo("Success", f"Configuration exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export config: {str(e)}")
    
    def _reset_to_default(self):
        """Reset configuration to default values"""
        if messagebox.askyesno("Confirm Reset", "Reset all settings to default values?"):
            self._set_default_config()
            messagebox.showinfo("Success", "Settings reset to default values")
    
    def _set_default_config(self):
        """Set default configuration"""
        self.current_config = {
            "api": {
                "key": "",
                "secret": "",
                "testnet": True
            },
            "trading": {
                "symbols": ["BTCUSDT", "ETHUSDT"],
                "timeframe": "15m",
                "leverage": 3
            },
            "risk": {
                "stop_loss": 2.0,
                "take_profit": 4.0,
                "max_drawdown": 10.0
            }
        }

    def create_settings_panel(self):
        """Create settings panel layout"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="⚙️ Bot Settings",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        # Create scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            height=600
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create sections
        self.create_api_settings()
        self.create_trading_settings()
        self.create_risk_settings()
        self.create_strategy_settings()
        self.create_notification_settings()
        self.create_control_buttons()
    
    def create_api_settings(self):
        """Create API settings section"""
        api_frame = ctk.CTkFrame(self.scrollable_frame)
        api_frame.pack(fill="x", pady=10)
        
        # Title
        title = ctk.CTkLabel(
            api_frame,
            text="🔐 API Configuration",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=10)
        
        # API Key
        self.create_setting_row(api_frame, "API Key", "BINANCE_API_KEY", "password")
        
        # API Secret
        self.create_setting_row(api_frame, "API Secret", "BINANCE_API_SECRET", "password")
        
        # Testnet toggle
        testnet_frame = ctk.CTkFrame(api_frame)
        testnet_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(testnet_frame, text="Testnet Mode:").pack(side="left", padx=10)
        
        self.config_vars["TESTNET"] = ctk.BooleanVar()
        testnet_switch = ctk.CTkSwitch(
            testnet_frame,
            text="Use Testnet",
            variable=self.config_vars["TESTNET"]
        )
        testnet_switch.pack(side="right", padx=10)
    
    def create_ai_settings(self):
        """Create AI settings section"""
        ai_frame = ctk.CTkFrame(self.scrollable_frame)
        ai_frame.pack(fill="x", pady=10)
        
        # Title
        title = ctk.CTkLabel(
            ai_frame,
            text="🤖 AI Configuration",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=10)
        
        # AI API Key
        self.create_setting_row(ai_frame, "Gemini AI API Key", "GEMINI_API_KEY", "password")
        
        # AI toggle
        ai_toggle_frame = ctk.CTkFrame(ai_frame)
        ai_toggle_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(ai_toggle_frame, text="Enable AI Analysis:").pack(side="left", padx=10)
        
        self.config_vars["AI_ENABLED"] = ctk.BooleanVar(value=True)
        ai_switch = ctk.CTkSwitch(
            ai_toggle_frame,
            text="Use AI for Trading Signals",
            variable=self.config_vars["AI_ENABLED"]
        )
        ai_switch.pack(side="right", padx=10)
        
        # AI Strategy Selection
        self.create_setting_combobox(ai_frame, "AI Strategy", "AI_STRATEGY",
                                    ["ai_enhanced", "multi_indicator", "scalping", "swing"])
        
        # AI Weight Settings
        ai_weights_frame = ctk.CTkFrame(ai_frame)
        ai_weights_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(ai_weights_frame, text="🎚️ AI Signal Weights", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        self.create_setting_row(ai_weights_frame, "AI Weight (0.0-1.0)", "AI_WEIGHT", "number", small=True)
        self.create_setting_row(ai_weights_frame, "Technical Weight (0.0-1.0)", "TECHNICAL_WEIGHT", "number", small=True)
        
        # AI Model Settings
        ai_model_frame = ctk.CTkFrame(ai_frame)
        ai_model_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(ai_model_frame, text="⚙️ Model Configuration", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        self.create_setting_row(ai_model_frame, "Temperature (0.0-1.0)", "AI_TEMPERATURE", "number", small=True)
        self.create_setting_row(ai_model_frame, "Max Tokens", "AI_MAX_TOKENS", "number", small=True)
        
        # Test AI Connection Button
        test_ai_frame = ctk.CTkFrame(ai_frame)
        test_ai_frame.pack(fill="x", padx=10, pady=10)
        
        test_ai_btn = ctk.CTkButton(
            test_ai_frame,
            text="🧪 Test AI Connection",
            command=self.test_ai_connection,
            fg_color="purple",
            hover_color="darkviolet",
            width=200
        )
        test_ai_btn.pack(pady=5)
    
    def create_trading_settings(self):
        """Create trading settings section"""
        trading_frame = ctk.CTkFrame(self.scrollable_frame)
        trading_frame.pack(fill="x", pady=10)
        
        # Title
        title = ctk.CTkLabel(
            trading_frame,
            text="📈 Trading Configuration",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=10)
        
        # Trading symbols
        symbols_frame = ctk.CTkFrame(trading_frame)
        symbols_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(symbols_frame, text="Trading Symbols:").pack(anchor="w", padx=10, pady=5)
        
        self.symbols_text = ctk.CTkTextbox(symbols_frame, height=60)
        self.symbols_text.pack(fill="x", padx=10, pady=5)
        
        # Timeframe
        self.create_setting_combobox(trading_frame, "Timeframe", "TIMEFRAME", 
                                    ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d"])
        
        # Scan interval
        self.create_setting_row(trading_frame, "Scan Interval (seconds)", "SCAN_INTERVAL", "number")
        
        # Leverage
        self.create_setting_combobox(trading_frame, "Max Leverage", "LEVERAGE",
                                    ["1", "5", "10", "20", "50", "100", "125"])
        
        # Minimum trade amount
        self.create_setting_row(trading_frame, "Min Trade Amount (USDT)", "MIN_TRADE_AMOUNT_USDT", "number")
    
    def create_risk_settings(self):
        """Create risk management settings section"""
        risk_frame = ctk.CTkFrame(self.scrollable_frame)
        risk_frame.pack(fill="x", pady=10)
        
        # Title
        title = ctk.CTkLabel(
            risk_frame,
            text="🛡️ Risk Management",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=10)
        
        # Max position size
        self.create_setting_row(risk_frame, "Max Position Size (%)", "MAX_POSITION_SIZE_PERCENT", "number")
        
        # Max daily loss
        self.create_setting_row(risk_frame, "Max Daily Loss (%)", "MAX_DAILY_LOSS_PERCENT", "number")
        
        # Max drawdown
        self.create_setting_row(risk_frame, "Max Drawdown (%)", "MAX_DRAWDOWN_PERCENT", "number")
        
        # Stop loss
        self.create_setting_row(risk_frame, "Stop Loss (%)", "STOP_LOSS_PERCENT", "number")
        
        # Take profit
        self.create_setting_row(risk_frame, "Take Profit (%)", "TAKE_PROFIT_PERCENT", "number")
        
        # Trailing stop
        self.create_setting_row(risk_frame, "Trailing Stop (%)", "TRAILING_STOP_PERCENT", "number")
    
    def create_strategy_settings(self):
        """Create strategy settings section"""
        strategy_frame = ctk.CTkFrame(self.scrollable_frame)
        strategy_frame.pack(fill="x", pady=10)
        
        # Title
        title = ctk.CTkLabel(
            strategy_frame,
            text="🎯 Strategy Configuration",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=10)
        
        # Strategy selection
        self.create_setting_combobox(strategy_frame, "Active Strategy", "STRATEGY_NAME",
                                    ["multi_indicator", "scalping", "swing"])
        
        # Min signal strength
        self.create_setting_row(strategy_frame, "Min Signal Strength (0-1)", "MIN_SIGNAL_STRENGTH", "number")
        
        # RSI settings
        rsi_frame = ctk.CTkFrame(strategy_frame)
        rsi_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(rsi_frame, text="📊 RSI Settings", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        self.create_setting_row(rsi_frame, "RSI Period", "RSI_PERIOD", "number", small=True)
        self.create_setting_row(rsi_frame, "RSI Oversold", "RSI_OVERSOLD", "number", small=True)
        self.create_setting_row(rsi_frame, "RSI Overbought", "RSI_OVERBOUGHT", "number", small=True)
        
        # MACD settings
        macd_frame = ctk.CTkFrame(strategy_frame)
        macd_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(macd_frame, text="📈 MACD Settings", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        self.create_setting_row(macd_frame, "MACD Fast", "MACD_FAST", "number", small=True)
        self.create_setting_row(macd_frame, "MACD Slow", "MACD_SLOW", "number", small=True)
        self.create_setting_row(macd_frame, "MACD Signal", "MACD_SIGNAL", "number", small=True)
        
        # EMA settings
        ema_frame = ctk.CTkFrame(strategy_frame)
        ema_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(ema_frame, text="📊 EMA Settings", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        self.create_setting_row(ema_frame, "EMA Fast", "EMA_FAST", "number", small=True)
        self.create_setting_row(ema_frame, "EMA Slow", "EMA_SLOW", "number", small=True)
        self.create_setting_row(ema_frame, "EMA Trend", "EMA_TREND", "number", small=True)
    
    def create_notification_settings(self):
        """Create notification settings section"""
        notif_frame = ctk.CTkFrame(self.scrollable_frame)
        notif_frame.pack(fill="x", pady=10)
        
        # Title
        title = ctk.CTkLabel(
            notif_frame,
            text="🔔 Notifications",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=10)
        
        # Telegram settings
        tg_frame = ctk.CTkFrame(notif_frame)
        tg_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(tg_frame, text="📱 Telegram", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        self.create_setting_row(tg_frame, "Bot Token", "TELEGRAM_BOT_TOKEN", "password")
        self.create_setting_row(tg_frame, "Chat ID", "TELEGRAM_CHAT_ID", "entry")
        
        # Discord settings
        discord_frame = ctk.CTkFrame(notif_frame)
        discord_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(discord_frame, text="💬 Discord", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        self.create_setting_row(discord_frame, "Webhook URL", "DISCORD_WEBHOOK_URL", "entry")
        
        # Notification toggles
        toggles_frame = ctk.CTkFrame(notif_frame)
        toggles_frame.pack(fill="x", padx=10, pady=5)
        
        self.create_setting_toggle(toggles_frame, "Trade Alerts", "SEND_TRADE_ALERTS")
        self.create_setting_toggle(toggles_frame, "Error Alerts", "SEND_ERROR_ALERTS")
        self.create_setting_toggle(toggles_frame, "Daily Reports", "SEND_DAILY_REPORT")
    
    def create_control_buttons(self):
        """Create control buttons"""
        buttons_frame = ctk.CTkFrame(self.scrollable_frame)
        buttons_frame.pack(fill="x", pady=20)
        
        # Buttons
        button_container = ctk.CTkFrame(buttons_frame)
        button_container.pack(pady=10)
        
        # Save button
        save_button = ctk.CTkButton(
            button_container,
            text="💾 Save Settings",
            command=self.save_settings,
            fg_color="green",
            hover_color="darkgreen",
            width=120
        )
        save_button.pack(side="left", padx=5)
        
        # Reset button
        reset_button = ctk.CTkButton(
            button_container,
            text="🔄 Reset to Default",
            command=self.reset_settings,
            fg_color="orange",
            hover_color="darkorange",
            width=120
        )
        reset_button.pack(side="left", padx=5)
        
        # Import button
        import_button = ctk.CTkButton(
            button_container,
            text="📂 Import",
            command=self.import_settings,
            width=120
        )
        import_button.pack(side="left", padx=5)
        
        # Export button
        export_button = ctk.CTkButton(
            button_container,
            text="💾 Export",
            command=self.export_settings,
            width=120
        )
        export_button.pack(side="left", padx=5)
        
        # Test API button
        test_button = ctk.CTkButton(
            button_container,
            text="🔌 Test API",
            command=self.test_api_connection,
            fg_color="purple",
            hover_color="darkviolet",
            width=120
        )
        test_button.pack(side="left", padx=5)
    
    def create_setting_row(self, parent, label_text, var_name, entry_type="entry", small=False):
        """Create a setting row with label and entry"""
        row_frame = ctk.CTkFrame(parent)
        row_frame.pack(fill="x", padx=10, pady=2)
        
        # Label
        label = ctk.CTkLabel(
            row_frame,
            text=f"{label_text}:",
            width=200 if not small else 150
        )
        label.pack(side="left", padx=10, pady=5)
        
        # Entry
        if entry_type == "password":
            entry = ctk.CTkEntry(row_frame, show="*", width=250 if not small else 150)
        else:
            entry = ctk.CTkEntry(row_frame, width=250 if not small else 150)
        
        entry.pack(side="right", padx=10, pady=5)
        
        # Store reference
        self.config_vars[var_name] = entry
    
    def create_setting_combobox(self, parent, label_text, var_name, values):
        """Create a setting row with label and combobox"""
        row_frame = ctk.CTkFrame(parent)
        row_frame.pack(fill="x", padx=10, pady=2)
        
        # Label
        label = ctk.CTkLabel(row_frame, text=f"{label_text}:", width=200)
        label.pack(side="left", padx=10, pady=5)
        
        # Combobox
        var = ctk.StringVar()
        combo = ctk.CTkComboBox(row_frame, values=values, variable=var, width=250)
        combo.pack(side="right", padx=10, pady=5)
        
        # Store reference
        self.config_vars[var_name] = var
    
    def create_setting_toggle(self, parent, label_text, var_name):
        """Create a setting toggle"""
        row_frame = ctk.CTkFrame(parent)
        row_frame.pack(fill="x", padx=10, pady=2)
        
        # Label
        label = ctk.CTkLabel(row_frame, text=f"{label_text}:", width=200)
        label.pack(side="left", padx=10, pady=5)
        
        # Toggle
        var = ctk.BooleanVar()
        toggle = ctk.CTkSwitch(row_frame, text="", variable=var)
        toggle.pack(side="right", padx=10, pady=5)
        
        # Store reference
        self.config_vars[var_name] = var
    
    def load_current_settings(self):
        """Load current settings from config"""
        try:
            if self.main_app.config:
                config = self.main_app.config
                
                # Load API settings
                if hasattr(self.config_vars.get("BINANCE_API_KEY"), "insert"):
                    self.config_vars["BINANCE_API_KEY"].insert(0, config.BINANCE_API_KEY)
                if hasattr(self.config_vars.get("BINANCE_API_SECRET"), "insert"):
                    self.config_vars["BINANCE_API_SECRET"].insert(0, config.BINANCE_API_SECRET)
                
                self.config_vars["TESTNET"].set(config.TESTNET)
                
                # Load trading settings
                symbols_text = ", ".join(config.TRADING_SYMBOLS)
                self.symbols_text.insert("1.0", symbols_text)
                
                self.config_vars["TIMEFRAME"].set(config.TIMEFRAME)
                self.config_vars["SCAN_INTERVAL"].insert(0, str(config.SCAN_INTERVAL))
                self.config_vars["LEVERAGE"].set(str(config.LEVERAGE))
                self.config_vars["MIN_TRADE_AMOUNT_USDT"].insert(0, str(config.MIN_TRADE_AMOUNT_USDT))
                
                # Load risk settings
                self.config_vars["MAX_POSITION_SIZE_PERCENT"].insert(0, str(config.MAX_POSITION_SIZE_PERCENT))
                self.config_vars["MAX_DAILY_LOSS_PERCENT"].insert(0, str(config.MAX_DAILY_LOSS_PERCENT))
                self.config_vars["MAX_DRAWDOWN_PERCENT"].insert(0, str(config.MAX_DRAWDOWN_PERCENT))
                self.config_vars["STOP_LOSS_PERCENT"].insert(0, str(config.STOP_LOSS_PERCENT))
                self.config_vars["TAKE_PROFIT_PERCENT"].insert(0, str(config.TAKE_PROFIT_PERCENT))
                self.config_vars["TRAILING_STOP_PERCENT"].insert(0, str(config.TRAILING_STOP_PERCENT))
                
                # Load strategy settings
                self.config_vars["STRATEGY_NAME"].set(config.STRATEGY_NAME)
                self.config_vars["MIN_SIGNAL_STRENGTH"].insert(0, str(config.MIN_SIGNAL_STRENGTH))
                
                # Technical indicator settings
                self.config_vars["RSI_PERIOD"].insert(0, str(config.RSI_PERIOD))
                self.config_vars["RSI_OVERSOLD"].insert(0, str(config.RSI_OVERSOLD))
                self.config_vars["RSI_OVERBOUGHT"].insert(0, str(config.RSI_OVERBOUGHT))
                
                self.config_vars["MACD_FAST"].insert(0, str(config.MACD_FAST))
                self.config_vars["MACD_SLOW"].insert(0, str(config.MACD_SLOW))
                self.config_vars["MACD_SIGNAL"].insert(0, str(config.MACD_SIGNAL))
                
                self.config_vars["EMA_FAST"].insert(0, str(config.EMA_FAST))
                self.config_vars["EMA_SLOW"].insert(0, str(config.EMA_SLOW))
                self.config_vars["EMA_TREND"].insert(0, str(config.EMA_TREND))
                
                # Notification settings
                self.config_vars["TELEGRAM_BOT_TOKEN"].insert(0, config.TELEGRAM_BOT_TOKEN)
                self.config_vars["TELEGRAM_CHAT_ID"].insert(0, config.TELEGRAM_CHAT_ID)
                self.config_vars["DISCORD_WEBHOOK_URL"].insert(0, config.DISCORD_WEBHOOK_URL)
                
                self.config_vars["SEND_TRADE_ALERTS"].set(config.SEND_TRADE_ALERTS)
                self.config_vars["SEND_ERROR_ALERTS"].set(config.SEND_ERROR_ALERTS)
                self.config_vars["SEND_DAILY_REPORT"].set(config.SEND_DAILY_REPORT)
                
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save settings to .env file"""
        try:
            # Validate settings first
            if not self._validate_settings():
                return
            
            # Create .env content
            env_content = []
            
            # API settings
            env_content.append("# Binance API Configuration")
            env_content.append(f"BINANCE_API_KEY={self.config_vars['BINANCE_API_KEY'].get()}")
            env_content.append(f"BINANCE_API_SECRET={self.config_vars['BINANCE_API_SECRET'].get()}")
            env_content.append(f"TESTNET={'true' if self.config_vars['TESTNET'].get() else 'false'}")
            env_content.append("")
            
            # Trading settings
            env_content.append("# Trading Configuration")
            symbols = [s.strip() for s in self.symbols_text.get("1.0", "end").strip().split(",")]
            env_content.append(f"TRADING_SYMBOLS={','.join(symbols)}")
            env_content.append(f"TIMEFRAME={self.config_vars['TIMEFRAME'].get()}")
            env_content.append(f"SCAN_INTERVAL={self.config_vars['SCAN_INTERVAL'].get()}")
            env_content.append(f"LEVERAGE={self.config_vars['LEVERAGE'].get()}")
            env_content.append(f"MIN_TRADE_AMOUNT_USDT={self.config_vars['MIN_TRADE_AMOUNT_USDT'].get()}")
            env_content.append("")
            
            # Risk settings
            env_content.append("# Risk Management")
            env_content.append(f"MAX_POSITION_SIZE_PERCENT={self.config_vars['MAX_POSITION_SIZE_PERCENT'].get()}")
            env_content.append(f"MAX_DAILY_LOSS_PERCENT={self.config_vars['MAX_DAILY_LOSS_PERCENT'].get()}")
            env_content.append(f"MAX_DRAWDOWN_PERCENT={self.config_vars['MAX_DRAWDOWN_PERCENT'].get()}")
            env_content.append(f"STOP_LOSS_PERCENT={self.config_vars['STOP_LOSS_PERCENT'].get()}")
            env_content.append(f"TAKE_PROFIT_PERCENT={self.config_vars['TAKE_PROFIT_PERCENT'].get()}")
            env_content.append(f"TRAILING_STOP_PERCENT={self.config_vars['TRAILING_STOP_PERCENT'].get()}")
            env_content.append("")
            
            # Strategy settings
            env_content.append("# Strategy Configuration")
            env_content.append(f"STRATEGY_NAME={self.config_vars['STRATEGY_NAME'].get()}")
            env_content.append(f"MIN_SIGNAL_STRENGTH={self.config_vars['MIN_SIGNAL_STRENGTH'].get()}")
            env_content.append(f"RSI_PERIOD={self.config_vars['RSI_PERIOD'].get()}")
            env_content.append(f"RSI_OVERSOLD={self.config_vars['RSI_OVERSOLD'].get()}")
            env_content.append(f"RSI_OVERBOUGHT={self.config_vars['RSI_OVERBOUGHT'].get()}")
            env_content.append(f"MACD_FAST={self.config_vars['MACD_FAST'].get()}")
            env_content.append(f"MACD_SLOW={self.config_vars['MACD_SLOW'].get()}")
            env_content.append(f"MACD_SIGNAL={self.config_vars['MACD_SIGNAL'].get()}")
            env_content.append(f"EMA_FAST={self.config_vars['EMA_FAST'].get()}")
            env_content.append(f"EMA_SLOW={self.config_vars['EMA_SLOW'].get()}")
            env_content.append(f"EMA_TREND={self.config_vars['EMA_TREND'].get()}")
            env_content.append("")
            
            # Notification settings
            env_content.append("# Notification Configuration")
            env_content.append(f"TELEGRAM_BOT_TOKEN={self.config_vars['TELEGRAM_BOT_TOKEN'].get()}")
            env_content.append(f"TELEGRAM_CHAT_ID={self.config_vars['TELEGRAM_CHAT_ID'].get()}")
            env_content.append(f"DISCORD_WEBHOOK_URL={self.config_vars['DISCORD_WEBHOOK_URL'].get()}")
            env_content.append(f"SEND_TRADE_ALERTS={'true' if self.config_vars['SEND_TRADE_ALERTS'].get() else 'false'}")
            env_content.append(f"SEND_ERROR_ALERTS={'true' if self.config_vars['SEND_ERROR_ALERTS'].get() else 'false'}")
            env_content.append(f"SEND_DAILY_REPORT={'true' if self.config_vars['SEND_DAILY_REPORT'].get() else 'false'}")
            
            # Write to .env file
            with open(".env", "w") as f:
                f.write("\n".join(env_content))
            
            messagebox.showinfo("Success", "Settings saved successfully!\n\nRestart the bot to apply changes.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings:\n\n{str(e)}")
    
    def reset_settings(self):
        """Reset settings to default"""
        if messagebox.askyesno("Confirm Reset", "Reset all settings to default values?"):
            try:
                # Clear all entries
                for var_name, widget in self.config_vars.items():
                    if hasattr(widget, 'delete') and hasattr(widget, 'insert'):
                        widget.delete(0, "end")
                    elif hasattr(widget, 'set'):
                        if isinstance(widget, ctk.BooleanVar):
                            widget.set(False)
                        else:
                            widget.set("")
                
                # Clear symbols text
                self.symbols_text.delete("1.0", "end")
                
                messagebox.showinfo("Success", "Settings reset to default values")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reset settings:\n\n{str(e)}")
    
    def import_settings(self):
        """Import settings from file"""
        try:
            file_path = filedialog.askopenfilename(
                title="Import Settings",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'r') as f:
                    settings = json.load(f)
                
                # Load settings into UI
                for key, value in settings.items():
                    if key in self.config_vars:
                        widget = self.config_vars[key]
                        if hasattr(widget, 'delete') and hasattr(widget, 'insert'):
                            widget.delete(0, "end")
                            widget.insert(0, str(value))
                        elif hasattr(widget, 'set'):
                            widget.set(value)
                
                messagebox.showinfo("Success", f"Settings imported from {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import settings:\n\n{str(e)}")
    
    def export_settings(self):
        """Export settings to file"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Export Settings",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                settings = {}
                
                # Collect all settings
                for key, widget in self.config_vars.items():
                    if hasattr(widget, 'get'):
                        settings[key] = widget.get()
                
                # Add symbols
                settings['TRADING_SYMBOLS'] = self.symbols_text.get("1.0", "end").strip()
                
                with open(file_path, 'w') as f:
                    json.dump(settings, f, indent=2)
                
                messagebox.showinfo("Success", f"Settings exported to {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export settings:\n\n{str(e)}")
    
    def test_api_connection(self):
        """Test API connection"""
        try:
            api_key = self.config_vars["BINANCE_API_KEY"].get()
            api_secret = self.config_vars["BINANCE_API_SECRET"].get()
            testnet = self.config_vars["TESTNET"].get()
            
            if not api_key or not api_secret:
                messagebox.showerror("Error", "Please enter API key and secret")
                return
            
            # Test connection (simplified)
            messagebox.showinfo("API Test", "API connection test would be performed here.\n\nIn real implementation, this would test the actual API connection.")
            
        except Exception as e:
            messagebox.showerror("Error", f"API test failed:\n\n{str(e)}")
    
    def test_ai_connection(self):
        """Test AI connection"""
        try:
            import asyncio
            import sys
            from pathlib import Path
            
            # Add src to path
            sys.path.append(str(Path(__file__).parent.parent / "src"))
            
            # Get AI API key
            ai_api_key = "AIzaSyC8Hlbk3I4k78OLIA6Chp1Zip6wJ6TRdqM"  # Default API key
            if "GEMINI_API_KEY" in self.config_vars:
                user_key = self.config_vars["GEMINI_API_KEY"].get()
                if user_key:
                    ai_api_key = user_key
            
            # Test AI connection in a separate thread
            def test_ai():
                try:
                    from src.ai_analyzer import AIAnalyzer
                    
                    # Initialize AI analyzer
                    ai_analyzer = AIAnalyzer(api_key=ai_api_key)
                    
                    # Create test event loop
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    try:
                        # Test connection
                        result = loop.run_until_complete(ai_analyzer.test_connection())
                        
                        if result['available']:
                            messagebox.showinfo(
                                "AI Connection Test", 
                                f"✅ AI Connection Successful!\n\n"
                                f"Status: {result['status']}\n"
                                f"Response: {result['message'][:100]}..."
                            )
                        else:
                            messagebox.showerror(
                                "AI Connection Test", 
                                f"❌ AI Connection Failed\n\n"
                                f"Status: {result['status']}\n"
                                f"Message: {result['message']}"
                            )
                    finally:
                        loop.close()
                        
                except ImportError as e:
                    messagebox.showerror(
                        "AI Connection Test", 
                        f"❌ AI dependencies not installed\n\n"
                        f"Please install: pip install google-generativeai\n\n"
                        f"Error: {str(e)}"
                    )
                except Exception as e:
                    messagebox.showerror(
                        "AI Connection Test", 
                        f"❌ AI connection test failed\n\n"
                        f"Error: {str(e)}"
                    )
            
            # Run test in background thread
            import threading
            test_thread = threading.Thread(target=test_ai, daemon=True)
            test_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to test AI connection:\n\n{str(e)}")
    
    def _validate_settings(self) -> bool:
        """Validate settings before saving"""
        try:
            # Check required fields
            api_key = self.config_vars["BINANCE_API_KEY"].get()
            api_secret = self.config_vars["BINANCE_API_SECRET"].get()
            
            if not api_key or not api_secret:
                messagebox.showerror("Validation Error", "API Key and Secret are required")
                return False
            
            # Validate numeric fields
            numeric_fields = [
                "SCAN_INTERVAL", "MIN_TRADE_AMOUNT_USDT", "MAX_POSITION_SIZE_PERCENT",
                "MAX_DAILY_LOSS_PERCENT", "MAX_DRAWDOWN_PERCENT", "STOP_LOSS_PERCENT",
                "TAKE_PROFIT_PERCENT", "TRAILING_STOP_PERCENT", "MIN_SIGNAL_STRENGTH",
                "RSI_PERIOD", "RSI_OVERSOLD", "RSI_OVERBOUGHT", "MACD_FAST",
                "MACD_SLOW", "MACD_SIGNAL", "EMA_FAST", "EMA_SLOW", "EMA_TREND"
            ]
            
            for field in numeric_fields:
                if field in self.config_vars:
                    value = self.config_vars[field].get()
                    try:
                        float(value)
                    except ValueError:
                        messagebox.showerror("Validation Error", f"{field} must be a valid number")
                        return False
            
            return True
            
        except Exception as e:
            messagebox.showerror("Validation Error", f"Settings validation failed:\n\n{str(e)}")
            return False
    
    def load_current_settings_from_config(self, config):
        """Load current settings from bot config"""
        try:
            if not config:
                return
                
            # Load API settings
            if "BINANCE_API_KEY" in self.config_vars:
                self.config_vars["BINANCE_API_KEY"].delete(0, "end")
                self.config_vars["BINANCE_API_KEY"].insert(0, config.BINANCE_API_KEY)
            if "BINANCE_API_SECRET" in self.config_vars:
                self.config_vars["BINANCE_API_SECRET"].delete(0, "end")
                self.config_vars["BINANCE_API_SECRET"].insert(0, config.BINANCE_API_SECRET)
            if "TESTNET" in self.config_vars:
                self.config_vars["TESTNET"].set(config.TESTNET)
                
            # Load trading settings
            if hasattr(config, 'TRADING_SYMBOLS') and hasattr(self, 'symbols_text'):
                self.symbols_text.delete("1.0", "end")
                symbols_text = ", ".join(config.TRADING_SYMBOLS)
                self.symbols_text.insert("1.0", symbols_text)
                
            if "TIMEFRAME" in self.config_vars:
                self.config_vars["TIMEFRAME"].set(config.TIMEFRAME)
            if "SCAN_INTERVAL" in self.config_vars:
                self.config_vars["SCAN_INTERVAL"].delete(0, "end")
                self.config_vars["SCAN_INTERVAL"].insert(0, str(config.SCAN_INTERVAL))
            if "LEVERAGE" in self.config_vars:
                self.config_vars["LEVERAGE"].set(str(config.LEVERAGE))
            if "MIN_TRADE_AMOUNT_USDT" in self.config_vars:
                self.config_vars["MIN_TRADE_AMOUNT_USDT"].delete(0, "end")
                self.config_vars["MIN_TRADE_AMOUNT_USDT"].insert(0, str(config.MIN_TRADE_AMOUNT_USDT))
                
            # Load risk settings
            if "MAX_POSITION_SIZE_PERCENT" in self.config_vars:
                self.config_vars["MAX_POSITION_SIZE_PERCENT"].delete(0, "end")
                self.config_vars["MAX_POSITION_SIZE_PERCENT"].insert(0, str(config.MAX_POSITION_SIZE_PERCENT))
            if "MAX_DAILY_LOSS_PERCENT" in self.config_vars:
                self.config_vars["MAX_DAILY_LOSS_PERCENT"].delete(0, "end")
                self.config_vars["MAX_DAILY_LOSS_PERCENT"].insert(0, str(config.MAX_DAILY_LOSS_PERCENT))
            if "MAX_DRAWDOWN_PERCENT" in self.config_vars:
                self.config_vars["MAX_DRAWDOWN_PERCENT"].delete(0, "end")
                self.config_vars["MAX_DRAWDOWN_PERCENT"].insert(0, str(config.MAX_DRAWDOWN_PERCENT))
            if "STOP_LOSS_PERCENT" in self.config_vars:
                self.config_vars["STOP_LOSS_PERCENT"].delete(0, "end")
                self.config_vars["STOP_LOSS_PERCENT"].insert(0, str(config.STOP_LOSS_PERCENT))
            if "TAKE_PROFIT_PERCENT" in self.config_vars:
                self.config_vars["TAKE_PROFIT_PERCENT"].delete(0, "end")
                self.config_vars["TAKE_PROFIT_PERCENT"].insert(0, str(config.TAKE_PROFIT_PERCENT))
            if "TRAILING_STOP_PERCENT" in self.config_vars:
                self.config_vars["TRAILING_STOP_PERCENT"].delete(0, "end")
                self.config_vars["TRAILING_STOP_PERCENT"].insert(0, str(config.TRAILING_STOP_PERCENT))
                
            # Load strategy settings
            if "STRATEGY_NAME" in self.config_vars:
                self.config_vars["STRATEGY_NAME"].set(config.STRATEGY_NAME)
            if "MIN_SIGNAL_STRENGTH" in self.config_vars:
                self.config_vars["MIN_SIGNAL_STRENGTH"].delete(0, "end")
                self.config_vars["MIN_SIGNAL_STRENGTH"].insert(0, str(config.MIN_SIGNAL_STRENGTH))
                
            # Technical indicator settings  
            if "RSI_PERIOD" in self.config_vars:
                self.config_vars["RSI_PERIOD"].delete(0, "end")
                self.config_vars["RSI_PERIOD"].insert(0, str(config.RSI_PERIOD))
            if "RSI_OVERSOLD" in self.config_vars:
                self.config_vars["RSI_OVERSOLD"].delete(0, "end")
                self.config_vars["RSI_OVERSOLD"].insert(0, str(config.RSI_OVERSOLD))
            if "RSI_OVERBOUGHT" in self.config_vars:
                self.config_vars["RSI_OVERBOUGHT"].delete(0, "end")
                self.config_vars["RSI_OVERBOUGHT"].insert(0, str(config.RSI_OVERBOUGHT))
                
            if "MACD_FAST" in self.config_vars:
                self.config_vars["MACD_FAST"].delete(0, "end")
                self.config_vars["MACD_FAST"].insert(0, str(config.MACD_FAST))
            if "MACD_SLOW" in self.config_vars:
                self.config_vars["MACD_SLOW"].delete(0, "end")
                self.config_vars["MACD_SLOW"].insert(0, str(config.MACD_SLOW))
            if "MACD_SIGNAL" in self.config_vars:
                self.config_vars["MACD_SIGNAL"].delete(0, "end")
                self.config_vars["MACD_SIGNAL"].insert(0, str(config.MACD_SIGNAL))
                
            if "EMA_FAST" in self.config_vars:
                self.config_vars["EMA_FAST"].delete(0, "end")
                self.config_vars["EMA_FAST"].insert(0, str(config.EMA_FAST))
            if "EMA_SLOW" in self.config_vars:
                self.config_vars["EMA_SLOW"].delete(0, "end")
                self.config_vars["EMA_SLOW"].insert(0, str(config.EMA_SLOW))
            if "EMA_TREND" in self.config_vars:
                self.config_vars["EMA_TREND"].delete(0, "end")
                self.config_vars["EMA_TREND"].insert(0, str(config.EMA_TREND))
                
            # Notification settings
            if "TELEGRAM_BOT_TOKEN" in self.config_vars:
                self.config_vars["TELEGRAM_BOT_TOKEN"].delete(0, "end")
                self.config_vars["TELEGRAM_BOT_TOKEN"].insert(0, config.TELEGRAM_BOT_TOKEN)
            if "TELEGRAM_CHAT_ID" in self.config_vars:
                self.config_vars["TELEGRAM_CHAT_ID"].delete(0, "end")
                self.config_vars["TELEGRAM_CHAT_ID"].insert(0, config.TELEGRAM_CHAT_ID)
            if "DISCORD_WEBHOOK_URL" in self.config_vars:
                self.config_vars["DISCORD_WEBHOOK_URL"].delete(0, "end")
                self.config_vars["DISCORD_WEBHOOK_URL"].insert(0, config.DISCORD_WEBHOOK_URL)
                
            if "SEND_TRADE_ALERTS" in self.config_vars:
                self.config_vars["SEND_TRADE_ALERTS"].set(config.SEND_TRADE_ALERTS)
            if "SEND_ERROR_ALERTS" in self.config_vars:
                self.config_vars["SEND_ERROR_ALERTS"].set(config.SEND_ERROR_ALERTS)
            if "SEND_DAILY_REPORT" in self.config_vars:
                self.config_vars["SEND_DAILY_REPORT"].set(config.SEND_DAILY_REPORT)
                
        except Exception as e:
            print(f"Error loading settings from config: {e}")
    
    def update_data(self, symbol: str, signals: Dict[str, Any], 
                   risk_assessment: Dict[str, Any]):
        """Update panel with latest trading data"""
        # Settings panel doesn't need real-time updates
        pass

#!/usr/bin/env python3
"""
Binance Futures Trading Bot - GUI Application
Modern GUI interface for the trading bot with real-time monitoring
"""

import sys
import asyncio
import threading
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
import logging

# GUI imports
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from PIL import Image, ImageTk

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

# Bot imports
from src.config import Config
from src.binance_client import BinanceClient
from src.technical_analyzer import TechnicalAnalyzer
from src.risk_manager import RiskManager
from src.strategy_manager import StrategyManager
from src.position_manager import PositionManager
from src.notification_manager import NotificationManager
from src.database import DatabaseManager

# GUI components
from gui.dashboard import DashboardFrame
from gui.trading_panel import TradingPanel
from gui.position_panel import PositionPanel
from gui.analytics_panel import AnalyticsPanel
from gui.logs_panel import LogsPanel
from gui.settings_panel import SettingsPanel

class BinanceFuturesBotGUI:
    """Main GUI Application for Binance Futures Trading Bot"""
    
    def __init__(self):
        """Initialize GUI application"""
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("🚀 Binance Futures Trading Bot v1.0")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Center window
        self._center_window()
        
        # Initialize variables
        self.bot_running = False
        self.bot_thread = None
        self.config = None
        self.bot_components = {}
        
        # Setup logging
        self._setup_gui_logging()
        
        # Create GUI
        self._create_gui()
        
        # Load configuration
        self._load_configuration()
        
        # Start update loop
        self._start_update_loop()
        
        print("✅ GUI initialized successfully")
    
    def _center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def _setup_gui_logging(self):
        """Setup logging for GUI"""
        # Create logs directory
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/gui.log'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def _create_gui(self):
        """Create the main GUI layout"""
        # Create main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create header
        self._create_header()
        
        # Create sidebar and content area
        self._create_main_layout()
        
        # Create status bar
        self._create_status_bar()
    
    def _create_header(self):
        """Create header with logo and controls"""
        header_frame = ctk.CTkFrame(self.main_frame, height=80, corner_radius=10)
        header_frame.pack(fill="x", padx=5, pady=5)
        header_frame.pack_propagate(False)
        
        # Left side - Logo and title
        left_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=15)
        
        # Bot title
        title_label = ctk.CTkLabel(
            left_frame,
            text="🚀 Binance Futures Trading Bot",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left")
        
        # Version label
        version_label = ctk.CTkLabel(
            left_frame,
            text="v1.0.0",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        version_label.pack(side="left", padx=(10, 0))
        
        # Right side - Control buttons
        right_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        right_frame.pack(side="right", padx=20, pady=15)
        
        # Bot status indicator
        self.status_indicator = ctk.CTkLabel(
            right_frame,
            text="●",
            font=ctk.CTkFont(size=20),
            text_color="red"
        )
        self.status_indicator.pack(side="right", padx=(0, 10))
        
        # Stop button
        self.stop_button = ctk.CTkButton(
            right_frame,
            text="⏹ Stop Bot",
            command=self._stop_bot,
            fg_color="red",
            hover_color="darkred",
            width=100,
            state="disabled"
        )
        self.stop_button.pack(side="right", padx=5)
        
        # Start button
        self.start_button = ctk.CTkButton(
            right_frame,
            text="▶ Start Bot",
            command=self._start_bot,
            fg_color="green",
            hover_color="darkgreen",
            width=100
        )
        self.start_button.pack(side="right", padx=5)
    
    def _create_main_layout(self):
        """Create main layout with sidebar and content"""
        # Create main content frame
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create sidebar
        self.sidebar = ctk.CTkFrame(content_frame, width=200, corner_radius=10)
        self.sidebar.pack(side="left", fill="y", padx=(5, 2.5), pady=5)
        self.sidebar.pack_propagate(False)
        
        # Create content area
        self.content_area = ctk.CTkFrame(content_frame, corner_radius=10)
        self.content_area.pack(side="right", fill="both", expand=True, padx=(2.5, 5), pady=5)
        
        # Setup sidebar
        self._setup_sidebar()
        
        # Setup content panels
        self._setup_content_panels()
    
    def _setup_sidebar(self):
        """Setup sidebar navigation"""
        # Sidebar title
        sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="Navigation",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        sidebar_title.pack(pady=(20, 10))
        
        # Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("📊 Dashboard", "dashboard"),
            ("📈 Trading", "trading"),
            ("📍 Positions", "positions"),
            ("📈 Analytics", "analytics"),
            ("📋 Logs", "logs"),
            ("⚙️ Settings", "settings"),
        ]
        
        for text, key in nav_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=lambda k=key: self._show_panel(k),
                width=160,
                height=40,
                anchor="w"
            )
            btn.pack(pady=5, padx=10)
            self.nav_buttons[key] = btn
        
        # Select dashboard by default
        self.current_panel = "dashboard"
        self.nav_buttons["dashboard"].configure(fg_color="gray")
    
    def _setup_content_panels(self):
        """Setup content panels"""
        self.panels = {}
        
        # Create a bot interface reference that can be passed to panels
        bot_interface = self  # The GUI class acts as the interface to bot components
        
        # Dashboard Panel
        self.panels["dashboard"] = DashboardFrame(self.content_area)
        
        # Trading Panel
        self.panels["trading"] = TradingPanel(self.content_area, bot_interface)
        
        # Positions Panel
        self.panels["positions"] = PositionPanel(self.content_area, bot_interface)
        
        # Analytics Panel  
        self.panels["analytics"] = AnalyticsPanel(self.content_area, bot_interface)
        
        # Logs Panel
        self.panels["logs"] = LogsPanel(self.content_area, bot_interface)
        
        # Settings Panel
        self.panels["settings"] = SettingsPanel(self.content_area, bot_interface)
        
        # Show dashboard initially
        self._show_panel("dashboard")
    
    def _show_panel(self, panel_name: str):
        """Show specific panel"""
        # Hide current panel
        if self.current_panel in self.panels:
            self.panels[self.current_panel].pack_forget()
        
        # Update navigation button colors
        for key, btn in self.nav_buttons.items():
            if key == panel_name:
                btn.configure(fg_color="gray")
            else:
                btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        
        # Show new panel
        if panel_name in self.panels:
            self.panels[panel_name].pack(fill="both", expand=True, padx=10, pady=10)
            self.current_panel = panel_name
    
    def _create_status_bar(self):
        """Create status bar"""
        self.status_bar = ctk.CTkFrame(self.main_frame, height=30, corner_radius=5)
        self.status_bar.pack(fill="x", padx=5, pady=(0, 5))
        self.status_bar.pack_propagate(False)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="left", padx=10, pady=5)
        
        # Time label
        self.time_label = ctk.CTkLabel(
            self.status_bar,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.time_label.pack(side="right", padx=10, pady=5)
    
    def _load_configuration(self):
        """Load bot configuration"""
        try:
            self.config = Config()
            errors = self.config.validate_config()
            
            if errors:
                error_msg = "\n".join(errors)
                messagebox.showerror(
                    "Configuration Error",
                    f"Configuration validation failed:\n\n{error_msg}\n\n"
                    "Please check your .env file and fix the issues."
                )
                self._update_status("Configuration Error", "red")
            else:
                self._update_status("Configuration Loaded", "green")
                
        except Exception as e:
            messagebox.showerror(
                "Configuration Error",
                f"Failed to load configuration:\n\n{str(e)}"
            )
            self._update_status("Configuration Error", "red")
    
    def _start_bot(self):
        """Start the trading bot"""
        if self.bot_running:
            return
        
        # Validate configuration first
        if not self.config:
            messagebox.showerror("Error", "Configuration not loaded!")
            return
        
        errors = self.config.validate_config()
        if errors:
            error_msg = "\n".join(errors)
            messagebox.showerror(
                "Configuration Error",
                f"Please fix configuration errors:\n\n{error_msg}"
            )
            return
        
        # Show warning dialog
        if not self._show_start_warning():
            return
        
        try:
            # Start bot in separate thread
            self.bot_running = True
            self.bot_thread = threading.Thread(target=self._run_bot_async, daemon=True)
            self.bot_thread.start()
            
            # Update UI
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.status_indicator.configure(text_color="green")
            self._update_status("Starting Bot...", "yellow")
            
        except Exception as e:
            self.logger.error(f"Error starting bot: {e}")
            messagebox.showerror("Error", f"Failed to start bot:\n\n{str(e)}")
            self.bot_running = False
    
    def _show_start_warning(self) -> bool:
        """Show warning dialog before starting bot"""
        warning_msg = """⚠️ WARNING ⚠️

You are about to start the trading bot.

IMPORTANT REMINDERS:
• Trading cryptocurrency is extremely risky
• You can lose all of your invested money  
• This bot does not guarantee profits
• Make sure you have tested in testnet first
• Only trade with money you can afford to lose

Current Mode: """
        
        mode = "TESTNET" if self.config.TESTNET else "LIVE TRADING"
        warning_msg += f"{mode}\n\nDo you want to continue?"
        
        result = messagebox.askyesno(
            "Start Trading Bot",
            warning_msg,
            icon="warning"
        )
        
        return result
    
    def _stop_bot(self):
        """Stop the trading bot"""
        if not self.bot_running:
            return
        
        self.bot_running = False
        self._update_status("Stopping Bot...", "yellow")
        
        # Update UI
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_indicator.configure(text_color="red")
        
        # Wait for thread to finish
        if self.bot_thread and self.bot_thread.is_alive():
            self.bot_thread.join(timeout=5)
        
        self._update_status("Bot Stopped", "red")
    
    def _run_bot_async(self):
        """Run bot in async context"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(self._run_bot())
        except Exception as e:
            self.logger.error(f"Bot error: {e}")
            self.root.after(0, lambda: self._update_status(f"Bot Error: {str(e)}", "red"))
        finally:
            loop.close()
            self.bot_running = False
    
    async def _run_bot(self):
        """Main bot execution logic"""
        try:
            self.root.after(0, lambda: self._update_status("Initializing Components...", "yellow"))
            
            # Initialize bot components
            self.bot_components = {
                'binance_client': BinanceClient(
                    api_key=self.config.BINANCE_API_KEY,
                    api_secret=self.config.BINANCE_API_SECRET,
                    testnet=self.config.TESTNET
                ),
                'technical_analyzer': TechnicalAnalyzer(),
                'risk_manager': RiskManager(self.config),
                'strategy_manager': StrategyManager(self.config),
                'notification_manager': NotificationManager(self.config),
                'database': DatabaseManager(self.config.DATABASE_URL)
            }
            
            # Test connection
            await self.bot_components['binance_client'].test_connection()
            await self.bot_components['database'].initialize()
            
            # Initialize position manager
            self.bot_components['position_manager'] = PositionManager(
                self.bot_components['binance_client'],
                self.bot_components['risk_manager']
            )
            
            self.root.after(0, lambda: self._update_status("Bot Running", "green"))
            
            # Send startup notification
            await self.bot_components['notification_manager'].send_startup_message()
            
            # Main trading loop
            while self.bot_running:
                try:
                    await self._bot_iteration()
                    await asyncio.sleep(self.config.SCAN_INTERVAL)
                    
                except Exception as e:
                    self.logger.error(f"Error in bot iteration: {e}")
                    await asyncio.sleep(10)
            
        except Exception as e:
            self.logger.error(f"Fatal bot error: {e}")
            self.root.after(0, lambda: messagebox.showerror("Bot Error", f"Fatal error:\n\n{str(e)}"))
        
        finally:
            # Cleanup
            if 'notification_manager' in self.bot_components:
                await self.bot_components['notification_manager'].send_shutdown_message()
            
            for component in self.bot_components.values():
                if hasattr(component, 'close'):
                    await component.close()
    
    async def _bot_iteration(self):
        """Single iteration of bot logic"""
        try:
            symbols = self.config.TRADING_SYMBOLS
            
            for symbol in symbols:
                if not self.bot_running:
                    break
                
                # Get market data
                klines = await self.bot_components['binance_client'].get_klines(
                    symbol, self.config.TIMEFRAME, limit=500
                )
                
                if not klines:
                    continue
                
                # Perform technical analysis
                analysis = await self.bot_components['technical_analyzer'].analyze(symbol, klines)
                
                # Get current position
                current_position = await self.bot_components['position_manager'].get_position(symbol)
                
                # Generate trading signals
                signals = await self.bot_components['strategy_manager'].generate_signals(
                    symbol, analysis, current_position
                )
                
                # Apply risk management
                risk_assessment = await self.bot_components['risk_manager'].assess_risk(
                    symbol, signals, current_position
                )
                
                # Execute trades if approved
                if risk_assessment['approved']:
                    await self._execute_trade(symbol, signals, risk_assessment)
                
                # Update GUI data
                self.root.after(0, lambda s=symbol, sig=signals, risk=risk_assessment: 
                               self._update_gui_data(s, sig, risk))
                
        except Exception as e:
            self.logger.error(f"Error in bot iteration: {e}")
    
    async def _execute_trade(self, symbol: str, signals: Dict[str, Any], 
                           risk_assessment: Dict[str, Any]):
        """Execute trading orders"""
        try:
            action = signals.get('action')
            position_manager = self.bot_components['position_manager']
            
            if action == 'BUY':
                success = await position_manager.open_long_position(
                    symbol, signals, risk_assessment
                )
            elif action == 'SELL':
                success = await position_manager.open_short_position(
                    symbol, signals, risk_assessment
                )
            elif action == 'CLOSE':
                success = await position_manager.close_position(symbol)
            else:
                return
            
            # Send notification if trade executed
            if success:
                await self.bot_components['notification_manager'].send_trade_alert(
                    symbol, action, {
                        'entry_price': signals.get('entry_price'),
                        'stop_loss': risk_assessment.get('stop_loss'),
                        'take_profit': risk_assessment.get('take_profit'),
                        'position_size': risk_assessment.get('position_size'),
                        'leverage': risk_assessment.get('leverage'),
                        'reason': signals.get('reason'),
                        'strategy': signals.get('strategy'),
                        'signal_strength': signals.get('signal_strength')
                    }
                )
                
        except Exception as e:
            self.logger.error(f"Error executing trade for {symbol}: {e}")
            await self.bot_components['notification_manager'].send_error_alert(
                f"Trade execution error for {symbol}: {e}"
            )
    
    def _update_gui_data(self, symbol: str, signals: Dict[str, Any], 
                        risk_assessment: Dict[str, Any]):
        """Update GUI with latest data"""
        # Update panels with new data
        for panel in self.panels.values():
            if hasattr(panel, 'update_data'):
                panel.update_data(symbol, signals, risk_assessment)
    
    def _update_status(self, message: str, color: str = "white"):
        """Update status bar message"""
        self.status_label.configure(text=message, text_color=color)
    
    def _start_update_loop(self):
        """Start GUI update loop"""
        self._update_time()
        self.root.after(1000, self._start_update_loop)
    
    def _update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.configure(text=current_time)
    
    def get_bot_component(self, component_name: str):
        """Get bot component"""
        return self.bot_components.get(component_name)
    
    def is_bot_running(self) -> bool:
        """Check if bot is running"""
        return self.bot_running
    
    def run(self):
        """Start the GUI application"""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"GUI error: {e}")
            messagebox.showerror("GUI Error", f"Application error:\n\n{str(e)}")
    
    def _on_closing(self):
        """Handle application closing"""
        try:
            if self.bot_running:
                result = messagebox.askyesno(
                    "Confirm Exit",
                    "The trading bot is still running.\n\nDo you want to stop the bot and exit?",
                    icon="warning"
                )
                
                if result:
                    self._stop_bot()
                    self._cleanup_on_close()
                else:
                    return  # Don't close if user cancels
            else:
                self._cleanup_on_close()
        except KeyboardInterrupt:
            print("Keyboard interrupt during shutdown")
            self._cleanup_on_close()
        except Exception as e:
            print(f"Error during shutdown: {e}")
            self._cleanup_on_close()
    
    def _cleanup_on_close(self):
        """Cleanup resources when closing the application"""
        try:
            print("Starting GUI cleanup...")
            
            # Stop background updates in panels
            if hasattr(self, 'panels'):
                for panel_name, panel in self.panels.items():
                    if hasattr(panel, 'stop_updates'):
                        try:
                            panel.stop_updates()
                            print(f"Stopped updates for {panel_name} panel")
                        except Exception as e:
                            print(f"Error stopping updates for {panel_name}: {e}")
            
            # Give threads time to stop
            import time
            time.sleep(0.5)
            
            print("GUI cleanup completed")
            
        except KeyboardInterrupt:
            print("Keyboard interrupt during cleanup")
        except Exception as e:
            print(f"Error during cleanup: {e}")
        finally:
            # Force destroy without raising exceptions
            try:
                self.root.quit()
                self.root.destroy()
            except Exception as e:
                print(f"Error destroying GUI: {e}")

def main():
    """Main entry point for GUI"""
    try:
        app = BinanceFuturesBotGUI()
        app.run()
    except Exception as e:
        print(f"Failed to start GUI: {e}")
        messagebox.showerror("Startup Error", f"Failed to start application:\n\n{str(e)}")

if __name__ == "__main__":
    main()

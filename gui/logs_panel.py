"""
Logs Panel for Monitoring Bot Activity
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Dict, List, Any, Optional
import threading
import time
from datetime import datetime
import os
import queue


class LogsPanel(ctk.CTkFrame):
    """Panel untuk menampilkan log aktivitas bot dengan real-time updates"""
    
    def __init__(self, parent, bot_interface=None):
        super().__init__(parent)
        
        self.bot_interface = bot_interface
        self.log_entries = []
        self.log_queue = queue.Queue()
        self.log_level_filter = "INFO"
        self.auto_scroll = True
        
        self._setup_ui()
        self._start_log_monitor()
    
    def _setup_ui(self):
        """Create logs panel layout"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="📋 Bot Logs & Activity",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        # Controls
        controls_frame = ctk.CTkFrame(self)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        # Log level filter
        ctk.CTkLabel(controls_frame, text="Log Level:").pack(side="left", padx=10)
        
        self.log_level_var = ctk.StringVar(value="INFO")
        log_level_combo = ctk.CTkOptionMenu(
            controls_frame,
            variable=self.log_level_var,
            values=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            command=self._on_log_level_changed
        )
        log_level_combo.pack(side="left", padx=10)
        
        # Auto-scroll toggle
        self.auto_scroll_var = ctk.BooleanVar(value=True)
        auto_scroll_switch = ctk.CTkSwitch(
            controls_frame,
            text="Auto Scroll",
            variable=self.auto_scroll_var,
            command=self.toggle_auto_scroll
        )
        auto_scroll_switch.pack(side="left", padx=20)
        
        # Clear logs button
        clear_button = ctk.CTkButton(
            controls_frame,
            text="🗑️ Clear",
            command=self.clear_logs,
            fg_color="red",
            hover_color="darkred",
            width=80
        )
        clear_button.pack(side="right", padx=5)
        
        # Export logs button
        export_button = ctk.CTkButton(
            controls_frame,
            text="💾 Export",
            command=self.export_logs,
            width=80
        )
        export_button.pack(side="right", padx=5)
        
        # Refresh button
        refresh_button = ctk.CTkButton(
            controls_frame,
            text="🔄 Refresh",
            command=self.refresh_logs,
            width=80
        )
        refresh_button.pack(side="right", padx=5)
        
        # Logs display
        logs_frame = ctk.CTkFrame(self)
        logs_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create text widget with scrollbar
        self.logs_text = ctk.CTkTextbox(
            logs_frame,
            font=ctk.CTkFont(family="Consolas", size=11),
            wrap="word"
        )
        self.logs_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add initial message
        self.add_log_entry("INFO", "Logs panel initialized")
    
    def add_log_entry(self, level: str, message: str):
        """Add log entry to display"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Color coding for log levels
        level_colors = {
            "DEBUG": "gray",
            "INFO": "white",
            "WARNING": "yellow",
            "ERROR": "orange",
            "CRITICAL": "red"
        }
        
        # Format log entry
        log_entry = f"[{timestamp}] {level:>8} | {message}\n"
        
        # Add to text widget
        self.logs_text.insert("end", log_entry)
        
        # Auto-scroll to bottom if enabled
        if self.auto_scroll_var.get():
            self.logs_text.see("end")
    
    def _on_log_level_changed(self, selected_level):
        """Handle log level filter change"""
        self.log_level_filter = selected_level
        self._refresh_log_display()
        self.add_log_entry("INFO", f"Log filter changed to: {selected_level}")
    
    def _refresh_log_display(self):
        """Refresh log display based on current filter"""
        if not self.log_entries:
            return
        
        # Clear current display
        self.logs_text.delete("1.0", "end")
        
        # Get log level hierarchy
        log_levels = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}
        current_level = log_levels.get(self.log_level_filter, 1)
        
        # Show only logs at or above the selected level
        for level, timestamp, message in self.log_entries:
            if log_levels.get(level, 0) >= current_level:
                log_entry = f"[{timestamp}] {level:>8} | {message}\n"
                self.logs_text.insert("end", log_entry)
        
        # Auto-scroll to bottom if enabled
        if self.auto_scroll_var.get():
            self.logs_text.see("end")
    
    def toggle_auto_scroll(self):
        """Toggle auto-scroll functionality"""
        self.auto_scroll = self.auto_scroll_var.get()
        status = "enabled" if self.auto_scroll else "disabled"
        self.add_log_entry("INFO", f"Auto-scroll {status}")
    
    def clear_logs(self):
        """Clear all logs from display"""
        if messagebox.askyesno("Confirm Clear", "Clear all logs from display?"):
            self.logs_text.delete("1.0", "end")
            self.add_log_entry("INFO", "Logs cleared")
    
    def refresh_logs(self):
        """Refresh logs from file"""
        try:
            # Load logs from file if it exists
            log_files = ["logs/trading_bot.log", "logs/gui.log"]
            
            for log_file in log_files:
                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        # Read last 100 lines
                        lines = f.readlines()[-100:]
                        
                    for line in lines:
                        # Parse log line and add to display
                        line = line.strip()
                        if line:
                            # Simple parsing - in real implementation would be more sophisticated
                            if "ERROR" in line:
                                level = "ERROR"
                            elif "WARNING" in line:
                                level = "WARNING"
                            elif "INFO" in line:
                                level = "INFO"
                            else:
                                level = "DEBUG"
                            
                            # Extract message (simplified)
                            parts = line.split(" - ", 2)
                            message = parts[-1] if len(parts) >= 3 else line
                            
                            self.logs_text.insert("end", f"{line}\n")
            
            if self.auto_scroll_var.get():
                self.logs_text.see("end")
                
            self.add_log_entry("INFO", "Logs refreshed from file")
            
        except Exception as e:
            self.add_log_entry("ERROR", f"Failed to refresh logs: {str(e)}")
    
    def export_logs(self):
        """Export logs to file"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Export Logs",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                logs_content = self.logs_text.get("1.0", "end")
                
                with open(file_path, 'w') as f:
                    f.write(logs_content)
                
                messagebox.showinfo("Success", f"Logs exported to {file_path}")
                self.add_log_entry("INFO", f"Logs exported to {file_path}")
                
        except Exception as e:
            error_msg = f"Failed to export logs: {str(e)}"
            messagebox.showerror("Error", error_msg)
            self.add_log_entry("ERROR", error_msg)
    
    def _start_log_monitor(self):
        """Start monitoring log files for changes"""
        # Don't start thread immediately, wait for GUI to be ready
        self.after(3000, self._delayed_log_start)  # Start after 3 seconds
    
    def _delayed_log_start(self):
        """Start log monitor after GUI is ready"""
        def monitor_logs():
            while True:
                try:
                    # Process log queue if available
                    if not self.log_queue.empty():
                        try:
                            level, message = self.log_queue.get_nowait()
                            # Use after() to update GUI from main thread
                            self.after(0, lambda: self.add_log_entry(level, message))
                        except queue.Empty:
                            pass
                    
                    # Check if bot is running and add periodic status
                    if self.bot_interface and hasattr(self.bot_interface, 'is_running'):
                        if self.bot_interface.is_running():
                            # Add periodic status updates (every 60 seconds)
                            time.sleep(60)
                            self.after(0, lambda: self.add_log_entry("DEBUG", "Bot is running - periodic status check"))
                        else:
                            time.sleep(10)
                    else:
                        time.sleep(10)
                        
                except Exception as e:
                    print(f"Log monitor error: {e}")
                    time.sleep(30)
        
        monitor_thread = threading.Thread(target=monitor_logs, daemon=True)
        monitor_thread.start()
    
    def log_trade_activity(self, symbol: str, action: str, details: Dict[str, Any]):
        """Log trading activity"""
        message = f"Trade activity - {action} {symbol}"
        if details.get('price'):
            message += f" @ ${details['price']:.4f}"
        if details.get('quantity'):
            message += f" qty: {details['quantity']:.4f}"
        
        self.add_log_entry("INFO", message)
    
    def log_signal_activity(self, symbol: str, signals: Dict[str, Any]):
        """Log signal activity"""
        action = signals.get('action', 'HOLD')
        strength = signals.get('signal_strength', 0)
        reason = signals.get('reason', 'No reason')
        
        message = f"Signal - {symbol}: {action} (strength: {strength:.2f}) - {reason}"
        
        if action in ['BUY', 'SELL', 'STRONG_BUY', 'STRONG_SELL']:
            self.add_log_entry("INFO", message)
        else:
            self.add_log_entry("DEBUG", message)
    
    def log_risk_event(self, event_type: str, symbol: str, details: str):
        """Log risk management events"""
        message = f"Risk event - {event_type}: {symbol} - {details}"
        
        if event_type in ['POSITION_CLOSED', 'STOP_LOSS', 'TAKE_PROFIT']:
            self.add_log_entry("WARNING", message)
        elif event_type in ['EMERGENCY_STOP', 'MAX_LOSS_REACHED']:
            self.add_log_entry("CRITICAL", message)
        else:
            self.add_log_entry("INFO", message)
    
    def log_error(self, error_message: str, context: str = ""):
        """Log error messages"""
        message = f"Error{(' in ' + context) if context else ''}: {error_message}"
        self.add_log_entry("ERROR", message)
    
    def update_data(self, symbol: str, signals: Dict[str, Any], 
                   risk_assessment: Dict[str, Any]):
        """Update panel with latest trading data"""
        # Log signal activity
        self.log_signal_activity(symbol, signals)
        
        # Log risk events if any
        risk_level = risk_assessment.get('risk_level', 'LOW')
        if risk_level in ['HIGH', 'CRITICAL']:
            violations = risk_assessment.get('violations', [])
            if violations:
                for violation in violations:
                    self.log_risk_event("RISK_VIOLATION", symbol, violation)

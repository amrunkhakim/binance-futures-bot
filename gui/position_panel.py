"""
Position Panel for Binance Futures Trading Bot GUI
Displays active positions, unrealized PnL, and position management
"""

import customtkinter as ctk
from typing import Dict, List, Any, Optional
import threading
import time
from datetime import datetime


class PositionPanel(ctk.CTkFrame):
    """Panel untuk menampilkan dan mengelola posisi trading"""
    
    def __init__(self, parent, bot_interface=None):
        super().__init__(parent)
        
        self.bot_interface = bot_interface
        self.positions_data = {}
        self.update_thread = None
        self.is_updating = False
        
        self._setup_ui()
        self._start_updates()
    
    def _setup_ui(self):
        """Setup UI components"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self._create_header()
        
        # Positions table
        self._create_positions_table()
        
        # Position actions
        self._create_position_actions()
    
    def _create_header(self):
        """Create header with summary info"""
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 Active Positions",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=4, pady=10)
        
        # Summary cards
        self.total_pnl_label = ctk.CTkLabel(
            header_frame,
            text="Total PnL: $0.00",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="gray"
        )
        self.total_pnl_label.grid(row=1, column=0, padx=5, pady=5)
        
        self.position_count_label = ctk.CTkLabel(
            header_frame,
            text="Positions: 0",
            font=ctk.CTkFont(size=14)
        )
        self.position_count_label.grid(row=1, column=1, padx=5, pady=5)
        
        self.margin_used_label = ctk.CTkLabel(
            header_frame,
            text="Margin Used: $0.00",
            font=ctk.CTkFont(size=14)
        )
        self.margin_used_label.grid(row=1, column=2, padx=5, pady=5)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄 Refresh",
            width=100,
            command=self._manual_refresh
        )
        refresh_btn.grid(row=1, column=3, padx=5, pady=5)
    
    def _create_positions_table(self):
        """Create scrollable table for positions"""
        # Main table frame
        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(1, weight=1)
        
        # Table headers
        headers_frame = ctk.CTkFrame(table_frame)
        headers_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 0))
        
        headers = [
            "Symbol", "Side", "Size", "Entry Price", 
            "Mark Price", "PnL", "ROE%", "Margin", "Actions"
        ]
        
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                headers_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold")
            )
            label.grid(row=0, column=i, padx=5, pady=5, sticky="w")
            headers_frame.grid_columnconfigure(i, weight=1)
        
        # Scrollable frame for position rows
        self.positions_scrollable = ctk.CTkScrollableFrame(
            table_frame,
            height=400
        )
        self.positions_scrollable.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure scrollable frame columns
        for i in range(len(headers)):
            self.positions_scrollable.grid_columnconfigure(i, weight=1)
        
        # No positions placeholder
        self.no_positions_label = ctk.CTkLabel(
            self.positions_scrollable,
            text="No active positions",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.no_positions_label.grid(row=0, column=0, columnspan=len(headers), pady=50)
    
    def _create_position_actions(self):
        """Create position action buttons"""
        actions_frame = ctk.CTkFrame(self)
        actions_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))
        actions_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Close all positions button
        close_all_btn = ctk.CTkButton(
            actions_frame,
            text="❌ Close All Positions",
            fg_color="red",
            hover_color="darkred",
            command=self._close_all_positions
        )
        close_all_btn.grid(row=0, column=0, padx=5, pady=10)
        
        # Reduce only mode toggle
        self.reduce_only_var = ctk.BooleanVar()
        reduce_only_checkbox = ctk.CTkCheckBox(
            actions_frame,
            text="Reduce Only Mode",
            variable=self.reduce_only_var,
            command=self._toggle_reduce_only
        )
        reduce_only_checkbox.grid(row=0, column=1, padx=5, pady=10)
        
        # Auto-close settings
        auto_close_btn = ctk.CTkButton(
            actions_frame,
            text="⚙️ Auto-Close Settings",
            command=self._show_auto_close_settings
        )
        auto_close_btn.grid(row=0, column=2, padx=5, pady=10)
    
    def _create_position_row(self, position_data: Dict, row: int):
        """Create a row for position data"""
        symbol = position_data.get('symbol', '')
        side = position_data.get('side', '')
        size = float(position_data.get('size', 0))
        entry_price = float(position_data.get('entryPrice', 0))
        mark_price = float(position_data.get('markPrice', 0))
        pnl = float(position_data.get('unRealizedProfit', 0))
        percentage = float(position_data.get('percentage', 0))
        margin = float(position_data.get('isolatedMargin', 0))
        
        # Determine colors based on side and PnL
        side_color = "green" if side == "LONG" else "red"
        pnl_color = "green" if pnl > 0 else "red" if pnl < 0 else "gray"
        
        # Symbol
        symbol_label = ctk.CTkLabel(
            self.positions_scrollable,
            text=symbol,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        symbol_label.grid(row=row, column=0, padx=5, pady=2, sticky="w")
        
        # Side
        side_label = ctk.CTkLabel(
            self.positions_scrollable,
            text=side,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=side_color
        )
        side_label.grid(row=row, column=1, padx=5, pady=2, sticky="w")
        
        # Size
        size_label = ctk.CTkLabel(
            self.positions_scrollable,
            text=f"{size:.4f}",
            font=ctk.CTkFont(size=12)
        )
        size_label.grid(row=row, column=2, padx=5, pady=2, sticky="w")
        
        # Entry Price
        entry_label = ctk.CTkLabel(
            self.positions_scrollable,
            text=f"${entry_price:.4f}",
            font=ctk.CTkFont(size=12)
        )
        entry_label.grid(row=row, column=3, padx=5, pady=2, sticky="w")
        
        # Mark Price
        mark_label = ctk.CTkLabel(
            self.positions_scrollable,
            text=f"${mark_price:.4f}",
            font=ctk.CTkFont(size=12)
        )
        mark_label.grid(row=row, column=4, padx=5, pady=2, sticky="w")
        
        # PnL
        pnl_label = ctk.CTkLabel(
            self.positions_scrollable,
            text=f"${pnl:.2f}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=pnl_color
        )
        pnl_label.grid(row=row, column=5, padx=5, pady=2, sticky="w")
        
        # ROE%
        roe_label = ctk.CTkLabel(
            self.positions_scrollable,
            text=f"{percentage:.2f}%",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=pnl_color
        )
        roe_label.grid(row=row, column=6, padx=5, pady=2, sticky="w")
        
        # Margin
        margin_label = ctk.CTkLabel(
            self.positions_scrollable,
            text=f"${margin:.2f}",
            font=ctk.CTkFont(size=12)
        )
        margin_label.grid(row=row, column=7, padx=5, pady=2, sticky="w")
        
        # Actions
        actions_frame = ctk.CTkFrame(self.positions_scrollable)
        actions_frame.grid(row=row, column=8, padx=5, pady=2, sticky="w")
        
        close_btn = ctk.CTkButton(
            actions_frame,
            text="Close",
            width=60,
            height=25,
            fg_color="red",
            hover_color="darkred",
            command=lambda: self._close_position(symbol)
        )
        close_btn.grid(row=0, column=0, padx=2)
        
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="Edit",
            width=60,
            height=25,
            command=lambda: self._edit_position(symbol)
        )
        edit_btn.grid(row=0, column=1, padx=2)
    
    def _clear_position_rows(self):
        """Clear all position rows"""
        try:
            children = self.positions_scrollable.winfo_children()
            for widget in children:
                try:
                    if widget.winfo_exists():
                        widget.destroy()
                except Exception as e:
                    print(f"Error destroying widget: {e}")
        except Exception as e:
            print(f"Error clearing position rows: {e}")
    
    def _update_positions_display(self):
        """Update positions display"""
        if not self.positions_data:
            # Show no positions message
            self._clear_position_rows()
            self.no_positions_label = ctk.CTkLabel(
                self.positions_scrollable,
                text="No active positions",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            self.no_positions_label.grid(row=0, column=0, columnspan=9, pady=50)
            return
        
        # Clear existing rows
        self._clear_position_rows()
        
        # Add position rows
        for i, (symbol, position) in enumerate(self.positions_data.items()):
            self._create_position_row(position, i)
        
        # Update summary
        self._update_summary()
    
    def _update_summary(self):
        """Update summary information"""
        if not self.positions_data:
            self.total_pnl_label.configure(text="Total PnL: $0.00", text_color="gray")
            self.position_count_label.configure(text="Positions: 0")
            self.margin_used_label.configure(text="Margin Used: $0.00")
            return
        
        # Calculate totals
        total_pnl = sum(float(pos.get('unRealizedProfit', 0)) for pos in self.positions_data.values())
        total_margin = sum(float(pos.get('isolatedMargin', 0)) for pos in self.positions_data.values())
        position_count = len(self.positions_data)
        
        # Update labels
        pnl_color = "green" if total_pnl > 0 else "red" if total_pnl < 0 else "gray"
        self.total_pnl_label.configure(
            text=f"Total PnL: ${total_pnl:.2f}",
            text_color=pnl_color
        )
        self.position_count_label.configure(text=f"Positions: {position_count}")
        self.margin_used_label.configure(text=f"Margin Used: ${total_margin:.2f}")
    
    def _manual_refresh(self):
        """Manual refresh of positions"""
        self._fetch_positions()
    
    def _fetch_positions(self):
        """Fetch positions from bot interface"""
        if not self.bot_interface:
            return
        
        try:
            # Simulate API call - replace with actual bot interface call
            positions = self.bot_interface.get_positions() if hasattr(self.bot_interface, 'get_positions') else {}
            self.positions_data = positions
            self._update_positions_display()
        except Exception as e:
            print(f"Error fetching positions: {e}")
    
    def _close_position(self, symbol: str):
        """Close specific position"""
        if not self.bot_interface:
            return
        
        try:
            # Confirm dialog would be good here
            result = self.bot_interface.close_position(symbol) if hasattr(self.bot_interface, 'close_position') else None
            if result:
                print(f"Position {symbol} closed successfully")
                self._fetch_positions()  # Refresh
        except Exception as e:
            print(f"Error closing position {symbol}: {e}")
    
    def _edit_position(self, symbol: str):
        """Edit position (add stop loss, take profit, etc.)"""
        # This would open a dialog for editing position parameters
        print(f"Edit position dialog for {symbol}")
    
    def _close_all_positions(self):
        """Close all positions"""
        if not self.bot_interface or not self.positions_data:
            return
        
        try:
            # Confirm dialog would be good here
            for symbol in self.positions_data.keys():
                self.bot_interface.close_position(symbol) if hasattr(self.bot_interface, 'close_position') else None
            
            print("All positions closed")
            self._fetch_positions()  # Refresh
        except Exception as e:
            print(f"Error closing all positions: {e}")
    
    def _toggle_reduce_only(self):
        """Toggle reduce only mode"""
        reduce_only = self.reduce_only_var.get()
        print(f"Reduce only mode: {'ON' if reduce_only else 'OFF'}")
        
        if self.bot_interface and hasattr(self.bot_interface, 'set_reduce_only_mode'):
            self.bot_interface.set_reduce_only_mode(reduce_only)
    
    def _show_auto_close_settings(self):
        """Show auto-close settings dialog"""
        # This would open a dialog for auto-close settings
        print("Auto-close settings dialog")
    
    def _start_updates(self):
        """Start background updates"""
        self.is_updating = True
        # Don't start thread immediately, wait for GUI to be ready
        self.after(5000, self._delayed_start)  # Start after 5 seconds
    
    def _delayed_start(self):
        """Start updates after GUI is ready"""
        if self.is_updating:
            self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
            self.update_thread.start()
    
    def _update_loop(self):
        """Background update loop"""
        while self.is_updating:
            try:
                self._fetch_positions()
                time.sleep(5)  # Update every 5 seconds
            except Exception as e:
                print(f"Error in position update loop: {e}")
                time.sleep(10)  # Wait longer on error
    
    def stop_updates(self):
        """Stop background updates"""
        self.is_updating = False
        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join(timeout=1)


if __name__ == "__main__":
    # Test the panel
    root = ctk.CTk()
    root.title("Position Panel Test")
    root.geometry("1200x800")
    
    panel = PositionPanel(root)
    panel.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Add some test data
    test_positions = {
        'BTCUSDT': {
            'symbol': 'BTCUSDT',
            'side': 'LONG',
            'size': '0.1',
            'entryPrice': '45000.0',
            'markPrice': '46500.0',
            'unRealizedProfit': '150.0',
            'percentage': '3.33',
            'isolatedMargin': '4500.0'
        },
        'ETHUSDT': {
            'symbol': 'ETHUSDT',
            'side': 'SHORT',
            'size': '1.5',
            'entryPrice': '3200.0',
            'markPrice': '3150.0',
            'unRealizedProfit': '75.0',
            'percentage': '2.34',
            'isolatedMargin': '4800.0'
        }
    }
    
    panel.positions_data = test_positions
    panel._update_positions_display()
    
    root.mainloop()

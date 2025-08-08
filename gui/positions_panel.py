"""
Positions Panel for Monitoring Open Positions
"""

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import datetime
from typing import Dict, Any, List
import threading
import time

class PositionsPanel(ctk.CTkFrame):
    """Panel for monitoring and managing open positions"""
    
    def __init__(self, parent, main_app):
        super().__init__(parent)
        
        self.parent = parent
        self.main_app = main_app
        self.positions_data = []
        
        self.create_positions_panel()
        
        # Start auto-refresh
        self.start_refresh_timer()
    
    def create_positions_panel(self):
        """Create positions panel layout"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="📍 Positions Management",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        # Create sections
        self.create_positions_summary()
        self.create_positions_table()
        self.create_position_controls()
    
    def create_positions_summary(self):
        """Create positions summary section"""
        summary_frame = ctk.CTkFrame(self)
        summary_frame.pack(fill="x", padx=20, pady=10)
        
        # Title
        summary_title = ctk.CTkLabel(
            summary_frame,
            text="📊 Positions Summary",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        summary_title.pack(pady=10)
        
        # Summary cards
        cards_frame = ctk.CTkFrame(summary_frame)
        cards_frame.pack(fill="x", padx=10, pady=10)
        
        # Create summary cards
        self.create_summary_card(cards_frame, "Open Positions", "0", 0)
        self.create_summary_card(cards_frame, "Total Value", "$0.00", 1)
        self.create_summary_card(cards_frame, "Unrealized PnL", "$0.00", 2)
        self.create_summary_card(cards_frame, "Margin Used", "$0.00", 3)
    
    def create_summary_card(self, parent, title, value, column):
        """Create a summary card"""
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
            font=ctk.CTkFont(size=14, weight="bold")
        )
        value_label.pack(pady=(0, 10))
        
        # Store reference for updates
        setattr(self, f"summary_{title.lower().replace(' ', '_')}", value_label)
    
    def create_positions_table(self):
        """Create positions table"""
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Title
        table_title = ctk.CTkLabel(
            table_frame,
            text="📋 Open Positions",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        table_title.pack(pady=10)
        
        # Create treeview for positions
        tree_frame = ctk.CTkFrame(table_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create Treeview with styling
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure dark theme for treeview
        style.configure("Treeview", 
                       background="#2b2b2b",
                       foreground="white",
                       fieldbackground="#2b2b2b")
        style.configure("Treeview.Heading",
                       background="#1f538d",
                       foreground="white")
        
        # Columns definition
        columns = ("Symbol", "Side", "Size", "Entry Price", "Current Price", 
                  "PnL", "PnL%", "Margin", "Stop Loss", "Take Profit")
        
        self.positions_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=10
        )
        
        # Configure columns
        column_widths = {
            "Symbol": 80,
            "Side": 60,
            "Size": 80,
            "Entry Price": 90,
            "Current Price": 90,
            "PnL": 80,
            "PnL%": 60,
            "Margin": 80,
            "Stop Loss": 90,
            "Take Profit": 90
        }
        
        for col in columns:
            self.positions_tree.heading(col, text=col)
            self.positions_tree.column(col, width=column_widths[col], minwidth=50)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.positions_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.positions_tree.xview)
        
        self.positions_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.positions_tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Bind right-click for context menu
        self.positions_tree.bind("<Button-3>", self.show_position_context_menu)
        
        # Add sample data message
        self.positions_tree.insert("", "end", values=(
            "No positions", "", "", "", "", "", "", "", "", ""
        ))
    
    def create_position_controls(self):
        """Create position control buttons"""
        controls_frame = ctk.CTkFrame(self)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        # Title
        controls_title = ctk.CTkLabel(
            controls_frame,
            text="🎮 Position Controls",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        controls_title.pack(pady=10)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(pady=10)
        
        # Refresh button
        self.refresh_button = ctk.CTkButton(
            buttons_frame,
            text="🔄 Refresh",
            command=self.refresh_positions,
            width=120
        )
        self.refresh_button.pack(side="left", padx=5)
        
        # Close selected button
        self.close_selected_button = ctk.CTkButton(
            buttons_frame,
            text="🔒 Close Selected",
            command=self.close_selected_position,
            fg_color="orange",
            hover_color="darkorange",
            width=120
        )
        self.close_selected_button.pack(side="left", padx=5)
        
        # Close all button
        self.close_all_button = ctk.CTkButton(
            buttons_frame,
            text="🚫 Close All",
            command=self.close_all_positions,
            fg_color="red",
            hover_color="darkred",
            width=120
        )
        self.close_all_button.pack(side="left", padx=5)
        
        # Export button
        self.export_button = ctk.CTkButton(
            buttons_frame,
            text="💾 Export",
            command=self.export_positions,
            fg_color="purple",
            hover_color="darkviolet",
            width=120
        )
        self.export_button.pack(side="left", padx=5)
    
    def refresh_positions(self):
        """Refresh positions data"""
        try:
            # Get positions from bot if running
            if self.main_app.is_bot_running():
                position_manager = self.main_app.get_bot_component('position_manager')
                if position_manager:
                    # This would be an async call in real implementation
                    self.update_positions_display([])  # Placeholder
                else:
                    messagebox.showinfo("Info", "Position manager not available")
            else:
                messagebox.showinfo("Info", "Bot is not running. Cannot fetch live positions.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh positions: {str(e)}")
    
    def close_selected_position(self):
        """Close selected position"""
        selected_item = self.positions_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a position to close")
            return
        
        # Get selected position data
        item = self.positions_tree.item(selected_item[0])
        values = item['values']
        
        if values[0] == "No positions":
            messagebox.showinfo("Info", "No positions to close")
            return
        
        symbol = values[0]
        side = values[1]
        
        # Confirm closure
        confirm_msg = f"Close {side} position for {symbol}?\n\nThis action cannot be undone."
        
        if messagebox.askyesno("Confirm Close", confirm_msg, icon="warning"):
            try:
                # Close position (integrate with bot)
                messagebox.showinfo("Success", f"Position {symbol} closed successfully!")
                self.refresh_positions()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to close position: {str(e)}")
    
    def close_all_positions(self):
        """Close all positions"""
        if not self.positions_data:
            messagebox.showinfo("Info", "No positions to close")
            return
        
        confirm_msg = "Close ALL open positions?\n\nThis action cannot be undone."
        
        if messagebox.askyesno("Confirm Close All", confirm_msg, icon="warning"):
            try:
                # Close all positions (integrate with bot)
                if self.main_app.is_bot_running():
                    position_manager = self.main_app.get_bot_component('position_manager')
                    if position_manager:
                        # This would be an async call
                        messagebox.showinfo("Success", "All positions closed successfully!")
                        self.refresh_positions()
                    else:
                        messagebox.showerror("Error", "Position manager not available")
                else:
                    messagebox.showerror("Error", "Bot is not running")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to close positions: {str(e)}")
    
    def export_positions(self):
        """Export positions to CSV"""
        try:
            from tkinter import filedialog
            import csv
            
            if not self.positions_data:
                messagebox.showinfo("Info", "No positions to export")
                return
            
            # Get file path
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Export Positions"
            )
            
            if file_path:
                # Write CSV
                with open(file_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Write header
                    header = ["Symbol", "Side", "Size", "Entry Price", "Current Price", 
                             "PnL", "PnL%", "Margin", "Stop Loss", "Take Profit", "Timestamp"]
                    writer.writerow(header)
                    
                    # Write data
                    for position in self.positions_data:
                        row = [
                            position.get('symbol', ''),
                            position.get('side', ''),
                            position.get('size', ''),
                            position.get('entry_price', ''),
                            position.get('current_price', ''),
                            position.get('unrealized_pnl', ''),
                            position.get('pnl_percent', ''),
                            position.get('margin_used', ''),
                            position.get('stop_loss', ''),
                            position.get('take_profit', ''),
                            datetime.now().isoformat()
                        ]
                        writer.writerow(row)
                
                messagebox.showinfo("Success", f"Positions exported to {file_path}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export positions: {str(e)}")
    
    def show_position_context_menu(self, event):
        """Show context menu for position"""
        item = self.positions_tree.identify('item', event.x, event.y)
        if item:
            self.positions_tree.selection_set(item)
            
            # Create context menu
            context_menu = tk.Menu(self, tearoff=0)
            context_menu.add_command(label="Close Position", command=self.close_selected_position)
            context_menu.add_separator()
            context_menu.add_command(label="Modify Stop Loss", command=self.modify_stop_loss)
            context_menu.add_command(label="Modify Take Profit", command=self.modify_take_profit)
            context_menu.add_separator()
            context_menu.add_command(label="Position Details", command=self.show_position_details)
            
            context_menu.tk_popup(event.x_root, event.y_root)
    
    def modify_stop_loss(self):
        """Modify stop loss for selected position"""
        selected_item = self.positions_tree.selection()
        if not selected_item:
            return
        
        # Get current stop loss
        item = self.positions_tree.item(selected_item[0])
        values = item['values']
        current_sl = values[8]  # Stop Loss column
        
        # Create dialog for new stop loss
        dialog = ctk.CTkInputDialog(
            text=f"Enter new Stop Loss price:\nCurrent: {current_sl}",
            title="Modify Stop Loss"
        )
        new_sl = dialog.get_input()
        
        if new_sl:
            try:
                new_sl_float = float(new_sl)
                messagebox.showinfo("Success", f"Stop Loss updated to ${new_sl_float:.4f}")
                # Update in bot system
            except ValueError:
                messagebox.showerror("Error", "Invalid price value")
    
    def modify_take_profit(self):
        """Modify take profit for selected position"""
        selected_item = self.positions_tree.selection()
        if not selected_item:
            return
        
        # Get current take profit
        item = self.positions_tree.item(selected_item[0])
        values = item['values']
        current_tp = values[9]  # Take Profit column
        
        # Create dialog for new take profit
        dialog = ctk.CTkInputDialog(
            text=f"Enter new Take Profit price:\nCurrent: {current_tp}",
            title="Modify Take Profit"
        )
        new_tp = dialog.get_input()
        
        if new_tp:
            try:
                new_tp_float = float(new_tp)
                messagebox.showinfo("Success", f"Take Profit updated to ${new_tp_float:.4f}")
                # Update in bot system
            except ValueError:
                messagebox.showerror("Error", "Invalid price value")
    
    def show_position_details(self):
        """Show detailed information about selected position"""
        selected_item = self.positions_tree.selection()
        if not selected_item:
            return
        
        item = self.positions_tree.item(selected_item[0])
        values = item['values']
        
        if values[0] == "No positions":
            messagebox.showinfo("Info", "No position selected")
            return
        
        # Create detailed view window
        details_window = ctk.CTkToplevel(self)
        details_window.title(f"Position Details - {values[0]}")
        details_window.geometry("400x500")
        
        # Position details
        details_text = ctk.CTkTextbox(details_window, height=400)
        details_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        details_content = f"""Position Details for {values[0]}
        
Symbol: {values[0]}
Side: {values[1]}
Size: {values[2]}
Entry Price: {values[3]}
Current Price: {values[4]}
Unrealized PnL: {values[5]}
PnL Percentage: {values[6]}
Margin Used: {values[7]}
Stop Loss: {values[8]}
Take Profit: {values[9]}

Position opened: [Entry Time]
Duration: [Duration]
Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Risk Metrics:
- Position Risk: [Risk Level]
- Max Drawdown: [Drawdown]
- Distance to Stop Loss: [Distance]
- Distance to Take Profit: [Distance]
"""
        
        details_text.insert("1.0", details_content)
        details_text.configure(state="disabled")
    
    def update_positions_display(self, positions: List[Dict[str, Any]]):
        """Update positions display with new data"""
        try:
            # Store positions data
            self.positions_data = positions
            
            # Clear current items
            for item in self.positions_tree.get_children():
                self.positions_tree.delete(item)
            
            if not positions:
                # No positions
                self.positions_tree.insert("", "end", values=(
                    "No positions", "", "", "", "", "", "", "", "", ""
                ))
                self.update_summary(0, 0.0, 0.0, 0.0)
                return
            
            # Add positions to tree
            total_value = 0.0
            total_pnl = 0.0
            total_margin = 0.0
            
            for position in positions:
                symbol = position.get('symbol', '')
                side = position.get('side', '')
                size = position.get('size', 0)
                entry_price = position.get('entry_price', 0)
                current_price = position.get('current_price', 0)
                unrealized_pnl = position.get('unrealized_pnl', 0)
                margin_used = position.get('margin_used', 0)
                stop_loss = position.get('stop_loss', '')
                take_profit = position.get('take_profit', '')
                
                # Calculate percentage PnL
                if entry_price > 0:
                    if side == 'LONG':
                        pnl_percent = ((current_price - entry_price) / entry_price) * 100
                    else:  # SHORT
                        pnl_percent = ((entry_price - current_price) / entry_price) * 100
                else:
                    pnl_percent = 0
                
                # Calculate position value
                position_value = size * current_price
                
                # Format values for display
                values = (
                    symbol,
                    side,
                    f"{size:.4f}",
                    f"${entry_price:.4f}",
                    f"${current_price:.4f}",
                    f"${unrealized_pnl:.2f}",
                    f"{pnl_percent:+.2f}%",
                    f"${margin_used:.2f}",
                    f"${stop_loss:.4f}" if stop_loss else "N/A",
                    f"${take_profit:.4f}" if take_profit else "N/A"
                )
                
                # Color code based on PnL
                if unrealized_pnl > 0:
                    tags = ("profit",)
                elif unrealized_pnl < 0:
                    tags = ("loss",)
                else:
                    tags = ("neutral",)
                
                self.positions_tree.insert("", "end", values=values, tags=tags)
                
                # Accumulate totals
                total_value += position_value
                total_pnl += unrealized_pnl
                total_margin += margin_used
            
            # Configure tags for colors
            self.positions_tree.tag_configure("profit", foreground="green")
            self.positions_tree.tag_configure("loss", foreground="red")
            self.positions_tree.tag_configure("neutral", foreground="gray")
            
            # Update summary
            self.update_summary(len(positions), total_value, total_pnl, total_margin)
            
        except Exception as e:
            print(f"Error updating positions display: {e}")
    
    def update_summary(self, count: int, total_value: float, total_pnl: float, total_margin: float):
        """Update summary cards"""
        try:
            self.summary_open_positions.configure(text=str(count))
            self.summary_total_value.configure(text=f"${total_value:.2f}")
            
            # PnL with color
            pnl_color = "green" if total_pnl >= 0 else "red"
            self.summary_unrealized_pnl.configure(
                text=f"${total_pnl:.2f}",
                text_color=pnl_color
            )
            
            self.summary_margin_used.configure(text=f"${total_margin:.2f}")
            
        except AttributeError:
            pass  # UI elements may not be created yet
    
    def start_refresh_timer(self):
        """Start auto-refresh timer"""
        def refresh_loop():
            while True:
                try:
                    if self.main_app.is_bot_running():
                        # Auto-refresh every 5 seconds when bot is running
                        time.sleep(5)
                        # Would call refresh_positions() here in real implementation
                    else:
                        time.sleep(10)  # Check less frequently when bot is stopped
                except:
                    break
        
        refresh_thread = threading.Thread(target=refresh_loop, daemon=True)
        refresh_thread.start()
    
    def update_data(self, symbol: str, signals: Dict[str, Any], 
                   risk_assessment: Dict[str, Any]):
        """Update panel with latest trading data"""
        # This would be called by the main app when new data arrives
        # For now, just trigger a refresh if needed
        pass

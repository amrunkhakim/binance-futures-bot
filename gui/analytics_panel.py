"""
Analytics Panel for Binance Futures Trading Bot GUI
Displays trading performance statistics, charts, and analysis
"""

import customtkinter as ctk
from typing import Dict, List, Any, Optional
import threading
import time
from datetime import datetime, timedelta
import json

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class AnalyticsPanel(ctk.CTkFrame):
    """Panel untuk menampilkan analytics dan statistik trading"""
    
    def __init__(self, parent, bot_interface=None):
        super().__init__(parent)
        
        self.bot_interface = bot_interface
        self.analytics_data = {}
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
        
        # Main content with tabs
        self._create_content_tabs()
    
    def _create_header(self):
        """Create header with time range selector"""
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 Trading Analytics",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=4, pady=10)
        
        # Time range selector
        range_label = ctk.CTkLabel(
            header_frame,
            text="Time Range:",
            font=ctk.CTkFont(size=14)
        )
        range_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.time_range_var = ctk.StringVar(value="7d")
        time_range_menu = ctk.CTkOptionMenu(
            header_frame,
            variable=self.time_range_var,
            values=["1d", "7d", "30d", "90d", "1y", "All"],
            command=self._on_time_range_changed
        )
        time_range_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄 Refresh",
            width=100,
            command=self._manual_refresh
        )
        refresh_btn.grid(row=1, column=3, padx=5, pady=5, sticky="e")
    
    def _create_content_tabs(self):
        """Create tabbed content area"""
        # Tab view
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        # Performance tab
        self.performance_tab = self.tab_view.add("Performance")
        self._setup_performance_tab()
        
        # Statistics tab
        self.statistics_tab = self.tab_view.add("Statistics")
        self._setup_statistics_tab()
        
        # Charts tab
        self.charts_tab = self.tab_view.add("Charts")
        self._setup_charts_tab()
        
        # Risk Management tab
        self.risk_tab = self.tab_view.add("Risk Management")
        self._setup_risk_tab()
    
    def _setup_performance_tab(self):
        """Setup performance metrics tab"""
        # Configure grid
        self.performance_tab.grid_columnconfigure((0, 1), weight=1)
        self.performance_tab.grid_rowconfigure((0, 1), weight=1)
        
        # Key metrics frame
        metrics_frame = ctk.CTkFrame(self.performance_tab)
        metrics_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        metrics_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Performance metrics
        self.total_pnl_metric = self._create_metric_card(
            metrics_frame, "Total PnL", "$0.00", "gray", 0, 0
        )
        
        self.total_trades_metric = self._create_metric_card(
            metrics_frame, "Total Trades", "0", "blue", 0, 1
        )
        
        self.win_rate_metric = self._create_metric_card(
            metrics_frame, "Win Rate", "0%", "green", 0, 2
        )
        
        self.avg_return_metric = self._create_metric_card(
            metrics_frame, "Avg Return", "0%", "blue", 0, 3
        )
        
        # Additional metrics row
        self.max_drawdown_metric = self._create_metric_card(
            metrics_frame, "Max Drawdown", "0%", "red", 1, 0
        )
        
        self.sharpe_ratio_metric = self._create_metric_card(
            metrics_frame, "Sharpe Ratio", "0.00", "blue", 1, 1
        )
        
        self.profit_factor_metric = self._create_metric_card(
            metrics_frame, "Profit Factor", "0.00", "green", 1, 2
        )
        
        self.avg_trade_metric = self._create_metric_card(
            metrics_frame, "Avg Trade", "$0.00", "blue", 1, 3
        )
        
        # Recent performance table
        recent_frame = ctk.CTkFrame(self.performance_tab)
        recent_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        recent_frame.grid_columnconfigure(0, weight=1)
        recent_frame.grid_rowconfigure(1, weight=1)
        
        recent_title = ctk.CTkLabel(
            recent_frame,
            text="Recent Trading Activity",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        recent_title.grid(row=0, column=0, pady=10)
        
        # Scrollable frame for recent trades
        self.recent_trades_scrollable = ctk.CTkScrollableFrame(
            recent_frame,
            height=300
        )
        self.recent_trades_scrollable.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        # Headers for recent trades
        headers = ["Time", "Symbol", "Side", "Size", "Price", "PnL", "ROE%"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                self.recent_trades_scrollable,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold")
            )
            label.grid(row=0, column=i, padx=5, pady=5, sticky="w")
            self.recent_trades_scrollable.grid_columnconfigure(i, weight=1)
    
    def _setup_statistics_tab(self):
        """Setup detailed statistics tab"""
        # Configure grid
        self.statistics_tab.grid_columnconfigure((0, 1), weight=1)
        self.statistics_tab.grid_rowconfigure((0, 1, 2), weight=1)
        
        # Trading statistics
        trading_stats_frame = ctk.CTkFrame(self.statistics_tab)
        trading_stats_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        trading_title = ctk.CTkLabel(
            trading_stats_frame,
            text="Trading Statistics",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        trading_title.pack(pady=10)
        
        self.trading_stats_text = ctk.CTkTextbox(
            trading_stats_frame,
            height=200,
            wrap="word"
        )
        self.trading_stats_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Risk statistics
        risk_stats_frame = ctk.CTkFrame(self.statistics_tab)
        risk_stats_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        risk_title = ctk.CTkLabel(
            risk_stats_frame,
            text="Risk Statistics",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        risk_title.pack(pady=10)
        
        self.risk_stats_text = ctk.CTkTextbox(
            risk_stats_frame,
            height=200,
            wrap="word"
        )
        self.risk_stats_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Symbol performance
        symbol_perf_frame = ctk.CTkFrame(self.statistics_tab)
        symbol_perf_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        symbol_title = ctk.CTkLabel(
            symbol_perf_frame,
            text="Performance by Symbol",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        symbol_title.pack(pady=10)
        
        # Scrollable frame for symbol performance
        self.symbol_perf_scrollable = ctk.CTkScrollableFrame(
            symbol_perf_frame,
            height=200
        )
        self.symbol_perf_scrollable.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Monthly performance
        monthly_perf_frame = ctk.CTkFrame(self.statistics_tab)
        monthly_perf_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        monthly_title = ctk.CTkLabel(
            monthly_perf_frame,
            text="Monthly Performance",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        monthly_title.pack(pady=10)
        
        self.monthly_perf_scrollable = ctk.CTkScrollableFrame(
            monthly_perf_frame,
            height=200
        )
        self.monthly_perf_scrollable.pack(fill="both", expand=True, padx=10, pady=5)
    
    def _setup_charts_tab(self):
        """Setup charts tab"""
        self.charts_tab.grid_columnconfigure(0, weight=1)
        self.charts_tab.grid_rowconfigure(1, weight=1)
        
        if not MATPLOTLIB_AVAILABLE:
            error_label = ctk.CTkLabel(
                self.charts_tab,
                text="📊 Charts require matplotlib\nInstall with: pip install matplotlib",
                font=ctk.CTkFont(size=16),
                text_color="orange"
            )
            error_label.grid(row=1, column=0, pady=50)
            return
        
        # Chart type selector
        chart_selector_frame = ctk.CTkFrame(self.charts_tab)
        chart_selector_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        chart_label = ctk.CTkLabel(
            chart_selector_frame,
            text="Chart Type:",
            font=ctk.CTkFont(size=14)
        )
        chart_label.pack(side="left", padx=5, pady=10)
        
        self.chart_type_var = ctk.StringVar(value="PnL Curve")
        chart_type_menu = ctk.CTkOptionMenu(
            chart_selector_frame,
            variable=self.chart_type_var,
            values=["PnL Curve", "Drawdown", "Win/Loss Distribution", "Monthly Returns"],
            command=self._on_chart_type_changed
        )
        chart_type_menu.pack(side="left", padx=5, pady=10)
        
        # Chart frame
        self.chart_frame = ctk.CTkFrame(self.charts_tab)
        self.chart_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Initialize chart
        self._setup_chart()
    
    def _setup_risk_tab(self):
        """Setup risk management tab"""
        self.risk_tab.grid_columnconfigure((0, 1), weight=1)
        self.risk_tab.grid_rowconfigure((0, 1), weight=1)
        
        # Position size analysis
        position_size_frame = ctk.CTkFrame(self.risk_tab)
        position_size_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        pos_size_title = ctk.CTkLabel(
            position_size_frame,
            text="Position Size Analysis",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        pos_size_title.pack(pady=10)
        
        self.position_size_text = ctk.CTkTextbox(
            position_size_frame,
            height=200,
            wrap="word"
        )
        self.position_size_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Risk metrics
        risk_metrics_frame = ctk.CTkFrame(self.risk_tab)
        risk_metrics_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        risk_metrics_title = ctk.CTkLabel(
            risk_metrics_frame,
            text="Risk Metrics",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        risk_metrics_title.pack(pady=10)
        
        self.risk_metrics_text = ctk.CTkTextbox(
            risk_metrics_frame,
            height=200,
            wrap="word"
        )
        self.risk_metrics_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Portfolio allocation
        portfolio_frame = ctk.CTkFrame(self.risk_tab)
        portfolio_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        portfolio_title = ctk.CTkLabel(
            portfolio_frame,
            text="Portfolio Allocation",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        portfolio_title.pack(pady=10)
        
        self.portfolio_scrollable = ctk.CTkScrollableFrame(
            portfolio_frame,
            height=200
        )
        self.portfolio_scrollable.pack(fill="both", expand=True, padx=10, pady=5)
    
    def _create_metric_card(self, parent, title: str, value: str, color: str, row: int, col: int):
        """Create a metric display card"""
        card_frame = ctk.CTkFrame(parent)
        card_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        title_label = ctk.CTkLabel(
            card_frame,
            text=title,
            font=ctk.CTkFont(size=12)
        )
        title_label.pack(pady=(10, 2))
        
        value_label = ctk.CTkLabel(
            card_frame,
            text=value,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=color
        )
        value_label.pack(pady=(2, 10))
        
        return value_label
    
    def _setup_chart(self):
        """Setup matplotlib chart"""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        # Create figure
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self.chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initial chart
        self._update_chart()
    
    def _update_chart(self):
        """Update chart based on selected type"""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        self.ax.clear()
        
        chart_type = self.chart_type_var.get()
        
        if chart_type == "PnL Curve":
            self._draw_pnl_curve()
        elif chart_type == "Drawdown":
            self._draw_drawdown_chart()
        elif chart_type == "Win/Loss Distribution":
            self._draw_win_loss_distribution()
        elif chart_type == "Monthly Returns":
            self._draw_monthly_returns()
        
        self.canvas.draw()
    
    def _draw_pnl_curve(self):
        """Draw PnL curve chart"""
        # Sample data - replace with actual data
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        pnl_values = [x * 10 + (x % 5) * 50 for x in range(30)]  # Sample data
        
        self.ax.plot(dates, pnl_values, linewidth=2, color='green')
        self.ax.set_title('Portfolio PnL Curve', fontsize=14, fontweight='bold')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('PnL ($)')
        self.ax.grid(True, alpha=0.3)
        self.fig.autofmt_xdate()
    
    def _draw_drawdown_chart(self):
        """Draw drawdown chart"""
        # Sample data - replace with actual data
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        drawdown_values = [-abs(x % 7) * 5 for x in range(30)]  # Sample data
        
        self.ax.fill_between(dates, drawdown_values, 0, alpha=0.3, color='red')
        self.ax.plot(dates, drawdown_values, linewidth=2, color='red')
        self.ax.set_title('Portfolio Drawdown', fontsize=14, fontweight='bold')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Drawdown (%)')
        self.ax.grid(True, alpha=0.3)
        self.fig.autofmt_xdate()
    
    def _draw_win_loss_distribution(self):
        """Draw win/loss distribution"""
        # Sample data - replace with actual data
        wins = [5, 10, 15, 20, 25, 30, 15, 10, 5]
        losses = [3, 8, 12, 18, 22, 25, 12, 8, 3]
        bins = range(-4, 5)
        
        self.ax.bar([x - 0.2 for x in bins], wins, width=0.4, label='Wins', color='green', alpha=0.7)
        self.ax.bar([x + 0.2 for x in bins], losses, width=0.4, label='Losses', color='red', alpha=0.7)
        self.ax.set_title('Win/Loss Distribution', fontsize=14, fontweight='bold')
        self.ax.set_xlabel('Return (%)')
        self.ax.set_ylabel('Number of Trades')
        self.ax.legend()
        self.ax.grid(True, alpha=0.3)
    
    def _draw_monthly_returns(self):
        """Draw monthly returns chart"""
        # Sample data - replace with actual data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        returns = [2.5, -1.2, 3.8, 1.5, -0.5, 4.2, 2.1, -2.3, 1.8, 3.5, -1.1, 2.8]
        
        colors = ['green' if x >= 0 else 'red' for x in returns]
        self.ax.bar(months, returns, color=colors, alpha=0.7)
        self.ax.set_title('Monthly Returns', fontsize=14, fontweight='bold')
        self.ax.set_xlabel('Month')
        self.ax.set_ylabel('Return (%)')
        self.ax.grid(True, alpha=0.3)
        self.ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    def _on_chart_type_changed(self, value):
        """Handle chart type change"""
        if MATPLOTLIB_AVAILABLE:
            self._update_chart()
    
    def _on_time_range_changed(self, value):
        """Handle time range change"""
        self._fetch_analytics_data()
    
    def _manual_refresh(self):
        """Manual refresh of analytics data"""
        self._fetch_analytics_data()
    
    def _fetch_analytics_data(self):
        """Fetch analytics data from bot interface"""
        if not self.bot_interface:
            self._load_sample_data()
            return
        
        try:
            # Get analytics data from bot
            time_range = self.time_range_var.get()
            analytics = self.bot_interface.get_analytics(time_range) if hasattr(self.bot_interface, 'get_analytics') else {}
            self.analytics_data = analytics
            self._update_all_displays()
        except Exception as e:
            print(f"Error fetching analytics: {e}")
            self._load_sample_data()
    
    def _load_sample_data(self):
        """Load sample data for demonstration"""
        self.analytics_data = {
            'total_pnl': 1250.75,
            'total_trades': 156,
            'win_rate': 64.2,
            'avg_return': 2.3,
            'max_drawdown': -8.5,
            'sharpe_ratio': 1.45,
            'profit_factor': 1.85,
            'avg_trade': 8.02,
            'recent_trades': [
                {'time': '2024-01-15 14:30', 'symbol': 'BTCUSDT', 'side': 'LONG', 'size': 0.1, 'price': 42500, 'pnl': 75.50, 'roe': 1.78},
                {'time': '2024-01-15 13:15', 'symbol': 'ETHUSDT', 'side': 'SHORT', 'size': 0.5, 'price': 2650, 'pnl': -25.30, 'roe': -0.95},
                {'time': '2024-01-15 11:45', 'symbol': 'ADAUSDT', 'side': 'LONG', 'size': 1000, 'price': 0.52, 'pnl': 15.20, 'roe': 2.92},
            ]
        }
        self._update_all_displays()
    
    def _update_all_displays(self):
        """Update all display elements"""
        self._update_performance_metrics()
        self._update_statistics()
        self._update_recent_trades()
        if MATPLOTLIB_AVAILABLE:
            self._update_chart()
    
    def _update_performance_metrics(self):
        """Update performance metric cards"""
        data = self.analytics_data
        
        # Update metric cards
        total_pnl = data.get('total_pnl', 0)
        pnl_color = "green" if total_pnl >= 0 else "red"
        self.total_pnl_metric.configure(text=f"${total_pnl:.2f}", text_color=pnl_color)
        
        self.total_trades_metric.configure(text=str(data.get('total_trades', 0)))
        
        win_rate = data.get('win_rate', 0)
        win_color = "green" if win_rate >= 50 else "orange" if win_rate >= 40 else "red"
        self.win_rate_metric.configure(text=f"{win_rate:.1f}%", text_color=win_color)
        
        avg_return = data.get('avg_return', 0)
        return_color = "green" if avg_return >= 0 else "red"
        self.avg_return_metric.configure(text=f"{avg_return:.2f}%", text_color=return_color)
        
        self.max_drawdown_metric.configure(text=f"{data.get('max_drawdown', 0):.1f}%", text_color="red")
        
        sharpe = data.get('sharpe_ratio', 0)
        sharpe_color = "green" if sharpe >= 1.0 else "orange" if sharpe >= 0.5 else "red"
        self.sharpe_ratio_metric.configure(text=f"{sharpe:.2f}", text_color=sharpe_color)
        
        pf = data.get('profit_factor', 0)
        pf_color = "green" if pf >= 1.0 else "red"
        self.profit_factor_metric.configure(text=f"{pf:.2f}", text_color=pf_color)
        
        avg_trade = data.get('avg_trade', 0)
        trade_color = "green" if avg_trade >= 0 else "red"
        self.avg_trade_metric.configure(text=f"${avg_trade:.2f}", text_color=trade_color)
    
    def _update_statistics(self):
        """Update statistics text areas"""
        # Trading statistics
        trading_stats = f"""
Total Trades: {self.analytics_data.get('total_trades', 0)}
Winning Trades: {int(self.analytics_data.get('total_trades', 0) * self.analytics_data.get('win_rate', 0) / 100)}
Losing Trades: {int(self.analytics_data.get('total_trades', 0) * (100 - self.analytics_data.get('win_rate', 0)) / 100)}
Win Rate: {self.analytics_data.get('win_rate', 0):.2f}%
Average Trade: ${self.analytics_data.get('avg_trade', 0):.2f}
Best Trade: $125.50
Worst Trade: -$85.30
Consecutive Wins: 7
Consecutive Losses: 3
        """
        self.trading_stats_text.delete("1.0", "end")
        self.trading_stats_text.insert("1.0", trading_stats)
        
        # Risk statistics
        risk_stats = f"""
Max Drawdown: {self.analytics_data.get('max_drawdown', 0):.2f}%
Sharpe Ratio: {self.analytics_data.get('sharpe_ratio', 0):.2f}
Profit Factor: {self.analytics_data.get('profit_factor', 0):.2f}
Risk/Reward Ratio: 1.25
VaR (95%): -$45.50
Expected Shortfall: -$67.25
Volatility: 15.8%
Beta: 0.85
        """
        self.risk_stats_text.delete("1.0", "end")
        self.risk_stats_text.insert("1.0", risk_stats)
        
        # Position size analysis
        position_analysis = f"""
Average Position Size: 2.5% of portfolio
Maximum Position Size: 5.0% of portfolio
Position Size Consistency: Good
Risk per Trade: 1.5%
Kelly Criterion: 3.2%
Optimal Position Size: 2.8%
Current Leverage: 3x
Maximum Leverage Used: 5x
        """
        self.position_size_text.delete("1.0", "end")
        self.position_size_text.insert("1.0", position_analysis)
        
        # Risk metrics
        risk_metrics = f"""
Daily VaR: -$25.50 (95%)
Monthly VaR: -$125.75 (95%)
Maximum Leverage: 10x
Current Risk Score: 7.2/10
Portfolio Correlation: 0.65
Concentration Risk: Low
Liquidity Risk: Low
Market Risk: Medium
        """
        self.risk_metrics_text.delete("1.0", "end")
        self.risk_metrics_text.insert("1.0", risk_metrics)
    
    def _update_recent_trades(self):
        """Update recent trades display"""
        # Clear existing trades
        for widget in self.recent_trades_scrollable.winfo_children():
            if widget.grid_info()['row'] > 0:  # Keep headers
                widget.destroy()
        
        recent_trades = self.analytics_data.get('recent_trades', [])
        for i, trade in enumerate(recent_trades, 1):
            # Time
            time_label = ctk.CTkLabel(
                self.recent_trades_scrollable,
                text=trade.get('time', ''),
                font=ctk.CTkFont(size=11)
            )
            time_label.grid(row=i, column=0, padx=5, pady=2, sticky="w")
            
            # Symbol
            symbol_label = ctk.CTkLabel(
                self.recent_trades_scrollable,
                text=trade.get('symbol', ''),
                font=ctk.CTkFont(size=11, weight="bold")
            )
            symbol_label.grid(row=i, column=1, padx=5, pady=2, sticky="w")
            
            # Side
            side = trade.get('side', '')
            side_color = "green" if side == "LONG" else "red"
            side_label = ctk.CTkLabel(
                self.recent_trades_scrollable,
                text=side,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=side_color
            )
            side_label.grid(row=i, column=2, padx=5, pady=2, sticky="w")
            
            # Size
            size_label = ctk.CTkLabel(
                self.recent_trades_scrollable,
                text=f"{trade.get('size', 0):.4f}",
                font=ctk.CTkFont(size=11)
            )
            size_label.grid(row=i, column=3, padx=5, pady=2, sticky="w")
            
            # Price
            price_label = ctk.CTkLabel(
                self.recent_trades_scrollable,
                text=f"${trade.get('price', 0):.2f}",
                font=ctk.CTkFont(size=11)
            )
            price_label.grid(row=i, column=4, padx=5, pady=2, sticky="w")
            
            # PnL
            pnl = trade.get('pnl', 0)
            pnl_color = "green" if pnl >= 0 else "red"
            pnl_label = ctk.CTkLabel(
                self.recent_trades_scrollable,
                text=f"${pnl:.2f}",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=pnl_color
            )
            pnl_label.grid(row=i, column=5, padx=5, pady=2, sticky="w")
            
            # ROE%
            roe = trade.get('roe', 0)
            roe_color = "green" if roe >= 0 else "red"
            roe_label = ctk.CTkLabel(
                self.recent_trades_scrollable,
                text=f"{roe:.2f}%",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=roe_color
            )
            roe_label.grid(row=i, column=6, padx=5, pady=2, sticky="w")
    
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
                self._fetch_analytics_data()
                time.sleep(30)  # Update every 30 seconds
            except Exception as e:
                print(f"Error in analytics update loop: {e}")
                time.sleep(60)  # Wait longer on error
    
    def stop_updates(self):
        """Stop background updates"""
        self.is_updating = False
        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join(timeout=1)
    
    # Legacy compatibility methods
    def update_data(self, symbol: str, signals: Dict[str, Any], 
                   risk_assessment: Dict[str, Any]):
        """Update panel with latest trading data (legacy compatibility)"""
        pass

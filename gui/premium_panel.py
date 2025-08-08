"""
Premium Subscription Panel
Interface untuk berlangganan premium dengan pembayaran QRIS
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from datetime import datetime
from typing import Dict, Any
import qrcode
from PIL import Image, ImageTk
import io
import threading
import webbrowser

from src.feature_gate import format_currency, calculate_savings_percentage

class PremiumPanel(ctk.CTkFrame):
    """Premium subscription panel with QRIS payment"""
    
    def __init__(self, parent, bot_interface):
        super().__init__(parent)
        
        self.parent = parent
        self.bot_interface = bot_interface
        self.subscription_manager = None
        self.current_payment_data = None
        
        # Initialize subscription manager
        self._init_subscription_manager()
        
        # Create UI
        self.create_premium_panel()
        
        # Start status refresh
        self.start_refresh_timer()
    
    def _init_subscription_manager(self):
        """Initialize subscription manager"""
        try:
            # Import here to avoid circular imports
            from src.subscription_manager import SubscriptionManager
            self.subscription_manager = SubscriptionManager()
        except Exception as e:
            print(f"Error initializing subscription manager: {e}")
            messagebox.showerror(
                "Error", 
                f"Failed to initialize subscription system: {e}"
            )
    
    def create_premium_panel(self):
        """Create premium subscription panel"""
        # Main scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title = ctk.CTkLabel(
            self.scrollable_frame,
            text="💎 Premium Subscription",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        # Create sections
        self.create_status_section()
        self.create_features_comparison()
        self.create_pricing_section()
        self.create_payment_section()
        self.create_contact_section()
    
    def create_status_section(self):
        """Create subscription status section"""
        status_frame = ctk.CTkFrame(self.scrollable_frame)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        # Section title
        status_title = ctk.CTkLabel(
            status_frame,
            text="📊 Status Berlangganan",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        status_title.pack(pady=10)
        
        # Status info frame
        self.status_info_frame = ctk.CTkFrame(status_frame)
        self.status_info_frame.pack(fill="x", padx=20, pady=10)
        
        # Status labels (will be updated)
        self.status_type_label = ctk.CTkLabel(
            self.status_info_frame,
            text="Tipe: Free",
            font=ctk.CTkFont(size=14)
        )
        self.status_type_label.pack(pady=5)
        
        self.status_expiry_label = ctk.CTkLabel(
            self.status_info_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.status_expiry_label.pack(pady=2)
        
        # Update status
        self.update_status_display()
    
    def create_features_comparison(self):
        """Create features comparison table"""
        features_frame = ctk.CTkFrame(self.scrollable_frame)
        features_frame.pack(fill="x", padx=20, pady=10)
        
        # Section title
        features_title = ctk.CTkLabel(
            features_frame,
            text="✨ Perbandingan Fitur",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        features_title.pack(pady=10)
        
        # Comparison table
        table_frame = ctk.CTkFrame(features_frame)
        table_frame.pack(fill="x", padx=20, pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(table_frame)
        header_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(header_frame, text="Fitur", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=20)
        ctk.CTkLabel(header_frame, text="Free", font=ctk.CTkFont(weight="bold")).pack(side="right", padx=50)
        ctk.CTkLabel(header_frame, text="Premium", font=ctk.CTkFont(weight="bold")).pack(side="right", padx=50)
        
        # Feature rows
        features = [
            ("Dashboard Basic", "✅", "✅"),
            ("Manual Trading", "✅", "✅"),
            ("Price Monitoring", "✅", "✅"),
            ("Bot Trading Otomatis", "❌", "✅"),
            ("AI Analysis", "❌", "✅"),
            ("Advanced Analytics", "❌", "✅"),
            ("Risk Management", "❌", "✅"),
            ("Multi-Strategy", "❌", "✅"),
            ("Telegram Alerts", "❌", "✅"),
            ("Backtesting", "❌", "✅"),
            ("Portfolio Management", "❌", "✅"),
            ("Custom Indicators", "❌", "✅"),
        ]
        
        for feature, free_status, premium_status in features:
            row_frame = ctk.CTkFrame(table_frame)
            row_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row_frame, text=feature).pack(side="left", padx=20)
            ctk.CTkLabel(row_frame, text=premium_status, text_color="green" if premium_status=="✅" else "red").pack(side="right", padx=50)
            ctk.CTkLabel(row_frame, text=free_status, text_color="green" if free_status=="✅" else "red").pack(side="right", padx=50)
    
    def create_pricing_section(self):
        """Create pricing section"""
        pricing_frame = ctk.CTkFrame(self.scrollable_frame)
        pricing_frame.pack(fill="x", padx=20, pady=10)
        
        # Section title
        pricing_title = ctk.CTkLabel(
            pricing_frame,
            text="💰 Paket Berlangganan",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        pricing_title.pack(pady=10)
        
        # Pricing cards container
        cards_frame = ctk.CTkFrame(pricing_frame)
        cards_frame.pack(fill="x", padx=20, pady=10)
        
        # Monthly plan
        monthly_card = self.create_pricing_card(
            cards_frame, 
            "Bulanan", 
            "Rp 99.000", 
            "per bulan",
            ["Semua fitur premium", "Support 24/7", "Update gratis"],
            "monthly",
            0
        )
        
        # Yearly plan  
        savings = calculate_savings_percentage(99000, 999000)
        yearly_card = self.create_pricing_card(
            cards_frame,
            "Tahunan",
            "Rp 999.000",
            f"per tahun (Hemat {savings}%)",
            ["Semua fitur premium", "Support 24/7", "Update gratis", "Prioritas support"],
            "yearly", 
            1,
            is_popular=True
        )
    
    def create_pricing_card(self, parent, title, price, period, features, plan_type, column, is_popular=False):
        """Create pricing card"""
        card = ctk.CTkFrame(parent)
        card.grid(row=0, column=column, padx=10, pady=5, sticky="nsew")
        parent.grid_columnconfigure(column, weight=1)
        
        if is_popular:
            # Popular badge
            badge = ctk.CTkLabel(
                card,
                text="🌟 POPULER",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="gold"
            )
            badge.pack(pady=(10, 5))
        
        # Title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Price
        price_label = ctk.CTkLabel(
            card,
            text=price,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="green"
        )
        price_label.pack(pady=5)
        
        # Period
        period_label = ctk.CTkLabel(
            card,
            text=period,
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        period_label.pack(pady=(0, 15))
        
        # Features
        for feature in features:
            feature_label = ctk.CTkLabel(
                card,
                text=f"✅ {feature}",
                font=ctk.CTkFont(size=12)
            )
            feature_label.pack(pady=2)
        
        # Subscribe button
        subscribe_button = ctk.CTkButton(
            card,
            text=f"Berlangganan {title}",
            command=lambda: self.show_payment_dialog(plan_type),
            fg_color="green",
            hover_color="darkgreen",
            font=ctk.CTkFont(weight="bold")
        )
        subscribe_button.pack(pady=20)
        
        return card
    
    def create_payment_section(self):
        """Create payment methods section"""
        payment_frame = ctk.CTkFrame(self.scrollable_frame)
        payment_frame.pack(fill="x", padx=20, pady=10)
        
        # Section title
        payment_title = ctk.CTkLabel(
            payment_frame,
            text="💳 Metode Pembayaran",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        payment_title.pack(pady=10)
        
        # Payment methods
        methods_frame = ctk.CTkFrame(payment_frame)
        methods_frame.pack(fill="x", padx=20, pady=10)
        
        methods_text = """
🏛️ Bank Transfer / Mobile Banking
💳 E-Wallet (GoPay, OVO, DANA, LinkAja)
📱 QRIS (Scan & Pay)
🛒 Virtual Account

Semua pembayaran menggunakan sistem QRIS untuk kemudahan dan keamanan.
        """
        
        methods_label = ctk.CTkLabel(
            methods_frame,
            text=methods_text.strip(),
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        methods_label.pack(pady=10)
    
    def create_contact_section(self):
        """Create contact section"""
        contact_frame = ctk.CTkFrame(self.scrollable_frame)
        contact_frame.pack(fill="x", padx=20, pady=10)
        
        # Section title
        contact_title = ctk.CTkLabel(
            contact_frame,
            text="📱 Bantuan & Support",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        contact_title.pack(pady=10)
        
        # Contact info
        contact_text = """
WhatsApp: 081391782567
📧 Email: support@binancebot.com
🕐 Waktu Layanan: 24/7

Untuk aktivasi manual setelah pembayaran, silakan hubungi WhatsApp
dengan menyertakan bukti pembayaran dan Transaction ID.
        """
        
        contact_label = ctk.CTkLabel(
            contact_frame,
            text=contact_text.strip(),
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        contact_label.pack(pady=10)
        
        # WhatsApp button
        whatsapp_button = ctk.CTkButton(
            contact_frame,
            text="💬 Chat WhatsApp",
            command=self.open_whatsapp,
            fg_color="green",
            hover_color="darkgreen"
        )
        whatsapp_button.pack(pady=10)
    
    def show_payment_dialog(self, plan_type: str):
        """Show QRIS payment dialog"""
        if not self.subscription_manager:
            messagebox.showerror("Error", "Subscription manager tidak tersedia")
            return
        
        # Generate QRIS payment data
        try:
            payment_data = self.subscription_manager.generate_qris_payment_data(plan_type)
            self.current_payment_data = payment_data
            
            # Create payment window
            self.create_payment_window(payment_data)
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuat QRIS: {e}")
    
    def create_payment_window(self, payment_data: Dict):
        """Create payment window with QRIS"""
        # Create new window
        payment_window = ctk.CTkToplevel(self)
        payment_window.title("Pembayaran QRIS")
        payment_window.geometry("500x700")
        payment_window.grab_set()  # Make modal
        
        # Center window
        payment_window.update_idletasks()
        x = (payment_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (payment_window.winfo_screenheight() // 2) - (700 // 2)
        payment_window.geometry(f"500x700+{x}+{y}")
        
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(payment_window)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            scroll_frame,
            text="💳 Pembayaran QRIS",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Payment details
        details_frame = ctk.CTkFrame(scroll_frame)
        details_frame.pack(fill="x", pady=10)
        
        details_text = f"""
📋 Detail Pembayaran

Merchant: {payment_data['merchant_name']}
Paket: {payment_data['plan_type'].title()}
Jumlah: {format_currency(payment_data['amount'])}
Transaction ID: {payment_data['transaction_id']}
        """
        
        details_label = ctk.CTkLabel(
            details_frame,
            text=details_text.strip(),
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        details_label.pack(pady=10)
        
        # Generate and display QR code
        self.create_qr_code_display(scroll_frame, payment_data)
        
        # Payment instructions
        instructions_frame = ctk.CTkFrame(scroll_frame)
        instructions_frame.pack(fill="x", pady=10)
        
        instructions_title = ctk.CTkLabel(
            instructions_frame,
            text="📝 Langkah Pembayaran",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        instructions_title.pack(pady=(10, 5))
        
        for i, instruction in enumerate(payment_data['payment_instructions'], 1):
            instruction_label = ctk.CTkLabel(
                instructions_frame,
                text=f"{instruction}",
                font=ctk.CTkFont(size=11),
                justify="left",
                anchor="w"
            )
            instruction_label.pack(fill="x", padx=10, pady=1)
        
        # Buttons
        button_frame = ctk.CTkFrame(scroll_frame)
        button_frame.pack(fill="x", pady=10)
        
        # Copy transaction ID button
        copy_button = ctk.CTkButton(
            button_frame,
            text="📋 Copy Transaction ID",
            command=lambda: self.copy_to_clipboard(payment_data['transaction_id']),
            fg_color="blue"
        )
        copy_button.pack(side="left", padx=5)
        
        # WhatsApp button
        whatsapp_button = ctk.CTkButton(
            button_frame,
            text="💬 WhatsApp Support",
            command=lambda: self.open_whatsapp_with_transaction(payment_data['transaction_id']),
            fg_color="green"
        )
        whatsapp_button.pack(side="right", padx=5)
        
        # Close button
        close_button = ctk.CTkButton(
            scroll_frame,
            text="Tutup",
            command=payment_window.destroy,
            fg_color="gray"
        )
        close_button.pack(pady=20)
    
    def create_qr_code_display(self, parent, payment_data: Dict):
        """Create and display QR code"""
        try:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(payment_data['qris_string'])
            qr.make(fit=True)
            
            # Create QR image
            qr_image = qr.make_image(fill_color="black", back_color="white")
            qr_image = qr_image.resize((250, 250))
            
            # Convert to PhotoImage
            qr_photo = ImageTk.PhotoImage(qr_image)
            
            # Display QR code
            qr_frame = ctk.CTkFrame(parent)
            qr_frame.pack(pady=10)
            
            qr_label = ctk.CTkLabel(qr_frame, text="", image=qr_photo)
            qr_label.image = qr_photo  # Keep reference
            qr_label.pack(pady=10)
            
            qr_title = ctk.CTkLabel(
                qr_frame,
                text="📱 Scan QR Code untuk membayar",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            qr_title.pack(pady=5)
            
        except Exception as e:
            error_label = ctk.CTkLabel(
                parent,
                text=f"Error generating QR Code: {e}",
                text_color="red"
            )
            error_label.pack(pady=10)
    
    def copy_to_clipboard(self, text: str):
        """Copy text to clipboard"""
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
            messagebox.showinfo("Success", f"Transaction ID copied: {text}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy: {e}")
    
    def open_whatsapp(self):
        """Open WhatsApp"""
        phone = "081391782567"
        message = "Halo, saya tertarik dengan Binance Bot Premium. Mohon informasi lebih lanjut."
        url = f"https://wa.me/{phone}?text={message}"
        webbrowser.open(url)
    
    def open_whatsapp_with_transaction(self, transaction_id: str):
        """Open WhatsApp with transaction info"""
        phone = "081391782567"
        message = f"Halo, saya telah melakukan pembayaran untuk Binance Bot Premium.\\nTransaction ID: {transaction_id}\\nMohon aktivasi akun premium saya."
        url = f"https://wa.me/{phone}?text={message}"
        webbrowser.open(url)
    
    def update_status_display(self):
        """Update subscription status display"""
        if not self.subscription_manager:
            return
        
        try:
            status = self.subscription_manager.get_subscription_status()
            
            # Update status type
            status_color = "green" if status['is_premium'] else "orange"
            self.status_type_label.configure(
                text=f"Status: {status['type']}", 
                text_color=status_color
            )
            
            # Update expiry info
            if status['is_premium']:
                expiry_text = f"Berakhir dalam {status['days_remaining']} hari"
                if status['days_remaining'] <= 7:
                    expiry_color = "red"
                elif status['days_remaining'] <= 30:
                    expiry_color = "orange"
                else:
                    expiry_color = "green"
                    
                self.status_expiry_label.configure(
                    text=expiry_text,
                    text_color=expiry_color
                )
            else:
                self.status_expiry_label.configure(
                    text="Upgrade ke Premium untuk fitur lengkap",
                    text_color="gray"
                )
                
        except Exception as e:
            print(f"Error updating status: {e}")
    
    def start_refresh_timer(self):
        """Start status refresh timer"""
        self.update_status_display()
        self.after(30000, self.start_refresh_timer)  # Update every 30 seconds
    
    def stop_updates(self):
        """Stop background updates"""
        # Called when panel is destroyed
        pass

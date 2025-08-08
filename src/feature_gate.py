"""
Feature Gate
Decorator dan utilities untuk membatasi akses fitur berdasarkan subscription
"""

import functools
from typing import Callable, Any
from tkinter import messagebox
import logging

logger = logging.getLogger(__name__)

class FeatureGate:
    """Feature gating system for subscription-based access control"""
    
    def __init__(self, subscription_manager):
        """Initialize feature gate with subscription manager"""
        self.subscription_manager = subscription_manager
    
    def require_premium(self, feature_name: str = None):
        """Decorator to require premium subscription for function access"""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Get feature name from function name if not provided
                if feature_name is None:
                    fname = func.__name__
                    # Convert function name to feature name
                    if fname.startswith('start_'):
                        fname = fname.replace('start_', '')
                    elif fname.startswith('enable_'):
                        fname = fname.replace('enable_', '')
                    elif fname.startswith('show_'):
                        fname = fname.replace('show_', '')
                else:
                    fname = feature_name
                
                # Check if user has access
                if self.subscription_manager.has_feature_access(fname):
                    return func(*args, **kwargs)
                else:
                    # Show premium upgrade message
                    self._show_premium_required_dialog(fname)
                    return None
            return wrapper
        return decorator
    
    def require_feature(self, feature_name: str):
        """Decorator to require specific feature access"""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if self.subscription_manager.has_feature_access(feature_name):
                    return func(*args, **kwargs)
                else:
                    self._show_premium_required_dialog(feature_name)
                    return None
            return wrapper
        return decorator
    
    def check_feature_access(self, feature_name: str, show_dialog: bool = True) -> bool:
        """Check if user has access to feature"""
        has_access = self.subscription_manager.has_feature_access(feature_name)
        
        if not has_access and show_dialog:
            self._show_premium_required_dialog(feature_name)
        
        return has_access
    
    def _show_premium_required_dialog(self, feature_name: str):
        """Show premium subscription required dialog"""
        message = self.subscription_manager.get_feature_limitation_message(feature_name)
        
        # Show custom dialog with upgrade option
        result = messagebox.askyesno(
            "Fitur Premium Diperlukan",
            message + "\n\nApakah Anda ingin melihat halaman berlangganan sekarang?",
            icon="info"
        )
        
        if result:
            # This would trigger showing the subscription panel
            # The actual implementation depends on the GUI framework
            logger.info(f"User wants to upgrade for feature: {feature_name}")
    
    def get_feature_button_text(self, base_text: str, feature_name: str) -> str:
        """Get appropriate button text based on feature access"""
        if self.subscription_manager.has_feature_access(feature_name):
            return base_text
        else:
            return f"🔒 {base_text} (Premium)"
    
    def get_feature_status_text(self, feature_name: str) -> str:
        """Get status text for feature"""
        if self.subscription_manager.has_feature_access(feature_name):
            return "✅ Aktif"
        else:
            return "🔒 Premium"
    
    def disable_widget_if_no_access(self, widget, feature_name: str):
        """Disable widget if user doesn't have access to feature"""
        if not self.subscription_manager.has_feature_access(feature_name):
            if hasattr(widget, 'configure'):
                widget.configure(state="disabled")
            elif hasattr(widget, 'config'):
                widget.config(state="disabled")
    
    def create_premium_overlay_frame(self, parent, feature_name: str):
        """Create overlay frame for premium features"""
        import customtkinter as ctk
        
        overlay = ctk.CTkFrame(parent)
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Premium lock icon and message
        lock_label = ctk.CTkLabel(
            overlay,
            text="🔒",
            font=ctk.CTkFont(size=48)
        )
        lock_label.pack(pady=(50, 10))
        
        title_label = ctk.CTkLabel(
            overlay,
            text="Fitur Premium",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=10)
        
        desc_label = ctk.CTkLabel(
            overlay,
            text="Fitur ini hanya tersedia untuk pengguna Premium.\nUpgrade sekarang untuk mengakses semua fitur bot!",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        desc_label.pack(pady=10)
        
        upgrade_button = ctk.CTkButton(
            overlay,
            text="💎 Upgrade ke Premium",
            command=lambda: self._show_premium_required_dialog(feature_name),
            fg_color="gold",
            hover_color="orange",
            text_color="black",
            font=ctk.CTkFont(weight="bold")
        )
        upgrade_button.pack(pady=20)
        
        return overlay


def premium_feature(feature_name: str = None):
    """Decorator function for premium features (standalone usage)"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Assume self has subscription_manager
            if hasattr(self, 'subscription_manager'):
                gate = FeatureGate(self.subscription_manager)
                if gate.check_feature_access(feature_name or func.__name__):
                    return func(self, *args, **kwargs)
            elif hasattr(self, 'bot_interface') and hasattr(self.bot_interface, 'subscription_manager'):
                gate = FeatureGate(self.bot_interface.subscription_manager)
                if gate.check_feature_access(feature_name or func.__name__):
                    return func(self, *args, **kwargs)
            else:
                # Fallback: show basic message
                messagebox.showwarning(
                    "Premium Feature", 
                    f"Fitur '{feature_name or func.__name__}' memerlukan subscription Premium."
                )
            return None
        return wrapper
    return decorator


# Utility functions
def format_currency(amount: int, currency: str = "IDR") -> str:
    """Format currency amount"""
    if currency == "IDR":
        return f"Rp {amount:,}".replace(",", ".")
    return f"{currency} {amount:,}"

def calculate_savings_percentage(monthly: int, yearly: int) -> int:
    """Calculate savings percentage for yearly plan"""
    monthly_yearly_cost = monthly * 12
    savings = monthly_yearly_cost - yearly
    return int((savings / monthly_yearly_cost) * 100)

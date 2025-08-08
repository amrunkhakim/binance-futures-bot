"""
Subscription Manager
Mengelola status berlangganan, validasi lisensi, dan pembatasan fitur
"""

import json
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class SubscriptionManager:
    """Manages subscription status and feature access"""
    
    def __init__(self):
        """Initialize subscription manager"""
        self.license_file = Path("config/license.json")
        self.subscription_data = self._load_subscription_data()
        
        # Free tier features
        self.free_features = [
            "basic_dashboard",
            "manual_trading", 
            "basic_logs",
            "price_monitoring"
        ]
        
        # Premium features
        self.premium_features = [
            "automated_trading",
            "ai_analysis", 
            "advanced_analytics",
            "risk_management",
            "multi_strategy",
            "telegram_alerts",
            "backtesting",
            "portfolio_management",
            "custom_indicators",
            "api_access"
        ]
        
        # Payment info
        self.payment_info = {
            "phone": "081391782567",
            "name": "Binance Bot Premium",
            "monthly_price": 99000,
            "yearly_price": 999000,
            "currency": "IDR"
        }
    
    def _load_subscription_data(self) -> Dict:
        """Load subscription data from file"""
        try:
            if self.license_file.exists():
                with open(self.license_file, 'r') as f:
                    data = json.load(f)
                    return data
            else:
                # Default free subscription data
                return {
                    "subscription_type": "free",
                    "expiry_date": None,
                    "license_key": None,
                    "features": [
                        "basic_dashboard",
                        "manual_trading", 
                        "basic_logs",
                        "price_monitoring"
                    ],
                    "payment_verified": False,
                    "created_at": datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Error loading subscription data: {e}")
            return {
                "subscription_type": "free",
                "expiry_date": None,
                "license_key": None,
                "features": [
                    "basic_dashboard",
                    "manual_trading", 
                    "basic_logs",
                    "price_monitoring"
                ],
                "payment_verified": False,
                "created_at": datetime.now().isoformat()
            }
    
    def _save_subscription_data(self):
        """Save subscription data to file"""
        try:
            # Create config directory if not exists
            self.license_file.parent.mkdir(exist_ok=True)
            
            with open(self.license_file, 'w') as f:
                json.dump(self.subscription_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving subscription data: {e}")
    
    def is_premium_user(self) -> bool:
        """Check if user has active premium subscription"""
        if not self.subscription_data.get("payment_verified", False):
            return False
            
        expiry_date = self.subscription_data.get("expiry_date")
        if not expiry_date:
            return False
            
        try:
            expiry = datetime.fromisoformat(expiry_date)
            return datetime.now() < expiry
        except:
            return False
    
    def has_feature_access(self, feature: str) -> bool:
        """Check if user has access to specific feature"""
        if feature in self.free_features:
            return True
            
        if feature in self.premium_features:
            return self.is_premium_user()
            
        return False
    
    def get_subscription_status(self) -> Dict:
        """Get current subscription status"""
        is_premium = self.is_premium_user()
        days_remaining = 0
        
        if is_premium:
            expiry_date = datetime.fromisoformat(self.subscription_data["expiry_date"])
            days_remaining = (expiry_date - datetime.now()).days
        
        return {
            "type": "Premium" if is_premium else "Free",
            "is_premium": is_premium,
            "expiry_date": self.subscription_data.get("expiry_date"),
            "days_remaining": days_remaining,
            "payment_verified": self.subscription_data.get("payment_verified", False),
            "available_features": self.get_available_features()
        }
    
    def get_available_features(self) -> List[str]:
        """Get list of available features for current subscription"""
        if self.is_premium_user():
            return self.free_features + self.premium_features
        else:
            return self.free_features.copy()
    
    def get_premium_features(self) -> List[str]:
        """Get list of premium-only features"""
        return self.premium_features.copy()
    
    def generate_qris_payment_data(self, plan_type: str = "monthly") -> Dict:
        """Generate QRIS payment data"""
        amount = self.payment_info["monthly_price"] if plan_type == "monthly" else self.payment_info["yearly_price"]
        
        # Generate unique transaction ID
        timestamp = str(int(time.time()))
        transaction_id = hashlib.md5(f"{timestamp}{plan_type}".encode()).hexdigest()[:8].upper()
        
        return {
            "merchant_name": self.payment_info["name"],
            "phone_number": self.payment_info["phone"],
            "amount": amount,
            "currency": self.payment_info["currency"],
            "transaction_id": transaction_id,
            "plan_type": plan_type,
            "description": f"Binance Bot Premium - {plan_type.title()} Subscription",
            "qris_string": self._generate_qris_string(amount, transaction_id),
            "payment_instructions": [
                "1. Buka aplikasi mobile banking atau e-wallet Anda",
                "2. Pilih menu 'Scan QR Code' atau 'QRIS'", 
                "3. Scan kode QR di atas",
                "4. Pastikan nominal dan merchant sesuai",
                "5. Masukkan PIN untuk konfirmasi pembayaran",
                "6. Simpan bukti pembayaran",
                "7. Kirim screenshot bukti pembayaran ke WhatsApp: 081391782567",
                "8. Sertakan Transaction ID dalam pesan"
            ]
        }
    
    def _generate_qris_string(self, amount: int, transaction_id: str) -> str:
        """Generate QRIS string (simplified format)"""
        # This is a simplified QRIS format for demonstration
        # In production, you would use proper QRIS library
        phone = self.payment_info["phone"]
        
        qris_data = f"00020101021126570014ID.CO.QRIS.WWW0215ID{phone}02153940{transaction_id}5204599953033605406{amount}5802ID5924{self.payment_info['name'][:24]}6007Jakarta61056130062070503***630445B9"
        
        return qris_data
    
    def verify_payment(self, transaction_id: str, payment_proof: str = None) -> bool:
        """Verify payment and activate subscription"""
        # In a real implementation, you would verify payment with payment gateway
        # For now, we'll simulate manual verification
        
        # This would be called after manual verification via WhatsApp
        return self._activate_premium_subscription(transaction_id)
    
    def _activate_premium_subscription(self, transaction_id: str, plan_type: str = "monthly") -> bool:
        """Activate premium subscription"""
        try:
            duration_days = 30 if plan_type == "monthly" else 365
            expiry_date = datetime.now() + timedelta(days=duration_days)
            
            # Generate license key
            license_key = hashlib.sha256(f"{transaction_id}{expiry_date.isoformat()}".encode()).hexdigest()[:16].upper()
            
            self.subscription_data.update({
                "subscription_type": "premium",
                "expiry_date": expiry_date.isoformat(),
                "license_key": license_key,
                "features": self.free_features + self.premium_features,
                "payment_verified": True,
                "transaction_id": transaction_id,
                "activated_at": datetime.now().isoformat(),
                "plan_type": plan_type
            })
            
            self._save_subscription_data()
            
            logger.info(f"Premium subscription activated: {transaction_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error activating subscription: {e}")
            return False
    
    def deactivate_subscription(self):
        """Deactivate subscription (reset to free)"""
        self.subscription_data.update({
            "subscription_type": "free",
            "expiry_date": None,
            "license_key": None,
            "features": self.free_features.copy(),
            "payment_verified": False,
            "deactivated_at": datetime.now().isoformat()
        })
        
        self._save_subscription_data()
        logger.info("Subscription deactivated")
    
    def get_feature_limitation_message(self, feature: str) -> str:
        """Get message for feature limitation"""
        feature_descriptions = {
            "automated_trading": "Bot Trading Otomatis",
            "ai_analysis": "Analisis AI & Machine Learning", 
            "advanced_analytics": "Analitik Mendalam & Reporting",
            "risk_management": "Manajemen Risiko Lanjutan",
            "multi_strategy": "Multi-Strategy Trading",
            "telegram_alerts": "Notifikasi Telegram Real-time",
            "backtesting": "Backtesting & Optimasi Strategi",
            "portfolio_management": "Manajemen Portfolio",
            "custom_indicators": "Custom Indicators",
            "api_access": "API Access untuk Integrasi"
        }
        
        feature_name = feature_descriptions.get(feature, feature.replace("_", " ").title())
        
        return f"""🔒 Fitur Premium: {feature_name}

Fitur ini hanya tersedia untuk pengguna Premium.

✨ Dengan berlangganan Premium, Anda mendapatkan:
• Bot trading otomatis 24/7
• Analisis AI & Machine Learning
• Manajemen risiko lanjutan  
• Multi-strategy trading
• Notifikasi real-time
• Backtesting & optimasi
• Dan masih banyak lagi!

💰 Harga berlangganan:
• Bulanan: Rp 99.000
• Tahunan: Rp 999.000 (hemat 17%)

📱 Untuk berlangganan, silakan hubungi:
WhatsApp: 081391782567

Atau gunakan menu 'Premium Upgrade' di aplikasi."""

    def get_payment_info(self) -> Dict:
        """Get payment information"""
        return self.payment_info.copy()

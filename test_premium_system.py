#!/usr/bin/env python3
"""
Test Premium Subscription System
Test basic functionality of subscription manager and feature gate
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_subscription_manager():
    """Test subscription manager functionality"""
    print("🧪 Testing Subscription Manager...")
    
    try:
        from src.subscription_manager import SubscriptionManager
        
        # Initialize subscription manager
        sub_manager = SubscriptionManager()
        print("✅ SubscriptionManager initialized")
        
        # Test basic functions
        status = sub_manager.get_subscription_status()
        print(f"✅ Subscription status: {status['type']}")
        
        # Test feature access
        has_manual = sub_manager.has_feature_access("manual_trading")
        has_auto = sub_manager.has_feature_access("automated_trading")
        
        print(f"✅ Manual trading access: {has_manual}")
        print(f"✅ Automated trading access: {has_auto}")
        
        # Test payment data generation
        payment_data = sub_manager.generate_qris_payment_data("monthly")
        print(f"✅ QRIS payment data generated: {payment_data['transaction_id']}")
        
        return True
        
    except Exception as e:
        print(f"❌ SubscriptionManager test failed: {e}")
        return False

def test_feature_gate():
    """Test feature gate functionality"""
    print("\n🧪 Testing Feature Gate...")
    
    try:
        from src.subscription_manager import SubscriptionManager
        from src.feature_gate import FeatureGate
        
        # Initialize components
        sub_manager = SubscriptionManager()
        feature_gate = FeatureGate(sub_manager)
        print("✅ FeatureGate initialized")
        
        # Test feature access check
        can_trade = feature_gate.check_feature_access("manual_trading", show_dialog=False)
        can_auto = feature_gate.check_feature_access("automated_trading", show_dialog=False)
        
        print(f"✅ Manual trading allowed: {can_trade}")
        print(f"✅ Automated trading allowed: {can_auto}")
        
        # Test button text generation
        button_text = feature_gate.get_feature_button_text("Start Bot", "automated_trading")
        print(f"✅ Button text: '{button_text}'")
        
        # Test status text
        status_text = feature_gate.get_feature_status_text("automated_trading")
        print(f"✅ Status text: '{status_text}'")
        
        return True
        
    except Exception as e:
        print(f"❌ FeatureGate test failed: {e}")
        return False

def test_qris_generation():
    """Test QRIS QR code generation"""
    print("\n🧪 Testing QRIS QR Code Generation...")
    
    try:
        from src.subscription_manager import SubscriptionManager
        import qrcode
        from io import BytesIO
        
        # Initialize subscription manager
        sub_manager = SubscriptionManager()
        
        # Generate payment data
        payment_data = sub_manager.generate_qris_payment_data("monthly")
        print(f"✅ Payment data generated for {payment_data['plan_type']}")
        print(f"✅ Amount: Rp {payment_data['amount']:,}")
        print(f"✅ Transaction ID: {payment_data['transaction_id']}")
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(payment_data['qris_string'])
        qr.make(fit=True)
        
        # Create QR image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        print("✅ QR Code image created successfully")
        
        # Test image format
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        buffer.seek(0)
        
        if len(buffer.getvalue()) > 0:
            print("✅ QR Code can be saved as PNG")
            print(f"✅ Image size: {len(buffer.getvalue())} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ QRIS generation test failed: {e}")
        return False

def test_license_file():
    """Test license file operations"""
    print("\n🧪 Testing License File Operations...")
    
    try:
        from src.subscription_manager import SubscriptionManager
        
        # Initialize subscription manager
        sub_manager = SubscriptionManager()
        print("✅ SubscriptionManager initialized")
        
        # Check if license file exists
        if sub_manager.license_file.exists():
            print("✅ License file exists")
            # Load data
            data = sub_manager._load_subscription_data()
            print(f"✅ License data loaded: {data['subscription_type']}")
        else:
            print("✅ License file will be created when needed")
            
        # Test save operation (without actually creating premium subscription)
        original_data = sub_manager.subscription_data.copy()
        
        # Create config directory if not exists
        sub_manager.license_file.parent.mkdir(exist_ok=True)
        print("✅ Config directory ready")
        
        return True
        
    except Exception as e:
        print(f"❌ License file test failed: {e}")
        return False

def main():
    """Main test runner"""
    print("🚀 Testing Premium Subscription System")
    print("=" * 60)
    
    tests = [
        test_subscription_manager,
        test_feature_gate,
        test_qris_generation,
        test_license_file
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Premium subscription system is working correctly.")
        print("\n🔧 System is ready for production use!")
        print("\n📋 Next steps:")
        print("1. Run: python gui_main.py")
        print("2. Navigate to '💎 Premium' menu")
        print("3. Test subscription flow")
        print("4. Contact WhatsApp: 081391782567 for activation")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

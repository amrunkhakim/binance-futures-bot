#!/usr/bin/env python3
"""
Install Dependencies for Premium Subscription System
Installs required packages: qrcode, pillow
"""

import subprocess
import sys
import os

def install_package(package_name):
    """Install a Python package using pip"""
    try:
        print(f"Installing {package_name}...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", package_name
        ], capture_output=True, text=True, check=True)
        print(f"✅ Successfully installed {package_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package_name}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_package(package_name):
    """Check if a package is already installed"""
    try:
        __import__(package_name)
        print(f"✅ {package_name} is already installed")
        return True
    except ImportError:
        print(f"❌ {package_name} is not installed")
        return False

def main():
    """Main installation script"""
    print("🚀 Installing Premium Subscription System Dependencies...")
    print("=" * 60)
    
    # List of required packages
    packages = [
        "qrcode[pil]",  # QR code generation with PIL support
        "Pillow",       # Image processing (if not included with qrcode[pil])
    ]
    
    # Check existing installations
    print("\n📋 Checking existing installations:")
    installed = []
    for package in ["qrcode", "PIL"]:
        if check_package(package):
            installed.append(package)
    
    # Install missing packages
    print("\n📦 Installing missing packages:")
    success_count = 0
    
    for package in packages:
        if install_package(package):
            success_count += 1
        print()
    
    print("=" * 60)
    
    # Final verification
    print("\n🔍 Verifying installations:")
    all_good = True
    
    try:
        import qrcode
        from PIL import Image
        print("✅ QR Code generation: OK")
        print("✅ Image processing (PIL): OK")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        all_good = False
    
    print("\n" + "=" * 60)
    
    if all_good:
        print("🎉 All dependencies installed successfully!")
        print("\nPremium subscription system is ready to use!")
        print("\nFeatures enabled:")
        print("• QRIS payment QR code generation")
        print("• Image processing for QR codes")
        print("• Subscription management")
        print("• Feature gating system")
    else:
        print("❌ Some dependencies failed to install.")
        print("Please check the errors above and try again.")
        print("\nYou can also install manually:")
        print("pip install qrcode[pil] Pillow")
        
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

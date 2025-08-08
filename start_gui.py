#!/usr/bin/env python3
"""
GUI Startup Script for Binance Futures Trading Bot
Launches the modern GUI interface
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

def check_gui_dependencies():
    """Check if GUI dependencies are installed"""
    required_packages = [
        'customtkinter',
        'PIL',  # Pillow
        'matplotlib'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            if package == 'PIL':
                missing.append('Pillow')
            else:
                missing.append(package)
    
    if missing:
        print("❌ Missing GUI dependencies:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n💡 Install GUI dependencies with:")
        print("   pip install -r requirements_gui.txt")
        return False
    
    return True

def main():
    """Main entry point for GUI"""
    print("🚀 Starting Binance Futures Trading Bot GUI...")
    
    # Check GUI dependencies
    if not check_gui_dependencies():
        return 1
    
    try:
        # Import and start GUI
        from gui_main import main as gui_main
        return gui_main()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        print("   pip install -r requirements_gui.txt")
        return 1
    
    except Exception as e:
        print(f"❌ Failed to start GUI: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

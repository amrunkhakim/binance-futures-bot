#!/usr/bin/env python3
"""
Quick Start Script for Binance Futures Trading Bot
This script provides an easy way to start the bot with basic validation
"""

import sys
import os
import asyncio
import logging
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

def setup_logging():
    """Setup basic logging configuration"""
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/bot_startup.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_environment():
    """Check if environment is properly configured"""
    errors = []
    
    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        errors.append("❌ .env file not found. Please copy .env.example to .env and configure it.")
    
    # Check Python version
    if sys.version_info < (3, 9):
        errors.append("❌ Python 3.9 or higher is required")
    
    # Check if required directories exist
    required_dirs = ['src', 'logs']
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            errors.append(f"❌ Directory '{dir_name}' not found")
    
    return errors

def print_banner():
    """Print welcome banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         🚀 BINANCE FUTURES TRADING BOT 🚀                    ║
║                                                              ║
║  Advanced Trading Bot with Technical Analysis & Risk Mgmt   ║
║                                                              ║
║  Author: Amrun Khakim                                       ║
║  Version: 1.0.0                                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_warnings():
    """Print important warnings"""
    warnings = """
⚠️  IMPORTANT WARNINGS ⚠️

🔹 TRADING CRYPTOCURRENCY IS EXTREMELY RISKY
🔹 You can lose ALL of your invested money
🔹 This bot does NOT guarantee profits
🔹 Always test with small amounts first
🔹 Use TESTNET for initial testing
🔹 Never invest more than you can afford to lose

📋 CHECKLIST BEFORE STARTING:
✓ API keys are correctly configured in .env
✓ You understand the risks involved
✓ You have tested strategies in testnet
✓ Risk management parameters are set appropriately
✓ You have sufficient balance for minimum trade amounts

    """
    print(warnings)

def get_user_confirmation():
    """Get user confirmation before starting"""
    print("🤔 Do you understand the risks and want to continue? (yes/no): ", end="")
    
    try:
        response = input().strip().lower()
        return response in ['yes', 'y']
    except KeyboardInterrupt:
        print("\n❌ Cancelled by user")
        return False

async def start_bot():
    """Start the trading bot"""
    try:
        # Import here to avoid issues if modules aren't available
        from main import main
        
        print("🚀 Starting Binance Futures Trading Bot...")
        print("📊 Initializing components...")
        
        # Run the main bot
        await main()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
        return False
    except KeyboardInterrupt:
        print("\n⏹️  Bot stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        return False

def main():
    """Main entry point"""
    setup_logging()
    
    print_banner()
    
    # Check environment
    errors = check_environment()
    if errors:
        print("❌ Environment check failed:")
        for error in errors:
            print(f"   {error}")
        print("\n💡 Please fix the above issues and try again.")
        return 1
    
    print("✅ Environment check passed")
    
    print_warnings()
    
    # Get user confirmation
    if not get_user_confirmation():
        print("❌ User cancelled. Bot not started.")
        return 1
    
    print("\n" + "="*60)
    print("🎯 STARTING TRADING BOT")
    print("="*60)
    
    try:
        # Run the bot
        asyncio.run(start_bot())
        return 0
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        return 0
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

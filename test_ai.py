#!/usr/bin/env python3
"""
Test script for AI Analyzer functionality
Tests the Gemini AI integration with sample data
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.ai_analyzer import AIAnalyzer

async def test_ai_analyzer():
    """Test AI Analyzer with sample data"""
    print("🤖 Testing AI Analyzer Integration")
    print("=" * 50)
    
    # Initialize AI analyzer
    ai_analyzer = AIAnalyzer()
    
    # Test connection
    print("\n1. Testing AI Connection...")
    connection_test = await ai_analyzer.test_connection()
    print(f"Status: {connection_test['status']}")
    print(f"Available: {connection_test['available']}")
    print(f"Message: {connection_test['message']}")
    
    if not connection_test['available']:
        print("❌ AI Analyzer not available. Please check your API key and internet connection.")
        return
    
    print("✅ AI Connection successful!")
    
    # Test market sentiment analysis
    print("\n2. Testing Market Sentiment Analysis...")
    
    # Sample market data
    sample_market_data = {
        "price": 43250.50,
        "volume": 1.5,
        "price_change_24h": 1250.75,
        "price_change_percent": 2.95,
        "high_24h": 44000.00,
        "low_24h": 42000.00
    }
    
    # Sample technical analysis data
    sample_technical_data = {
        "rsi": {"value": 65.5},
        "macd": {"signal": "BULLISH"},
        "ema": {"trend": "BULLISH"},
        "bollinger_bands": {"position": "MIDDLE"},
        "support_resistance": {
            "support": 42000.00,
            "resistance": 45000.00
        },
        "volume": {"ratio": 1.5}
    }
    
    try:
        sentiment_result = await ai_analyzer.analyze_market_sentiment(
            "BTCUSDT", sample_market_data, sample_technical_data
        )
        
        print("Market Sentiment Analysis Results:")
        print(f"  • Sentiment: {sentiment_result['ai_sentiment']}")
        print(f"  • Confidence: {sentiment_result['confidence']:.2f}")
        print(f"  • Recommendation: {sentiment_result['recommendation']}")
        print(f"  • Risk Level: {sentiment_result['risk_level']}")
        print(f"  • Key Factors: {sentiment_result['key_factors']}")
        print(f"  • Reasoning: {sentiment_result['reasoning'][:100]}...")
        
    except Exception as e:
        print(f"❌ Error in sentiment analysis: {e}")
    
    # Test trading signal generation
    print("\n3. Testing AI Trading Signal Generation...")
    
    # Sample historical data
    sample_historical_data = [
        {"close": 42000, "volume": 1000000},
        {"close": 42500, "volume": 1200000},
        {"close": 43000, "volume": 800000},
        {"close": 43250, "volume": 1500000},
        {"close": 43100, "volume": 900000}
    ]
    
    # Sample technical indicators
    sample_indicators = {
        "rsi": 65.5,
        "macd": {
            "macd": 150.25,
            "signal": 120.30,
            "histogram": 29.95
        },
        "ema": {
            "fast": 43100,
            "slow": 42800,
            "trend": 42950
        },
        "bollinger_bands": {
            "upper": 44500,
            "middle": 43250,
            "lower": 42000,
            "position": "MIDDLE"
        }
    }
    
    try:
        signal_result = await ai_analyzer.generate_trading_signals(
            "BTCUSDT", sample_historical_data, sample_indicators
        )
        
        print("AI Trading Signal Results:")
        print(f"  • Action: {signal_result['action']}")
        print(f"  • Signal Strength: {signal_result['signal_strength']:.2f}")
        print(f"  • Entry Price: {signal_result['entry_price']}")
        print(f"  • Stop Loss: {signal_result['stop_loss']}")
        print(f"  • Take Profit: {signal_result['take_profit']}")
        print(f"  • Risk/Reward Ratio: {signal_result['risk_reward_ratio']:.2f}")
        print(f"  • Time Horizon: {signal_result['time_horizon']}")
        print(f"  • AI Confidence: {signal_result['ai_confidence']:.2f}")
        print(f"  • Reasoning: {signal_result['reasoning'][:100]}...")
        
    except Exception as e:
        print(f"❌ Error in signal generation: {e}")
    
    # Test risk assessment
    print("\n4. Testing AI Risk Assessment...")
    
    # Sample position data
    sample_position = {
        "size": 0.1,
        "entry_price": 42000,
        "current_price": 43250,
        "unrealized_pnl": 125.0,
        "leverage": 3
    }
    
    # Sample market conditions
    sample_market_conditions = {
        "volatility": 0.025,
        "trend": "BULLISH",
        "volume_profile": "NORMAL"
    }
    
    try:
        risk_result = await ai_analyzer.analyze_risk_assessment(
            "BTCUSDT", sample_position, sample_market_conditions
        )
        
        print("AI Risk Assessment Results:")
        print(f"  • Risk Level: {risk_result['risk_level']}")
        print(f"  • Risk Score: {risk_result['risk_score']:.2f}")
        print(f"  • Max Position Size: {risk_result['max_position_size']:.1%}")
        print(f"  • Stop Loss Adjustment: {risk_result['stop_loss_adjustment']:.2f}%")
        print(f"  • Volatility Assessment: {risk_result['volatility_assessment']}")
        print(f"  • Risk Factors: {risk_result['risk_factors']}")
        print(f"  • Recommendations: {risk_result['recommendations']}")
        print(f"  • AI Confidence: {risk_result['ai_confidence']:.2f}")
        
    except Exception as e:
        print(f"❌ Error in risk assessment: {e}")
    
    # Test market insights
    print("\n5. Testing Market Insights...")
    
    try:
        insights_result = await ai_analyzer.get_market_insights("BTCUSDT", "1h")
        
        print("Market Insights Results:")
        print(f"  • Symbol: {insights_result['symbol']}")
        print(f"  • Timeframe: {insights_result['timeframe']}")
        print(f"  • Source: {insights_result['source']}")
        print(f"  • Insights: {insights_result['insights'][:200]}...")
        
    except Exception as e:
        print(f"❌ Error getting market insights: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 AI Analyzer testing completed!")

async def main():
    """Main test function"""
    try:
        await test_ai_analyzer()
    except KeyboardInterrupt:
        print("\n⏸️ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    print("🚀 Starting AI Analyzer Test")
    print("Make sure you have installed: pip install google-generativeai")
    print("API Key will be loaded from environment or default value")
    print()
    
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Failed to run tests: {e}")

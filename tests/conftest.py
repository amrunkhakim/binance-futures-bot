"""
Pytest configuration and fixtures for the Binance Futures Bot tests
"""
import asyncio
import pytest
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def sample_market_data():
    """Sample market data for testing"""
    return {
        "price": 43250.50,
        "volume": 1.5,
        "price_change_24h": 1250.75,
        "price_change_percent": 2.95,
        "high_24h": 44000.00,
        "low_24h": 42000.00
    }

@pytest.fixture
def sample_technical_data():
    """Sample technical analysis data for testing"""
    return {
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

@pytest.fixture
def sample_historical_data():
    """Sample historical data for testing"""
    return [
        {"close": 42000, "volume": 1000000},
        {"close": 42500, "volume": 1200000},
        {"close": 43000, "volume": 800000},
        {"close": 43250, "volume": 1500000},
        {"close": 43100, "volume": 900000}
    ]

"""
AI-Enhanced Trading Analysis using Gemini AI
Provides intelligent market analysis and trading recommendations
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

try:
    import google.generativeai as genai
except ImportError:
    genai = None

class AIAnalyzer:
    """AI-powered trading analysis using Gemini AI"""
    
    def __init__(self, api_key: str = "AIzaSyC8Hlbk3I4k78OLIA6Chp1Zip6wJ6TRdqM"):
        """Initialize AI analyzer with Gemini API key"""
        self.api_key = api_key
        self.model = None
        self.logger = logging.getLogger(__name__)
        
        # Initialize Gemini AI
        self._initialize_ai()
        
    def _initialize_ai(self):
        """Initialize Gemini AI model"""
        try:
            if genai is None:
                self.logger.error("Google Generative AI library not installed. Install with: pip install google-generativeai")
                return False
                
            genai.configure(api_key=self.api_key)
            
            # Configure model settings for trading analysis
            generation_config = {
                "temperature": 0.7,  # Balanced creativity vs consistency
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
            
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
            ]
            
            self.model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            self.logger.info("✅ Gemini AI initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Gemini AI: {e}")
            return False
    
    async def analyze_market_sentiment(self, symbol: str, market_data: Dict[str, Any], 
                                     technical_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze market sentiment using AI
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            market_data: Current market data
            technical_analysis: Technical indicators data
            
        Returns:
            Dict containing AI sentiment analysis
        """
        try:
            if not self.model:
                return self._fallback_sentiment_analysis(market_data, technical_analysis)
            
            # Prepare data for AI analysis
            analysis_data = self._prepare_market_data(symbol, market_data, technical_analysis)
            
            # Create prompt for AI analysis
            prompt = self._create_sentiment_prompt(analysis_data)
            
            # Get AI response
            response = await self._get_ai_response(prompt)
            
            # Parse AI response
            sentiment_result = self._parse_sentiment_response(response)
            
            return {
                "ai_sentiment": sentiment_result.get("sentiment", "NEUTRAL"),
                "confidence": sentiment_result.get("confidence", 0.5),
                "reasoning": sentiment_result.get("reasoning", "AI analysis unavailable"),
                "key_factors": sentiment_result.get("key_factors", []),
                "recommendation": sentiment_result.get("recommendation", "HOLD"),
                "risk_level": sentiment_result.get("risk_level", "MEDIUM"),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in AI sentiment analysis: {e}")
            return self._fallback_sentiment_analysis(market_data, technical_analysis)
    
    async def generate_trading_signals(self, symbol: str, historical_data: List[Dict], 
                                     technical_indicators: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate AI-enhanced trading signals
        
        Args:
            symbol: Trading symbol
            historical_data: Historical price data
            technical_indicators: Technical analysis results
            
        Returns:
            Dict containing AI trading signals
        """
        try:
            if not self.model:
                return self._fallback_trading_signals(technical_indicators)
            
            # Prepare comprehensive analysis data
            signal_data = self._prepare_signal_data(symbol, historical_data, technical_indicators)
            
            # Create prompt for signal generation
            prompt = self._create_signal_prompt(signal_data)
            
            # Get AI response
            response = await self._get_ai_response(prompt)
            
            # Parse AI response
            signal_result = self._parse_signal_response(response)
            
            return {
                "action": signal_result.get("action", "HOLD"),
                "signal_strength": signal_result.get("signal_strength", 0.5),
                "entry_price": signal_result.get("entry_price"),
                "stop_loss": signal_result.get("stop_loss"),
                "take_profit": signal_result.get("take_profit"),
                "reasoning": signal_result.get("reasoning", "AI analysis"),
                "risk_reward_ratio": signal_result.get("risk_reward_ratio", 1.0),
                "time_horizon": signal_result.get("time_horizon", "SHORT"),
                "ai_confidence": signal_result.get("confidence", 0.5),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in AI signal generation: {e}")
            return self._fallback_trading_signals(technical_indicators)
    
    async def analyze_risk_assessment(self, symbol: str, position_data: Dict[str, Any], 
                                    market_conditions: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered risk assessment for trading decisions
        
        Args:
            symbol: Trading symbol
            position_data: Current position information
            market_conditions: Current market conditions
            
        Returns:
            Dict containing AI risk assessment
        """
        try:
            if not self.model:
                return self._fallback_risk_assessment(position_data, market_conditions)
            
            # Prepare risk analysis data
            risk_data = self._prepare_risk_data(symbol, position_data, market_conditions)
            
            # Create prompt for risk assessment
            prompt = self._create_risk_prompt(risk_data)
            
            # Get AI response
            response = await self._get_ai_response(prompt)
            
            # Parse AI response
            risk_result = self._parse_risk_response(response)
            
            return {
                "risk_level": risk_result.get("risk_level", "MEDIUM"),
                "risk_score": risk_result.get("risk_score", 0.5),
                "max_position_size": risk_result.get("max_position_size", 0.02),
                "stop_loss_adjustment": risk_result.get("stop_loss_adjustment", 0.0),
                "risk_factors": risk_result.get("risk_factors", []),
                "recommendations": risk_result.get("recommendations", []),
                "volatility_assessment": risk_result.get("volatility_assessment", "NORMAL"),
                "ai_confidence": risk_result.get("confidence", 0.5),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in AI risk assessment: {e}")
            return self._fallback_risk_assessment(position_data, market_conditions)
    
    def _prepare_market_data(self, symbol: str, market_data: Dict, technical_analysis: Dict) -> Dict:
        """Prepare market data for AI analysis"""
        return {
            "symbol": symbol,
            "current_price": market_data.get("price", 0),
            "volume_24h": market_data.get("volume", 0),
            "price_change_24h": market_data.get("price_change_24h", 0),
            "price_change_percent": market_data.get("price_change_percent", 0),
            "high_24h": market_data.get("high_24h", 0),
            "low_24h": market_data.get("low_24h", 0),
            "rsi": technical_analysis.get("rsi", {}).get("value", 50),
            "macd_signal": technical_analysis.get("macd", {}).get("signal", "NEUTRAL"),
            "ema_trend": technical_analysis.get("ema", {}).get("trend", "NEUTRAL"),
            "bollinger_position": technical_analysis.get("bollinger_bands", {}).get("position", "MIDDLE"),
            "support_resistance": technical_analysis.get("support_resistance", {}),
            "volume_analysis": technical_analysis.get("volume", {})
        }
    
    def _prepare_signal_data(self, symbol: str, historical_data: List, technical_indicators: Dict) -> Dict:
        """Prepare data for signal generation"""
        # Calculate additional metrics
        prices = [float(candle.get("close", 0)) for candle in historical_data[-20:]]
        volumes = [float(candle.get("volume", 0)) for candle in historical_data[-20:]]
        
        return {
            "symbol": symbol,
            "recent_prices": prices,
            "recent_volumes": volumes,
            "price_trend": "UP" if prices[-1] > prices[-5] else "DOWN",
            "volume_trend": "INCREASING" if volumes[-1] > sum(volumes[-5:])/5 else "DECREASING",
            "technical_indicators": technical_indicators,
            "volatility": np.std(prices) if prices else 0,
            "momentum": (prices[-1] - prices[-10]) / prices[-10] * 100 if len(prices) >= 10 and prices[-10] != 0 else 0
        }
    
    def _prepare_risk_data(self, symbol: str, position_data: Dict, market_conditions: Dict) -> Dict:
        """Prepare data for risk assessment"""
        return {
            "symbol": symbol,
            "position_size": position_data.get("size", 0),
            "entry_price": position_data.get("entry_price", 0),
            "current_price": position_data.get("current_price", 0),
            "unrealized_pnl": position_data.get("unrealized_pnl", 0),
            "leverage": position_data.get("leverage", 1),
            "market_volatility": market_conditions.get("volatility", 0),
            "market_trend": market_conditions.get("trend", "NEUTRAL"),
            "volume_profile": market_conditions.get("volume_profile", "NORMAL")
        }
    
    def _create_sentiment_prompt(self, data: Dict) -> str:
        """Create prompt for sentiment analysis"""
        return f"""
        As an expert cryptocurrency trading analyst, analyze the following market data for {data['symbol']} and provide a comprehensive sentiment analysis:

        Market Data:
        - Current Price: ${data['current_price']}
        - 24h Change: {data['price_change_percent']}%
        - 24h Volume: {data['volume_24h']}
        - 24h High/Low: ${data['high_24h']} / ${data['low_24h']}

        Technical Indicators:
        - RSI: {data['rsi']}
        - MACD Signal: {data['macd_signal']}
        - EMA Trend: {data['ema_trend']}
        - Bollinger Position: {data['bollinger_position']}

        Please provide your analysis in JSON format with the following structure:
        {{
            "sentiment": "BULLISH|BEARISH|NEUTRAL",
            "confidence": 0.0-1.0,
            "reasoning": "detailed explanation of your analysis",
            "key_factors": ["factor1", "factor2", "factor3"],
            "recommendation": "BUY|SELL|HOLD",
            "risk_level": "LOW|MEDIUM|HIGH"
        }}

        Focus on:
        1. Technical indicator convergence/divergence
        2. Volume and price action correlation
        3. Market structure and trend strength
        4. Risk factors and potential catalysts
        """
    
    def _create_signal_prompt(self, data: Dict) -> str:
        """Create prompt for signal generation"""
        return f"""
        As an expert cryptocurrency trader, analyze the following data for {data['symbol']} and generate precise trading signals:

        Market Analysis:
        - Recent Prices: {data['recent_prices'][-5:]}
        - Price Trend: {data['price_trend']}
        - Volume Trend: {data['volume_trend']}
        - Volatility: {data['volatility']:.4f}
        - Momentum: {data['momentum']:.2f}%

        Technical Indicators:
        {json.dumps(data['technical_indicators'], indent=2)}

        Please provide trading signals in JSON format:
        {{
            "action": "BUY|SELL|HOLD",
            "signal_strength": 0.0-1.0,
            "entry_price": price_value,
            "stop_loss": price_value,
            "take_profit": price_value,
            "reasoning": "detailed explanation",
            "risk_reward_ratio": ratio_value,
            "time_horizon": "SCALP|SHORT|MEDIUM|LONG",
            "confidence": 0.0-1.0
        }}

        Consider:
        1. Multiple timeframe confirmation
        2. Risk-reward optimization
        3. Market structure and momentum
        4. Entry and exit timing
        """
    
    def _create_risk_prompt(self, data: Dict) -> str:
        """Create prompt for risk assessment"""
        return f"""
        As a professional risk management analyst, assess the trading risk for {data['symbol']} based on:

        Position Data:
        - Position Size: {data['position_size']}
        - Entry Price: ${data['entry_price']}
        - Current Price: ${data['current_price']}
        - Unrealized PnL: {data['unrealized_pnl']}
        - Leverage: {data['leverage']}x

        Market Conditions:
        - Volatility: {data['market_volatility']}
        - Trend: {data['market_trend']}
        - Volume Profile: {data['volume_profile']}

        Provide risk assessment in JSON format:
        {{
            "risk_level": "LOW|MEDIUM|HIGH|EXTREME",
            "risk_score": 0.0-1.0,
            "max_position_size": percentage,
            "stop_loss_adjustment": adjustment_percentage,
            "risk_factors": ["factor1", "factor2"],
            "recommendations": ["recommendation1", "recommendation2"],
            "volatility_assessment": "LOW|NORMAL|HIGH|EXTREME",
            "confidence": 0.0-1.0
        }}

        Focus on:
        1. Position sizing optimization
        2. Stop loss placement
        3. Market volatility impact
        4. Risk mitigation strategies
        """
    
    async def _get_ai_response(self, prompt: str) -> str:
        """Get response from AI model"""
        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            return response.text
        except Exception as e:
            self.logger.error(f"Error getting AI response: {e}")
            return "{}"
    
    def _parse_sentiment_response(self, response: str) -> Dict[str, Any]:
        """Parse AI sentiment response"""
        try:
            # Try to extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
        except Exception as e:
            self.logger.error(f"Error parsing sentiment response: {e}")
        
        return {
            "sentiment": "NEUTRAL",
            "confidence": 0.5,
            "reasoning": "Unable to parse AI response",
            "key_factors": [],
            "recommendation": "HOLD",
            "risk_level": "MEDIUM"
        }
    
    def _parse_signal_response(self, response: str) -> Dict[str, Any]:
        """Parse AI signal response"""
        try:
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
        except Exception as e:
            self.logger.error(f"Error parsing signal response: {e}")
        
        return {
            "action": "HOLD",
            "signal_strength": 0.5,
            "entry_price": None,
            "stop_loss": None,
            "take_profit": None,
            "reasoning": "Unable to parse AI response",
            "risk_reward_ratio": 1.0,
            "time_horizon": "SHORT",
            "confidence": 0.5
        }
    
    def _parse_risk_response(self, response: str) -> Dict[str, Any]:
        """Parse AI risk response"""
        try:
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
        except Exception as e:
            self.logger.error(f"Error parsing risk response: {e}")
        
        return {
            "risk_level": "MEDIUM",
            "risk_score": 0.5,
            "max_position_size": 0.02,
            "stop_loss_adjustment": 0.0,
            "risk_factors": [],
            "recommendations": [],
            "volatility_assessment": "NORMAL",
            "confidence": 0.5
        }
    
    def _fallback_sentiment_analysis(self, market_data: Dict, technical_analysis: Dict) -> Dict[str, Any]:
        """Fallback sentiment analysis when AI is unavailable"""
        # Simple rule-based sentiment
        sentiment_score = 0
        
        # Price change contribution
        price_change = market_data.get("price_change_percent", 0)
        if price_change > 5:
            sentiment_score += 0.3
        elif price_change < -5:
            sentiment_score -= 0.3
        
        # RSI contribution
        rsi = technical_analysis.get("rsi", {}).get("value", 50)
        if rsi > 70:
            sentiment_score -= 0.2  # Overbought
        elif rsi < 30:
            sentiment_score += 0.2  # Oversold
        
        # Determine sentiment
        if sentiment_score > 0.2:
            sentiment = "BULLISH"
        elif sentiment_score < -0.2:
            sentiment = "BEARISH"
        else:
            sentiment = "NEUTRAL"
        
        return {
            "ai_sentiment": sentiment,
            "confidence": 0.6,
            "reasoning": "Rule-based analysis (AI unavailable)",
            "key_factors": ["Price change", "RSI levels"],
            "recommendation": "HOLD",
            "risk_level": "MEDIUM",
            "timestamp": datetime.now().isoformat()
        }
    
    def _fallback_trading_signals(self, technical_indicators: Dict) -> Dict[str, Any]:
        """Fallback trading signals when AI is unavailable"""
        return {
            "action": "HOLD",
            "signal_strength": 0.5,
            "entry_price": None,
            "stop_loss": None,
            "take_profit": None,
            "reasoning": "AI analysis unavailable, using fallback",
            "risk_reward_ratio": 1.0,
            "time_horizon": "SHORT",
            "ai_confidence": 0.5,
            "timestamp": datetime.now().isoformat()
        }
    
    def _fallback_risk_assessment(self, position_data: Dict, market_conditions: Dict) -> Dict[str, Any]:
        """Fallback risk assessment when AI is unavailable"""
        return {
            "risk_level": "MEDIUM",
            "risk_score": 0.5,
            "max_position_size": 0.02,
            "stop_loss_adjustment": 0.0,
            "risk_factors": ["AI analysis unavailable"],
            "recommendations": ["Use conservative position sizing"],
            "volatility_assessment": "NORMAL",
            "ai_confidence": 0.5,
            "timestamp": datetime.now().isoformat()
        }
    
    async def get_market_insights(self, symbol: str, timeframe: str = "1h") -> Dict[str, Any]:
        """
        Get comprehensive market insights using AI analysis
        
        Args:
            symbol: Trading symbol
            timeframe: Analysis timeframe
            
        Returns:
            Dict containing comprehensive market insights
        """
        try:
            if not self.model:
                return {"error": "AI model not available"}
            
            prompt = f"""
            Provide comprehensive market insights for {symbol} on {timeframe} timeframe.
            Include:
            1. Current market structure analysis
            2. Key support and resistance levels
            3. Potential breakout scenarios
            4. Risk factors to watch
            5. Trading opportunities
            
            Provide insights in a structured format focusing on actionable information for traders.
            """
            
            response = await self._get_ai_response(prompt)
            
            return {
                "symbol": symbol,
                "timeframe": timeframe,
                "insights": response,
                "timestamp": datetime.now().isoformat(),
                "source": "Gemini AI"
            }
            
        except Exception as e:
            self.logger.error(f"Error getting market insights: {e}")
            return {
                "error": f"Failed to get market insights: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def is_available(self) -> bool:
        """Check if AI analyzer is available and working"""
        return self.model is not None
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test AI connection and functionality"""
        try:
            if not self.model:
                return {
                    "status": "error",
                    "message": "AI model not initialized",
                    "available": False
                }
            
            test_prompt = "Respond with 'AI connection test successful' if you can understand this message."
            response = await self._get_ai_response(test_prompt)
            
            return {
                "status": "success" if "successful" in response.lower() else "warning",
                "message": response,
                "available": True,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"AI connection test failed: {str(e)}",
                "available": False,
                "timestamp": datetime.now().isoformat()
            }

"""
Binance Futures API Client
Handles all interactions with Binance Futures API
"""

import asyncio
import time
import hmac
import hashlib
import aiohttp
import json
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode
import logging

logger = logging.getLogger(__name__)

class BinanceClient:
    """Binance Futures API Client"""
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """Initialize Binance client"""
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        
        # API endpoints
        if testnet:
            self.base_url = "https://testnet.binancefuture.com"
        else:
            self.base_url = "https://fapi.binance.com"
        
        self.session = None
        self.server_time_offset = 0
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers={'X-MBX-APIKEY': self.api_key}
            )
        return self.session
    
    async def close(self):
        """Close the session"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    def _generate_signature(self, query_string: str) -> str:
        """Generate signature for signed requests"""
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def _get_timestamp(self) -> int:
        """Get current timestamp with server time offset"""
        return int(time.time() * 1000) + self.server_time_offset
    
    async def _rate_limit(self):
        """Apply rate limiting"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            await asyncio.sleep(self.min_request_interval - time_since_last_request)
        
        self.last_request_time = time.time()
    
    async def _make_request(self, method: str, endpoint: str, params: Dict = None,
                          signed: bool = False) -> Dict:
        """Make HTTP request to Binance API"""
        await self._rate_limit()
        
        url = f"{self.base_url}{endpoint}"
        params = params or {}
        
        if signed:
            params['timestamp'] = self._get_timestamp()
            query_string = urlencode(params)
            params['signature'] = self._generate_signature(query_string)
        
        session = await self._get_session()
        
        try:
            if method == 'GET':
                async with session.get(url, params=params) as response:
                    return await self._handle_response(response)
            elif method == 'POST':
                async with session.post(url, params=params) as response:
                    return await self._handle_response(response)
            elif method == 'DELETE':
                async with session.delete(url, params=params) as response:
                    return await self._handle_response(response)
        
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise
    
    async def _handle_response(self, response: aiohttp.ClientResponse) -> Dict:
        """Handle API response"""
        text = await response.text()
        
        if response.status == 200:
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON response: {text}")
                raise ValueError("Invalid JSON response")
        else:
            error_data = {}
            try:
                error_data = json.loads(text)
            except:
                pass
            
            error_msg = error_data.get('msg', f"HTTP {response.status}")
            logger.error(f"API Error: {error_msg}")
            raise Exception(f"Binance API Error: {error_msg}")
    
    async def test_connection(self) -> Dict:
        """Test API connection"""
        try:
            # Test connectivity
            await self._make_request('GET', '/fapi/v1/ping')
            
            # Get server time and calculate offset
            server_time_data = await self._make_request('GET', '/fapi/v1/time')
            server_time = server_time_data['serverTime']
            local_time = int(time.time() * 1000)
            self.server_time_offset = server_time - local_time
            
            # Test authenticated endpoint
            await self.get_account_info()
            
            logger.info("✅ Binance API connection successful")
            return {"status": "success", "server_time_offset": self.server_time_offset}
            
        except Exception as e:
            logger.error(f"❌ Binance API connection failed: {e}")
            raise
    
    # Market Data Endpoints
    
    async def get_exchange_info(self) -> Dict:
        """Get exchange trading rules and symbol information"""
        return await self._make_request('GET', '/fapi/v1/exchangeInfo')
    
    async def get_ticker_price(self, symbol: str) -> Dict:
        """Get symbol price ticker"""
        params = {'symbol': symbol}
        return await self._make_request('GET', '/fapi/v1/ticker/price', params)
    
    async def get_klines(self, symbol: str, interval: str, limit: int = 500,
                        start_time: Optional[int] = None,
                        end_time: Optional[int] = None) -> List[List]:
        """Get kline/candlestick data"""
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        
        if start_time:
            params['startTime'] = start_time
        if end_time:
            params['endTime'] = end_time
        
        return await self._make_request('GET', '/fapi/v1/klines', params)
    
    async def get_orderbook(self, symbol: str, limit: int = 100) -> Dict:
        """Get order book depth"""
        params = {'symbol': symbol, 'limit': limit}
        return await self._make_request('GET', '/fapi/v1/depth', params)
    
    async def get_24hr_ticker(self, symbol: str) -> Dict:
        """Get 24hr ticker price change statistics"""
        params = {'symbol': symbol}
        return await self._make_request('GET', '/fapi/v1/ticker/24hr', params)
    
    # Account Endpoints
    
    async def get_account_info(self) -> Dict:
        """Get account information"""
        return await self._make_request('GET', '/fapi/v2/account', signed=True)
    
    async def get_balance(self) -> List[Dict]:
        """Get account balance"""
        account_info = await self.get_account_info()
        return account_info.get('assets', [])
    
    async def get_positions(self) -> List[Dict]:
        """Get position information"""
        return await self._make_request('GET', '/fapi/v2/positionRisk', signed=True)
    
    async def get_position(self, symbol: str) -> Optional[Dict]:
        """Get position for specific symbol"""
        positions = await self.get_positions()
        for position in positions:
            if position['symbol'] == symbol:
                return position
        return None
    
    # Trading Endpoints
    
    async def place_order(self, symbol: str, side: str, order_type: str,
                         quantity: float, price: Optional[float] = None,
                         stop_price: Optional[float] = None,
                         time_in_force: str = 'GTC',
                         reduce_only: bool = False) -> Dict:
        """Place a new order"""
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
            'timeInForce': time_in_force
        }
        
        if price:
            params['price'] = price
        
        if stop_price:
            params['stopPrice'] = stop_price
        
        if reduce_only:
            params['reduceOnly'] = 'true'
        
        return await self._make_request('POST', '/fapi/v1/order', params, signed=True)
    
    async def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """Cancel an active order"""
        params = {'symbol': symbol, 'orderId': order_id}
        return await self._make_request('DELETE', '/fapi/v1/order', params, signed=True)
    
    async def cancel_all_orders(self, symbol: str) -> Dict:
        """Cancel all open orders for a symbol"""
        params = {'symbol': symbol}
        return await self._make_request('DELETE', '/fapi/v1/allOpenOrders', 
                                      params, signed=True)
    
    async def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get all open orders"""
        params = {}
        if symbol:
            params['symbol'] = symbol
        return await self._make_request('GET', '/fapi/v1/openOrders', params, signed=True)
    
    async def get_order_history(self, symbol: str, limit: int = 500) -> List[Dict]:
        """Get order history"""
        params = {'symbol': symbol, 'limit': limit}
        return await self._make_request('GET', '/fapi/v1/allOrders', params, signed=True)
    
    # Position Management
    
    async def change_leverage(self, symbol: str, leverage: int) -> Dict:
        """Change leverage for a symbol"""
        params = {'symbol': symbol, 'leverage': leverage}
        return await self._make_request('POST', '/fapi/v1/leverage', params, signed=True)
    
    async def change_margin_type(self, symbol: str, margin_type: str) -> Dict:
        """Change margin type (ISOLATED or CROSSED)"""
        params = {'symbol': symbol, 'marginType': margin_type}
        return await self._make_request('POST', '/fapi/v1/marginType', params, signed=True)
    
    # Convenience Methods
    
    async def market_buy(self, symbol: str, quantity: float) -> Dict:
        """Place market buy order"""
        return await self.place_order(symbol, 'BUY', 'MARKET', quantity)
    
    async def market_sell(self, symbol: str, quantity: float) -> Dict:
        """Place market sell order"""
        return await self.place_order(symbol, 'SELL', 'MARKET', quantity)
    
    async def limit_buy(self, symbol: str, quantity: float, price: float) -> Dict:
        """Place limit buy order"""
        return await self.place_order(symbol, 'BUY', 'LIMIT', quantity, price)
    
    async def limit_sell(self, symbol: str, quantity: float, price: float) -> Dict:
        """Place limit sell order"""
        return await self.place_order(symbol, 'SELL', 'LIMIT', quantity, price)
    
    async def stop_loss_order(self, symbol: str, side: str, quantity: float,
                            stop_price: float) -> Dict:
        """Place stop loss order"""
        return await self.place_order(symbol, side, 'STOP_MARKET', quantity,
                                    stop_price=stop_price, reduce_only=True)

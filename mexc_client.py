import hashlib
import hmac
import time
import requests
from typing import Dict, Optional, List


class MEXCClient:
    """MEXC Exchange API Client"""
    
    def __init__(self, api_key: str, secret_key: str, base_url: str = "https://api.mexc.com"):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
        
    def _generate_signature(self, params: Dict) -> str:
        """Generate signature for authenticated requests"""
        query_string = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _send_request(self, method: str, endpoint: str, params: Optional[Dict] = None, signed: bool = False) -> Dict:
        """Send HTTP request to MEXC API"""
        url = f"{self.base_url}{endpoint}"
        
        if params is None:
            params = {}
        
        headers = {
            "X-MEXC-APIKEY": self.api_key,
            "Content-Type": "application/json"
        }
        
        if signed:
            params["timestamp"] = int(time.time() * 1000)
            params["signature"] = self._generate_signature(params)
        
        try:
            if method == "GET":
                response = requests.get(url, params=params, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, params=params, headers=headers, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, params=params, headers=headers, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            return {"error": str(e)}
    
    def get_ticker_price(self, symbol: str) -> Dict:
        """Get current ticker price for a symbol"""
        endpoint = "/api/v3/ticker/price"
        params = {"symbol": symbol}
        return self._send_request("GET", endpoint, params)
    
    def get_account_info(self) -> Dict:
        """Get account information"""
        endpoint = "/api/v3/account"
        return self._send_request("GET", endpoint, signed=True)
    
    def get_open_orders(self, symbol: str) -> List[Dict]:
        """Get all open orders for a symbol"""
        endpoint = "/api/v3/openOrders"
        params = {"symbol": symbol}
        result = self._send_request("GET", endpoint, params, signed=True)
        return result if isinstance(result, list) else []
    
    def create_order(self, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None) -> Dict:
        """Create a new order
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            order_type: 'LIMIT' or 'MARKET'
            quantity: Order quantity
            price: Order price (required for LIMIT orders)
        """
        endpoint = "/api/v3/order"
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity
        }
        
        if order_type == "LIMIT":
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            params["price"] = price
            params["timeInForce"] = "GTC"
        
        return self._send_request("POST", endpoint, params, signed=True)
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """Cancel an open order"""
        endpoint = "/api/v3/order"
        params = {
            "symbol": symbol,
            "orderId": order_id
        }
        return self._send_request("DELETE", endpoint, params, signed=True)
    
    def get_klines(self, symbol: str, interval: str = "1m", limit: int = 100) -> List:
        """Get kline/candlestick data
        
        Args:
            symbol: Trading pair symbol
            interval: Kline interval (1m, 5m, 15m, 30m, 1h, 4h, 1d, etc.)
            limit: Number of klines to retrieve (max 1000)
        """
        endpoint = "/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        result = self._send_request("GET", endpoint, params)
        return result if isinstance(result, list) else []

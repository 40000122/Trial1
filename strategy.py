from typing import List, Dict, Optional


class TradingStrategy:
    """Base class for trading strategies"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.position = None  # None, 'LONG', or 'SHORT'
        self.entry_price = 0.0
        
    def analyze(self, klines: List) -> str:
        """Analyze market data and return signal
        
        Args:
            klines: List of kline data
            
        Returns:
            'BUY', 'SELL', or 'HOLD'
        """
        raise NotImplementedError("Subclasses must implement analyze method")


class SimpleMAStrategy(TradingStrategy):
    """Simple Moving Average Crossover Strategy"""
    
    def __init__(self, symbol: str, short_period: int = 10, long_period: int = 20):
        super().__init__(symbol)
        self.short_period = short_period
        self.long_period = long_period
        
    def calculate_ma(self, klines: List, period: int) -> Optional[float]:
        """Calculate simple moving average"""
        if len(klines) < period:
            return None
        
        # MEXC klines format: [timestamp, open, high, low, close, volume, ...]
        closes = [float(k[4]) for k in klines[-period:]]
        return sum(closes) / period
    
    def analyze(self, klines: List) -> str:
        """Analyze using MA crossover strategy"""
        if len(klines) < self.long_period:
            return 'HOLD'
        
        short_ma = self.calculate_ma(klines, self.short_period)
        long_ma = self.calculate_ma(klines, self.long_period)
        
        # Calculate previous MAs for crossover detection
        prev_short_ma = self.calculate_ma(klines[:-1], self.short_period)
        prev_long_ma = self.calculate_ma(klines[:-1], self.long_period)
        
        if short_ma is None or long_ma is None or prev_short_ma is None or prev_long_ma is None:
            return 'HOLD'
        
        # Bullish crossover: short MA crosses above long MA
        if prev_short_ma <= prev_long_ma and short_ma > long_ma:
            if self.position != 'LONG':
                return 'BUY'
        
        # Bearish crossover: short MA crosses below long MA
        elif prev_short_ma >= prev_long_ma and short_ma < long_ma:
            if self.position == 'LONG':
                return 'SELL'
        
        return 'HOLD'


class RSIStrategy(TradingStrategy):
    """Relative Strength Index (RSI) Strategy"""
    
    def __init__(self, symbol: str, period: int = 14, oversold: int = 30, overbought: int = 70):
        super().__init__(symbol)
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
    
    def calculate_rsi(self, klines: List) -> Optional[float]:
        """Calculate RSI indicator"""
        if len(klines) < self.period + 1:
            return None
        
        closes = [float(k[4]) for k in klines[-(self.period + 1):]]
        
        gains = []
        losses = []
        
        for i in range(1, len(closes)):
            change = closes[i] - closes[i - 1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains) / self.period
        avg_loss = sum(losses) / self.period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def analyze(self, klines: List) -> str:
        """Analyze using RSI strategy"""
        rsi = self.calculate_rsi(klines)
        
        if rsi is None:
            return 'HOLD'
        
        # Buy when RSI is oversold
        if rsi < self.oversold and self.position != 'LONG':
            return 'BUY'
        
        # Sell when RSI is overbought
        elif rsi > self.overbought and self.position == 'LONG':
            return 'SELL'
        
        return 'HOLD'

import os
import time
import logging
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

from mexc_client import MEXCClient
from strategy import SimpleMAStrategy, RSIStrategy


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TradingBot:
    """Automated Trading Bot for MEXC Exchange"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # API Configuration
        api_key = os.getenv('MEXC_API_KEY')
        secret_key = os.getenv('MEXC_SECRET_KEY')
        
        if not api_key or not secret_key:
            raise ValueError("API keys not found. Please set MEXC_API_KEY and MEXC_SECRET_KEY in .env file")
        
        self.client = MEXCClient(api_key, secret_key)
        
        # Trading Configuration
        self.symbol = os.getenv('TRADING_SYMBOL', 'BTCUSDT')
        self.trade_amount = float(os.getenv('TRADE_AMOUNT', '10'))
        self.check_interval = int(os.getenv('CHECK_INTERVAL', '60'))
        
        # Risk Management
        self.max_position_size = float(os.getenv('MAX_POSITION_SIZE', '1000'))
        self.stop_loss_pct = float(os.getenv('STOP_LOSS_PERCENTAGE', '2.0'))
        self.take_profit_pct = float(os.getenv('TAKE_PROFIT_PERCENTAGE', '3.0'))
        
        # Strategy Selection (can be configured via environment)
        strategy_type = os.getenv('STRATEGY', 'MA')
        if strategy_type == 'MA':
            self.strategy = SimpleMAStrategy(self.symbol)
        elif strategy_type == 'RSI':
            self.strategy = RSIStrategy(self.symbol)
        else:
            self.strategy = SimpleMAStrategy(self.symbol)
        
        self.running = False
        self.current_position = None
        
        logger.info(f"Trading Bot initialized for {self.symbol}")
        logger.info(f"Strategy: {strategy_type}")
    
    def get_current_price(self) -> Optional[float]:
        """Get current market price"""
        try:
            ticker = self.client.get_ticker_price(self.symbol)
            if 'price' in ticker:
                return float(ticker['price'])
            logger.error(f"Error getting price: {ticker}")
            return None
        except Exception as e:
            logger.error(f"Error getting current price: {e}")
            return None
    
    def check_risk_management(self, current_price: float) -> bool:
        """Check if stop loss or take profit should be triggered"""
        if not self.strategy.position or not self.strategy.entry_price:
            return False
        
        price_change_pct = ((current_price - self.strategy.entry_price) / self.strategy.entry_price) * 100
        
        # Check stop loss
        if price_change_pct <= -self.stop_loss_pct:
            logger.warning(f"Stop loss triggered! Loss: {price_change_pct:.2f}%")
            return True
        
        # Check take profit
        if price_change_pct >= self.take_profit_pct:
            logger.info(f"Take profit triggered! Profit: {price_change_pct:.2f}%")
            return True
        
        return False
    
    def execute_buy(self, price: float) -> bool:
        """Execute buy order"""
        try:
            # Calculate quantity based on trade amount
            quantity = self.trade_amount / price
            
            # Round quantity to appropriate precision (this may need adjustment based on symbol)
            quantity = round(quantity, 6)
            
            logger.info(f"Executing BUY order: {quantity} {self.symbol} at {price}")
            
            # Create market order
            order = self.client.create_order(
                symbol=self.symbol,
                side='BUY',
                order_type='MARKET',
                quantity=quantity
            )
            
            if 'orderId' in order:
                logger.info(f"Buy order executed successfully. Order ID: {order['orderId']}")
                self.strategy.position = 'LONG'
                self.strategy.entry_price = price
                return True
            else:
                logger.error(f"Buy order failed: {order}")
                return False
                
        except Exception as e:
            logger.error(f"Error executing buy order: {e}")
            return False
    
    def execute_sell(self, price: float) -> bool:
        """Execute sell order"""
        try:
            # Get current position size (simplified - in production, track this properly)
            quantity = self.trade_amount / self.strategy.entry_price
            quantity = round(quantity, 6)
            
            logger.info(f"Executing SELL order: {quantity} {self.symbol} at {price}")
            
            # Create market order
            order = self.client.create_order(
                symbol=self.symbol,
                side='SELL',
                order_type='MARKET',
                quantity=quantity
            )
            
            if 'orderId' in order:
                profit_loss = ((price - self.strategy.entry_price) / self.strategy.entry_price) * 100
                logger.info(f"Sell order executed successfully. Order ID: {order['orderId']}")
                logger.info(f"Position closed with P&L: {profit_loss:.2f}%")
                self.strategy.position = None
                self.strategy.entry_price = 0.0
                return True
            else:
                logger.error(f"Sell order failed: {order}")
                return False
                
        except Exception as e:
            logger.error(f"Error executing sell order: {e}")
            return False
    
    def run_trading_cycle(self):
        """Run one trading cycle"""
        try:
            # Get current price
            current_price = self.get_current_price()
            if current_price is None:
                logger.warning("Could not get current price, skipping cycle")
                return
            
            logger.info(f"Current price: {current_price}")
            
            # Check risk management first
            if self.check_risk_management(current_price):
                self.execute_sell(current_price)
                return
            
            # Get market data for analysis
            klines = self.client.get_klines(self.symbol, interval='5m', limit=100)
            
            if not klines:
                logger.warning("Could not get klines data, skipping cycle")
                return
            
            # Analyze market and get signal
            signal = self.strategy.analyze(klines)
            logger.info(f"Strategy signal: {signal}")
            
            # Execute trades based on signal
            if signal == 'BUY':
                self.execute_buy(current_price)
            elif signal == 'SELL':
                self.execute_sell(current_price)
            
        except Exception as e:
            logger.error(f"Error in trading cycle: {e}")
    
    def start(self):
        """Start the trading bot"""
        self.running = True
        logger.info("Trading Bot started")
        logger.info(f"Checking market every {self.check_interval} seconds")
        
        try:
            while self.running:
                self.run_trading_cycle()
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            logger.info("Trading Bot stopped by user")
            self.running = False
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            self.running = False
    
    def stop(self):
        """Stop the trading bot"""
        self.running = False
        logger.info("Trading Bot stopped")


def main():
    """Main entry point"""
    try:
        bot = TradingBot()
        bot.start()
    except Exception as e:
        logger.error(f"Failed to start trading bot: {e}")


if __name__ == "__main__":
    main()

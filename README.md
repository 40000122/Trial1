# MEXC Auto Trading Bot

An automated cryptocurrency trading bot for the MEXC exchange with API integration. This bot supports multiple trading strategies, risk management, and continuous market monitoring.

## Features

- **MEXC API Integration**: Full integration with MEXC exchange API
- **Multiple Trading Strategies**:
  - Simple Moving Average (SMA) Crossover
  - Relative Strength Index (RSI)
- **Risk Management**:
  - Stop Loss protection
  - Take Profit targets
  - Maximum position size limits
- **Real-time Monitoring**: Continuous market analysis and automated trading
- **Logging**: Comprehensive logging of all trading activities
- **Configurable**: Easy configuration via environment variables

## Prerequisites

- Python 3.7 or higher
- MEXC exchange account
- API Key and Secret Key from MEXC

## Installation

1. Clone the repository:
```bash
git clone https://github.com/40000122/Trial1.git
cd Trial1
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your environment:
```bash
cp .env.example .env
```

4. Edit `.env` file with your MEXC API credentials and trading preferences:
```
MEXC_API_KEY=your_api_key_here
MEXC_SECRET_KEY=your_secret_key_here
TRADING_SYMBOL=BTCUSDT
TRADE_AMOUNT=10
CHECK_INTERVAL=60
STRATEGY=MA
```

## Configuration

### Environment Variables

- `MEXC_API_KEY`: Your MEXC API key (required)
- `MEXC_SECRET_KEY`: Your MEXC secret key (required)
- `TRADING_SYMBOL`: Trading pair symbol (default: BTCUSDT)
- `TRADE_AMOUNT`: Amount in USDT to trade per order (default: 10)
- `CHECK_INTERVAL`: Interval in seconds between market checks (default: 60)
- `STRATEGY`: Trading strategy to use - 'MA' or 'RSI' (default: MA)
- `MAX_POSITION_SIZE`: Maximum position size in USDT (default: 1000)
- `STOP_LOSS_PERCENTAGE`: Stop loss percentage (default: 2.0)
- `TAKE_PROFIT_PERCENTAGE`: Take profit percentage (default: 3.0)

### Trading Strategies

#### 1. Simple Moving Average (MA) Crossover
Set `STRATEGY=MA` in your `.env` file.

This strategy uses two moving averages (short and long period):
- **Buy Signal**: When the short-term MA crosses above the long-term MA
- **Sell Signal**: When the short-term MA crosses below the long-term MA

#### 2. Relative Strength Index (RSI)
Set `STRATEGY=RSI` in your `.env` file.

This strategy uses the RSI indicator:
- **Buy Signal**: When RSI falls below the oversold threshold (default: 30)
- **Sell Signal**: When RSI rises above the overbought threshold (default: 70)

## Usage

### Running the Bot

```bash
python trading_bot.py
```

The bot will:
1. Connect to MEXC exchange
2. Monitor the specified trading pair
3. Analyze market data using the selected strategy
4. Execute trades based on signals
5. Manage risk with stop loss and take profit
6. Log all activities to `trading_bot.log`

### Stopping the Bot

Press `Ctrl+C` to gracefully stop the bot.

## Project Structure

```
Trial1/
├── trading_bot.py      # Main trading bot application
├── mexc_client.py      # MEXC API client
├── strategy.py         # Trading strategy implementations
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment configuration
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## API Client (mexc_client.py)

The `MEXCClient` class provides methods to interact with MEXC API:

- `get_ticker_price(symbol)`: Get current price for a symbol
- `get_account_info()`: Get account balance and information
- `get_open_orders(symbol)`: Get open orders for a symbol
- `create_order()`: Create a new order (market or limit)
- `cancel_order()`: Cancel an existing order
- `get_klines()`: Get historical candlestick data

## Safety and Risk Management

⚠️ **Important Safety Notes:**

1. **Test First**: Always test with small amounts first
2. **API Permissions**: Only grant necessary permissions to your API keys
3. **Monitor Regularly**: Keep an eye on bot activity, especially in the beginning
4. **Risk Limits**: Set appropriate stop loss and position size limits
5. **Market Conditions**: Bot performance varies with market conditions
6. **No Guarantees**: Trading involves risk - there are no guaranteed profits

## Logging

All trading activities are logged to:
- Console output (real-time)
- `trading_bot.log` file (persistent)

Log includes:
- Price updates
- Strategy signals
- Order executions
- Profit/Loss calculations
- Errors and warnings

## Customization

### Adding New Strategies

1. Create a new class in `strategy.py` that inherits from `TradingStrategy`
2. Implement the `analyze()` method
3. Update `trading_bot.py` to support the new strategy

Example:
```python
class MyCustomStrategy(TradingStrategy):
    def analyze(self, klines: List) -> str:
        # Your strategy logic here
        return 'BUY' or 'SELL' or 'HOLD'
```

## Troubleshooting

### Common Issues

1. **API Authentication Error**
   - Verify your API key and secret are correct
   - Ensure API key has trading permissions enabled

2. **Order Execution Failed**
   - Check if you have sufficient balance
   - Verify the trading pair is correct
   - Check minimum order size requirements

3. **Connection Timeout**
   - Check your internet connection
   - MEXC API might be experiencing issues

## Disclaimer

This bot is provided for educational purposes. Trading cryptocurrencies carries significant risk. Use at your own risk. The authors are not responsible for any financial losses incurred while using this software.

## License

MIT License - Feel free to modify and distribute

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Support

For issues and questions, please open an issue on GitHub.

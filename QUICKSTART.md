# Quick Start Guide

## Getting Started with MEXC Auto Trading Bot

### Step 1: Get MEXC API Credentials

1. Log in to your MEXC account
2. Go to API Management section
3. Create a new API key with **Spot Trading** permissions
4. Save your API Key and Secret Key securely

### Step 2: Set Up the Bot

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your credentials:
   ```bash
   nano .env  # or use any text editor
   ```

3. Update these required fields:
   ```
   MEXC_API_KEY=your_actual_api_key
   MEXC_SECRET_KEY=your_actual_secret_key
   ```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Test Your Connection

Before running the bot, test your API connection:

```bash
python3 test_connection.py
```

You should see:
- ✓ API keys found
- ✓ MEXC Client initialized
- ✓ Current price information
- ✓ Successfully authenticated

### Step 5: Configure Trading Parameters

Edit `.env` to customize your trading:

```bash
# Start with small amounts for testing!
TRADING_SYMBOL=BTCUSDT
TRADE_AMOUNT=10          # Start small, e.g., $10
CHECK_INTERVAL=60        # Check market every 60 seconds
STRATEGY=MA              # Use Moving Average strategy

# Risk Management
STOP_LOSS_PERCENTAGE=2.0     # Exit if loss reaches 2%
TAKE_PROFIT_PERCENTAGE=3.0   # Exit if profit reaches 3%
MAX_POSITION_SIZE=100        # Maximum $100 position
```

### Step 6: Run the Bot

```bash
python3 trading_bot.py
```

The bot will:
1. Start monitoring the market
2. Analyze price movements
3. Execute trades based on your strategy
4. Log all activities to console and `trading_bot.log`

### Step 7: Monitor the Bot

- Watch the console output for real-time updates
- Check `trading_bot.log` for detailed logs
- Monitor your MEXC account for executed trades

### Stopping the Bot

Press `Ctrl+C` to stop the bot gracefully.

## Important Tips

### For Beginners

1. **Start Small**: Use small trade amounts ($10-20) when starting
2. **Test First**: Run for a few hours to see how it behaves
3. **Monitor Closely**: Watch the bot's actions carefully at first
4. **Understand Risks**: No bot guarantees profits

### Safety Checklist

- [ ] API key has only Spot Trading permissions (no withdrawal)
- [ ] Started with small trade amounts
- [ ] Set reasonable stop loss (2-5%)
- [ ] Limited max position size
- [ ] Read and understood the README
- [ ] Tested connection successfully

### Common First-Time Issues

**"API keys not found"**
- Make sure you copied `.env.example` to `.env`
- Check that API keys are set without quotes

**"Authentication failed"**
- Verify your API key and secret are correct
- Ensure API key has trading permissions
- Check if API key is active on MEXC

**"Insufficient balance"**
- Make sure you have enough USDT in your spot wallet
- Reduce TRADE_AMOUNT in .env

### Recommended Settings for Testing

```bash
TRADING_SYMBOL=BTCUSDT
TRADE_AMOUNT=10
CHECK_INTERVAL=300      # 5 minutes - less frequent checks
STRATEGY=MA
STOP_LOSS_PERCENTAGE=1.5
TAKE_PROFIT_PERCENTAGE=2.0
MAX_POSITION_SIZE=50
```

## Next Steps

1. Monitor bot performance for at least a few days
2. Review trades in `trading_bot.log`
3. Adjust parameters based on results
4. Consider testing different strategies (MA vs RSI)
5. Gradually increase trade amounts as you gain confidence

## Need Help?

- Check `trading_bot.log` for error messages
- Review the full README.md for detailed documentation
- Open an issue on GitHub for support

## Remember

⚠️ **Trading involves risk. Never invest more than you can afford to lose.**

The bot is a tool - it doesn't guarantee profits. Market conditions change, and past performance doesn't predict future results. Always monitor your bot and be prepared to stop it if needed.

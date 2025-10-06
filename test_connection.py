#!/usr/bin/env python3
"""
Test script to verify MEXC API connection and configuration
"""

import os
from dotenv import load_dotenv
from mexc_client import MEXCClient


def test_connection():
    """Test MEXC API connection and credentials"""
    
    print("=" * 60)
    print("MEXC Trading Bot - Connection Test")
    print("=" * 60)
    print()
    
    # Load environment variables
    load_dotenv()
    
    # Check if API keys are set
    api_key = os.getenv('MEXC_API_KEY')
    secret_key = os.getenv('MEXC_SECRET_KEY')
    
    if not api_key or not secret_key:
        print("❌ ERROR: API keys not found!")
        print("Please set MEXC_API_KEY and MEXC_SECRET_KEY in .env file")
        return False
    
    if api_key == 'your_api_key_here' or secret_key == 'your_secret_key_here':
        print("❌ ERROR: Please replace placeholder API keys with actual keys")
        return False
    
    print("✓ API keys found")
    print()
    
    # Initialize client
    try:
        client = MEXCClient(api_key, secret_key)
        print("✓ MEXC Client initialized")
        print()
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return False
    
    # Test public endpoint (get ticker price)
    symbol = os.getenv('TRADING_SYMBOL', 'BTCUSDT')
    print(f"Testing public API endpoint (get ticker for {symbol})...")
    try:
        ticker = client.get_ticker_price(symbol)
        if 'price' in ticker:
            print(f"✓ Current {symbol} price: {ticker['price']}")
        else:
            print(f"⚠ Warning: Unexpected response: {ticker}")
    except Exception as e:
        print(f"❌ Failed to get ticker price: {e}")
    
    print()
    
    # Test authenticated endpoint (get account info)
    print("Testing authenticated API endpoint (get account info)...")
    try:
        account = client.get_account_info()
        if 'balances' in account:
            print("✓ Successfully authenticated with MEXC API")
            print(f"✓ Account has {len(account['balances'])} balances")
            
            # Show some non-zero balances
            non_zero = [b for b in account['balances'] if float(b.get('free', 0)) > 0]
            if non_zero:
                print(f"✓ Found {len(non_zero)} assets with balance")
                for bal in non_zero[:5]:  # Show first 5
                    asset = bal.get('asset', 'Unknown')
                    free = bal.get('free', '0')
                    print(f"  - {asset}: {free}")
        elif 'error' in account:
            print(f"❌ Authentication failed: {account['error']}")
            print("Please check your API keys and permissions")
        else:
            print(f"⚠ Warning: Unexpected response: {account}")
    except Exception as e:
        print(f"❌ Failed to get account info: {e}")
    
    print()
    
    # Display configuration
    print("=" * 60)
    print("Current Configuration:")
    print("=" * 60)
    print(f"Trading Symbol: {os.getenv('TRADING_SYMBOL', 'BTCUSDT')}")
    print(f"Trade Amount: ${os.getenv('TRADE_AMOUNT', '10')}")
    print(f"Check Interval: {os.getenv('CHECK_INTERVAL', '60')} seconds")
    print(f"Strategy: {os.getenv('STRATEGY', 'MA')}")
    print(f"Stop Loss: {os.getenv('STOP_LOSS_PERCENTAGE', '2.0')}%")
    print(f"Take Profit: {os.getenv('TAKE_PROFIT_PERCENTAGE', '3.0')}%")
    print(f"Max Position Size: ${os.getenv('MAX_POSITION_SIZE', '1000')}")
    print()
    
    print("=" * 60)
    print("Connection test completed!")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    test_connection()

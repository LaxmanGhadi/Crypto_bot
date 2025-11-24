
import os
from dotenv import load_dotenv
from dotenv import load_dotenv
env = load_dotenv(dotenv_path=r"C:\Users\Com\OneDrive\Documents\GitHub\Crypto_bot\.env")



load_dotenv()
class Configs:
    EXCHANGE  = "binance"
    SYMBOL = "BTC/USDT"
    TIMEFRAME = "1h"
    # FEAR_API =  "3f9744d167msh30e7ae02893acbcp17b3c2jsn2232770bcfe8",
    # Dominance_API =  '3ba2ac07-2928-4613-9357-97957983e1ac'
    API_KEY = os.getenv('BINANCE_API_KEY')
    SECRET_KEY =os.getenv('BINANCE_SECRET_KEY')
    SANDBOX = True

    INIT_BALANCE = 10000
    RISK_PER_TRADE = 0.01
    STOP_LOSS_PCT  = 0.02
    TAKE_PROFIT_PCT  = 0.04
    # Strategy Parameters
    RSI_PERIOD = 14
    RSI_OVERSOLD = 30
    RSI_OVERBOUGHT = 70
    EMA_SHORT = 20
    EMA_LONG = 50
    RISK_PER_TRADE = 0.01
    # Execution Settings
    MIN_TRADES_FOR_METRICS = 50
    UPDATE_INTERVAL = 60  # seconds
    

    # For model training
    MIN_DATA_POINTS = 300
    LOOKBACK_DAYS = 7
    # RETRAIN_HOURS = 6

    # Logging
    LOG_FILE = 'trades.csv'
    DB_FILE = 'trading_bot.db'


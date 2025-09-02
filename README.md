# AI Crypto Trading Bot

A real-time cryptocurrency trading bot that uses machine learning models to generate buy/sell signals on live market data. The bot made using AI strategies and includes comprehensive risk management, logging, and visualization features.

## Features

- **Live Market Data**: Real-time OHLCV data from major exchange - Binance
- **AI/ML Strategies**: Implemented approaches Random Forest
- **Risk Management**:  stop-loss, take-profit, and position sizing
- **Paper Trading**: Safe testing environment with sandbox mode
- **Real-time Dashboard**: Live charts with trade markers and performance metrics
- **Comprehensive Logging**: CSV and SQLite database trade records
- **Performance Analytics**: Win rate, Sharpe ratio, drawdown calculations

## Project Structure

```
crypto_bot/
├── main.py                 # Main bot execution
├── config.py              # Configuration settings
├── GetData.py             # Data fetching and management
├── FeatureExtract.py      # Feature engineering for ML
├── strategy_*.py          # AI/ML strategy implementations
├── Manage_orders.py       # Trade execution engine
├── Logger.py              # Trade logging and metrics
├── Visualizer.py          # Dashboard and charts
├── Test.ipynb/            # Trained and tried ML models
├── trades.csv             # Generated reports
└── requirements.txt       # Dependencies
```

## Installation

### Prerequisites
- Python 3.8+
- Stable internet connection
- Exchange API keys (start with testnet)

### Setup

1. **Clone and install dependencies:**
```bash
git clone <repository-url>
cd crypto_trading_bot
pip install -r requirements.txt
```

2. **Install TA-Lib (Technical Analysis Library):**
```bash
# Windows
pip install talib-binary

# macOS
brew install ta-lib
pip install TA-Lib

# Linux
sudo apt-get install libta-lib-dev
pip install TA-Lib
```

3. **Configure API credentials:**
```python
# In config.py, add your exchange API keys:
API_KEY = 'your_api_key_here'
API_SECRET = 'your_api_secret_here'
SANDBOX = True  # Start with testnet
```

## Quick Start

### 1. Test Connection
```python
from ai_data_manager import AIDataManager
data_manager = AIDataManager()
df = data_manager.get_training_data()
print(f"Data fetched: {len(df)} candles")
```

### 2. Run Bot LIVE (Paper Trading)
```python
Run main.py
```

### 3. View Dashboard
Open browser to: `http://127.0.0.1:8050`

## AI/ML Strategies

### Random Forest (Recommended for beginners)
- **Training Time**: 2-4 minutes
- **Features**: 11 technical indicators
- **Expected Win Rate**: 60-70%
- **Pros**: Fast, interpretable, robust



## Configuration

### Key Settings (config.py)
```python
# Trading Parameters
INITIAL_BALANCE = 10000     # Starting capital (USDT)
RISK_PER_TRADE = 0.01      # 1% risk per trade
STOP_LOSS_PCT = 0.02       # 2% stop loss
TAKE_PROFIT_PCT = 0.04     # 4% take profit

# AI Strategy Selection
STRATEGY_TYPE = 'random_forest'  # Choose: random_forest, xgboost, lstm

# Model Settings
RETRAIN_HOURS = 6          # Retrain every 6 hours
CONFIDENCE_THRESHOLD = 0.6  # Minimum prediction confidence
```

## Feature Engineering

The bot creates 11 key features for ML models:

1. **Price Movement**: `price_change`, `price_change_5`
2. **Position Indicators**: `price_position`, `pos_range_prc`
3. **Technical Indicators**: `rsi`, `rsi_oversold`, `rsi_overbought`
4. **Trend Analysis**: `price_above_sma10`, `price_above_sma20`, `sma_trend`
5. **Volume/Volatility**: `volume_high`, `high_volatility`

### Target Variable
```python
# Y variable for supervised learning
df['future_return'] = df['price_change'].shift(-1)
df['target'] = np.where(df['future_return'] > 0.002, 1,      # BUY
               np.where(df['future_return'] < -0.002, -1,     # SELL
                        0))                                   # HOLD
```

## Risk Management

### Position Sizing
```python
risk_amount = balance * RISK_PER_TRADE  # 1% of balance
position_size = risk_amount / (price * STOP_LOSS_PCT)  # Size based on stop loss
```

### Stop Loss & Take Profit
- **Stop Loss**: 2% below entry (buy) / above entry (sell)
- **Take Profit**: 4% above entry (buy) / below entry (sell)
- **Risk-Reward Ratio**: 1:2

## Model Persistence

Models are automatically saved and loaded:
```
models/
├── random_forest_model.joblib    # Trained Random Forest
```

**Benefits:**
- Instant startup (no retraining needed)
- Preserves learned patterns
- Smart retraining only when needed

## Performance Metrics

### Target Metrics
- **Win Rate**: ≥60% (minimum 50 trades)
- **Risk-Reward**: 1:2 ratio
- **Maximum Drawdown**: <10% of initial balance
- **Sharpe Ratio**: >1.0

### Calculated Metrics
```python
metrics = {
    'total_trades': int,
    'win_rate': float,      # Percentage of profitable trades
    'total_pnl': float,     # Total profit/loss
    'sharpe_ratio': float,  # Risk-adjusted returns
    'max_drawdown': float   # Worst peak-to-trough loss
}
```

## Usage Examples

### Basic Usage
```python
# Create bot with your data
df = pd.read_csv('your_crypto_data.csv')
bot = CryptoTradingBot(df=df)

# Run backtest
bot.run_bot()

# Check results
metrics = bot.logger.calculate_metrics(bot.execution_engine.trades)
print(f"Win Rate: {metrics['win_rate']:.1f}%")
```

### Live Trading
```python
# Set live trading in config.py
SANDBOX = False  # Enable live trading
API_KEY = 'your_live_api_key'
API_SECRET = 'your_live_api_secret'

# Run bot
bot = CryptoTradingBot()
asyncio.run(bot.run())
```

### Strategy Comparison
```python
# Test different strategies
strategies = ['random_forest', 'xgboost', 'lstm']

for strategy in strategies:
    Config.STRATEGY_TYPE = strategy
    bot = CryptoTradingBot(df=data)
    bot.run_bot()
    # Compare results...
```

## API Key Setup

### Binance Testnet (Recommended for testing)
1. Visit: https://testnet.binance.vision
2. Login with GitHub account
3. Generate API key with spot trading permissions
4. Get free test USDT for paper trading

### Live Trading Setup
1. Create account on chosen exchange
2. Generate API key with trading permissions
3. Set IP restrictions for security
4. Start with small amounts ($50-100)


## File Dependencies

### Required Files
- `config.py`: Configuration settings
- `GetData.py`: Data management class
- `FeatureExtract.py`: Feature engineering
- `Manage_orders.py`: Execution engine
- `Logger.py`: Trade logging
- `Visualizer.py`: Dashboard components

### Required Model
- `Weighted_model.pkl`: Pre-trained ML model

## Performance Expectations

### Hardware Requirements
- **CPU**: Any modern processor (your Ryzen 5 3550H is perfect)
- **RAM**: 8GB+ (16GB recommended)
- **Storage**: 1GB for data and models
- **GPU**: Optional (helpful for LSTM training)

### Execution Speed
- **Data fetching**: 1-2 seconds per update
- **Prediction**: <0.1 seconds per signal
- **Model training**: 2-15 minutes (depending on strategy)
- **Dashboard updates**: Every 5 seconds

## Security Considerations

### API Key Safety
- Never commit API keys to version control
- Use environment variables or config files
- Set IP restrictions on exchange
- Start with testnet/sandbox mode
- Use minimal permissions (spot trading only)

### Risk Management
- Never risk more than 1-2% per trade
- Set maximum daily loss limits
- Monitor bot performance regularly
- Have manual override capabilities

## Contributing

### Adding New Strategies
1. Inherit from base strategy class
2. Implement `train()` and `predict()` methods
3. Add model saving/loading functionality
4. Update config options

### Extending Features
1. Add new indicators in `FeatureExtract.py`
2. Update feature lists in strategies
3. Test with backtesting before live trading

## License and Disclaimers

**IMPORTANT**: This software is for educational purposes. Cryptocurrency trading involves significant financial risk. Past performance does not guarantee future results.

**Risk Warnings:**
- You can lose all invested capital
- Markets are volatile and unpredictable
- No trading system guarantees profits
- Start with small amounts and paper trading
- Never invest more than you can afford to lose

**No Financial Advice**: This bot is a tool, not financial advice. Make your own informed decisions.

## Support

For issues and questions:
1. Check troubleshooting section above
2. Review console output for error messages
3. Test components individually using debug functions
4. Start with paper trading to verify functionality

## Version History

- **v1.0**: Initial release with Random Forest strategy
- **v1.1**: Will Add XGBoost and LSTM strategies
- **v1.2**: Model persistence and smart retraining
- **v1.3**: Dashboard fixes and comprehensive debugging
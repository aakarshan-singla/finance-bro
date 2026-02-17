# Claude Integration for Automated Trade Suggestions

This finance-bro project now integrates Claude AI to automatically analyze technical signals and suggest trades.

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set your Claude API key:**
```bash
export ANTHROPIC_API_KEY='your-anthropic-api-key'
```

## How It Works

The `FinancialAgent` now includes Claude integration in three layers:

### 1. Technical Analysis (Trading Engine)
- Calculates RSI, MACD, and other technical indicators
- Generates initial BUY/SELL/HOLD signals
- Identifies entry/exit price levels

### 2. Claude Analysis Layer
- Reviews the technical signals with Claude
- Provides reasoning for trade decisions
- Assesses risk levels and probability of success

### 3. Trade Suggestion Generation
- Claude generates specific trade recommendations
- Includes entry, stop loss, and take profit levels
- Suggests position sizing and time horizons

## Usage

### Basic Usage with Claude

```python
from agent import FinancialAgent

# Initialize agent with Claude enabled
agent = FinancialAgent(use_llm=True)

# Get trade suggestions for symbols
symbols = ["AAPL", "MSFT", "GOOGL"]
suggestions = agent.get_trade_suggestions(symbols)

# Export results
agent.export_trade_suggestions("trade_suggestions.json")
agent.export_results("analysis_results.json")
```

### Get Single Symbol Suggestion

```python
# Analyze and get Claude's recommendation for one stock
suggestion = agent.get_claude_trade_suggestion("TSLA")

print(f"Recommendation: {suggestion['recommendation']}")
print(f"Entry Price: ${suggestion['entry_price']}")
print(f"Take Profit 1: ${suggestion['take_profit_target_1']}")
print(f"Take Profit 2: ${suggestion['take_profit_target_2']}")
print(f"Stop Loss: ${suggestion['suggested_stop_loss']}")
print(f"Position Size: {suggestion['position_size_suggestion']}")
```

### Filter Results

```python
# Get only BUY signals
buy_signals = agent.get_buy_signals()

# Get only SELL signals
sell_signals = agent.get_sell_signals()
```

## Output Format

Claude suggestions include:

```json
{
  "symbol": "AAPL",
  "recommendation": "Strong Buy",
  "entry_price": 150.25,
  "suggested_stop_loss": 148.50,
  "take_profit_target_1": 155.00,
  "take_profit_target_2": 160.00,
  "position_size_suggestion": "10%",
  "risk_reward_ratio": "1:3",
  "time_horizon": "2-3 weeks",
  "urgency": "This Week",
  "probability_of_success": 72,
  "key_factors": ["RSI oversold", "Trend confirmation", "Volume breakout"],
  "timestamp": "2026-02-17T10:30:00"
}
```

## Key Classes

### FinancialAgent
Main orchestrator that:
- Manages technical analysis
- Coordinates Claude analysis
- Generates trade suggestions
- Exports results

Methods:
- `analyze_symbol(symbol)` - Single symbol analysis
- `get_claude_trade_suggestion(symbol)` - Get Claude recommendation
- `get_trade_suggestions(symbols)` - Batch suggestions
- `export_trade_suggestions(filepath)` - Save suggestions

### LLMAnalyst
Claude interface for:
- `analyze_signal()` - Evaluate technical signals
- `generate_trade_suggestion()` - Create actionable trades
- `assess_market_conditions()` - Overall market analysis

### TradingEngine
Technical analysis:
- RSI, MACD calculations
- Support/resistance identification
- Entry/exit point calculation

## Configuration

Adjust trading parameters in `config.py`:

```python
config = TradingConfig(
    analysis_period_days=60,      # Historical data period
    rsi_oversold=30.0,            # RSI threshold
    rsi_overbought=70.0,
    stop_loss_percent=2.0,
    take_profit_percent=5.0,
    # ... other parameters
)

agent = FinancialAgent(config=config, use_llm=True)
```

## Using with Claude Code

When using this with Claude Code:

1. Set `ANTHROPIC_API_KEY` in your environment
2. Initialize agent with `use_llm=True`
3. Call `get_trade_suggestions()` for multiple stocks
4. Claude.Code will provide interactive analysis and recommendations

Example Claude Code prompt:
```
Analyze the tech sector and suggest the top 3 trades using the finance-bro agent.
Consider risk/reward ratios and give specific entry/exit points.
```

## Error Handling

The agent gracefully handles:
- Missing API key (disables Claude features)
- Network errors (retries with backoff)
- Missing symbol data (skips to next symbol)
- Invalid responses from Claude (returns raw response)

## Privacy & Cost

- All analysis happens locally except Claude API calls
- Claude costs ~$0.003-0.01 per symbol analyzed
- No data is stored on external servers
- Consider API costs when analyzing many symbols

## Next Steps

Enhance with:
- Real-time data streaming
- Historical backtesting
- Portfolio optimization
- Risk management rules
- Automated order execution

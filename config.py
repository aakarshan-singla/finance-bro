"""Configuration settings for the financial analysis agent."""

from dataclasses import dataclass
from typing import List

@dataclass
class TradingConfig:
    """Configuration for trading analysis parameters."""
    
    # Timeframe settings
    analysis_period_days: int = 60  # Historical data period for analysis
    trading_window_days: int = 7    # Days to look ahead for trading
    
    # Technical indicator thresholds
    rsi_oversold: float = 30.0      # RSI threshold for oversold condition
    rsi_overbought: float = 70.0    # RSI threshold for overbought condition
    macd_signal_threshold: float = 0.5  # MACD signal line crossover threshold
    
    # Volume analysis
    volume_threshold_percentile: float = 75.0  # Volume threshold for valid trades
    
    # Price action thresholds
    min_daily_change_percent: float = 0.5  # Minimum daily volatility %
    max_daily_change_percent: float = 15.0  # Maximum daily volatility %
    
    # Support/Resistance levels
    lookback_period: int = 20  # Period for identifying S/R levels
    
    # Risk management
    stop_loss_percent: float = 2.0  # Stop loss percentage
    take_profit_percent: float = 5.0  # Take profit percentage
    
    # Stock selection
    min_price: float = 5.0      # Minimum stock price
    max_price: float = 500.0    # Maximum stock price
    min_market_cap_millions: float = 1000.0  # Minimum market cap
    
    # Scoring weights
    rsi_weight: float = 0.25
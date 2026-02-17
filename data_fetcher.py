"""Module for fetching financial data from various sources."""

import yfinance as yf
import pandas as pd
from typing import Optional, List, Tuple
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataFetcher:
    """Fetches financial data for stocks."""
    
    def __init__(self):
        """Initialize the data fetcher."""
        self.cache = {}
    
    def get_historical_data(
        self,
        symbol: str,
        period_days: int = 60,
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """
        Fetch historical price data for a stock.
        
        Args:
            symbol: Stock ticker symbol
            period_days: Number of days of historical data
            interval: Data interval (1d, 1h, etc.)
            
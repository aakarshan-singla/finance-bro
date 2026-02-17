"""Module for technical analysis calculations."""

import pandas as pd
import numpy as np
from typing import Tuple, Optional
import ta


class TechnicalAnalyzer:
    """Performs technical analysis on stock data."""
    
    @staticmethod
    def calculate_rsi(df: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI).
        
        Args:
            df: DataFrame with 'Close' column
            period: RSI period
            
        Returns:
            Series with RSI values
        """
        if 'close' in df.columns:
            close_col = 'close'
        else:
            close_col = 'Close'
        
        return ta.momentum.rsi(df[close_col], window=period)
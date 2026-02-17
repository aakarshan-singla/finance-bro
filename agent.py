"""Main financial analysis agent."""

import json
import logging
from typing import List, Optional
from datetime import datetime

from config import TradingConfig, AnalysisResult
from data_fetcher import DataFetcher
from trading_engine import TradingEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FinancialAgent:
    """Main financial analysis agent."""
    
    def __init__(self, config: TradingConfig = None):
        """
        Initialize the financial analysis agent.
        
        Args:
            config: TradingConfig instance with analysis parameters
        """
        self.config = config or TradingConfig()
        self.data_fetcher = DataFetcher()
        self.trading_engine = TradingEngine(self.config)
        self.results: List[AnalysisResult] = []
    
    def analyze_symbol(self, symbol: str) -> Optional[AnalysisResult]:
        """
        Analyze a single stock symbol.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            AnalysisResult with trading signal and details
        """
        try:
            # Fetch historical data
            df = self.data_fetcher.get_historical_data(
                symbol,
                period_days=self.config.analysis_period_days
            )
            
            if df is None or df.empty:
                logger.warning(f"No data available for {symbol}")
                return None
            
            # Generate trading signal
            signal_result = self.trading_engine.evaluate_signal(symbol, df)
            
            if signal_result:
                result = AnalysisResult(
                    symbol=symbol,
                    timestamp=datetime.now(),
                    signal=signal_result.get('signal', 'HOLD'),
                    confidence=signal_result.get('confidence', 0.0),
                    entry_price=signal_result.get('entry_price'),
                    stop_loss=signal_result.get('stop_loss'),
                    take_profit=signal_result.get('take_profit'),
                    analysis_data=signal_result
                )
                self.results.append(result)
                return result
        
        except Exception as e:
            logger.error(f"Error analyzing {symbol}: {str(e)}")
            return None
    
    def analyze_symbols(self, symbols: List[str]) -> List[AnalysisResult]:
        """
        Analyze multiple stock symbols.
        
        Args:
            symbols: List of stock ticker symbols
            
        Returns:
            List of AnalysisResult objects
        """
        results = []
        for symbol in symbols:
            result = self.analyze_symbol(symbol)
            if result:
                results.append(result)
        
        return results
    
    def get_buy_signals(self) -> List[AnalysisResult]:
        """Get all current BUY signals."""
        return [r for r in self.results if r.signal == 'BUY']
    
    def get_sell_signals(self) -> List[AnalysisResult]:
        """Get all current SELL signals."""
        return [r for r in self.results if r.signal == 'SELL']
    
    def export_results(self, filepath: str) -> None:
        """
        Export analysis results to JSON.
        
        Args:
            filepath: Path to save the results
        """
        data = [
            {
                'symbol': r.symbol,
                'timestamp': r.timestamp.isoformat(),
                'signal': r.signal,
                'confidence': r.confidence,
                'entry_price': r.entry_price,
                'stop_loss': r.stop_loss,
                'take_profit': r.take_profit
            }
            for r in self.results
        ]
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Results exported to {filepath}")
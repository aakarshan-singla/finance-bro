"""Main financial analysis agent."""

import json
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from config import TradingConfig, AnalysisResult
from data_fetcher import DataFetcher
from trading_engine import TradingEngine
from llm_analyst import LLMAnalyst

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FinancialAgent:
    """Main financial analysis agent with Claude integration."""
    
    def __init__(self, config: TradingConfig = None, use_llm: bool = True):
        """
        Initialize the financial analysis agent.
        
        Args:
            config: TradingConfig instance with analysis parameters
            use_llm: Whether to use Claude for analysis suggestions
        """
        self.config = config or TradingConfig()
        self.data_fetcher = DataFetcher()
        self.trading_engine = TradingEngine(self.config)
        self.llm_analyst = None
        self.results: List[AnalysisResult] = []
        self.trade_suggestions: List[Dict[str, Any]] = []
        
        if use_llm:
            try:
                self.llm_analyst = LLMAnalyst()
                logger.info("LLM analyst initialized successfully")
            except (ImportError, ValueError) as e:
                logger.warning(f"Could not initialize LLM analyst: {e}. Continuing without LLM.")
                self.llm_analyst = None
    
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
    
    def get_claude_trade_suggestion(self, symbol: str, result: Optional[AnalysisResult] = None) -> Optional[Dict[str, Any]]:
        """
        Get Claude's trade suggestion for a symbol.
        
        Args:
            symbol: Stock ticker symbol
            result: Optional AnalysisResult (will analyze if not provided)
            
        Returns:
            Dictionary with Claude's trade suggestion
        """
        if not self.llm_analyst:
            logger.warning("LLM analyst not available. Initialize with use_llm=True")
            return None
        
        if result is None:
            result = self.analyze_symbol(symbol)
        
        if result is None:
            logger.error(f"Could not analyze {symbol}")
            return None
        
        try:
            # Get Claude's analysis of the technical signals
            analysis = self.llm_analyst.analyze_signal(
                symbol=symbol,
                signal=result.signal,
                confidence=result.confidence,
                technical_data=result.analysis_data or {}
            )
            
            # Get current price from the data
            current_price = result.entry_price or self._get_current_price(symbol)
            if not current_price:
                logger.warning(f"Could not get current price for {symbol}")
                return None
            
            # Generate specific trade suggestion
            suggestion = self.llm_analyst.generate_trade_suggestion(
                symbol=symbol,
                current_price=current_price,
                analysis=analysis
            )
            
            suggestion['technical_analysis'] = result.analysis_data
            suggestion['llm_analysis'] = analysis
            
            self.trade_suggestions.append(suggestion)
            return suggestion
        
        except Exception as e:
            logger.error(f"Error getting Claude suggestion for {symbol}: {str(e)}")
            return None
    
    def get_trade_suggestions(self, symbols: List[str]) -> List[Dict[str, Any]]:
        """
        Get Claude's trade suggestions for multiple symbols.
        
        Args:
            symbols: List of stock ticker symbols
            
        Returns:
            List of trade suggestions
        """
        suggestions = []
        for symbol in symbols:
            suggestion = self.get_claude_trade_suggestion(symbol)
            if suggestion:
                suggestions.append(suggestion)
        
        return suggestions
    
    def export_trade_suggestions(self, filepath: str) -> None:
        """
        Export trade suggestions to JSON.
        
        Args:
            filepath: Path to save the suggestions
        """
        with open(filepath, 'w') as f:
            json.dump(self.trade_suggestions, f, indent=2, default=str)
        
        logger.info(f"Trade suggestions exported to {filepath}")
    
    def _get_current_price(self, symbol: str) -> Optional[float]:
        """
        Get current price for a symbol.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Current price or None
        """
        try:
            df = self.data_fetcher.get_historical_data(symbol, period_days=1)
            if df is not None and not df.empty:
                # Try different column names
                if 'Close' in df.columns:
                    return float(df['Close'].iloc[-1])
                elif 'close' in df.columns:
                    return float(df['close'].iloc[-1])
        except Exception as e:
            logger.error(f"Error getting current price for {symbol}: {str(e)}")
        
        return None
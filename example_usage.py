"""Example usage of the financial analysis agent with Claude integration."""

import sys
import os
from agent import FinancialAgent
from config import TradingConfig


def main():
    """Main example demonstrating the financial agent with Claude."""
    
    # Initialize the agent with Claude integration
    print("Initializing Financial Agent with Claude...")
    agent = FinancialAgent(use_llm=True)
    
    # Example symbols to analyze
    symbols = ["AAPL", "MSFT", "GOOGL"]
    
    print(f"\nAnalyzing symbols: {symbols}")
    print("-" * 50)
    
    # Analyze symbols with technical analysis
    results = agent.analyze_symbols(symbols)
    
    print(f"\nFound {len(results)} analysis results")
    
    # Get Claude-powered trade suggestions
    if agent.llm_analyst:
        print("\nGetting Claude trade suggestions...")
        print("-" * 50)
        
        suggestions = agent.get_trade_suggestions(symbols)
        
        print(f"\nReceived {len(suggestions)} trade suggestions from Claude:")
        for suggestion in suggestions:
            print(f"\n{suggestion.get('symbol', 'UNKNOWN')}:")
            print(f"  Recommendation: {suggestion.get('recommendation', 'N/A')}")
            print(f"  Entry Price: ${suggestion.get('entry_price', 'N/A')}")
            print(f"  Risk/Reward: {suggestion.get('risk_reward_ratio', 'N/A')}")
            print(f"  Position Size: {suggestion.get('position_size_suggestion', 'N/A')}")
        
        # Export suggestions
        agent.export_trade_suggestions("trade_suggestions.json")
        print(f"\nTrade suggestions exported to trade_suggestions.json")
    
    # Export technical analysis results
    agent.export_results("analysis_results.json")
    print(f"Analysis results exported to analysis_results.json")
    
    # Get buy signals
    buy_signals = agent.get_buy_signals()
    print(f"\n\nBUY Signals: {len(buy_signals)}")
    for signal in buy_signals:
        print(f"  {signal.symbol} - Confidence: {signal.confidence:.2%}")
    
    # Get sell signals
    sell_signals = agent.get_sell_signals()
    print(f"\nSELL Signals: {len(sell_signals)}")
    for signal in sell_signals:
        print(f"  {signal.symbol} - Confidence: {signal.confidence:.2%}")


def example_single_symbol_with_claude():
    """Example of analyzing a single symbol with detailed Claude analysis."""
    
    print("Single Symbol Analysis with Claude")
    print("=" * 50)
    
    agent = FinancialAgent(use_llm=True)
    
    symbol = "TSLA"
    print(f"\nAnalyzing {symbol}...")
    
    # Get technical analysis
    result = agent.analyze_symbol(symbol)
    
    if result:
        print(f"\nTechnical Analysis Results:")
        print(f"  Signal: {result.signal}")
        print(f"  Confidence: {result.confidence:.2%}")
        print(f"  Entry Price: ${result.entry_price}")
        print(f"  Stop Loss: ${result.stop_loss}")
        print(f"  Take Profit: ${result.take_profit}")
        
        # Get Claude's trade suggestion
        if agent.llm_analyst:
            print(f"\nGetting Claude's recommendation...")
            suggestion = agent.get_claude_trade_suggestion(symbol, result)
            
            if suggestion:
                print(f"\nClaude's Trade Suggestion:")
                print(f"  Recommendation: {suggestion.get('recommendation', 'N/A')}")
                print(f"  Entry Price: ${suggestion.get('entry_price', 'N/A')}")
                print(f"  Stop Loss: ${suggestion.get('suggested_stop_loss', 'N/A')}")
                print(f"  Take Profit Target 1: ${suggestion.get('take_profit_target_1', 'N/A')}")
                print(f"  Take Profit Target 2: ${suggestion.get('take_profit_target_2', 'N/A')}")
                print(f"  Position Size: {suggestion.get('position_size_suggestion', 'N/A')}")
                print(f"  Risk/Reward Ratio: {suggestion.get('risk_reward_ratio', 'N/A')}")
                print(f"  Urgency: {suggestion.get('urgency', 'N/A')}")
                print(f"  Time Horizon: {suggestion.get('time_horizon', 'N/A')}")


if __name__ == "__main__":
    # Set ANTHROPIC_API_KEY environment variable before running
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Warning: ANTHROPIC_API_KEY not set. Claude features will be disabled.")
        print("To enable Claude trade suggestions, set: export ANTHROPIC_API_KEY='your-key'")
    
    # Run the main example
    main()
    
    # Uncomment to run single symbol example
    # example_single_symbol_with_claude()
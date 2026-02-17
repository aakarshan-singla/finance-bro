"""LLM-based analysis using Claude for trade suggestions."""

import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import os

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

logger = logging.getLogger(__name__)


class LLMAnalyst:
    """Uses Claude to analyze technical signals and suggest trades."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        """
        Initialize the LLM analyst.
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Claude model to use
        """
        if Anthropic is None:
            raise ImportError("anthropic package required. Install with: pip install anthropic")
        
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        self.conversation_history = []
    
    def analyze_signal(
        self,
        symbol: str,
        signal: str,
        confidence: float,
        technical_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze a trading signal with Claude.
        
        Args:
            symbol: Stock ticker symbol
            signal: Trading signal ('BUY', 'SELL', 'HOLD')
            confidence: Confidence score (0-1)
            technical_data: Dictionary with technical indicators
            
        Returns:
            Dictionary with Claude's analysis and recommendation
        """
        prompt = f"""
You are an expert financial analyst. Analyze the following trading signal and provide a detailed assessment.

Stock Symbol: {symbol}
Trading Signal: {signal}
Confidence Level: {confidence:.2%}

Technical Indicators:
{json.dumps(technical_data, indent=2)}

Provide your analysis in JSON format with the following fields:
- recommendation: Strong Buy, Buy, Hold, Sell, or Strong Sell
- reasoning: Brief explanation of your assessment
- risk_level: Low, Medium, or High
- key_factors: List of main factors influencing the decision
- suggested_entry: Suggested entry price (or null if not applicable)
- suggested_stop_loss: Suggested stop loss level
- suggested_take_profit: Suggested take profit level
- probability_of_success: Estimated probability of profit (0-100)
- additional_analysis: Any other relevant insights

Be concise but thorough. Consider technical momentum, trend confirmation, and risk/reward ratio.
"""
        
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        try:
            # Extract JSON from response
            json_start = assistant_message.find('{')
            json_end = assistant_message.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                analysis = json.loads(assistant_message[json_start:json_end])
            else:
                analysis = {"error": "Could not parse response", "raw_response": assistant_message}
        except json.JSONDecodeError:
            analysis = {"error": "Invalid JSON in response", "raw_response": assistant_message}
        
        return analysis
    
    def generate_trade_suggestion(
        self,
        symbol: str,
        current_price: float,
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a complete trade suggestion with Claude's input.
        
        Args:
            symbol: Stock ticker symbol
            current_price: Current stock price
            analysis: Analysis data from LLMAnalyst.analyze_signal
            
        Returns:
            Complete trade suggestion dictionary
        """
        prompt = f"""
Based on the previous analysis of {symbol}, generate a specific trade suggestion.

Current Price: ${current_price:.2f}

Here's the analysis we discussed:
{json.dumps(analysis, indent=2)}

Create a concrete trade suggestion in JSON format with:
- symbol: {symbol}
- recommendation: Trading recommendation (Strong Buy, Buy, Hold, Sell, Strong Sell)
- entry_price: Specific entry price to execute at
- stop_loss: Hard stop loss level for risk management
- take_profit_target_1: First profit target (typically 50% of position)
- take_profit_target_2: Second profit target (typically remaining position)
- position_size_suggestion: Percentage of portfolio (5%, 10%, 15%, etc.)
- time_horizon: Expected hold duration (days/weeks)
- urgency: Immediate, This Week, This Month, or Accumulate
- risk_reward_ratio: Expected ratio (e.g., "1:3")

Make the suggestion actionable and specific. Consider capital preservation.
"""
        
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1200,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        try:
            json_start = assistant_message.find('{')
            json_end = assistant_message.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                suggestion = json.loads(assistant_message[json_start:json_end])
            else:
                suggestion = {"error": "Could not parse suggestion", "raw": assistant_message}
        except json.JSONDecodeError:
            suggestion = {"error": "Invalid JSON in suggestion", "raw": assistant_message}
        
        suggestion['timestamp'] = datetime.now().isoformat()
        return suggestion
    
    def assess_market_conditions(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ask Claude to assess overall market conditions.
        
        Args:
            market_data: Dictionary with market indices and conditions
            
        Returns:
            Market assessment with trading implications
        """
        prompt = f"""
Assess the current market conditions and their implications for trading.

Market Data:
{json.dumps(market_data, indent=2)}

Provide assessment in JSON with:
- overall_sentiment: Bullish, Neutral, or Bearish
- volatility_level: Low, Moderate, High, or Extreme
- sector_strength: Top-performing and weak sectors
- risk_environment: Current risk factors to watch
- trading_bias: Long, Neutral, or Short bias recommended
- key_support_resistance: Important price levels to monitor
- recommended_strategy: Scalping, Day Trading, Swing Trading, or Position Trading
- cash_allocation: Suggested percentage to keep in cash (0-100%)
"""
        
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        try:
            json_start = assistant_message.find('{')
            json_end = assistant_message.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                assessment = json.loads(assistant_message[json_start:json_end])
            else:
                assessment = {"error": "Could not parse assessment", "raw": assistant_message}
        except json.JSONDecodeError:
            assessment = {"error": "Invalid JSON in assessment", "raw": assistant_message}
        
        return assessment
    
    def reset_conversation(self):
        """Reset conversation history for a new analysis session."""
        self.conversation_history = []

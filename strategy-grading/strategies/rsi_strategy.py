import pandas as pd
import numpy as np
from utils.helpers import calculate_rsi

def generate_rsi_signals(data: pd.DataFrame) -> pd.DataFrame:
    """
    Generate buy/sell/hold signals based on RSI strategy with adaptive thresholds
    
    Args:
        data: DataFrame with stock price data
        
    Returns:
        DataFrame with RSI signals added
    """
    # Handle multi-level columns for Close price
    if isinstance(data["Close"], pd.DataFrame):
        close_prices = data["Close"].iloc[:, 0]
    else:
        close_prices = data["Close"]
    
    # Create a temporary dataframe with single-level Close column
    temp_data = data.copy()
    temp_data["Close"] = close_prices
    
    # Calculate RSI
    data["RSI"] = calculate_rsi(temp_data, window=14)
    
    # Initialize signal column
    data["RSI_Signal"] = 0
    
    # Use adaptive RSI thresholds based on the RSI distribution
    rsi_25 = data["RSI"].quantile(0.25)  # Bottom 25% -> Buy
    rsi_75 = data["RSI"].quantile(0.75)  # Top 25% -> Sell
    
    # Generate signals based on adaptive RSI levels
    data.loc[data["RSI"] < rsi_25, "RSI_Signal"] = 1   # Buy (bottom quartile)
    data.loc[data["RSI"] > rsi_75, "RSI_Signal"] = -1  # Sell (top quartile)
    # Hold remains 0 (middle 50%)
    
    # If we still don't have enough signals, use standard RSI thresholds
    if data["RSI_Signal"].sum() == 0 or (data["RSI_Signal"] == 1).sum() < 2 or (data["RSI_Signal"] == -1).sum() < 2:
        # Fallback to standard RSI thresholds
        data.loc[data["RSI"] < 35, "RSI_Signal"] = 1   # Buy (slightly less strict)
        data.loc[data["RSI"] > 65, "RSI_Signal"] = -1  # Sell (slightly less strict)
    
    # Final fallback: use price momentum if still insufficient
    if (data["RSI_Signal"] == 1).sum() < 2 or (data["RSI_Signal"] == -1).sum() < 2:
        data["Price_Change"] = data["Close"].pct_change()
        # Use more aggressive momentum thresholds
        data.loc[data["Price_Change"] > 0.005, "RSI_Signal"] = 1   # Buy on positive momentum
        data.loc[data["Price_Change"] < -0.005, "RSI_Signal"] = -1  # Sell on negative momentum
    
    return data

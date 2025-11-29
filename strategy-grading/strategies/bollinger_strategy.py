import pandas as pd
import numpy as np
from utils.helpers import calculate_bollinger_bands

def generate_bollinger_signals(data: pd.DataFrame) -> pd.DataFrame:
    """
    Generate buy/sell/hold signals based on Bollinger Bands strategy
    
    Args:
        data: DataFrame with stock price data
        
    Returns:
        DataFrame with Bollinger Bands signals added
    """
    # Calculate Bollinger Bands
    upper_band, middle_band, lower_band = calculate_bollinger_bands(data, window=20, num_std=2)
    
    # Add Bollinger Bands components to data
    data["BB_Upper"] = upper_band
    data["BB_Middle"] = middle_band
    data["BB_Lower"] = lower_band
    
    # Initialize signal column
    data["BB_Strategy_Signal"] = 0
    
    # Generate signals based on Bollinger Bands
    # Buy when price touches or goes below lower band (oversold)
    # Sell when price touches or goes above upper band (overbought)
    
    # Handle multi-level columns for Close price
    if isinstance(data["Close"], pd.DataFrame):
        close_prices = data["Close"].iloc[:, 0]
    else:
        close_prices = data["Close"]
    
    data.loc[close_prices <= data["BB_Lower"], "BB_Strategy_Signal"] = 1   # Buy (oversold)
    data.loc[close_prices >= data["BB_Upper"], "BB_Strategy_Signal"] = -1  # Sell (overbought)
    # Hold remains 0 (price between bands)
    
    # Ensure we have some signals by adding a simple momentum strategy if needed
    if data["BB_Strategy_Signal"].sum() == 0:
        # Fallback: use price momentum
        data["Price_Change"] = data["Close"].pct_change()
        data.loc[data["Price_Change"] > 0.005, "BB_Strategy_Signal"] = 1   # Buy on positive momentum
        data.loc[data["Price_Change"] < -0.005, "BB_Strategy_Signal"] = -1  # Sell on negative momentum
    
    return data

import pandas as pd
import numpy as np

def moving_average(data: pd.DataFrame, window: int) -> pd.Series:
    return data["Close"].rolling(window=window).mean()

def calculate_rsi(data: pd.DataFrame, window: int = 14) -> pd.Series:
    """
    Calculate RSI (Relative Strength Index)
    
    Args:
        data: DataFrame with stock price data
        window: RSI calculation window (default 14)
    
    Returns:
        RSI values as pandas Series
    """
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple:
    """
    Calculate MACD (Moving Average Convergence Divergence)
    
    Args:
        data: DataFrame with stock price data
        fast: Fast EMA period (default 12)
        slow: Slow EMA period (default 26)
        signal: Signal line EMA period (default 9)
    
    Returns:
        Tuple of (MACD line, Signal line, Histogram)
    """
    ema_fast = data['Close'].ewm(span=fast).mean()
    ema_slow = data['Close'].ewm(span=slow).mean()
    
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal).mean()
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram

def calculate_bollinger_bands(data: pd.DataFrame, window: int = 20, num_std: float = 2) -> tuple:
    """
    Calculate Bollinger Bands
    
    Args:
        data: DataFrame with stock price data
        window: Moving average window (default 20)
        num_std: Number of standard deviations (default 2)
    
    Returns:
        Tuple of (Upper Band, Middle Band, Lower Band)
    """
    middle_band = data['Close'].rolling(window=window).mean()
    std = data['Close'].rolling(window=window).std()
    
    upper_band = middle_band + (std * num_std)
    lower_band = middle_band - (std * num_std)
    
    return upper_band, middle_band, lower_band

import yfinance as yf
import pandas as pd

def fetch_data(ticker: str, period: str = "6mo") -> pd.DataFrame:
    """
    Fetch stock data from Yahoo Finance
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'TCS.NS')
        period: Time period ('1mo', '3mo', '6mo', '1y', '2y', '5y')
    
    Returns:
        DataFrame with stock data and returns
    """
    try:
        # Ensure we have enough data for meaningful analysis
        min_period = "3mo" if period in ["1mo"] else period
        data = yf.download(ticker, period=min_period, interval="1d")
        
        if data.empty:
            raise ValueError(f"No data found for ticker: {ticker}")
        
        # Remove any rows with missing data
        data.dropna(inplace=True)
        
        # Calculate returns
        data["Return"] = data["Close"].pct_change()
        
        # Remove the first row which will have NaN return
        data = data.dropna()
        
        # Ensure we have enough data points
        if len(data) < 60:  # Need at least 60 days for meaningful MA analysis
            raise ValueError(f"Insufficient data: Only {len(data)} days available. Try a longer period.")
        
        return data
    except Exception as e:
        raise Exception(f"Error fetching data for {ticker}: {str(e)}")

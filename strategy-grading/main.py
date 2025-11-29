from data.data_fetcher import fetch_data
from strategies.rsi_strategy import generate_rsi_signals
from strategies.macd_strategy import generate_macd_signals
from strategies.bollinger_strategy import generate_bollinger_signals
from analysis.indicator_comparison import compare_indicators, rank_indicators, get_indicator_summary

def run_indicator_comparison(ticker: str = "AAPL", period: str = "6mo", indicator1: str = "RSI", indicator2: str = "MACD", signal1: str = "All", signal2: str = "All"):
    """
    Run indicator comparison analysis for RSI, MACD, and Bollinger Bands
    
    Args:
        ticker: Stock ticker symbol
        period: Time period for data
        
    Returns:
        Tuple of (data, comparison_results, indicator_ranking, summary)
    """
    # Fetch data
    data = fetch_data(ticker, period)
    
    # Generate signals for each indicator
    rsi_data = generate_rsi_signals(data.copy())
    macd_data = generate_macd_signals(data.copy())
    bb_data = generate_bollinger_signals(data.copy())
    
    # Combine all signals into one dataframe
    combined_data = data.copy()
    combined_data["RSI_Signal"] = rsi_data["RSI_Signal"]
    combined_data["MACD_Strategy_Signal"] = macd_data["MACD_Strategy_Signal"]
    combined_data["BB_Strategy_Signal"] = bb_data["BB_Strategy_Signal"]
    
    # Add indicator components for visualization
    combined_data["RSI"] = rsi_data["RSI"]
    combined_data["MACD"] = macd_data["MACD"]
    combined_data["MACD_Signal"] = macd_data["MACD_Signal"]
    combined_data["BB_Upper"] = bb_data["BB_Upper"]
    combined_data["BB_Middle"] = bb_data["BB_Middle"]
    combined_data["BB_Lower"] = bb_data["BB_Lower"]
    
    # Compare indicators
    comparison_results = compare_indicators(combined_data, indicator1, indicator2, signal1, signal2)
    
    # Rank indicators
    indicator_ranking = rank_indicators(comparison_results)
    
    # Get summary statistics
    summary = get_indicator_summary(combined_data)
    
    return combined_data, comparison_results, indicator_ranking, summary

if __name__ == "__main__":
    _, ttest_results, grades = run_strategy_grading("AAPL")
    print("T-test Results:", ttest_results)
    print("Grades:", grades)

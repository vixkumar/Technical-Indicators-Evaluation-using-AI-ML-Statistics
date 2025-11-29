from scipy import stats
import numpy as np
import pandas as pd

def remove_outliers(returns: pd.Series, threshold: float = 3.0) -> pd.Series:
    """
    Remove outliers from returns data using z-score method
    
    Args:
        returns: Series of returns
        threshold: Z-score threshold (default 3.0)
        
    Returns:
        Series with outliers removed
    """
    if len(returns) < 3:  # Need at least 3 points for z-score
        return returns
    
    z_scores = np.abs((returns - returns.mean()) / returns.std())
    return returns[z_scores < threshold]

def filter_returns_by_signal(data: pd.DataFrame, signal_column: str, signal_type: str) -> pd.Series:
    """
    Filter returns based on signal type
    
    Args:
        data: DataFrame with signals and returns
        signal_column: Name of the signal column
        signal_type: "All", "Buy", or "Sell"
        
    Returns:
        Series of filtered returns
    """
    if signal_type == "Buy":
        return data[data[signal_column] == 1]["Return"].dropna()
    elif signal_type == "Sell":
        return data[data[signal_column] == -1]["Return"].dropna()
    else:  # All
        return data[data[signal_column] != 0]["Return"].dropna()

def compare_indicators(data: pd.DataFrame, indicator1: str, indicator2: str, signal1: str = "All", signal2: str = "All") -> dict:
    """
    Compare two specific indicators using standard t-tests with signal type filtering
    
    Args:
        data: DataFrame with all indicator signals and returns
        indicator1: First indicator name ("RSI", "MACD", "Bollinger")
        indicator2: Second indicator name ("RSI", "MACD", "Bollinger")
        signal1: Signal type for first indicator ("All", "Buy", "Sell")
        signal2: Signal type for second indicator ("All", "Buy", "Sell")
        
    Returns:
        Dictionary with comparison results
    """
    # Map indicator names to signal columns
    signal_columns = {
        "RSI": "RSI_Signal",
        "MACD": "MACD_Strategy_Signal", 
        "Bollinger": "BB_Strategy_Signal"
    }
    
    # Get filtered returns for each indicator strategy based on signal types
    returns1 = filter_returns_by_signal(data, signal_columns[indicator1], signal1)
    returns2 = filter_returns_by_signal(data, signal_columns[indicator2], signal2)
    
    # Generate comparison key with signal types
    comparison_key = f"{indicator1}_{signal1} vs {indicator2}_{signal2}"
    
    results = {}
    
    # Perform comparison if we have at least 2 observations for each group
    if len(returns1) >= 2 and len(returns2) >= 2:
        t_stat, p_val = stats.ttest_ind(returns1, returns2, equal_var=False)
        results[comparison_key] = {
            't_statistic': t_stat,
            'p_value': p_val,
            f'{indicator1.lower()}_mean': returns1.mean(),
            f'{indicator2.lower()}_mean': returns2.mean(),
            f'{indicator1.lower()}_count': len(returns1),
            f'{indicator2.lower()}_count': len(returns2),
            'winner': determine_winner_simple(t_stat, p_val, indicator1, indicator2),
            'significance': get_significance_level(p_val)
        }
    
    return results

def get_significance_level(p_value: float) -> str:
    """
    Determine significance level based on p-value
    
    Args:
        p_value: P-value from t-test
        
    Returns:
        Significance level string
    """
    if p_value < 0.01:
        return 'Highly Significant (p < 0.01)'
    elif p_value < 0.05:
        return 'Significant (p < 0.05)'
    elif p_value < 0.1:
        return 'Moderately Significant (p < 0.1)'
    else:
        return 'Not Significant (p ≥ 0.1)'

def determine_winner_simple(t_statistic: float, p_value: float, indicator1: str, indicator2: str) -> str:
    """
    Determine winner based on standard t-test criteria
    
    Args:
        t_statistic: T-statistic from t-test
        p_value: P-value from t-test
        indicator1: Name of first indicator
        indicator2: Name of second indicator
        
    Returns:
        Winner string or 'Inconclusive' if not significant
    """
    # Standard statistical significance (p < 0.05)
    if p_value < 0.05:
        if t_statistic > 0:
            return indicator1
        elif t_statistic < 0:
            return indicator2
        else:
            return 'Tie'
    else:
        return 'Inconclusive'

def rank_indicators(comparison_results: dict) -> list:
    """
    Rank indicators based on their performance in comparisons
    
    Args:
        comparison_results: Results from compare_indicators function
        
    Returns:
        List of indicators ranked by performance
    """
    indicator_scores = {'RSI': 0, 'MACD': 0, 'Bollinger': 0}
    
    for comparison, result in comparison_results.items():
        if result['significance'] != 'Not Significant (p ≥ 0.1)' and result['winner'] != 'Inconclusive':
            winner = result['winner']
            if winner in indicator_scores:
                indicator_scores[winner] += 1
    
    # Sort by score (descending)
    ranked_indicators = sorted(indicator_scores.items(), key=lambda x: x[1], reverse=True)
    
    return ranked_indicators

def get_indicator_summary(data: pd.DataFrame) -> dict:
    """
    Get summary statistics for each indicator
    
    Args:
        data: DataFrame with all indicator signals and returns
        
    Returns:
        Dictionary with summary statistics
    """
    rsi_returns = data[data["RSI_Signal"] != 0]["Return"].dropna()
    macd_returns = data[data["MACD_Strategy_Signal"] != 0]["Return"].dropna()
    bb_returns = data[data["BB_Strategy_Signal"] != 0]["Return"].dropna()
    
    summary = {
        'RSI': {
            'mean_return': rsi_returns.mean(),
            'std_return': rsi_returns.std(),
            'count': len(rsi_returns),
            'total_return': rsi_returns.sum()
        },
        'MACD': {
            'mean_return': macd_returns.mean(),
            'std_return': macd_returns.std(),
            'count': len(macd_returns),
            'total_return': macd_returns.sum()
        },
        'Bollinger': {
            'mean_return': bb_returns.mean(),
            'std_return': bb_returns.std(),
            'count': len(bb_returns),
            'total_return': bb_returns.sum()
        }
    }
    
    return summary

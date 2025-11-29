from scipy import stats
import numpy as np
import pandas as pd

def perform_ttests(data: pd.DataFrame):
    buy_returns = data.loc[data["Signal"] == 1, "Return"].dropna()
    sell_returns = data.loc[data["Signal"] == -1, "Return"].dropna()
    hold_returns = data.loc[data["Signal"] == 0, "Return"].dropna()

    results = {}
    if len(buy_returns) > 2 and len(sell_returns) > 2:
        t_stat, p_val = stats.ttest_ind(buy_returns, sell_returns, equal_var=False)
        results["Buy vs Sell"] = p_val
    if len(buy_returns) > 2 and len(hold_returns) > 2:
        t_stat, p_val = stats.ttest_ind(buy_returns, hold_returns, equal_var=False)
        results["Buy vs Hold"] = p_val
    if len(sell_returns) > 2 and len(hold_returns) > 2:
        t_stat, p_val = stats.ttest_ind(sell_returns, hold_returns, equal_var=False)
        results["Sell vs Hold"] = p_val

    return results

def perform_pairwise_ttest(data: pd.DataFrame, strategy1: str, strategy2: str):
    """
    Perform t-test between two specific strategies
    
    Args:
        data: DataFrame with stock data and signals
        strategy1: First strategy ('Buy', 'Sell', 'Hold')
        strategy2: Second strategy ('Buy', 'Sell', 'Hold')
    
    Returns:
        Dictionary with t-test results and interpretation
    """
    # Map strategy names to signal values
    strategy_map = {'Buy': 1, 'Sell': -1, 'Hold': 0}
    
    signal1 = strategy_map[strategy1]
    signal2 = strategy_map[strategy2]
    
    # Get returns for each strategy
    returns1 = data.loc[data["Signal"] == signal1, "Return"].dropna()
    returns2 = data.loc[data["Signal"] == signal2, "Return"].dropna()
    
    # Debug information (commented out for production)
    # print(f"Debug: {strategy1} (signal {signal1}) has {len(returns1)} observations")
    # print(f"Debug: {strategy2} (signal {signal2}) has {len(returns2)} observations")
    # print(f"Debug: Total data points: {len(data)}")
    # print(f"Debug: Signal distribution: {data['Signal'].value_counts().to_dict()}")
    
    if len(returns1) < 2 or len(returns2) < 2:
        return {
            'p_value': 1.0,
            't_statistic': 0.0,
            'significance': 'Insufficient Data',
            'grade': 'N/A',
            'sample_size_1': len(returns1),
            'sample_size_2': len(returns2),
            'debug_info': f"Need at least 2 observations for each strategy. {strategy1}: {len(returns1)}, {strategy2}: {len(returns2)}"
        }
    
    # Perform t-test
    t_stat, p_val = stats.ttest_ind(returns1, returns2, equal_var=False)
    
    # Determine significance level
    if p_val < 0.01:
        significance = 'Highly Significant (p < 0.01)'
        grade = 'A+'
    elif p_val < 0.05:
        significance = 'Significant (p < 0.05)'
        grade = 'A'
    elif p_val < 0.1:
        significance = 'Moderately Significant (p < 0.1)'
        grade = 'B'
    else:
        significance = 'Not Significant (p ≥ 0.1)'
        grade = 'C'
    
    return {
        'p_value': p_val,
        't_statistic': t_stat,
        'significance': significance,
        'grade': grade,
        'sample_size_1': len(returns1),
        'sample_size_2': len(returns2),
        'mean_return_1': returns1.mean(),
        'mean_return_2': returns2.mean(),
        'std_return_1': returns1.std(),
        'std_return_2': returns2.std()
    }

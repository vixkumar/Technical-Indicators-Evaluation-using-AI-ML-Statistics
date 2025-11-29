def grade_strategies(ttest_results: dict):
    grades = {}
    for pair, p_val in ttest_results.items():
        if p_val < 0.01:
            grades[pair] = "A+ (Highly Significant)"
        elif p_val < 0.05:
            grades[pair] = "A (Significant)"
        elif p_val < 0.1:
            grades[pair] = "B (Moderately Significant)"
        else:
            grades[pair] = "C (Not Significant)"
    return grades

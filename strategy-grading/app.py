import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from main import run_indicator_comparison

# Configure page for fintech styling
st.set_page_config(
    page_title="Trading Stratergy Analyzer using Statistical Analysis & Methods",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for fintech styling
st.markdown("""
<style>
    /* Main theme colors */
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    .success-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    .info-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    .sidebar-content {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
    
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .stSelectbox > div > div {
        background: white;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        color: #333333 !important;
    }
    
    .stSelectbox > div > div > div {
        color: #333333 !important;
    }
    
    .stSelectbox > div > div > div > div {
        color: #333333 !important;
    }
    
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        background-color: white !important;
        color: #000000 !important;
    }
    
    .stTextInput > div > div > input:focus {
        background-color: white !important;
        color: #000000 !important;
        border-color: #667eea !important;
    }
    
    .stTextInput label {
        color: #333333 !important;
    }
    
    /* Fix dropdown text visibility */
    .stSelectbox label {
        color: #333333 !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        color: #333333 !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        color: #333333 !important;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    /* Additional fixes for dropdown visibility */
    .stSelectbox [data-baseweb="select"] [data-baseweb="select__value-container"] {
        color: #333333 !important;
    }
    
    .stSelectbox [data-baseweb="select"] [data-baseweb="select__single-value"] {
        color: #333333 !important;
    }
    
    .stSelectbox [data-baseweb="select"] [data-baseweb="select__placeholder"] {
        color: #666666 !important;
    }
    
    /* Ensure all text in selectbox is dark */
    .stSelectbox * {
        color: #333333 !important;
    }
    
    .stSelectbox [data-baseweb="select"] * {
        color: #333333 !important;
    }
    
    /* Fix sidebar headings to be white */
    .stSidebar h3 {
        color: white !important;
    }
    
    .stSidebar h4 {
        color: white !important;
    }
    
    .stSidebar strong {
        color: white !important;
    }
    
    .stSidebar p {
        color: #e0e0e0 !important;
    }
    
    /* Fix all text in sidebar to be visible */
    .stSidebar .sidebar-content h3 {
        color: white !important;
    }
    
    .stSidebar .sidebar-content p {
        color: #e0e0e0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Main header with fintech styling
st.markdown("""
<div class="main-header">
    <h1>📈 Strategy Analyzer Pro</h1>
    <p>Advanced Statistical Analysis for Trading Indicators</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for inputs with fintech styling
st.sidebar.markdown("""
<div class="sidebar-content">
    <h3>📊 Analysis Parameters</h3>
</div>
""", unsafe_allow_html=True)

# Stock selection with enhanced styling
st.sidebar.markdown("**🏢 Stock Selection**")
ticker = st.sidebar.text_input("Enter Stock Ticker Symbol:", "AAPL", 
                               help="Examples: AAPL, MSFT, TCS.NS, INFY.NS")

# Period selection with market context
st.sidebar.markdown("**⏰ Time Period**")
period = st.sidebar.selectbox("Select Time Period:", 
                             ["1mo", "3mo", "6mo", "1y", "2y", "5y"], 
                             index=2,
                             help="Longer periods provide more reliable statistical results")

# Indicator comparison selection with fintech styling
st.sidebar.markdown("""
<div class="sidebar-content">
    <h3>🔍 Strategy Comparison</h3>
    <p>Select indicators and signal types for statistical analysis</p>
</div>
""", unsafe_allow_html=True)

indicator_options = ["RSI", "MACD", "Bollinger Bands"]
signal_options = ["All", "Buy", "Sell"]

col1, col2 = st.sidebar.columns(2)

with col1:
    indicator1 = st.selectbox("First Indicator:", indicator_options, index=0)
    signal1 = st.selectbox("First Signal Type:", signal_options, index=0)

with col2:
    indicator2 = st.selectbox("Second Indicator:", indicator_options, index=1)
    signal2 = st.selectbox("Second Signal Type:", signal_options, index=0)

# Ensure different indicators are selected
if indicator1 == indicator2:
    st.sidebar.warning("⚠️ Please select two different indicators for comparison")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    if st.button("🚀 Run Analysis", type="primary"):
        if indicator1 == indicator2:
            st.error("Please select two different indicators for comparison")
        else:
            with st.spinner("Fetching data and performing indicator comparison..."):
                try:
                    # Map UI names to internal names
                    indicator_mapping = {
                        "RSI": "RSI",
                        "MACD": "MACD", 
                        "Bollinger Bands": "Bollinger"
                    }
                    
                    mapped_indicator1 = indicator_mapping[indicator1]
                    mapped_indicator2 = indicator_mapping[indicator2]
                    
                    data, comparison_results, indicator_ranking, summary = run_indicator_comparison(ticker, period, mapped_indicator1, mapped_indicator2, signal1, signal2)
                    
                    # Store data in session state for charts
                    st.session_state['data'] = data
                    st.session_state['ticker'] = ticker
                    st.session_state['comparison_results'] = comparison_results
                    st.session_state['indicator_ranking'] = indicator_ranking
                    st.session_state['summary'] = summary
                    st.session_state['selected_indicators'] = (indicator1, indicator2)
                    
                    # Display results with fintech styling
                    st.markdown(f"""
                    <div class="main-header">
                        <h2>📊 {indicator1} {signal1} vs {indicator2} {signal2} Analysis</h2>
                        <p>Statistical Performance Comparison</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                    # Generate comparison key with signal types
                    comparison_key = f"{mapped_indicator1}_{signal1} vs {mapped_indicator2}_{signal2}"
                    
                    if comparison_key and comparison_key in comparison_results:
                        result = comparison_results[comparison_key]
                        
                        # Show comparison results with fintech cards
                        st.markdown("### 📈 Statistical Results")
                        
                        # Create fintech-style metric cards
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.markdown(f"""
                            <div class="metric-card">
                                <h4>T-Statistic</h4>
                                <h2>{result['t_statistic']:.4f}</h2>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                            <div class="metric-card">
                                <h4>P-Value</h4>
                                <h2>{result['p_value']:.6f}</h2>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            winner_color = "success-card" if result['winner'] != 'Inconclusive' else "warning-card"
                            st.markdown(f"""
                            <div class="{winner_color}">
                                <h4>Winner</h4>
                                <h2>{result['winner']}</h2>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col4:
                            st.markdown(f"""
                            <div class="info-card">
                                <h4>Significance</h4>
                                <h2>{result['significance'].split('(')[0].strip()}</h2>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Show sample information with fintech cards
                        st.markdown("### 📊 Data Quality Metrics")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown(f"""
                            <div class="metric-card">
                                <h4>{indicator1} Signals</h4>
                                <h2>{result[f'{mapped_indicator1.lower()}_count']}</h2>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                            <div class="metric-card">
                                <h4>{indicator2} Signals</h4>
                                <h2>{result[f'{mapped_indicator2.lower()}_count']}</h2>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            mean_diff = abs(result[f'{mapped_indicator1.lower()}_mean'] - result[f'{mapped_indicator2.lower()}_mean'])
                            st.markdown(f"""
                            <div class="metric-card">
                                <h4>Mean Difference</h4>
                                <h2>{mean_diff:.4f}</h2>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Show warning if present
                        if 'warning' in result:
                            st.warning(f"⚠️ **Warning**: {result['warning']}")
                        
                        # Show detailed significance information
                        st.subheader("📊 Detailed Significance Analysis")
                        significance_info = f"""
                        **Significance Level**: {result['significance']}
                        
                        **P-Value Interpretation**:
                        - P-value = {result['p_value']:.6f}
                        - This means there is a {result['p_value']*100:.2f}% probability that the observed difference occurred by chance
                        
                        **Statistical Interpretation**:
                        """
                        
                        if result['p_value'] < 0.01:
                            significance_info += f"- **Highly Significant (p < 0.01)**: Strong evidence of difference (less than 1% chance of random variation)"
                        elif result['p_value'] < 0.05:
                            significance_info += f"- **Significant (p < 0.05)**: Good evidence of difference (less than 5% chance of random variation)"
                        elif result['p_value'] < 0.1:
                            significance_info += f"- **Moderately Significant (p < 0.1)**: Some evidence of difference (less than 10% chance of random variation)"
                        else:
                            significance_info += f"- **Not Significant (p ≥ 0.1)**: Weak evidence of difference (more than 10% chance of random variation)"
                        
                        significance_info += f"""
                        
                        **T-Statistic**: {result['t_statistic']:.4f}
                        - Positive t-statistic favors the first indicator ({mapped_indicator1})
                        - Negative t-statistic favors the second indicator ({mapped_indicator2})
                        - Larger absolute values indicate stronger evidence
                        """
                        
                        st.markdown(significance_info)
                        
                        # Show means
                        st.write("**Mean Returns:**")
                        if 'rsi_mean' in result:
                            st.write(f"• RSI: {result['rsi_mean']:.4f}")
                        if 'macd_mean' in result:
                            st.write(f"• MACD: {result['macd_mean']:.4f}")
                        if 'bb_mean' in result:
                            st.write(f"• Bollinger: {result['bb_mean']:.4f}")
                        
                        # Show sample sizes
                        st.write("**Sample Sizes:**")
                        if 'rsi_count' in result:
                            st.write(f"• RSI: {result['rsi_count']} signals")
                        if 'macd_count' in result:
                            st.write(f"• MACD: {result['macd_count']} signals")
                        if 'bb_count' in result:
                            st.write(f"• Bollinger: {result['bb_count']} signals")
                    else:
                        st.error("Comparison not found. Please try again.")
                    
                    # Show summary statistics for selected indicators
                    st.subheader("📊 Indicator Summary")
                    try:
                        # Helper function to safely convert count to int
                        def safe_int(value, default=0):
                            """Safely convert value to int, handling NaN, None, and string cases"""
                            if value is None:
                                return default
                            try:
                                # Check if it's a pandas scalar NaN
                                if hasattr(value, '__class__') and pd.isna(value):
                                    return default
                                # Check if it's a numpy NaN
                                import numpy as np
                                if isinstance(value, (float, np.floating)) and np.isnan(value):
                                    return default
                            except:
                                pass
                            if isinstance(value, str):
                                try:
                                    return int(float(value))
                                except (ValueError, TypeError):
                                    return default
                            try:
                                # Convert to native Python int (not numpy/pandas scalar)
                                result = int(float(value))
                                return result
                            except (ValueError, TypeError):
                                return default
                        
                        # Helper function to safely get float value
                        def safe_float(value, default=0.0):
                            """Safely convert value to float, handling NaN and None cases"""
                            if value is None:
                                return default
                            try:
                                # Check if it's a pandas scalar NaN
                                if hasattr(value, '__class__') and pd.isna(value):
                                    return default
                                # Check if it's a numpy NaN
                                import numpy as np
                                if isinstance(value, (float, np.floating)) and np.isnan(value):
                                    return default
                            except:
                                pass
                            try:
                                result = float(value)
                                # Check if result is NaN
                                import numpy as np
                                if np.isnan(result):
                                    return default
                                return result
                            except (ValueError, TypeError):
                                return default
                        
                        # Process first indicator
                        summary1 = summary.get(mapped_indicator1, {})
                        if not summary1:
                            summary1 = {}
                        
                        # Extract and convert values to native Python types
                        count1_val = summary1.get('count', 0)
                        mean1_val = summary1.get('mean_return', 0)
                        std1_val = summary1.get('std_return', 0)
                        total1_val = summary1.get('total_return', 0)
                        
                        count1 = int(safe_int(count1_val, 0))
                        mean1 = float(safe_float(mean1_val, 0.0))
                        std1 = float(safe_float(std1_val, 0.0))
                        total1 = float(safe_float(total1_val, 0.0))
                        
                        # Process second indicator
                        summary2 = summary.get(mapped_indicator2, {})
                        if not summary2:
                            summary2 = {}
                        
                        # Extract and convert values to native Python types
                        count2_val = summary2.get('count', 0)
                        mean2_val = summary2.get('mean_return', 0)
                        std2_val = summary2.get('std_return', 0)
                        total2_val = summary2.get('total_return', 0)
                        
                        count2 = int(safe_int(count2_val, 0))
                        mean2 = float(safe_float(mean2_val, 0.0))
                        std2 = float(safe_float(std2_val, 0.0))
                        total2 = float(safe_float(total2_val, 0.0))
                        
                        # Create DataFrame with explicit column structure and types
                        summary_df = pd.DataFrame({
                            'Mean Return': [mean1, mean2],
                            'Std Return': [std1, std2],
                            'Count': [count1, count2],
                            'Total Return': [total1, total2]
                        })
                        
                        # Set index with indicator names
                        summary_df.index = pd.Index([str(indicator1), str(indicator2)], dtype='object')
                        
                        # Ensure Count column is integer type
                        summary_df['Count'] = summary_df['Count'].astype('int64')
                        
                        # Display the dataframe (removed width parameter for compatibility)
                        st.dataframe(summary_df)
                    except Exception as e:
                        import traceback
                        st.error(f"Error displaying summary: {str(e)}")
                        st.error(f"Traceback: {traceback.format_exc()}")
                        # Fallback: display as formatted text
                        st.write(f"**{indicator1} Summary:**")
                        summary1_fallback = summary.get(mapped_indicator1, {})
                        for key, value in summary1_fallback.items():
                            if pd.isna(value):
                                display_value = "N/A"
                            elif isinstance(value, (int, float)):
                                display_value = f"{value:.4f}"
                            else:
                                display_value = str(value)
                            st.write(f"- {key.replace('_', ' ').title()}: {display_value}")
                        st.write(f"**{indicator2} Summary:**")
                        summary2_fallback = summary.get(mapped_indicator2, {})
                        for key, value in summary2_fallback.items():
                            if pd.isna(value):
                                display_value = "N/A"
                            elif isinstance(value, (int, float)):
                                display_value = f"{value:.4f}"
                            else:
                                display_value = str(value)
                            st.write(f"- {key.replace('_', ' ').title()}: {display_value}")
                
                    # Interpretation
                    st.subheader("📈 Statistical Interpretation")
                    if comparison_key in comparison_results:
                        result = comparison_results[comparison_key]
                        winner = result['winner']
                        significance = result['significance']
                        
                        if winner == 'Inconclusive':
                            st.warning(f"⚠️ **Inconclusive**: No statistically significant difference between {indicator1} and {indicator2} ({significance})")
                        elif significance != 'Not Significant (p ≥ 0.1)':
                            st.success(f"🏆 **Winner**: {winner} (Significant difference: {significance})")
                        else:
                            st.info(f"ℹ️ **No significant difference** between {indicator1} and {indicator2}")
                        
                        # Detailed interpretation
                        if winner == 'Inconclusive':
                            st.info(f"ℹ️ **Inconclusive Result**: The difference between indicators is not statistically significant (p = {result['p_value']:.4f}). More data or different market conditions may be needed to determine a clear winner.")
                        elif result['p_value'] < 0.01:
                            st.success(f"🎯 **Highly Significant (p < 0.01)**: {winner} significantly outperforms the other indicator")
                        elif result['p_value'] < 0.05:
                            st.success(f"✅ **Significant (p < 0.05)**: {winner} shows significant advantage")
                        elif result['p_value'] < 0.1:
                            st.warning(f"⚠️ **Moderately Significant (p < 0.1)**: {winner} shows moderate advantage")
                        else:
                            st.info(f"ℹ️ **Not Significant (p ≥ 0.1)**: No significant difference between the indicators")
                    
                    # Charts section with fintech styling
                    st.markdown("### 📈 Market Analysis Charts")
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    fig = go.Figure()
                    
                    # Handle multi-level columns from yfinance
                    if isinstance(data["Close"], pd.DataFrame):
                        close_prices = data["Close"].iloc[:, 0]  # Get first column if multi-level
                    else:
                        close_prices = data["Close"]
                    
                    fig.add_trace(go.Scatter(x=data.index, y=close_prices, mode="lines", name="Close Price", line=dict(color='blue')))
                    fig.update_layout(title=f"{ticker} Stock Price", 
                                     xaxis_title="Date", yaxis_title="Price")
                    st.plotly_chart(fig, width='stretch')
                    
                    # Show charts for selected indicators only
                    if indicator1 == "RSI" or indicator2 == "RSI":
                        st.subheader("📈 RSI Indicator")
                        fig_rsi = go.Figure()
                        fig_rsi.add_trace(go.Scatter(x=data.index, y=data["RSI"], mode="lines", name="RSI", line=dict(color='purple')))
                        
                        # Add adaptive RSI thresholds based on the data
                        rsi_25 = data["RSI"].quantile(0.25)
                        rsi_75 = data["RSI"].quantile(0.75)
                        
                        fig_rsi.add_hline(y=rsi_75, line_dash="dash", line_color="red", annotation_text=f"Top 25% ({rsi_75:.1f})")
                        fig_rsi.add_hline(y=rsi_25, line_dash="dash", line_color="green", annotation_text=f"Bottom 25% ({rsi_25:.1f})")
                        fig_rsi.update_layout(title=f"{ticker} RSI Indicator with Adaptive Thresholds", 
                                             xaxis_title="Date", yaxis_title="RSI",
                                             yaxis=dict(range=[0, 100]))
                        st.plotly_chart(fig_rsi, width='stretch')
                    
                    if indicator1 == "MACD" or indicator2 == "MACD":
                        st.subheader("📈 MACD Indicator")
                        fig_macd = go.Figure()
                        fig_macd.add_trace(go.Scatter(x=data.index, y=data["MACD"], mode="lines", name="MACD", line=dict(color='blue')))
                        fig_macd.add_trace(go.Scatter(x=data.index, y=data["MACD_Signal"], mode="lines", name="Signal", line=dict(color='red')))
                        fig_macd.update_layout(title=f"{ticker} MACD Indicator", 
                                             xaxis_title="Date", yaxis_title="MACD")
                        st.plotly_chart(fig_macd, width='stretch')
                    
                    if indicator1 == "Bollinger Bands" or indicator2 == "Bollinger Bands":
                        st.subheader("📈 Bollinger Bands")
                        fig_bb = go.Figure()
                        fig_bb.add_trace(go.Scatter(x=data.index, y=close_prices, mode="lines", name="Close Price", line=dict(color='blue')))
                        fig_bb.add_trace(go.Scatter(x=data.index, y=data["BB_Upper"], mode="lines", name="Upper Band", line=dict(color='red', dash='dash')))
                        fig_bb.add_trace(go.Scatter(x=data.index, y=data["BB_Middle"], mode="lines", name="Middle Band", line=dict(color='green', dash='dot')))
                        fig_bb.add_trace(go.Scatter(x=data.index, y=data["BB_Lower"], mode="lines", name="Lower Band", line=dict(color='red', dash='dash')))
                        fig_bb.update_layout(title=f"{ticker} Bollinger Bands", 
                                           xaxis_title="Date", yaxis_title="Price")
                        st.plotly_chart(fig_bb, width='stretch')

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Please check if the ticker symbol is correct and try again.")

with col1:
    st.markdown("""
    <div class="sidebar-content">
        <h3>📊 Statistical Interpretation</h3>
        <h4>P-Value Significance:</h4>
        <ul>
            <li><strong>p < 0.01</strong>: Highly significant difference</li>
            <li><strong>p < 0.05</strong>: Significant difference</li>
            <li><strong>p < 0.1</strong>: Moderately significant</li>
            <li><strong>p ≥ 0.1</strong>: No significant difference</li>
        </ul>
        <h4>Confidence Levels:</h4>
        <ul>
            <li>p < 0.05 = 95% confidence</li>
            <li>p < 0.01 = 99% confidence</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="sidebar-content">
        <h3>📈 T-Statistic Guide</h3>
        <h4>Evidence Strength:</h4>
        <ul>
            <li><strong>|t| < 1</strong>: Weak evidence</li>
            <li><strong>1 ≤ |t| < 2</strong>: Moderate evidence</li>
            <li><strong>2 ≤ |t| < 3</strong>: Strong evidence</li>
            <li><strong>|t| ≥ 3</strong>: Very strong evidence</li>
        </ul>
        <h4>Direction:</h4>
        <ul>
            <li><strong>t > 0</strong>: First indicator wins</li>
            <li><strong>t < 0</strong>: Second indicator wins</li>
            <li><strong>t = 0</strong>: No difference (rare)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


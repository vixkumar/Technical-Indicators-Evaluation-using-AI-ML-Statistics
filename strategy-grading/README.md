# Strategy Grading using T-Tests

A Streamlit application that compares Buy, Sell, and Hold strategies on stock data using statistical t-tests.

## Features

- **Interactive UI**: Select stock ticker and time period
- **Strategy Comparison**: Compare any two strategies (Buy vs Sell, Buy vs Hold, Sell vs Hold)
- **Statistical Analysis**: T-test results with significance levels and grades
- **Visualization**: Stock price charts with moving averages and strategy signals
- **Real-time Data**: Fetches data from Yahoo Finance

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the provided local URL (usually http://localhost:8501)

3. Use the sidebar to:
   - Enter a stock ticker symbol (e.g., AAPL, MSFT, TCS.NS, INFY.NS)
   - Select a time period (1mo, 3mo, 6mo, 1y, 2y, 5y)
   - Choose two strategies to compare

4. Click "Run Analysis" to see the results

## Strategy Definitions

- **Buy**: When 20-day moving average > 50-day moving average
- **Sell**: When 20-day moving average < 50-day moving average
- **Hold**: When signals are neutral

## T-Test Interpretation

- **p < 0.01**: Highly significant difference (Grade A+)
- **p < 0.05**: Significant difference (Grade A)
- **p < 0.1**: Moderately significant (Grade B)
- **p ≥ 0.1**: No significant difference (Grade C)

## Example Stock Symbols

- US Stocks: AAPL, MSFT, GOOGL, AMZN, TSLA
- Indian Stocks: TCS.NS, INFY.NS, RELIANCE.NS, HDFCBANK.NS
- International: ^GSPC (S&P 500), ^DJI (Dow Jones)

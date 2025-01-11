import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns

def fetch_stock_data(tickers, start_date, end_date):
    """
    Fetch historical stock data for given tickers
    """
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        data[ticker] = stock.history(start=start_date, end=end_date)
    return data

def calculate_metrics(data):
    """
    Calculate key metrics for each stock
    """
    metrics = {}
    for ticker, df in data.items():
        metrics[ticker] = {
            'Total Return': ((df['Close'][-1] - df['Close'][0]) / df['Close'][0] * 100),
            'Max Price': df['High'].max(),
            'Min Price': df['Low'].min(),
            'Average Volume': df['Volume'].mean(),
            'Volatility': df['Close'].pct_change().std() * 100
        }
    return metrics

def plot_comparison(data, title):
    """
    Create comparison plot for closing prices
    """
    plt.figure(figsize=(15, 8))
    for ticker, df in data.items():
        plt.plot(df.index, df['Close'], label=ticker)
    
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Stock Price (USD)')
    plt.legend()
    plt.grid(True)
    return plt

def main():
    # Define parameters
    tickers = ['AAPL', 'GOOGL', 'MSFT']
    start_date = '2015-01-01'
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Fetch data
    print("Fetching historical data...")
    stock_data = fetch_stock_data(tickers, start_date, end_date)
    
    # Calculate metrics
    metrics = calculate_metrics(stock_data)
    
    # Print metrics
    print("\nKey Metrics (2015 - Present):")
    print("-" * 50)
    for ticker, metric in metrics.items():
        print(f"\n{ticker}:")
        for key, value in metric.items():
            print(f"{key}: {value:.2f}")
    
    # Create visualization
    plt = plot_comparison(stock_data, 'Stock Price Comparison (2015 - Present)')
    plt.show()
    
    # Create normalized comparison (starting from 100)
    normalized_data = {}
    for ticker, df in stock_data.items():
        normalized_data[ticker] = df.copy()
        first_price = normalized_data[ticker]['Close'][0]
        normalized_data[ticker]['Close'] = (normalized_data[ticker]['Close'] / first_price) * 100
    
    plt = plot_comparison(normalized_data, 'Normalized Stock Price Comparison (2015 - Present)')
    plt.ylabel('Normalized Price (Starting at 100)')
    plt.show()

if __name__ == "__main__":
    main()
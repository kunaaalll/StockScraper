import pandas as pd
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# Stock names
stock = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META']

# Download last one year data of any 5 stocks from yahoo finance
data = yf.download(stock, start='2024-01-01', end='2025-01-01', group_by='ticker')
# Ensure that the date column is correctly parsed and formatted
data.index = pd.to_datetime(data.index)
print(data.head())
print(data.columns)
for s in stock:
    try:
        # Check if the stock data is available
        if s in data.columns.levels[0]:
            stock_data = data[s]
            if 'Adj Close' in stock_data.columns:
                adj_close = stock_data['Adj Close']
            else:
                print(f"The 'Adj Close' column is missing from the data for {s}.")
                # Fallback to 'Close' column if 'Adj Close' is not available
                if 'Close' in stock_data.columns:
                    adj_close = stock_data['Close']
                else:
                    print(f"Neither 'Adj Close' nor 'Close' columns are available in the data for {s}.")
                    continue  # Skip this stock if no relevant columns are available

            # Calculate daily returns in % and 10 days and 30 days moving average of returns
            stock_data.loc[:, 'daily_returns'] = adj_close.pct_change()
            stock_data.loc[:, '10_days_moving_avg'] = stock_data['daily_returns'].rolling(10).mean()
            stock_data.loc[:, '30_days_moving_avg'] = stock_data['daily_returns'].rolling(30).mean()

            # Fill missing values in moving averages with NaN
            stock_data['10_days_moving_avg'].fillna(method='bfill', inplace=True)
            stock_data['30_days_moving_avg'].fillna(method='bfill', inplace=True)

            # Save the data in a csv file
            stock_data.to_csv(f'{s}_23020241054_KanishkaDwivedi.csv')

            # Generate candlestick chart for the stock
            mpf.plot(stock_data, type='candle', volume=True, style='charles', title=s)

        else:
            print(f"No data available for {s}.")

    except KeyError as e:
        print(f"Error processing data for {s}: {e}")

# Generate line chart for daily returns and 10 days and 30 days moving average of returns
for s in stock:
    if 'daily_returns' in data[s].columns:
        data[s][['daily_returns', '10_days_moving_avg', '30_days_moving_avg']].plot()
        plt.title(s)
        plt.savefig(f'{s}_stock_chart.png')
        plt.show()

# Display the data
print(data)

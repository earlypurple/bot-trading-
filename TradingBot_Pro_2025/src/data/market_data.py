import yfinance as yf
import pandas as pd

def get_historical_data(ticker, start_date, end_date):
    """
    Fetches historical market data for a given ticker from Yahoo Finance.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL').
        start_date (str): The start date for the data (e.g., '2020-01-01').
        end_date (str): The end date for the data (e.g., '2023-01-01').

    Returns:
        pd.DataFrame: A pandas DataFrame containing the historical data,
                      or None if the download fails.
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            print(f"No data found for ticker {ticker} from {start_date} to {end_date}.")
            return None
        return data
    except Exception as e:
        print(f"An error occurred while downloading data for {ticker}: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    ticker = 'AAPL'
    start_date = '2021-01-01'
    end_date = '2023-01-01'

    aapl_data = get_historical_data(ticker, start_date, end_date)

    if aapl_data is not None:
        print(f"Successfully downloaded data for {ticker}.")
        print("First 5 rows:")
        print(aapl_data.head())
        print("\nLast 5 rows:")
        print(aapl_data.tail())

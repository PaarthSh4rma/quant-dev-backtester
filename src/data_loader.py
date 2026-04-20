from pathlib import Path
from typing import Optional

import pandas as pd
import yfinance as yf


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flatten yfinance MultiIndex columns into simple lowercase column names.
    Example:
    ('Close', 'AAPL') -> 'close'
    ('Date', '') -> 'date'
    """
    if isinstance(df.columns, pd.MultiIndex):
        flattened = []
        for col in df.columns:
            base = col[0] if col[0] else col[1]
            flattened.append(str(base).strip().lower().replace(" ", "_"))
        df.columns = flattened
    else:
        df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]

    return df


def download_stock_data(ticker: str, start: str, end: Optional[str] = None) -> pd.DataFrame:
    """
    Download historical stock data for a ticker.
    """
    df = yf.download(ticker, start=start, end=end, auto_adjust=False, progress=False)

    if df.empty:
        raise ValueError(f"No data returned for ticker '{ticker}'.")

    df = df.reset_index()
    df = normalize_columns(df)

    expected_columns = ["date", "open", "high", "low", "close", "adj_close", "volume"]
    missing = [col for col in expected_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}. Got: {df.columns.tolist()}")

    return df


def save_to_csv(df: pd.DataFrame, ticker: str) -> Path:
    """
    Save the downloaded dataframe to a CSV file.
    """
    output_path = DATA_DIR / f"{ticker.lower()}_historical_data.csv"
    df.to_csv(output_path, index=False)
    return output_path


def main() -> None:
    ticker = "AAPL"
    start_date = "2020-01-01"

    print(f"Downloading data for {ticker}...")
    df = download_stock_data(ticker=ticker, start=start_date)

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    output_path = save_to_csv(df, ticker)
    print(f"\nSaved CSV to: {output_path}")


if __name__ == "__main__":
    main()
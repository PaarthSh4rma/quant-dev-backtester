from pathlib import Path
from typing import Optional

import pandas as pd
import yfinance as yf


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
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


def save_raw_data(df: pd.DataFrame, raw_data_file: Path) -> None:
    raw_data_file.parent.mkdir(exist_ok=True)
    df.to_csv(raw_data_file, index=False)
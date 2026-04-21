import pandas as pd

from config import RAW_DATA_FILE, SIGNALS_FILE, SMA_WINDOW


def load_price_data() -> pd.DataFrame:
    df = pd.read_csv(RAW_DATA_FILE)

    if "date" not in df.columns or "close" not in df.columns:
        raise ValueError(f"Expected 'date' and 'close' columns. Got: {df.columns.tolist()}")

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df


def add_moving_average(df: pd.DataFrame, window: int = SMA_WINDOW) -> pd.DataFrame:
    df = df.copy()
    df[f"sma_{window}"] = df["close"].rolling(window=window).mean()
    return df


def add_signal(df: pd.DataFrame, ma_column: str = f"sma_{SMA_WINDOW}") -> pd.DataFrame:
    df = df.copy()
    df["signal"] = ((df["close"] > df[ma_column]) & df[ma_column].notna()).astype(int)
    return df


def save_signals(df: pd.DataFrame) -> None:
    df.to_csv(SIGNALS_FILE, index=False)
import pandas as pd

from config import (
    RAW_DATA_FILE,
    SIGNALS_FILE,
    SMA_WINDOW,
    SHORT_SMA_WINDOW,
    LONG_SMA_WINDOW,
)


def load_price_data() -> pd.DataFrame:
    df = pd.read_csv(RAW_DATA_FILE)

    if "date" not in df.columns or "close" not in df.columns:
        raise ValueError(f"Expected 'date' and 'close' columns. Got: {df.columns.tolist()}")

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df


def add_moving_average(df: pd.DataFrame, window: int) -> pd.DataFrame:
    df = df.copy()
    df[f"sma_{window}"] = df["close"].rolling(window=window).mean()
    return df


def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for window in [SMA_WINDOW, SHORT_SMA_WINDOW, LONG_SMA_WINDOW]:
        col_name = f"sma_{window}"
        if col_name not in df.columns:
            df[col_name] = df["close"].rolling(window=window).mean()
    return df


def add_sma_trend_signal(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    ma_column = f"sma_{SMA_WINDOW}"
    df["signal_sma_trend"] = (
        (df["close"] > df[ma_column]) & df[ma_column].notna()
    ).astype(int)
    return df


def add_sma_crossover_signal(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    short_col = f"sma_{SHORT_SMA_WINDOW}"
    long_col = f"sma_{LONG_SMA_WINDOW}"

    df["signal_sma_crossover"] = (
        (df[short_col] > df[long_col])
        & df[short_col].notna()
        & df[long_col].notna()
    ).astype(int)
    return df


def build_signals(df: pd.DataFrame) -> pd.DataFrame:
    df = add_all_indicators(df)
    df = add_sma_trend_signal(df)
    df = add_sma_crossover_signal(df)
    return df


def select_signal(df: pd.DataFrame, strategy_name: str) -> pd.DataFrame:
    df = df.copy()

    signal_map = {
        "sma_trend": "signal_sma_trend",
        "sma_crossover": "signal_sma_crossover",
    }

    if strategy_name not in signal_map:
        raise ValueError(
            f"Unknown strategy '{strategy_name}'. Valid options: {list(signal_map.keys())}"
        )

    selected_signal = signal_map[strategy_name]
    df["signal"] = df[selected_signal]

    return df


def save_signals(df: pd.DataFrame) -> None:
    df.to_csv(SIGNALS_FILE, index=False)
from pathlib import Path
import pandas as pd


def load_price_data(raw_data_file: Path) -> pd.DataFrame:
    df = pd.read_csv(raw_data_file)

    if "date" not in df.columns or "close" not in df.columns:
        raise ValueError(f"Expected 'date' and 'close' columns. Got: {df.columns.tolist()}")

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df


def add_moving_average(df: pd.DataFrame, window: int) -> pd.DataFrame:
    df = df.copy()
    df[f"sma_{window}"] = df["close"].rolling(window=window).mean()
    return df


def add_all_indicators(
    df: pd.DataFrame,
    sma_window: int,
    short_window: int,
    long_window: int,
) -> pd.DataFrame:
    df = df.copy()

    for window in sorted(set([sma_window, short_window, long_window])):
        col_name = f"sma_{window}"
        if col_name not in df.columns:
            df[col_name] = df["close"].rolling(window=window).mean()

    return df


def add_sma_trend_signal(df: pd.DataFrame, sma_window: int) -> pd.DataFrame:
    df = df.copy()
    ma_column = f"sma_{sma_window}"

    df["signal_sma_trend"] = (
        (df["close"] > df[ma_column]) & df[ma_column].notna()
    ).astype(int)

    return df


def add_sma_crossover_signal(
    df: pd.DataFrame,
    short_window: int,
    long_window: int,
) -> pd.DataFrame:
    df = df.copy()
    short_col = f"sma_{short_window}"
    long_col = f"sma_{long_window}"

    df["signal_sma_crossover"] = (
        (df[short_col] > df[long_col])
        & df[short_col].notna()
        & df[long_col].notna()
    ).astype(int)

    return df


def build_signals(
    df: pd.DataFrame,
    sma_window: int,
    short_window: int,
    long_window: int,
) -> pd.DataFrame:
    df = add_all_indicators(
        df,
        sma_window=sma_window,
        short_window=short_window,
        long_window=long_window,
    )
    df = add_sma_trend_signal(df, sma_window=sma_window)
    df = add_sma_crossover_signal(
        df,
        short_window=short_window,
        long_window=long_window,
    )
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

    df["signal"] = df[signal_map[strategy_name]]
    return df


def save_signals(df: pd.DataFrame, signals_file: Path) -> None:
    df.to_csv(signals_file, index=False)
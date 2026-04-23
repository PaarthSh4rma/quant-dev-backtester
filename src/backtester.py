from pathlib import Path
import pandas as pd


def load_signal_data(signals_file: Path) -> pd.DataFrame:
    df = pd.read_csv(signals_file)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df


def compute_returns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["returns"] = df["close"].pct_change()
    return df


def compute_positions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["position"] = df["signal"].shift(1).fillna(0)
    return df


def compute_strategy_returns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["strategy_returns"] = df["position"] * df["returns"]
    return df


def compute_cumulative_returns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["cum_market"] = (1 + df["returns"]).cumprod()
    df["cum_strategy"] = (1 + df["strategy_returns"]).cumprod()
    return df


def save_backtest(df: pd.DataFrame, backtest_file: Path) -> None:
    backtest_file.parent.mkdir(exist_ok=True)
    df.to_csv(backtest_file, index=False)
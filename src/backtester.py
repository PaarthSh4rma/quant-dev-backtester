from pathlib import Path
import pandas as pd


DATA_DIR = Path("data")
INPUT_FILE = DATA_DIR / "aapl_signals.csv"
OUTPUT_FILE = DATA_DIR / "aapl_backtest.csv"


def load_data(file_path: Path) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    return df


def compute_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute daily returns.
    """
    df = df.copy()
    df["returns"] = df["close"].pct_change()
    return df


def compute_positions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Shift signal to avoid lookahead bias.
    """
    df = df.copy()
    df["position"] = df["signal"].shift(1)

    # First row will be NaN → assume no position
    df["position"] = df["position"].fillna(0)

    return df


def compute_strategy_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strategy returns = position * market returns
    """
    df = df.copy()
    df["strategy_returns"] = df["position"] * df["returns"]
    return df


def compute_cumulative_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute cumulative returns for both strategy and market.
    """
    df = df.copy()

    df["cum_market"] = (1 + df["returns"]).cumprod()
    df["cum_strategy"] = (1 + df["strategy_returns"]).cumprod()

    return df


def main() -> None:
    print(f"Loading data from {INPUT_FILE}...")
    df = load_data(INPUT_FILE)

    df = compute_returns(df)
    df = compute_positions(df)
    df = compute_strategy_returns(df)
    df = compute_cumulative_returns(df)

    print("\nPreview:")
    print(
        df[
            [
                "date",
                "close",
                "signal",
                "position",
                "returns",
                "strategy_returns",
                "cum_market",
                "cum_strategy",
            ]
        ].tail(10)
    )

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved backtest results to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
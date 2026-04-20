from pathlib import Path
import pandas as pd


DATA_DIR = Path("data")
INPUT_FILE = DATA_DIR / "aapl_historical_data.csv"
OUTPUT_FILE = DATA_DIR / "aapl_signals.csv"


def load_price_data(file_path: Path) -> pd.DataFrame:
    """
    Load historical price data from CSV.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Could not find file: {file_path}")

    df = pd.read_csv(file_path)

    if "date" not in df.columns or "close" not in df.columns:
        raise ValueError(
            f"Expected 'date' and 'close' columns. Got: {df.columns.tolist()}"
        )

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    return df


def add_moving_average(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Add a simple moving average column.
    """
    df = df.copy()
    df[f"sma_{window}"] = df["close"].rolling(window=window).mean()
    return df


def add_signal(df: pd.DataFrame, ma_column: str = "sma_20") -> pd.DataFrame:
    """
    Add a simple trading signal:
    1 when close > moving average, else 0.
    """
    df = df.copy()
    df["signal"] = (df["close"] > df[ma_column]).astype(int)
    return df


def save_output(df: pd.DataFrame, file_path: Path) -> None:
    """
    Save dataframe with signals to CSV.
    """
    df.to_csv(file_path, index=False)


def main() -> None:
    print(f"Loading data from {INPUT_FILE}...")
    df = load_price_data(INPUT_FILE)

    df = add_moving_average(df, window=20)
    df = add_signal(df, ma_column="sma_20")

    print("\nFirst 10 rows:")
    print(df[["date", "close", "sma_20", "signal"]].head(10))

    print("\nLast 10 rows:")
    print(df[["date", "close", "sma_20", "signal"]].tail(10))

    save_output(df, OUTPUT_FILE)
    print(f"\nSaved signal data to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
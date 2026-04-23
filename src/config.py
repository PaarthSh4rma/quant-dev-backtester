from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PLOTS_DIR = BASE_DIR / "plots"

DATA_DIR.mkdir(exist_ok=True)
PLOTS_DIR.mkdir(exist_ok=True)

TICKER = "AAPL"
START_DATE = "2020-01-01"

RAW_DATA_FILE = DATA_DIR / f"{TICKER.lower()}_historical_data.csv"
SIGNALS_FILE = DATA_DIR / f"{TICKER.lower()}_signals.csv"
BACKTEST_FILE = DATA_DIR / f"{TICKER.lower()}_backtest.csv"

TRADING_DAYS_PER_YEAR = 252
RISK_FREE_RATE = 0.0

SMA_WINDOW = 20
SHORT_SMA_WINDOW = 10
LONG_SMA_WINDOW = 50

STRATEGY_NAME = "sma_crossover"  # options: "sma_trend", "sma_crossover"
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PLOTS_DIR = BASE_DIR / "plots"

DATA_DIR.mkdir(exist_ok=True)
PLOTS_DIR.mkdir(exist_ok=True)

DEFAULT_TICKER = "AAPL"
DEFAULT_START_DATE = "2020-01-01"

TRADING_DAYS_PER_YEAR = 252
RISK_FREE_RATE = 0.0

DEFAULT_SMA_WINDOW = 20
DEFAULT_SHORT_SMA_WINDOW = 10
DEFAULT_LONG_SMA_WINDOW = 50
DEFAULT_STRATEGY_NAME = "sma_trend"
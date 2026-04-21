import numpy as np
import pandas as pd

from config import BACKTEST_FILE, RISK_FREE_RATE, TRADING_DAYS_PER_YEAR


def load_backtest_data() -> pd.DataFrame:
    df = pd.read_csv(BACKTEST_FILE)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df


def compute_drawdown(cumulative_returns: pd.Series) -> pd.Series:
    running_max = cumulative_returns.cummax()
    return cumulative_returns / running_max - 1.0


def total_return(cumulative_returns: pd.Series) -> float:
    clean = cumulative_returns.dropna()
    return clean.iloc[-1] - 1.0


def annualized_return(daily_returns: pd.Series) -> float:
    clean = daily_returns.dropna()
    if len(clean) == 0:
        return np.nan

    cumulative_growth = (1 + clean).prod()
    n_days = len(clean)
    return cumulative_growth ** (TRADING_DAYS_PER_YEAR / n_days) - 1.0


def annualized_volatility(daily_returns: pd.Series) -> float:
    clean = daily_returns.dropna()
    if len(clean) == 0:
        return np.nan
    return clean.std() * np.sqrt(TRADING_DAYS_PER_YEAR)


def sharpe_ratio(daily_returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    clean = daily_returns.dropna()
    if len(clean) == 0:
        return np.nan

    excess_daily_return = clean.mean() - (risk_free_rate / TRADING_DAYS_PER_YEAR)
    daily_vol = clean.std()

    if daily_vol == 0:
        return np.nan

    return (excess_daily_return / daily_vol) * np.sqrt(TRADING_DAYS_PER_YEAR)


def max_drawdown(cumulative_returns: pd.Series) -> float:
    drawdown = compute_drawdown(cumulative_returns)
    return drawdown.min()


def calculate_metrics(daily_returns: pd.Series, cumulative_returns: pd.Series, label: str) -> dict:
    return {
        "label": label,
        "total_return": total_return(cumulative_returns),
        "annualized_return": annualized_return(daily_returns),
        "annualized_volatility": annualized_volatility(daily_returns),
        "sharpe_ratio": sharpe_ratio(daily_returns, risk_free_rate=RISK_FREE_RATE),
        "max_drawdown": max_drawdown(cumulative_returns),
    }


def print_metrics_table(metrics: list[dict]) -> None:
    def format_pct(value: float) -> str:
        return f"{value:.2%}"

    def format_num(value: float) -> str:
        return f"{value:.4f}"

    print("\nPerformance Summary")
    print("-" * 95)
    print(
        f"{'Strategy':<15}"
        f"{'Total Return':<18}"
        f"{'Annual Return':<18}"
        f"{'Annual Vol':<15}"
        f"{'Sharpe':<12}"
        f"{'Max Drawdown':<15}"
    )
    print("-" * 95)

    for m in metrics:
        print(
            f"{m['label']:<15}"
            f"{format_pct(m['total_return']):<18}"
            f"{format_pct(m['annualized_return']):<18}"
            f"{format_pct(m['annualized_volatility']):<15}"
            f"{format_num(m['sharpe_ratio']):<12}"
            f"{format_pct(m['max_drawdown']):<15}"
        )

    print("-" * 95)
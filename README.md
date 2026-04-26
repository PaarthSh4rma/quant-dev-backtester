# Quant Dev Backtester

A modular quantitative research and backtesting framework built in Python for evaluating systematic trading strategies across multiple assets.
---

## Overview

This project implements a **configurable, modular backtesting engine** designed to simulate and evaluate rule-based trading strategies on historical market data.

It is structured to resemble a lightweight quant research pipeline, with clear separation between:

- Data ingestion
- Feature engineering
- Strategy logic
- Backtesting engine
- Performance evaluation
- Visualization

---

## Features
- Market data ingestion via yFinance
- Modular strategy design
- CLI-based parameter configuration
- Backtesting with position simulation
- Performance metrics (Sharpe, volatility, drawdown)
- Visualization (price, returns, drawdowns)
- Parameter sweep + strategy optimization
- Cross-asset evaluation (AAPL, GOOG, MSFT, SPY)

---

## Strategies

### 1. SMA Trend Strategy
- Long when: `Close > SMA(N)`
- Otherwise: out of market
- Simple trend-following logic
- Captures directional momentum
- Lower turnover, smoother equity curve

### 2. SMA Crossover Strategy
- Long when: `SMA(short) > SMA(long)`
- Otherwise: out of market
- Filters noise using dual moving averages
- More conservative, slower signal

---

## Research Findings
### 1. Strategy Performance is Asset-Dependent

Different assets exhibit different levels of exploitable structure:

- GOOG → strongest performance (Sharpe ≈ 1.15)
- AAPL → consistent trend behavior
- SPY → stable but lower alpha
- MSFT → weaker signal structure


### 2. Optimal Parameters Vary by Asset

| Asset | Best Strategy | Key Parameters   |
| ----- | ------------- | ---------------- |
| AAPL  | SMA Trend     | 20-day           |
| GOOG  | SMA Crossover | (20, 100)        |
| SPY   | SMA Trend     | 100-day          |
| MSFT  | Weak signal   | No clear optimum |


### 3. Longer Horizons Improve Stability

Across multiple assets:

- Increasing the long window reduces noise
- Leads to higher Sharpe ratios
- Reduces overtrading

  
### 4. Risk-Return Tradeoff
- Trend strategies → higher Sharpe, smoother drawdowns
- Crossover strategies → lower exposure, but miss strong rallies
---

## Limitations
- Results are in-sample only
- No transaction costs or slippage
- No walk-forward validation

* Future work should include out-of-sample testing to avoid overfitting.
---

## Project Structure
```text
src/
├── config.py           # Configuration values
├── data_loader.py      # Market data ingestion
├── strategy.py         # Strategy logic
├── backtester.py       # Core backtesting engine
├── metrics.py          # Performance metrics
├── visualize.py        # Plotting and analysis
├── parameter_sweep.py  # Strategy optimization
└── run_pipeline.py     # CLI entry point
```

---

## How to Run

### 1. Clone repo

```
git clone https://github.com/YOUR_USERNAME/quant-dev-backtester.git
cd quant-dev-backtester
```

### 2. Create environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### 3. Run pipeline
#### Default Run
```
python src/run_pipeline.py
```

#### SMA Trend strategy
```
python src/run_pipeline.py --strategy sma_trend --sma-window 20
```

#### SMA Crossover strategy
```
python src/run_pipeline.py --strategy sma_crossover --short-window 5 --long-window 30
```

#### Different stock
```
python src/run_pipeline.py --ticker MSFT --strategy sma_trend --sma-window 30
```

---
## Output

Running the pipeline will:

- Download historical data
- Generate signals
- Run backtest
- Compute metrics
- Save plots:
  - price vs SMA
  - cumulative returns
  - drawdowns

---

## Tech Stack
Python
Pandas / NumPy
Matplotlib
yFinance

---

## Motivation

This project was built to:

- Develop quantitative trading intuition
- Practice building data-driven systems and pipelines
- Satisfy Curiosity about the Quant Field

---

## Next Steps

- Transaction cost modeling
- Position sizing and portfolio allocation
- Walk-forward validation
- Additional strategies (momentum, mean reversion)
- Multi-asset portfolio backtesting

---
## Author
Paarth Sharma
Software Engineer / Quant Dev

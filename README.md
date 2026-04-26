# Quant Dev Backtester

A modular quantitative trading backtesting engine built in Python to evaluate systematic trading strategies on historical market data.

---

## Overview

This project implements a **modular and configurable quantitative trading backtesting engine** in Python.

It supports:

- Market data ingestion via yFinance
- Feature engineering (technical indicators)
- Multiple strategy implementations
- Configurable parameters via CLI
- Backtesting and portfolio simulation
- Performance evaluation (Sharpe, drawdown, volatility)
- Visualization of results

The system is designed to behave like a lightweight research framework for testing trading strategies.

---

## Strategies

### 1. SMA Trend Strategy
- Long when: `Close > SMA(N)`
- Otherwise: out of market
- Simple trend-following logic

### 2. SMA Crossover Strategy
- Long when: `SMA(short) > SMA(long)`
- Otherwise: out of market
- More conservative, slower signal

---

### Key Insight

Different strategies produce **tradeoffs between return and risk**:

- Trend strategy: higher Sharpe, smoother performance
- Crossover: lower exposure, but may miss strong rallies

---

## Project Structure
```
src/
├── config.py           # Default configuration values
├── data_loader.py      # Market data ingestion
├── strategy.py         # Strategy definitions (trend, crossover)
├── backtester.py       # Backtesting engine
├── metrics.py          # Performance evaluation
├── visualize.py        # Plotting and analysis
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

### Multi-Asset Insight

Strategy performance varies significantly across assets.  
For example:

- AAPL: SMA trend (20) performed best  
- GOOG: SMA crossover (20,100) achieved highest Sharpe (~1.15)  
- SPY: Longer-term trend strategies were more effective  

This highlights the importance of cross-asset validation in strategy development.

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
- Practice building data-driven systems
- Satisfy Curiosity about the Quant Field

---

## 🔜 Next Steps

- Transaction cost modeling
- Position sizing and portfolio allocation
- Additional strategies (momentum, mean reversion)

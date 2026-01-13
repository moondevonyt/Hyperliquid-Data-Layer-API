# Moon Dev API Examples

**Developer Porn Dashboard Collection** - Beautiful, colorful examples showing how to use every endpoint of the Moon Dev API.

## What's Inside

Each file in this folder is a standalone Python script that demonstrates one section of the API with a gorgeous terminal dashboard output. Run any script to see live data beautifully formatted.

| File | API Section | What You'll See |
|------|-------------|-----------------|
| `01_liquidations.py` | Hyperliquid Liqs | Real-time liquidation heatmaps, top liqs, long/short breakdowns |
| `02_positions.py` | Large Positions | Whale positions near liquidation, per-symbol support (148 symbols!) |
| `03_whales.py` | Whale Activity | Whale addresses, recent trades, smart money moves |
| `04_events.py` | Blockchain Events | Live event stream, transfers, swaps, deposits |
| `05_contracts.py` | Contract Registry | High-value contracts, activity tracking |
| `06_ticks.py` | Tick Data | Live prices, historical charts, volatility |
| `07_orderflow.py` | Order Flow | Buy/sell pressure, cumulative delta, imbalance |
| `08_trades.py` | Recent Trades | Trade stream, large trades, volume analysis |
| `09_smart_money.py` | Smart Money | Top performers, PnL rankings, trading signals |
| `10_user_positions.py` | User Positions | Get all positions for any Hyperliquid wallet |
| `11_user_fills.py` | Trade History | Historical fills, PnL analysis, win/loss streaks |
| `12_hlp_positions.py` | HLP Dashboard | All 7 HLP strategies, trades, liquidators, deltas |
| `13_binance_liquidations.py` | Binance Liqs | Binance Futures liquidations, stats, top events |
| `14_multi_liquidations.py` | Multi-Exchange | Combined liqs from Hyperliquid, Binance, Bybit, OKX |
| `15_buyers.py` | Buyer Watcher | $5k+ buyers on HYPE/SOL/XRP/ETH (buyers only!) |
| `16_depositors.py` | Depositors | All Hyperliquid depositors - every address that bridged |
| `17_hlp_sentiment.py` | HLP Sentiment | THE BIG ONE! Z-scores and retail positioning signals |
| `18_hlp_analytics.py` | HLP Analytics | Liquidator status, market maker, timing, correlation |

---

## Quick Start Guide

### Step 1: Install Dependencies

```bash
# Make sure you have the required packages
pip install requests rich python-dotenv
```

### Step 2: Set Your API Key

Create a `.env` file in the project root (or api_examples folder):

```bash
# Option A: Create .env file manually
echo "MOONDEV_API_KEY=your_key_here" > .env

# Option B: Or edit .env directly
nano .env
# Add: MOONDEV_API_KEY=your_api_key_from_moondev_com
```

### Step 3: Run Any Dashboard

```bash
# From the project root directory:
python api_examples/01_liquidations.py
python api_examples/07_orderflow.py
python api_examples/09_smart_money.py
python api_examples/11_user_fills.py
python api_examples/12_hlp_positions.py

# Or run the main API test suite:
python api.py
```

---

## Complete API Reference

### Base URL
```
https://api.moondev.com
```

### Authentication

Every request (except /health) requires an API key:

```python
# Method 1: Header (RECOMMENDED)
headers = {'X-API-Key': 'YOUR_API_KEY'}
response = requests.get('https://api.moondev.com/api/trades.json', headers=headers)

# Method 2: Query parameter
response = requests.get('https://api.moondev.com/api/trades.json?api_key=YOUR_API_KEY')
```

### Rate Limits
- **3,600 requests per minute** (60 req/sec)
- Data updates every 30 seconds
- 60-day data retention

---

## Available Endpoints

### CORE ENDPOINTS

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Service health check (no auth required) |
| `GET /api/liquidations/{timeframe}.json` | Hyperliquid liquidation data (10m, 1h, 4h, 12h, 24h, 2d, 7d, 14d, 30d) |
| `GET /api/liquidations/stats.json` | Aggregated Hyperliquid liquidation statistics |
| `GET /api/positions.json` | Top 50 longs/shorts across ALL symbols (updates every 1s) |
| `GET /api/positions/all.json` | All 148 symbols with top 50 positions each (500KB, updates every 60s) |
| `GET /api/whales.json` | Recent whale trades ($25k+, buys & sells) |
| `GET /api/buyers.json` | Recent buyers only ($5k+, HYPE/SOL/XRP/ETH) |
| `GET /api/depositors.json` | All Hyperliquid depositors (canonical address list) |
| `GET /api/whale_addresses.txt` | Plain text whale address list |
| `GET /api/events.json` | Real-time blockchain events |
| `GET /api/contracts.json` | Contract registry with metadata |

### MULTI-EXCHANGE LIQUIDATIONS

| Endpoint | Description |
|----------|-------------|
| `GET /api/all_liquidations/{timeframe}.json` | Combined liqs from ALL exchanges |
| `GET /api/all_liquidations/stats.json` | Combined stats with exchange breakdown |
| `GET /api/binance_liquidations/{timeframe}.json` | Binance Futures liquidations |
| `GET /api/bybit_liquidations/{timeframe}.json` | Bybit liquidations |
| `GET /api/okx_liquidations/{timeframe}.json` | OKX liquidations |

**Timeframes:** 10m, 1h, 4h, 12h, 24h, 2d, 7d, 14d, 30d

### TICK DATA

| Endpoint | Description |
|----------|-------------|
| `GET /api/ticks/stats.json` | Collection stats and summary |
| `GET /api/ticks/latest.json` | Current prices for all symbols |
| `GET /api/ticks/{symbol}_{timeframe}.json` | Historical ticks |

**Symbols:** btc, eth, hype, sol, xrp
**Timeframes:** 10m, 1h, 4h, 24h, 7d

### ORDER FLOW & TRADES

| Endpoint | Description |
|----------|-------------|
| `GET /api/trades.json` | Recent 500 trades (real-time) |
| `GET /api/large_trades.json` | Large trades >$100k (24h) |
| `GET /api/orderflow.json` | Order flow imbalance by timeframe + per coin |
| `GET /api/orderflow/stats.json` | Service stats (uptime, trades/sec) |
| `GET /api/imbalance/{timeframe}.json` | Buy/sell imbalance (5m, 15m, 1h, 4h, 24h) |

### SMART MONEY

| Endpoint | Description |
|----------|-------------|
| `GET /api/smart_money/rankings.json` | Top 100 smart + Bottom 100 dumb money |
| `GET /api/smart_money/leaderboard.json` | Top 50 performers with details |
| `GET /api/smart_money/signals_{timeframe}.json` | Trading signals (10m, 1h, 24h) |

### USER DATA (Moon Dev Local Node)

| Endpoint | Description |
|----------|-------------|
| `GET /api/user/{address}/positions` | Current positions for any wallet |
| `GET /api/user/{address}/fills?limit=N` | Historical fills (default: 100, max: 2000, -1 for ALL) |

### HLP (HYPERLIQUIDITY PROVIDER) - Complete Reverse Engineering

| Endpoint | Description |
|----------|-------------|
| `GET /api/hlp/positions` | All 7 HLP strategy positions + combined net exposure |
| `GET /api/hlp/positions?include_strategies=false` | Summary only (faster response) |
| `GET /api/hlp/trades?limit=N` | Historical HLP trade fills (5,000+ collected) |
| `GET /api/hlp/trades/stats` | Trade volume/fee statistics |
| `GET /api/hlp/positions/history?hours=N` | Position snapshots over time |
| `GET /api/hlp/liquidators` | Liquidator activation events |
| `GET /api/hlp/deltas?hours=N` | Net exposure changes over time |
| `GET /api/hlp/sentiment` | **THE BIG ONE!** Z-scores and retail positioning signals |
| `GET /api/hlp/liquidators/status` | Real-time liquidator status (active/idle + PnL) |
| `GET /api/hlp/market-maker` | Strategy B tracker for BTC/ETH/SOL |
| `GET /api/hlp/timing` | Hourly/session profitability analysis |
| `GET /api/hlp/correlation` | Delta-price correlation by coin |

---

## Python SDK Usage

The `api.py` file provides a complete Python SDK:

```python
from api import MoonDevAPI

# Initialize (reads MOONDEV_API_KEY from .env automatically)
api = MoonDevAPI()

# Or pass key directly
api = MoonDevAPI(api_key="your_key_here")

# === HYPERLIQUID LIQUIDATIONS ===
liqs = api.get_liquidations("1h")           # 10m, 1h, 4h, 12h, 24h, 2d, 7d, 14d, 30d
stats = api.get_liquidation_stats()

# === MULTI-EXCHANGE LIQUIDATIONS ===
all_stats = api.get_all_liquidation_stats()          # Combined stats all exchanges
all_liqs = api.get_all_liquidations("1h")            # Combined liquidations
binance_liqs = api.get_binance_liquidations("1h")    # Binance only
bybit_liqs = api.get_bybit_liquidations("1h")        # Bybit only
okx_liqs = api.get_okx_liquidations("1h")            # OKX only

# === POSITIONS & WHALES ===
positions = api.get_positions()              # Top 50 positions across ALL symbols (fast, 1s updates)
all_positions = api.get_all_positions()      # All 148 symbols (500KB, 60s updates)
btc_data = all_positions['symbols']['BTC']   # Filter to BTC ($1.9B)
hype_data = all_positions['symbols']['HYPE'] # Filter to HYPE ($528M)
whales = api.get_whales()                    # Recent whale trades ($25k+, buys & sells)
buyers = api.get_buyers()                    # Recent buyers only ($5k+, HYPE/SOL/XRP/ETH)
depositors = api.get_depositors()            # All Hyperliquid depositors (canonical list)
whale_addrs = api.get_whale_addresses()      # List of whale addresses

# === EVENTS & CONTRACTS ===
events = api.get_events()                    # Blockchain events
contracts = api.get_contracts()              # Contract registry

# === TICK DATA ===
tick_stats = api.get_tick_stats()
latest = api.get_tick_latest()               # Current prices
btc_ticks = api.get_ticks("btc", "1h")       # Historical ticks

# === ORDER FLOW & TRADES ===
trades = api.get_trades()                    # Recent 500 trades
large = api.get_large_trades()               # Trades >$100k
orderflow = api.get_orderflow()
imbalance = api.get_imbalance("1h")          # 5m, 15m, 1h, 4h, 24h

# === SMART MONEY ===
rankings = api.get_smart_money_rankings()
leaderboard = api.get_smart_money_leaderboard()
signals = api.get_smart_money_signals("1h")  # 10m, 1h, 24h

# === USER DATA (Local Node - FAST!) ===
positions = api.get_user_positions("0x...")          # Via Hyperliquid API
positions_api = api.get_user_positions_api("0x...")  # Via Moon Dev API
fills = api.get_user_fills("0x...", limit=100)       # Historical fills
fills_all = api.get_user_fills("0x...", limit=-1)   # ALL fills

# === HLP (HYPERLIQUIDITY PROVIDER) ===
hlp = api.get_hlp_positions()                        # Full details
hlp_summary = api.get_hlp_positions(include_strategies=False)  # Summary only
hlp_trades = api.get_hlp_trades(limit=100)           # Historical trades
hlp_trade_stats = api.get_hlp_trade_stats()          # Volume/fee stats
hlp_history = api.get_hlp_position_history(hours=24) # Position snapshots
hlp_liquidators = api.get_hlp_liquidators()          # Liquidator events
hlp_deltas = api.get_hlp_deltas(hours=24)            # Net exposure changes

# === HLP ADVANCED ANALYTICS (NEW!) ===
sentiment = api.get_hlp_sentiment()                  # THE BIG ONE! Z-scores & signals
liq_status = api.get_hlp_liquidator_status()         # Real-time liquidator status
market_maker = api.get_hlp_market_maker()            # Strategy B (BTC/ETH/SOL)
timing = api.get_hlp_timing()                        # Hourly/session profitability
correlation = api.get_hlp_correlation()              # Delta-price correlation
```

---

## Example Scripts Deep Dive

### 02_positions.py - Per-Symbol Position Dashboard

Track whale positions near liquidation for any of the 148 symbols on Hyperliquid:

```bash
# All symbols - top 50 across everything (fast, 1s updates)
python examples/02_positions.py

# Per-symbol filtering (uses /api/positions/all.json, filters client-side)
python examples/02_positions.py BTC          # 1,085 BTC positions ($1.9B total)
python examples/02_positions.py ETH          # 620 ETH positions ($2.7B total)
python examples/02_positions.py HYPE         # 386 HYPE positions ($528M total)
python examples/02_positions.py SOL          # 326 SOL positions ($469M total)
python examples/02_positions.py FARTCOIN     # 92 FARTCOIN positions ($56M total)

# List all 148 available symbols
python examples/02_positions.py --list
```

**Features:**
- Position statistics (total value, long/short breakdown)
- Top 50 positions sorted by liquidation distance (highest risk first)
- Risk analysis (critical <2%, high 2-5%, medium 5-10%)
- Top 5 whale positions by value
- Per-symbol filtering for any of 148 symbols (one API call gets all data)

### 11_user_fills.py - Trade History Dashboard

Analyze any wallet's complete trading history:

```bash
# Default wallet, last 100 fills
python api_examples/11_user_fills.py

# Custom wallet, last 500 fills
python api_examples/11_user_fills.py 0xYOUR_ADDRESS 500

# Get ALL fills for a wallet
python api_examples/11_user_fills.py 0xYOUR_ADDRESS -1
```

**Features:**
- Trade overview (volume, fees, date range)
- PnL summary with win rate
- Largest win/loss tracking
- Coin breakdown table
- Trade direction analysis (Open Long, Close Short, etc.)
- Win/loss streak analysis
- Color-coded trade history table

### 12_hlp_positions.py - Complete HLP Reverse Engineering Dashboard

Monitor Hyperliquid's native market-making protocol (~$210M+ AUM, 5,000+ trades):

```bash
# Full dashboard (all sections)
python api_examples/12_hlp_positions.py

# Positions only
python api_examples/12_hlp_positions.py --positions

# Trade history only
python api_examples/12_hlp_positions.py --trades

# Quick summary only
python api_examples/12_hlp_positions.py --summary
```

**Features:**
- Total account value across all 7 HLP strategies
- Combined NET exposure (longs - shorts across strategies)
- Which strategies are long vs short each coin
- Individual strategy breakdowns with positions
- Visual exposure charts and sparklines
- Trade history with 5,000+ fills tracked
- Trade statistics (volume, fees, breakdown by coin/strategy)
- Liquidator monitoring (activation events)
- Net exposure delta tracking over time
- Date range: Nov 3, 2025 to present

### 17_hlp_sentiment.py - THE BIG ONE! Retail Positioning

Track what retail is actually doing by watching HLP's counter-positioning:

```bash
python examples/17_hlp_sentiment.py
```

**Features:**
- Z-score indicator showing how extreme current positioning is
- Signal interpretation (short squeeze potential, long squeeze potential, neutral)
- Visual z-score bar (-3σ to +3σ)
- Historical context (mean, std dev, range)
- Action suggestions based on positioning

**Key Insight:**
- Z-Score > +2.0 = HLP unusually LONG = Retail heavily SHORT = Buy signal
- Z-Score < -2.0 = HLP unusually SHORT = Retail heavily LONG = Sell signal

### 18_hlp_analytics.py - HLP Advanced Analytics

Deep analytics on HLP operations:

```bash
python examples/18_hlp_analytics.py
```

**Features:**
- Liquidator status (active/idle, PnL tracking)
- Strategy B market maker positions (BTC/ETH/SOL)
- Timing analysis (best/worst hours, session profitability)
- Delta-price correlation by coin

---

## Get an API Key

Visit **https://moondev.com** to get your API key.

---

## Troubleshooting

### "No API key found"
Make sure your `.env` file exists and contains:
```
MOONDEV_API_KEY=your_actual_key_here
```

### "401 Unauthorized"
- Check your API key is correct
- Ensure you're using the header or query param correctly

### "Rate limit exceeded"
- You're making more than 3,600 requests/minute
- Add delays between requests or cache responses

### Import errors
```bash
pip install requests rich python-dotenv pandas
```

---

## Support

- **Issues:** https://github.com/moondevonyt/trading-bots/issues
- **Website:** https://moondev.com
- **API Status:** https://api.moondev.com/health

---

Built with love by Moon Dev

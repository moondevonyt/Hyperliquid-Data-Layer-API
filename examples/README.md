# Moon Dev API Examples

**Developer Porn Dashboard Collection** - Beautiful, colorful examples showing how to use every endpoint of the Moon Dev API.

## What's Inside

Each file in this folder is a standalone Python script that demonstrates one section of the API with a gorgeous terminal dashboard output. Run any script to see live data beautifully formatted.

| File | API Section | What You'll See |
|------|-------------|-----------------|
| `01_liquidations.py` | Hyperliquid Liqs | Real-time liquidation heatmaps, top liqs, long/short breakdowns |
| `02_positions.py` | Large Positions | Whale positions - crypto & HIP-3 SEPARATE! Per-symbol support (182 symbols!) |
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
| `19_market_data.py` | Market Data | All prices, orderbooks, account state - NO RATE LIMITS |
| `20_hip3_liquidations.py` | HIP3 Liqs | Stocks, Commodities, Indices & FX liquidations |
| `21_hip3_market_data.py` | HIP3 Data | OHLCV candles & tick data for 33 TradFi assets |
| `24_position_snapshots.py` | Position Snapshots | Positions near liquidation - squeeze signals |
| `25_ai_chat.py` | AI Chat | OpenAI-compatible AI API - drop-in replacement |
| `26_hip3_funding.py` | HIP3 Funding | Funding rates for stocks, commodities, ETFs across dexes |
| `27_bulk_binance_liquidations.py` | Bulk Binance Liqs | 35M+ historical Binance liquidations + live feed (Quant Elite) - coverage-aware download |
| `35_ohlcv_data.py` | OHLCV Data | Universe + single-symbol and multi-symbol bars from the new bars layer |
| `35_btc_tick_stream.py` | BTC Tick Stream | Live BTC tick tape with rolling stats and JSONL sink for bots |
| `34_polymarket_traders.py` | Polymarket Traders | **NEW!** Profitable Polymarket traders by 7-day P&L, discovery sources |
| `36_hl_direct_proxy.py` | HL Direct-Proxy | **NEW!** Drop-in `info.user_state` + `info.open_orders` — no 429s, local node w/ public fallback |
| `37_liquidation_totals.py` | Liquidation Totals | **NEW!** Long/short split across 6 rolling windows (5m→4h) + squeeze detector, per-exchange breakdown |

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
| `GET /api/positions.json` | Top 50 longs/shorts across ALL symbols - crypto + HIP-3 combined (updates every 1s) |
| `GET /api/positions/all.json` | All 182 symbols with top 50 positions each - crypto + HIP-3 combined (updates every 60s) |
| `GET /api/whales.json` | Recent whale trades ($25k+, buys & sells) |
| `GET /api/buyers.json` | Recent buyers only ($5k+, HYPE/SOL/XRP/ETH) |
| `GET /api/depositors.json` | All Hyperliquid depositors (canonical address list) |
| `GET /api/whale_addresses.txt` | Plain text whale address list |
| `GET /api/events.json` | Real-time blockchain events |
| `GET /api/contracts.json` | Contract registry with metadata |

### MULTI-EXCHANGE LIQUIDATIONS (29x Faster!)

Combines Hyperliquid, Binance, Bybit, OKX with Live + Archive architecture.

**Live Endpoints (30-second updates):**
| Endpoint | Description |
|----------|-------------|
| `GET /api/all_liquidations/10m.json` | Last 10 minutes |
| `GET /api/all_liquidations/1h.json` | Last 1 hour |
| `GET /api/all_liquidations/4h.json` | Last 4 hours |
| `GET /api/all_liquidations/12h.json` | Last 12 hours |
| `GET /api/all_liquidations/24h.json` | Last 24 hours |
| `GET /api/all_liquidations/2d.json` | Last 2 days |
| `GET /api/all_liquidations/5d.json` | Last 5 days |
| `GET /api/all_liquidations/stats.json` | Summary statistics |
| `GET /api/all_liquidations/totals.json` | Rolling totals w/ long/short split (5m, 15m, 1h, 2h, 3h, 4h + per-exchange, 20s updates) |

**Archive Endpoints (15-minute updates):**
| Endpoint | Description |
|----------|-------------|
| `GET /api/all_liquidations/7d.json` | Last 7 days |
| `GET /api/all_liquidations/14d.json` | Last 14 days |
| `GET /api/all_liquidations/30d.json` | Last 30 days |

**Per-Exchange Endpoints:**
| Endpoint | Description |
|----------|-------------|
| `GET /api/binance_liquidations/{timeframe}.json` | Binance Futures liquidations |
| `GET /api/bybit_liquidations/{timeframe}.json` | Bybit liquidations |
| `GET /api/okx_liquidations/{timeframe}.json` | OKX liquidations |

**Timeframes:** 10m, 1h, 4h, 12h, 24h, 2d, 5d (live) | 7d, 14d, 30d (archive)

### BULK BINANCE LIQUIDATIONS (Quant Elite)

Historical + live Binance Futures liquidations - 35 million+ records back to June 2024. See `27_bulk_binance_liquidations.py`.

| Endpoint | Description |
|----------|-------------|
| `GET /api/binance_liquidations/coverage.json` | Data coverage: segment boundaries + gap info (standard key works) |
| `GET /api/bulk/binance_liquidations` | Bulk paginated liquidation data (Quant Elite `_qe` key only) |

⚠️ **Data gap: 2026-04-23 → 2026-07-18 (permanent).** The dataset has two segments - a frozen historical archive (2024-06-04 → 2026-04-23) and the live feed (2026-07-18 onward) - with no data in between. Always hit the coverage endpoint first for exact, current boundaries.

**Selecting a segment:**
| Goal | Request |
|------|---------|
| Historical archive only | `?end=2026-04-23` |
| Live feed only | `?start=2026-07-18` |
| Everything | no date filter (gap rows simply don't exist) |

**Bulk params:** `start`, `end` (YYYY-MM-DD or unix ms), `symbol` (e.g. BTCUSDT), `side` (BUY = short liquidated, SELL = long liquidated), `min_usd`, `limit` (default 10k, max 100k), `offset`. Page with `limit` + `offset`; follow `next_offset` until `has_more` is false.

### HIP3 LIQUIDATIONS (Stocks, Commodities, Indices, FX)

| Endpoint | Description |
|----------|-------------|
| `GET /api/hip3_liquidations/{timeframe}.json` | HIP3 liquidations (traditional finance assets) |
| `GET /api/hip3_liquidations/stats.json` | HIP3 liquidation statistics with category breakdown |

**Timeframes:** 10m, 1h, 24h, 7d

**Categories tracked:**
- **Stocks:** TSLA, NVDA, AAPL, META, MSFT, GOOGL, AMZN, AMD, INTC, PLTR, COIN, HOOD, MSTR, ORCL, MU, NFLX, RIVN, BABA (~$100M+ OI)
- **Commodities:** GOLD, SILVER, COPPER, CL (Oil), NATGAS, URANIUM (~$125M OI)
- **Indices:** XYZ100 (Nasdaq proxy, ~$120M OI)
- **FX:** EUR, JPY (~$3M OI)

### HIP3 MARKET DATA (Multi-Dex: 51 symbols)

| Endpoint | Description |
|----------|-------------|
| `GET /api/hip3/meta` | All 51 symbols from all 4 dexes with current prices |
| `GET /api/hip3_ticks/stats.json` | Tick collector stats with dex breakdown |
| `GET /api/hip3_ticks/{dex}_{ticker}.json` | Individual tick data (e.g., xyz_tsla.json, hyna_btc.json) |

**Symbol Format:** `{dex}:{ticker}` (e.g., xyz:TSLA, hyna:BTC, km:US500)

**4 Dexes tracked (51 symbols):**
- **xyz (27):** Stocks, commodities, FX, indices (TSLA, NVDA, GOLD, SILVER, EUR, JPY, XYZ100)
- **flx (7):** Stocks, commodities, XMR (XMR, GOLD, SILVER, OIL)
- **hyna (12):** Crypto (BTC, ETH, HYPE, SOL, FARTCOIN, PUMP)
- **km (5):** US indices (US500, USTECH, SMALL2000)

**Categories:** Stocks (22) | Indices (4) | Commodities (4) | FX (2) | Crypto (12)

### HIP3 TICK DATA & CANDLES (NEW! — Top 10 by Volume)

Live tick collection for the top 10 HIP3 symbols by 24h volume across xyz, cash, and flx dexes. Volume ranking refreshes every 5 minutes. 30-day data retention. Candles are computed server-side from stored ticks.

| Endpoint | Description |
|----------|-------------|
| `GET /api/hip3/candles/symbols` | List all currently tracked HIP3 symbols with categories |
| `GET /api/hip3/ticks/{coin}` | Raw tick data for a HIP3 symbol |
| `GET /api/hip3/candles/{coin}` | OHLCV candles computed from ticks |
| `GET /api/hip3/price/{coin}` | Latest price for a single HIP3 symbol |
| `GET /api/hip3/prices` | All latest prices for all tracked HIP3 symbols |

**Symbol Lookup — three formats work:**
```bash
# Bare ticker (auto-resolves to correct dex)
/api/hip3/ticks/CL?duration=1h
/api/hip3/candles/SILVER?interval=5m
/api/hip3/price/NVDA

# Full dex:ticker format
/api/hip3/ticks/xyz:CL?duration=1h
/api/hip3/candles/cash:USA500?interval=1h

# Non-xyz dex
/api/hip3/ticks/cash:USA500?duration=1h
```

**Tick Parameters:**
| Param | Default | Description |
|-------|---------|-------------|
| `duration` | `1h` | Time window: `10m`, `1h`, `4h`, `24h`, `7d` |

**Candle Parameters:**
| Param | Default | Description |
|-------|---------|-------------|
| `interval` | `5m` | Candle size: `1m`, `5m`, `15m`, `1h`, `4h`, `1d` |
| `startTime` | auto | Start timestamp (Unix ms) |
| `endTime` | now | End timestamp (Unix ms) |

**Tick Response:**
```json
{
  "symbol": "cash:USA500",
  "category": "indices",
  "market_type": "HIP3",
  "duration": "1h",
  "tick_count": 1842,
  "latest_price": 6780.20,
  "ticks": [
    {"t": 1741611600500, "p": 6779.97, "sz": 2.5, "side": "B", "dt": "2026-03-10T13:12:33+00:00"}
  ]
}
```

**Candle Response:**
```json
{
  "t": 1741611600000, "T": 1741611899999,
  "s": "SILVER", "i": "5m",
  "o": "89.28", "h": "89.30", "l": "89.25", "c": "89.28",
  "v": "0", "n": 42
}
```

**All Prices Response:**
```json
{
  "generated_at": "2026-03-10T13:05:15+00:00",
  "market_type": "HIP3",
  "mode": "top_10_by_volume",
  "dexes": ["xyz", "cash", "flx"],
  "prices": {
    "cash:USA500": {"dex": "cash", "ticker": "USA500", "price": 6780.60, "category": "indices"},
    "cash:NVDA":   {"dex": "cash", "ticker": "NVDA",   "price": 182.02,  "category": "stocks"}
  }
}
```

**Key notes:**
- **Top 10 by volume** — symbol list refreshes every 5 min based on 24h notional volume
- **30-day retention** — historical data goes back up to 30 days
- **Multi-dex** — symbols span xyz, cash, and flx dexes
- **~500ms tick resolution** — polling interval for tick collection
- **Candles are server-computed** — built from stored tick data, not proxied from Hyperliquid
- **Tick size rollout** — newly ingested rows may include `sz` and `side`; older rows may be price-only
- **Volume transition** — OHLC is valid across history, while `v` is only complete where stored ticks include size

### TICK DATA

| Endpoint | Description |
|----------|-------------|
| `GET /api/ticks/stats.json` | Collection stats and summary |
| `GET /api/ticks/latest.json` | Current prices for all symbols |
| `GET /api/ticks/{symbol}_{timeframe}.json` | Historical ticks |

**Symbols:** btc, eth, hype, sol, xrp
**Timeframes:** 10m, 1h, 4h, 24h, 7d

Newly ingested tick rows may include:
- `p`: trade price
- `sz`: trade size
- `side`: trade side when provided upstream
- `t`: event timestamp

Historical rows collected before the size rollout may not contain `sz` or `side`.

### BARS & UNIVERSE

| Endpoint | Description |
|----------|-------------|
| `GET /api/universe` | Tracked symbol universe plus tick coverage metadata |
| `GET /api/bars` | Bulk OHLCV-style bars for multiple symbols |
| `GET /api/bars/{symbol}` | OHLCV-style bars for a single symbol |

Bar behavior:
- `o`, `h`, `l`, and `c` are built from stored tick history
- `v` is summed stored tick size where size exists
- `n` is the number of ticks or trades contributing to the bar
- Pre-rollout historical bars may have `v = 0` while still having valid OHLC

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
| `GET /api/hlp/funding/hip3` | HIP3 funding rates (stocks, commodities, ETFs) |

### POLYMARKET

| Endpoint | Description |
|----------|-------------|
| `GET /api/poly/profitable-traders` | Profitable Polymarket traders sorted by 7-day P&L ($300+ threshold) |
| `GET /api/poly/whales` | Live whale trade log — every Polymarket fill $1,000+ (newest first) |
| `GET /api/poly/whales/top-traders` | Whale leaderboard by wallet (volume, trade count, biggest trade) |
| `GET /api/poly/whales/top-markets` | Whale leaderboard by market (volume, unique whales, biggest trade) |
| `GET /api/poly/whales/daily` | Per-day rollup of whale activity (charting) |
| `GET /api/poly/whales/health` | Whale ingestion service status (no auth) |
| `GET /api/poly/health` | Polymarket service health check (no auth) |

**Access tiers:** Quant Elite (`_qe`) keys get the full result set. Standard keys are capped per endpoint (profitable-traders: top 25; whales: 250 rows; top-traders: 50).

### AI CHAT API

OpenAI-compatible drop-in replacement. No need for OpenAI or Anthropic API keys!

**Base URL:** `https://api.moondev.com/api/ai`

| Endpoint | Description |
|----------|-------------|
| `POST /api/ai/v1/chat/completions` | OpenAI-compatible chat completions |
| `POST /api/ai/chat` | Simple chat endpoint |
| `GET /api/ai/health` | Health check |

**OpenAI SDK Drop-in (just change base_url!):**
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.moondev.com/api/ai/v1",
    api_key="YOUR_MOONDEV_API_KEY"
)

response = client.chat.completions.create(
    model="moondev-ai",
    messages=[{"role": "user", "content": "What is Hyperliquid?"}],
    max_tokens=500
)
print(response.choices[0].message.content)
```

**cURL:**
```bash
curl -X POST "https://api.moondev.com/api/ai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_MOONDEV_API_KEY" \
  -d '{"messages":[{"role":"user","content":"Who is Moon Dev?"}],"max_tokens":500}'
```

Full docs: https://moondev.com/docs

### POSITION SNAPSHOTS

Track positions within 15% of liquidation on HyperLiquid. Updated every 1 minute.

| Endpoint | Description |
|----------|-------------|
| `GET /api/position_snapshots/symbol/{symbol}` | Historical snapshots for BTC, ETH, SOL, XRP, HYPE |
| `GET /api/position_snapshots/stats` | Aggregate statistics for all tracked symbols |

**Snapshot Parameters:**
| Param | Default | Description |
|-------|---------|-------------|
| `hours` | 24 | Lookback period |
| `limit` | 1000 | Max records to return |
| `min_distance_pct` | - | Filter by min distance to liquidation |
| `max_distance_pct` | - | Filter by max distance to liquidation |
| `side` | - | Filter by 'long' or 'short' |

**Stats Response includes:**
- Overall stats (total snapshots, unique users, avg distance)
- Per-symbol breakdown
- Top 10 positions closest to liquidation
- Recent scan metadata

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

# === HIP3 LIQUIDATIONS (Stocks, Commodities, Indices, FX) ===
hip3_stats = api.get_hip3_liquidation_stats()        # Stats with category breakdown
hip3_liqs = api.get_hip3_liquidations("1h")          # HIP3 liquidations (10m, 1h, 24h, 7d)
hip3_24h = api.get_hip3_liquidations("24h")          # 24h of HIP3 liqs

# === HIP3 MARKET DATA (Multi-Dex: 51 symbols) ===
hip3_meta = api.get_hip3_meta()                      # All 51 symbols from all dexes
hip3_stats = api.get_hip3_tick_stats()               # Tick collector stats
tsla_ticks = api.get_hip3_ticks("xyz", "tsla")       # xyz:TSLA tick data
btc_ticks = api.get_hip3_ticks("hyna", "btc")        # hyna:BTC tick data
gold_ticks = api.get_hip3_ticks("xyz", "gold")       # xyz:GOLD tick data
us500_ticks = api.get_hip3_ticks("km", "us500")      # km:US500 tick data

# === HIP3 TICK DATA & CANDLES (Top 10 by Volume) ===
hip3_symbols = api.get_hip3_candle_symbols()          # List tracked symbols
hip3_raw = api.get_hip3_raw_ticks("CL", duration="1h")        # Raw ticks (bare ticker)
hip3_raw = api.get_hip3_raw_ticks("cash:USA500", duration="4h") # Raw ticks (dex:ticker)
hip3_candles = api.get_hip3_candles("SILVER", interval="5m")   # OHLCV candles
hip3_candles = api.get_hip3_candles("cash:USA500", interval="1h") # Candles with dex prefix
hip3_price = api.get_hip3_price("NVDA")               # Single symbol price
hip3_prices = api.get_hip3_all_prices()                # All tracked prices

# === POSITIONS & WHALES ===
# Combined (crypto + HIP-3 mixed)
positions = api.get_positions()              # Top 50 positions across ALL symbols (fast, 1s updates)
all_positions = api.get_all_positions()      # All 182 symbols (60s updates)

# SEPARATE - Crypto only (BTC, ETH, SOL, HYPE, etc.)
crypto_pos = api.get_crypto_positions()      # Crypto-only top positions
all_crypto = api.get_all_crypto_positions()  # All 134 crypto symbols
btc_data = all_crypto['symbols']['BTC']      # Filter to BTC
hype_data = all_crypto['symbols']['HYPE']    # Filter to HYPE

# SEPARATE - HIP-3 only (stocks, commodities, indices, FX)
hip3_pos = api.get_hip3_positions()          # HIP-3-only top positions
all_hip3 = api.get_all_hip3_positions()      # All 48 HIP-3 symbols
gold_data = all_hip3['symbols']['xyz:GOLD']  # Filter to GOLD
tsla_data = all_hip3['symbols']['cash:TSLA'] # Filter to TSLA

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

# === HLP ADVANCED ANALYTICS ===
sentiment = api.get_hlp_sentiment()                  # THE BIG ONE! Z-scores & signals
liq_status = api.get_hlp_liquidator_status()         # Real-time liquidator status
market_maker = api.get_hlp_market_maker()            # Strategy B (BTC/ETH/SOL)
timing = api.get_hlp_timing()                        # Hourly/session profitability
correlation = api.get_hlp_correlation()              # Delta-price correlation
hip3_funding = api.get_hlp_funding_hip3()            # HIP3 funding rates (stocks, commodities, ETFs)

# === POSITION SNAPSHOTS ===
btc_snaps = api.get_position_snapshots("BTC", hours=24)           # BTC positions near liq
eth_risky = api.get_position_snapshots("ETH", max_distance_pct=5) # ETH <5% from liq
stats = api.get_position_snapshot_stats(hours=12)                 # Aggregate stats

# === POLYMARKET ===
traders = api.get_poly_profitable_traders()            # Profitable traders by 7-day P&L
for t in traders["traders"]:
    print(f"{t['wallet']}: ${t['pnl_7d']:,.2f} P&L | {t['polymarket_link']}")

# === POLYMARKET WHALES (live $1,000+ fills) ===
whales = api.get_poly_whales(min_usd=5000, days=7, side="BUY")  # Recent whale buys
top_wallets = api.get_poly_whale_top_traders(days=7)            # Leaderboard by wallet
top_markets = api.get_poly_whale_top_markets(days=7)            # Leaderboard by market
daily = api.get_poly_whale_daily(days=30)                       # Per-day rollup (charting)
print(api.poly_whales_health())                                 # WS status, no auth

# === AI CHAT API ===
# Use OpenAI SDK as drop-in replacement:
from openai import OpenAI
client = OpenAI(base_url="https://api.moondev.com/api/ai/v1", api_key="YOUR_KEY")
response = client.chat.completions.create(
    model="moondev-ai",
    messages=[{"role": "user", "content": "Analyze BTC sentiment"}],
    max_tokens=500
)
print(response.choices[0].message.content)
```

---

## Example Scripts Deep Dive

### 02_positions.py - Per-Symbol Position Dashboard

Track whale positions near liquidation for any of the 182 symbols on Hyperliquid (crypto + HIP-3):

```bash
# All symbols - top 50 across everything (fast, 1s updates)
python examples/02_positions.py

# CRYPTO ONLY - no HIP-3 mixed in!
python examples/02_positions.py --crypto

# HIP-3 ONLY - stocks, commodities, indices, FX
python examples/02_positions.py --hip3

# Per-symbol filtering (uses /api/positions/all.json, filters client-side)
python examples/02_positions.py BTC          # BTC positions only
python examples/02_positions.py ETH          # ETH positions only
python examples/02_positions.py HYPE         # HYPE positions only
python examples/02_positions.py SOL          # SOL positions only

# List all 182 available symbols (134 crypto + 48 HIP-3)
python examples/02_positions.py --list
```

**Features:**
- **Separate crypto vs HIP-3** - no more mixing! Use `--crypto` or `--hip3` flags
- Position statistics (total value, long/short breakdown)
- Top 50 positions sorted by liquidation distance (highest risk first)
- Risk analysis (critical <2%, high 2-5%, medium 5-10%)
- Top 5 whale positions by value
- Per-symbol filtering for any of 182 symbols (one API call gets all data)

**SDK Methods:**
```python
api.get_crypto_positions()       # Crypto-only top positions
api.get_hip3_positions()         # HIP-3-only top positions
api.get_all_crypto_positions()   # All 134 crypto symbols
api.get_all_hip3_positions()     # All 48 HIP-3 symbols
```

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

### 24_position_snapshots.py - Position Snapshot Dashboard

Track positions near liquidation for squeeze and cascade signals:

```bash
# Default: all symbols, last 24 hours
python examples/24_position_snapshots.py

# Specific symbol
python examples/24_position_snapshots.py BTC

# Filter to positions very close to liquidation
python examples/24_position_snapshots.py ETH --max-distance 5
```

**Features:**
- Positions within 15% of liquidation price
- Minimum $10k position value filter
- Tracks BTC, ETH, SOL, XRP, HYPE
- 1-minute snapshot frequency
- Historical lookback up to 24+ hours
- Top 10 closest to liquidation
- Long/short side filtering

**Use Cases:**
- Identify potential liquidation cascades
- Spot short/long squeeze setups
- Monitor at-risk whale positions
- Track liquidation pressure building on specific symbols

### 25_ai_chat.py - AI Chat API Dashboard

Use Moon Dev's AI as an OpenAI drop-in replacement:

```bash
python examples/25_ai_chat.py
```

**Features:**
- OpenAI SDK compatible (just change base_url)
- Simple chat endpoint for quick queries
- No need for OpenAI or Anthropic API keys
- Works with any OpenAI-compatible library

**Use Cases:**
- Trading analysis and insights
- Market sentiment interpretation
- Strategy brainstorming
- Any AI chat needs without extra API keys

Full documentation: https://moondev.com/docs

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

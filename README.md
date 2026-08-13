# Hyperliquid Data Layer API

## The Rigged Game Ends Here

Wall Street has been playing a rigged game for decades.

They see your positions. They see your liquidations. They hunt your stops. They know exactly where to push the price to wipe you out.

But you? You've been blind.

When hedge funds open massive positions, you don't see it. When institutions are about to get liquidated, you don't see it. When smart money is accumulating, you don't see it.

**They see everything. You see nothing.**

That's how Wall Street has worked for your entire life. The house always wins because the house can see everyone's cards.

Until now.

---

## Enter Hyperliquid

Hyperliquid is building something different. An open financial system. A decentralized exchange that's already doing more volume than most centralized exchanges. A blockchain where everything is transparent.

They're calling themselves **the housecoin of all finance**.

Why? Because they're not just building another exchange. They're rebuilding the entire financial system on a foundation of transparency. On Hyperliquid, everyone can see what used to be hidden.

The liquidations? Visible.
The whale positions? Visible.
The smart money flows? Visible.

For the first time in history, regular traders can see what Wall Street has always seen.

---

## Why This Data Layer Exists

Here's the problem: Hyperliquid opened up all this data, but nobody built an easy way to access it.

Until now, there were **zero open node providers** creating a data layer for Hyperliquid. The data was there, but developers couldn't easily tap into it.

I'm Moon Dev, and I built this data layer because I believe in the vision.

My vision for Hyperliquid:
- **Billions of users** on an open financial system
- **Thousands of successful apps** serving those users
- **Millions of apps** being built by developers worldwide

But here's the thing: before we get a billion people on Hyperliquid, we need thousands of great apps. Before we get thousands of apps, developers need data. Easy data. Fast data. Real data.

**That's why I built the first open data layer for Hyperliquid.**

I'm already building the first major consumer app on this data layer - a Quant App that helps regular traders compete with institutions. It helps you take over liquidations, set intelligent limit orders, and manage risk in ways humans simply can't do manually.

But one app isn't enough. We need thousands of apps. And for that, we need thousands of developers with access to this data.

That's you.

---

## What You Get

This data layer gives you access to everything Wall Street kept hidden:

| What You Can See | Why It Matters |
|-----------------|----------------|
| **Liquidations** | See when positions are about to get wiped out - in real-time |
| **Multi-Exchange Liqs** | Combined liquidations from Hyperliquid, Binance, Bybit, OKX (Live + Archive) |
| **HIP3 Liquidations** | Stocks, Commodities, Indices & FX liquidations (TSLA, GOLD, XYZ100, EUR) |
| **HIP3 Market Data** | Multi-dex coverage: 136+ symbols across 7 dexes (xyz, flx, vntl, hyna, km, cash, para) |
| **HIP3 Tick Data & Candles (UPDATED!)** | EVERY HIP3 symbol — raw ticks, OHLCV candles, prices — auto-discovers new listings |
| **Position Snapshots** | Track positions within 15% of liquidation (BTC, ETH, SOL, XRP, HYPE) |
| **Whale Positions** | Track positions for any of 182 symbols - crypto AND HIP-3 separately! |
| **Buyer Tracking** | $5k+ buyers on HYPE/SOL/XRP/ETH - accumulation signals |
| **Smart Money Rankings** | Top 100 profitable traders vs Bottom 100 |
| **Trading Signals** | Know when smart money is buying or selling |
| **Any Wallet's Positions** | Look up any Hyperliquid address and see their full portfolio |
| **Trade History** | Get complete fill history for any wallet |
| **HLP Strategies** | See inside Hyperliquid's $210M+ market-making protocol |
| **HLP Sentiment** | THE BIG ONE! Z-scores showing retail positioning (squeeze signals) |
| **HLP Flip Tracker (NEW!)** | Live delta + historical flips when HLP crosses long↔short |
| **Order Flow** | Buy pressure vs sell pressure, cumulative delta |
| **Live Prices** | Real-time tick data for all major coins |
| **Blockchain Events** | Transfers, swaps, deposits - as they happen |
| **All Depositors** | Canonical list of every address that ever bridged to Hyperliquid |
| **Market Data (NEW!)** | All 224 prices + funding + OI - NO RATE LIMITS |
| **Orderbooks** | Full L2 orderbook (~20 levels) - replaces Hyperliquid's rate-limited call |
| **Account State** | Full account data for any wallet - NO RATE LIMITS |
| **Fills (NEW!)** | Trade fills in Hyperliquid-compatible format - drop-in replacement |
| **Candles (80 symbols!)** | OHLCV candles (1m-1d) for 80 symbols: majors, DeFi, memes (FARTCOIN, TRUMP...) |
| **Tick Data (80 symbols!)** | Raw price ticks with custom time windows for any tracked symbol |
| **AI Chat API (NEW!)** | OpenAI-compatible drop-in replacement - no extra API keys needed |

This is the data that used to cost hedge funds millions of dollars. Now it's accessible to anyone with an API key.

---

## Quick Start

### Step 1: Get Your API Key
Visit **https://moondev.com** to get your free API key. Check out the **[full docs](https://moondev.com/docs)** for detailed guides.

### Step 2: Install Dependencies
```bash
pip install requests rich python-dotenv
```

### Step 3: Set Your API Key
Create a `.env` file:
```bash
MOONDEV_API_KEY=your_api_key_here
```

### Step 4: Run Any Example
```bash
python examples/01_liquidations.py        # See real-time liquidations
python examples/09_smart_money.py         # Track smart money
python examples/12_hlp_positions.py       # See HLP's $210M positions
python examples/14_multi_liquidations.py  # All exchanges: Hyperliquid, Binance, Bybit, OKX
python examples/15_buyers.py              # $5k+ buyers on HYPE/SOL/XRP/ETH
python examples/16_depositors.py          # All Hyperliquid depositors
python examples/19_market_data.py         # Prices, orderbooks, accounts - NO RATE LIMITS!
python examples/20_hip3_liquidations.py   # HIP3 liqs: stocks, commodities, indices, FX
python examples/21_hip3_market_data.py    # HIP3 candles & ticks: TSLA, GOLD, EUR, etc.
python examples/24_position_snapshots.py  # Positions near liquidation (BTC/ETH/SOL/XRP/HYPE)
python examples/25_ai_chat.py             # AI Chat API - drop-in OpenAI replacement
python examples/35_ohlcv_data.py         # Open, High, Low, Close, Volume Data (new bars layer)
python examples/35_btc_tick_stream.py     # Live BTC tick stream + JSONL sink for bots
```

That's it. You're now seeing what Wall Street sees.

---

## API Examples

Every example is a standalone Python script with beautiful terminal output. Run any of them to see live data.

| File | What It Shows |
|------|---------------|
| `01_liquidations.py` | Real-time liquidation heatmaps, top liqs, long/short breakdowns |
| `02_positions.py` | Whale positions - crypto & HIP-3 SEPARATE! (182 symbols! Use: `02_positions.py BTC`) |
| `03_whales.py` | Whale addresses, recent trades, smart money moves |
| `04_events.py` | Live blockchain events, transfers, swaps, deposits |
| `05_contracts.py` | High-value contracts, activity tracking |
| `06_ticks.py` | Live prices, historical charts, volatility |
| `07_orderflow.py` | Buy/sell pressure, cumulative delta, imbalance |
| `08_trades.py` | Trade stream, large trades, volume analysis |
| `09_smart_money.py` | Top 100 smart money, Bottom 100 dumb money, trading signals |
| `10_user_positions.py` | Get all positions for ANY Hyperliquid wallet |
| `11_user_fills.py` | Historical fills, PnL analysis, win/loss streaks (add a `minutes` window for the fast lane) |
| `12_hlp_positions.py` | All 7 HLP strategies, liquidators, deltas |
| `13_binance_liquidations.py` | Binance Futures liquidations for comparison |
| `14_multi_liquidations.py` | Combined liqs from Hyperliquid, Binance, Bybit, OKX |
| `15_buyers.py` | $5k+ buyers on HYPE/SOL/XRP/ETH (buyers only - accumulation signals!) |
| `16_depositors.py` | All Hyperliquid depositors - canonical list of bridged addresses |
| `17_hlp_sentiment.py` | THE BIG ONE! HLP z-scores showing retail positioning |
| `18_hlp_analytics.py` | HLP liquidators, market maker, timing, correlation |
| `19_market_data.py` | All prices, orderbooks, account state - NO RATE LIMITS |
| `20_hip3_liquidations.py` | HIP3 liquidations - stocks, commodities, indices, FX |
| `21_hip3_market_data.py` | HIP3 OHLCV candles & tick data for 33 TradFi assets |
| `24_position_snapshots.py` | Positions within 15% of liquidation - squeeze signals |
| `25_ai_chat.py` | **NEW!** AI Chat API - OpenAI-compatible drop-in replacement |
| `35_ohlcv_data.py` | Universe + single-symbol and multi-symbol bars from the new OHLCV layer |
| `35_btc_tick_stream.py` | Live BTC tick stream with rolling tape + JSONL sink for bots |
| `37_liquidation_totals.py` | **NEW!** Long/short liquidation totals across 6 rolling windows (5m→4h) + squeeze detector |
| `38_fills_polling.py` | **NEW!** Time-windowed fills polling - ~50ms for any wallet, with dedupe + 503 handling |

See the [examples/README.md](examples/README.md) for the API reference, or visit **https://moondev.com/docs** for the full documentation.

---

## Market Data API (NO RATE LIMITS!)

These endpoints replace Hyperliquid's rate-limited API calls. All requests go through Moon Dev's node - no more 429 errors!

### Endpoints

| Endpoint | Replaces | Description |
|----------|----------|-------------|
| `GET /api/prices` | `metaAndAssetCtxs` | All 224 coin prices + funding rates + open interest |
| `GET /api/price/{coin}` | - | Quick single-coin price with bid/ask/spread |
| `GET /api/orderbook/{coin}` | `l2Book` | Full L2 orderbook (~20 levels each side) |
| `GET /api/account/{address}` | `clearinghouseState` | Full account state for any wallet |
| `GET /api/hl/clearinghouse/{address}` | `info.user_state()` | Direct proxy alias of `/api/account` (try local node, fall back to public) |
| `GET /api/hl/open_orders/{address}` | `info.open_orders()` | All resting orders (optional `?coin=BTC` filter) |
| `GET /api/fills/{address}` | `userFills` | Trade fills in Hyperliquid-compatible format |
| `GET /api/fills/{address}?startTime=MS` | `userFillsByTime` | Same param name and units as HL, so HL code ports directly (or use `?minutes=N`) |
| `GET /api/candles/{coin}` | `candleSnapshot` | OHLCV candles (1m, 5m, 15m, 1h, 4h, 1d) |
| `GET /api/candles/symbols` | - | List all 80 tracked symbols |
| `GET /api/ticks/{symbol}` | - | Raw tick data with custom time windows |
| `GET /api/universe` | - | Tracked symbol universe plus tick coverage metadata |
| `GET /api/bars` | - | Bulk OHLCV-style bars for aligned multi-symbol history |
| `GET /api/bars/{symbol}` | - | OHLCV-style bars for a single symbol |

### Symbol Discovery

**80 symbols tracked** based on $750k+ daily volume:

```python
# Get all available symbols
symbols = api.get_candle_symbols()
print(f"{symbols['count']} symbols available")
print(symbols['symbols'])  # ['AAVE', 'ACE', 'ADA', 'APT', 'ARB', ...]
```

**Categories:**
- **Major:** BTC, ETH, SOL, XRP, DOGE, LTC, BCH, ADA, DOT, LINK, AVAX, BNB, TRX, XMR, XLM
- **DeFi:** AAVE, UNI, CRV, LDO, PENDLE, JUP, MORPHO, ONDO, ENA
- **L2/Alt L1:** ARB, OP, SUI, SEI, APT, NEAR, TON, ICP, TIA, STRK, MOVE, BERA, HBAR, MNT
- **Memes:** HYPE, FARTCOIN, PUMP, WIF, POPCAT, PENGU, kPEPE, kBONK, kSHIB, TRUMP

### Tick Data API

Get raw price ticks for any of 80 symbols:

```python
# FARTCOIN ticks for last 10 minutes
ticks = api.get_ticks("FARTCOIN", duration="10m")
print(f"{ticks['tick_count']} ticks, latest: ${ticks['latest_price']}")

# TRUMP ticks for last hour
ticks = api.get_ticks("TRUMP", duration="1h")

# Custom time range (Unix ms)
ticks = api.get_ticks("DOGE", start_time=1768400000000, end_time=1768486000000)
```

MoonDev tick history now supports trade-level size for newly ingested trade-stream data.
Historical rows collected before the rollout remain price-only.
Tick APIs now expose `sz` and `side` when available.

Practical guidance:
- New post-rollout tick rows may include `p`, `sz`, `side`, and `t`
- Older historical rows may not include `sz` or `side`
- Clients should treat `sz` as expected for new data and nullable for old data

**Parameters:**

| Param | Default | Description |
|-------|---------|-------------|
| `duration` | `1h` | Time window: `10m`, `1h`, `4h`, `24h`, `7d` |
| `limit` | `10000` | Max ticks to return |
| `startTime` | - | Start time (Unix ms) |
| `endTime` | - | End time (Unix ms) |

**Tick Response Notes:**
```json
{
  "t": 1736121600123,
  "p": 73924.5,
  "sz": 0.125,
  "side": "B"
}
```

- `p`: trade price
- `sz`: trade size when stored in the underlying tick row
- `side`: trade side when provided by upstream
- `t`: event timestamp
- For pre-rollout historical ranges, `sz` may be null or absent
- For post-rollout ranges, `sz` should contain real stored trade size when the collector captured it

### Bars API

MoonDev bars are aggregated server-side from stored tick history.

```python
# Aligned multi-symbol history
bars = api.get_bars(["BTC", "ETH", "SOL"], interval="1h")

# Single symbol
btc_bars = api.get_bars_symbol("BTC", interval="1h")

# Universe and coverage metadata
universe = api.get_universe()
```

**Endpoints:**

| Endpoint | Description |
|----------|-------------|
| `GET /api/bars?symbols=BTC,ETH,SOL&interval=1h&startTime=...&endTime=...` | Bulk bars across multiple symbols |
| `GET /api/bars/{symbol}?interval=1h&startTime=...&endTime=...` | Bars for one symbol |
| `GET /api/universe` | Tracked symbol list plus coverage metadata |

**Bar fields:**
- `o`: first trade price in the interval
- `h`: highest trade price in the interval
- `l`: lowest trade price in the interval
- `c`: last trade price in the interval
- `v`: summed tick size across the interval when size exists in stored ticks
- `n`: number of ticks or trades contributing to the bar

**Volume behavior:**
- OHLC is valid across the full stored tick history
- For historical bars built from pre-rollout price-only ticks, `v` may be `0`
- For bars built from newly collected trade-stream ticks, `v` reflects summed stored trade size
- `volume_available: true` means the pipeline supports size-backed volume, not that every historical bar already has it

**Client guidance:**
- Use `/api/bars` for aligned multi-symbol history
- Use `/api/ticks/{symbol}` for raw event-level inspection
- Expect a transition period where OHLC is complete across history, but volume is only complete for post-rollout data

### Candles API

Get OHLCV candles for any of **80 tracked symbols**:

```python
# BTC 5-minute candles
candles = api.get_candles("BTC", interval="5m")

# FARTCOIN 1-minute candles
candles = api.get_candles("FARTCOIN", interval="1m")

# TRUMP hourly candles
candles = api.get_candles("TRUMP", interval="1h")

# Custom time range
candles = api.get_candles("DOGE", interval="15m", start_time=0)  # All available
```

**Parameters:**

| Param | Default | Description |
|-------|---------|-------------|
| `interval` | `5m` | Candle size: `1m`, `5m`, `15m`, `1h`, `4h`, `1d` |
| `startTime` | auto | Start timestamp (Unix ms) |
| `endTime` | now | End timestamp (Unix ms) |

**Response Format (Hyperliquid-compatible):**
```json
{
  "t": 1736121600000,  // Open time (ms)
  "T": 1736125199999,  // Close time (ms)
  "s": "FARTCOIN",     // Symbol
  "i": "5m",           // Interval
  "o": "0.385",        // Open
  "h": "0.390",        // High
  "l": "0.380",        // Low
  "c": "0.387",        // Close
  "v": "12.45",        // Summed stored size when available, else may be 0
  "n": 45              // Number of ticks
}
```

Volume transition note:
- OHLC is complete across the full tick history
- `v` is only complete where the underlying stored ticks include `sz`
- Historical pre-rollout candles and bars may therefore show `v = 0` while still having valid OHLC and `n`

### Python Usage

```python
from api import MoonDevAPI

api = MoonDevAPI()

# All 224 prices at once
prices = api.get_prices()
print(f"BTC: ${prices['prices']['BTC']}")

# Quick single price
btc = api.get_price("BTC")
print(f"Spread: {btc['spread_bps']} bps")

# Full orderbook
book = api.get_orderbook("BTC")
print(f"Best bid: {book['best_bid']}, Best ask: {book['best_ask']}")

# Any wallet's account
account = api.get_account("0x...")
print(f"Account value: ${account['marginSummary']['accountValue']}")

# Trade fills
fills = api.get_fills("0x...", limit=100)
for fill in fills[:5]:
    print(f"{fill['coin']} {fill['side']} @ {fill['px']}")

# Trade fills in a time window - ~50ms for ANY wallet, always use this when polling
recent = api.get_fills("0x...", minutes=60)                  # HL format, last hour
recent = api.get_user_fills("0x...", limit=2000, minutes=10) # Moon Dev format, last 10 min

# OHLCV candles
candles = api.get_candles("BTC", interval="1m")
for c in candles[-5:]:
    print(f"O:{c['o']} H:{c['h']} L:{c['l']} C:{c['c']}")

# Raw ticks with size when available
ticks = api.get_ticks("BTC", duration="10m")
for t in ticks.get("ticks", [])[:5]:
    print(t.get("p"), t.get("sz"), t.get("side"))

# New bars layer
bars = api.get_bars(["BTC", "ETH", "SOL"], interval="1h")
btc_bars = api.get_bars_symbol("BTC", interval="1h")
universe = api.get_universe()
```

---

## Multi-Exchange Liquidations (29x Faster!)

The all-liquidations API combines data from Hyperliquid, Binance, Bybit, and OKX with a high-performance architecture:

**Base URL:** `https://api.moondev.com/api/all_liquidations/`

### Live Endpoints (30-second updates)
| Endpoint | Description |
|----------|-------------|
| `10m.json` | Last 10 minutes |
| `1h.json` | Last 1 hour |
| `4h.json` | Last 4 hours |
| `12h.json` | Last 12 hours |
| `24h.json` | Last 24 hours |
| `2d.json` | Last 2 days |
| `5d.json` | Last 5 days |
| `stats.json` | Summary statistics |
| `totals.json` | Rolling totals w/ full long/short split — 5m, 15m, 1h, 2h, 3h, 4h windows + per-exchange breakdown (updates every 20s) |

### Archive Endpoints (15-minute updates)
| Endpoint | Description |
|----------|-------------|
| `7d.json` | Last 7 days |
| `14d.json` | Last 14 days |
| `30d.json` | Last 30 days |

**Performance:** Split architecture achieves 5-second cycles vs 150-second legacy - 29x faster data freshness.

---

## Separate Crypto vs HIP-3 Positions

Positions are now cleanly separated - no more mixing crypto perps with stocks and commodities!

### Python SDK

```python
from api import MoonDevAPI
api = MoonDevAPI()

# CRYPTO ONLY - BTC, ETH, SOL, HYPE, etc. (134 symbols)
crypto_positions = api.get_crypto_positions()          # Top positions, crypto only
all_crypto = api.get_all_crypto_positions()            # All 134 crypto symbols

# HIP-3 ONLY - Stocks, Commodities, Indices, FX (48 symbols)
hip3_positions = api.get_hip3_positions()              # Top positions, HIP-3 only
all_hip3 = api.get_all_hip3_positions()                # All 48 HIP-3 symbols

# Combined (original behavior - both mixed)
all_positions = api.get_positions()                    # Top 50 across everything
all_data = api.get_all_positions()                     # All 182 symbols
```

### Command Line

```bash
python examples/02_positions.py --crypto    # Crypto only
python examples/02_positions.py --hip3      # HIP-3 only (stocks, commodities, etc.)
python examples/02_positions.py             # Combined (default)
python examples/02_positions.py BTC         # Specific symbol
```

**How it works:** HIP-3 symbols use a `dex:ticker` format (e.g., `xyz:GOLD`, `cash:TSLA`, `km:USA500`). The SDK filters based on this prefix so you always get clean, separated data.

---

## Position Snapshots API (NEW!)

Track positions close to liquidation on HyperLiquid. Perfect for identifying squeeze setups and liquidation cascades.

**Features:**
- Snapshots every 1 minute
- Tracks: BTC, ETH, SOL, XRP, HYPE
- Positions within 15% of liquidation price
- Minimum $10k position value

### Get Historical Snapshots

```
GET /api/position_snapshots/symbol/{symbol}
```

**Parameters:**
| Param | Default | Description |
|-------|---------|-------------|
| `symbol` | required | BTC, ETH, SOL, XRP, HYPE |
| `hours` | 24 | Lookback period |
| `limit` | 1000 | Max records |
| `min_distance_pct` | - | Filter by min distance to liquidation |
| `max_distance_pct` | - | Filter by max distance to liquidation |
| `side` | - | Filter by 'long' or 'short' |

### Get Aggregate Statistics

```
GET /api/position_snapshots/stats
```

**Parameters:**
| Param | Default | Description |
|-------|---------|-------------|
| `hours` | 24 | Lookback period |

**Returns:**
- Overall stats (total snapshots, unique users, avg distance to liquidation)
- Per-symbol breakdown
- Top 10 positions closest to liquidation
- Recent scan metadata

### Python Usage

```python
from api import MoonDevAPI

api = MoonDevAPI()

# Get BTC positions near liquidation
btc_snapshots = api.get_position_snapshots("BTC", hours=24)

# Filter to positions very close to liquidation
risky = api.get_position_snapshots("ETH", max_distance_pct=5)

# Get aggregate stats
stats = api.get_position_snapshot_stats(hours=12)
print(f"Top 10 at risk: {stats['top_10_closest']}")
```

---

## HIP3 Tick Data & Candles (UPDATED!)

**Every HIP3 symbol on HyperLiquid** — currently **136 across 7 dexes** (xyz, flx, vntl, hyna, km, cash, para). New symbols are auto-discovered as HyperLiquid lists them; no config changes needed. Data is served on-demand from the tick DB at request time, so the API scales to thousands of symbols without pre-generating files. 30-day retention, sub-second freshness, ~500ms tick resolution, 24/7 (HyperLiquid is always open).

### Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/hip3/meta` | All symbols with current prices, categories, dex info |
| `GET /api/hip3/candles/symbols` | List of all 136+ tracked symbols by category |
| `GET /api/hip3/price/{coin}` | Latest price for a single symbol |
| `GET /api/hip3/prices` | All latest prices for all tracked symbols at once |
| `GET /api/hip3/ticks/{coin}` | Raw ticks (durations: `10m`, `1h`, `4h`, `24h`, `7d`; or `startTime`/`endTime` ms) |
| `GET /api/hip3/candles/{coin}` | OHLCV candles (intervals: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`) |

**Symbol naming** — pass the bare ticker (case-insensitive): `HIMS`, `tsla`, `cl`, `usa500`. Or use the full `dex:ticker` form: `xyz:HIMS`, `cash:USA500`, `hyna:BTC`. Bare tickers resolve automatically when only one dex carries them; for ambiguous tickers (e.g. `GOLD` exists on xyz, flx, and km) pass the full form.

**Categories covered:** stocks, commodities, indices, FX, crypto, pre-IPO (Ventuals: OPENAI, ANTHROPIC, SPACEX), and thematic baskets (MAG7, NUCLEAR, ROBOT).

### Python Usage

```python
from api import MoonDevAPI
api = MoonDevAPI()

# List every tracked symbol
symbols = api.get_hip3_candle_symbols()
print(f"{symbols['count']} symbols across categories:", list(symbols['by_category'].keys()))

# Raw ticks — bare ticker or dex:ticker, with optional limit / time window / order
ticks = api.get_hip3_raw_ticks("HIMS", duration="1h", limit=500, order="desc")
print(f"{ticks['tick_count']} ticks for {ticks['symbol']}")

# OHLCV candles — HL convention: t, T, s, i, o, h, l, c, v, n
candles = api.get_hip3_candles("SILVER", interval="5m", limit=100)
for c in candles[-3:]:
    print(f"O:{c['o']} H:{c['h']} L:{c['l']} C:{c['c']} V:{c['v']}")

# Single price (auto-resolves bare ticker)
price = api.get_hip3_price("NVDA")
print(f"NVDA: ${price['price']} ({price['category']})")

# All 136+ prices at once
prices = api.get_hip3_all_prices()
print(f"Got {len(prices['prices'])} prices across {len(prices['dexes'])} dexes")
```

### Why this matters
HIP3 tick data on traditional venues costs thousands per month per symbol. Because we run a HyperLiquid node, every HIP3 symbol — stocks, commodities, FX, indices, crypto, pre-IPO — is available through one API at no marginal cost, 24/7, with sub-second freshness and OHLCV at any interval. The legacy static-file endpoints (`/api/hip3_ticks/{dex}_{symbol}_{duration}.json`) continue to publish for the top 10 symbols for backward compatibility — new integrations should use the on-demand endpoints above.

---

## Polymarket Whales API (NEW!)

**Live whale tracker for Polymarket prediction markets.** A background service holds a persistent WebSocket to `wss://ws-live-data.polymarket.com` and records every trade with USD notional **≥ $1,000** into a database. The endpoints below let you query that log by time window, dollar threshold, wallet, and market. Anything below $1,000 is never collected — `min_usd` has a hard floor.

### Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/poly/whales` | Recent whale fills, newest first |
| `GET /api/poly/whales/top-traders` | Leaderboard by wallet (volume desc) |
| `GET /api/poly/whales/top-markets` | Leaderboard by market (volume desc) |
| `GET /api/poly/whales/daily` | Per-day rollup of whale activity (charting) |
| `GET /api/poly/whales/health` | Ingestion service status (no auth) |

**Params** — `min_usd` (default 1000, floor 1000), `days` (default 1, max 365), `wallet` (proxyWallet), `market` (market_slug or event_slug), `side` (`BUY`/`SELL`), `limit`. Standard keys are capped per endpoint (whales: 250, top-traders: 50); Quant Elite (`_qe`) keys get the full set (whales up to 5,000, top-traders up to 1,000).

### Python Usage

```python
from api import MoonDevAPI
api = MoonDevAPI()

# Recent whale buys ≥ $5k over the last 7 days
whales = api.get_poly_whales(min_usd=5000, days=7, side="BUY")
for t in whales["trades"][:5]:
    print(f"{t['side']} ${t['usd_amount']:,.0f} | {t['market_title']} | {t['wallet']}")

# Who's moving the most size?
top = api.get_poly_whale_top_traders(days=7)

# Which markets are whales piling into?
markets = api.get_poly_whale_top_markets(days=7)

# Daily rollup for charting
daily = api.get_poly_whale_daily(days=30)

# Confirm the WebSocket is connected and ingestion is fresh (no auth)
print(api.poly_whales_health())
```

### Why this matters
This is the live order-flow log — every large bet on Polymarket as it happens. Pair it with `/api/poly/profitable-traders` (the "who's actually making money" filter, a separate 7-day P&L service) by cross-referencing wallet addresses: the whales endpoint tells you *what* big money is doing right now, profitable-traders tells you *who's* worth following.

---

## AI Swarm Agent (Supplementary Tool)

**Optional: Get analysis from 6+ AI models simultaneously.**

The main feature of this repo is the data layer API itself - the examples above show you how to access institutional-grade data. This AI Swarm Agent is a supplementary tool to help you understand and explore what's available.

This repo includes an AI swarm agent that can:
- **Chat** with a Director AI that understands all 40+ API endpoints
- **Propose** analysis plans using the available data
- **Execute** multi-model analysis via OpenRouter (Claude, GPT, Gemini, Qwen, and more)

### Quick Start

```bash
# Add to your .env (one key for everything!):
OPENROUTER_API_KEY=your_openrouter_key_here

# Install dependencies
pip install -r requirements.txt

# Run it!
python ai_agents/run.py
```

### Example Session

```
🌙 Moon Dev's Director Agent
==================================================

> What can I do with these APIs?

You can analyze Hyperliquid data including:
- Real-time liquidations from 4 exchanges
- 148 symbols with whale positions
- HLP sentiment (THE BIG ONE) - retail positioning signals
- Smart money vs dumb money rankings
- Order flow and trade data
...

> Is there a short squeeze brewing on BTC?

[PLAN]
1. get_hlp_sentiment() - Check retail positioning
2. get_liquidations("24h") - Recent liquidation pressure
3. get_smart_money_signals("1h") - Smart money activity

📋 Proceed with this plan? [y/n] > y

📡 Fetching data from Moon Dev API...
   ✅ get_hlp_sentiment()
   ✅ get_liquidations("24h")
   ✅ get_smart_money_signals("1h")

🌊 Sending to AI Swarm for analysis...
   ✅ Claude Opus 4.5
   ✅ GPT-5 Mini
   ✅ Qwen3 Max
   ✅ GLM 4.6
   ✅ Gemini 2.5 Flash
   ✅ DeepSeek R1

============================================================
🤖 AI SWARM RESPONSES
============================================================

💡 Claude Opus 4.5:
Based on the HLP z-score of +2.3, retail is heavily short. Combined with
$45M in short liquidations over 24h, there's building squeeze pressure...

💡 GPT-5 Mini:
The sentiment data shows extreme short positioning. Smart money signals
are net bullish. Classic squeeze setup forming...

💡 Qwen3 Max:
Cross-referencing HLP delta with liquidation data suggests accumulation
by market makers while retail is betting against the trend...

[More AI responses...]

============================================================
🌙 Analysis complete! - Moon Dev
```

### Why This Matters

You now have:
- **Institutional-grade data** from the Hyperliquid Data Layer
- **Multi-perspective AI analysis** from 6+ different models
- **One simple interface** to explore and analyze everything

This is institutional-grade alpha. The data costs hedge funds thousands per month. The AI swarm gives you perspectives from the best models in the world. And it's all available right here.

---

## The Vision

Hyperliquid is building the housecoin of all finance.

I'm building the data layer that will help developers create the thousands of apps needed to onboard billions of users.

This isn't just about trading. This is about rebuilding finance. Transparent. Open. Fair.

Wall Street had their turn. Now it's ours.

---

## Links

- **Get API Key:** https://moondev.com
- **Full Documentation:** https://moondev.com/docs
- **API Reference:** [examples/README.md](examples/README.md)
- **Hyperliquid:** https://hyperliquid.xyz
- **Issues:** https://github.com/moondevonyt/Hyperliquid-Data-Layer-API/issues

---

Built with love by Moon Dev

*The housecoin of all finance starts here.*

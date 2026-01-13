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
| **Multi-Exchange Liqs** | Combined liquidations from Hyperliquid, Binance, Bybit, OKX |
| **Whale Positions** | Track positions for any of 148 symbols (BTC: $1.9B, ETH: $2.7B, HYPE: $528M) |
| **Buyer Tracking** | $5k+ buyers on HYPE/SOL/XRP/ETH - accumulation signals |
| **Smart Money Rankings** | Top 100 profitable traders vs Bottom 100 |
| **Trading Signals** | Know when smart money is buying or selling |
| **Any Wallet's Positions** | Look up any Hyperliquid address and see their full portfolio |
| **Trade History** | Get complete fill history for any wallet |
| **HLP Strategies** | See inside Hyperliquid's $210M+ market-making protocol |
| **HLP Sentiment** | THE BIG ONE! Z-scores showing retail positioning (squeeze signals) |
| **Order Flow** | Buy pressure vs sell pressure, cumulative delta |
| **Live Prices** | Real-time tick data for all major coins |
| **Blockchain Events** | Transfers, swaps, deposits - as they happen |
| **All Depositors** | Canonical list of every address that ever bridged to Hyperliquid |

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
```

That's it. You're now seeing what Wall Street sees.

---

## API Examples

Every example is a standalone Python script with beautiful terminal output. Run any of them to see live data.

| File | What It Shows |
|------|---------------|
| `01_liquidations.py` | Real-time liquidation heatmaps, top liqs, long/short breakdowns |
| `02_positions.py` | Whale positions for any symbol (148 symbols! Use: `02_positions.py BTC`) |
| `03_whales.py` | Whale addresses, recent trades, smart money moves |
| `04_events.py` | Live blockchain events, transfers, swaps, deposits |
| `05_contracts.py` | High-value contracts, activity tracking |
| `06_ticks.py` | Live prices, historical charts, volatility |
| `07_orderflow.py` | Buy/sell pressure, cumulative delta, imbalance |
| `08_trades.py` | Trade stream, large trades, volume analysis |
| `09_smart_money.py` | Top 100 smart money, Bottom 100 dumb money, trading signals |
| `10_user_positions.py` | Get all positions for ANY Hyperliquid wallet |
| `11_user_fills.py` | Historical fills, PnL analysis, win/loss streaks |
| `12_hlp_positions.py` | All 7 HLP strategies, trades, liquidators, deltas |
| `13_binance_liquidations.py` | Binance Futures liquidations for comparison |
| `14_multi_liquidations.py` | Combined liqs from Hyperliquid, Binance, Bybit, OKX |
| `15_buyers.py` | $5k+ buyers on HYPE/SOL/XRP/ETH (buyers only - accumulation signals!) |
| `16_depositors.py` | All Hyperliquid depositors - canonical list of bridged addresses |
| `17_hlp_sentiment.py` | THE BIG ONE! HLP z-scores showing retail positioning |
| `18_hlp_analytics.py` | HLP liquidators, market maker, timing, correlation |

See the [examples/README.md](examples/README.md) for the API reference, or visit **https://moondev.com/docs** for the full documentation.

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

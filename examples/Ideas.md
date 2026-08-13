# Alpha Extraction Ideas - Moon Dev API

**Brain Ticklers for the Hyperliquid Data Layer**

## Disclaimer

**None of this is financial advice.** These are random ideas that aren't necessarily going to work. Seriously - don't just run any of this in a bot and lose money.

The point of this doc is to tickle your brain cells so YOU come up with your own ideas that you can then backtest, validate, and iterate on. Treat these as conversation starters, not trading strategies.

If something sounds interesting, go explore it. Pull the data. Look at it. See if the pattern even exists. Then if it does, backtest the hell out of it before risking real money.

Built with love by Moon Dev

---

## 01_liquidations.py - Hyperliquid Liquidations

**Endpoint:** `/api/liquidations/{timeframe}.json`

1. **Liquidation Cascade Patterns** - Liquidations tend to cause more liquidations. Could there be something interesting when liquidation volume spikes way above normal? Maybe the cascade direction matters. Worth exploring.

2. **Liquidation Exhaustion** - After massive liquidation events, does the market tend to reverse? Or continue? Pull the data and see if extreme liquidations mark turning points.

3. **Long vs Short Imbalance** - What happens when liquidations are heavily one-sided for extended periods? Is the market actually overextended, or does the trend continue? The data's there to find out.

---

## 02_positions.py - Whale Positions Near Liquidation

**Endpoint:** `/api/positions/all.json` (148 symbols)

1. **Liquidation Level Clustering** - You can see where positions are close to getting liquidated. Are there price levels where a bunch of liquidations would trigger at once? What happens when price approaches those clusters?

2. **Whale Consensus** - When most big players are positioned the same direction, does that mean anything? Do they know something, or do they get rekt together? Check the data.

3. **Crowded Trades** - When everyone's on one side of a trade, sometimes it unwinds violently. Sometimes the crowd is right. Which is it for different setups? Worth investigating.

---

## 03_whales.py - Whale Activity Tracker

**Endpoint:** `/api/whales.json` ($25k+ trades)

1. **Whale Flow Direction** - Whales are making $25k+ trades all the time. Is the aggregate direction meaningful? Does heavy whale buying actually precede price moves, or is it noise?

2. **Whale Behavior Patterns** - Can you identify when a whale switches from buying to selling? Does that transition tell you anything useful about what's coming?

3. **Coordinated Activity** - When multiple whales buy the same thing around the same time, is that signal or coincidence? The data lets you find out.

---

## 04_events.py - Blockchain Events

**Endpoint:** `/api/events.json`

1. **Deposit Watching** - When someone bridges a large amount to Hyperliquid, they probably want to trade. What happens after large deposits? Any patterns worth tracking?

2. **Withdrawal Patterns** - Do mass withdrawals tell you anything about what's coming? Or is it just noise? The event stream has the data.

3. **Swap Flow Analysis** - If swaps are consistently going one direction (like USDC into a specific asset), could that be early accumulation signal? Explore it.

---

## 05_contracts.py - Contract Registry

**Endpoint:** `/api/contracts.json`

1. **New Contract Activity** - When new contracts show up and start trading, what are they doing? Could be interesting to watch early behavior of new protocols.

2. **Dormant Contract Wakeups** - If a contract that's been quiet suddenly gets active, why? Something changed. Might be worth investigating.

3. **Aggregate Contract Flows** - Are smart contracts as a whole net buying or selling? Does that aggregate flow tell you anything useful?

---

## 06_ticks.py - Live Price Data

**Endpoint:** `/api/ticks/{symbol}_{timeframe}.json`

1. **Tick Frequency Changes** - Does the rate of ticks (trades per second) tell you anything about what's coming? Does activity pick up before big moves?

2. **Volatility Compression** - What happens after periods of low volatility? Does the data show any patterns around volatility expansion?

3. **Tick Patterns** - Are there any recurring tick sequences that seem to precede certain moves? Might be nothing, might be something. The tick data lets you look.

---

## 07_orderflow.py - Order Flow Analysis

**Endpoint:** `/api/orderflow.json`, `/api/imbalance/{timeframe}.json`

1. **Delta Divergence** - When price goes up but the order flow delta doesn't confirm, is that meaningful? Classic order flow concept - worth checking if it actually works here.

2. **Absorption Patterns** - Heavy buying but price not moving could mean sellers are absorbing. Or it could mean nothing. The order flow data lets you investigate.

3. **Extreme Imbalances** - When buy/sell imbalance gets really one-sided, what tends to happen next? Continuation? Reversal? Find out.

---

## 08_trades.py - Recent Trades

**Endpoint:** `/api/trades.json`, `/api/large_trades.json`

1. **Large Trade Clusters** - When multiple large trades hit in the same direction in a short window, does that momentum mean anything? Or is it just noise?

2. **Trade Size Trends** - Is the average trade size going up or down? Does that correlate with price direction or trend strength? Interesting question.

3. **Recent vs Old Trades** - Maybe recent trades matter more than older ones. Maybe not. You could weight them differently and see what kind of signals emerge.

---

## 09_smart_money.py - Smart Money Rankings

**Endpoint:** `/api/smart_money/rankings.json`, `/api/smart_money/signals_{timeframe}.json`

1. **Following Top Performers** - The API ranks traders by performance. Does following the top performers actually work going forward? Or is past performance just that - past?

2. **Fading Poor Performers** - If you know who's consistently losing money, maybe fading them has edge? Classic contrary indicator concept. Test it.

3. **Smart vs Dumb Disagreement** - When the best traders and worst traders are positioned opposite each other, who tends to be right? Might be an interesting divergence to track.

---

## 10_user_positions.py - Any Wallet's Positions

**Endpoint:** `/api/user/{address}/positions`

1. **Tracking Specific Wallets** - You can see any wallet's positions. If you identify traders who seem consistently good, what are they holding? Does tracking them help?

2. **Position Size Changes** - When someone you're watching significantly increases or decreases a position, does that tell you anything? Maybe they know something, maybe they don't.

3. **Portfolio Rotation** - If you watch how certain wallets rotate between assets over time, are there patterns? Do they rotate before moves happen?

---

## 11_user_fills.py - Trade History

**Endpoint:** `/api/user/{address}/fills`

1. **Win Rate Analysis** - You can calculate any wallet's historical win rate from their fills. Does a high historical win rate predict future performance? Worth checking.

2. **Entry Style Study** - How do profitable traders enter positions? All at once? Scaled in? Does their entry style correlate with outcomes?

3. **Exit Patterns** - When do good traders take profits? When do they cut losses? Studying their fills might reveal discipline patterns worth learning from.

---

## 12_hlp_positions.py - HLP Protocol Positions

**Endpoint:** `/api/hlp/positions`

1. **HLP as Counter-Indicator** - HLP takes the other side of retail trades. If you can see what HLP is positioned, you know what retail is doing. Is fading retail profitable?

2. **Strategy Disagreement** - HLP has multiple strategies. When they're positioned differently on the same asset, what does that mean? Confusion? Hedging? Opportunity?

3. **HLP Position Size** - When HLP builds an unusually large position in one coin, does that tell you anything about market conditions or expected moves?

---

## 13_binance_liquidations.py - Binance Liquidations

**Endpoint:** `/api/binance_liquidations/{timeframe}.json`

1. **Cross-Exchange Patterns** - When Binance has liquidations but Hyperliquid doesn't (or vice versa), does that divergence mean anything? Does one exchange lead the other?

2. **Exchange Comparison** - Do liquidations hit different exchanges at different times? Is there a consistent leader/follower relationship?

3. **Binance as Indicator** - Binance is bigger. Maybe their liquidation data predicts what happens on smaller venues? Or maybe not. Check it out.

---

## 14_multi_liquidations.py - All Exchange Liquidations

**Endpoint:** `/api/all_liquidations/{timeframe}.json`

1. **Global Liquidation Events** - When liquidations spike across ALL exchanges simultaneously, that's a market-wide event. What typically follows? The data can tell you.

2. **Liquidation Sequencing** - Which exchange gets hit first during cascade events? Is there a pattern to the order? Could that be useful?

3. **Isolated vs Correlated** - When only one exchange has liquidations but others don't, that's different from correlated liquidations. Different situations, maybe different plays.

---

## 15_buyers.py - Buyer Tracker

**Endpoint:** `/api/buyers.json` ($5k+ buyers, HYPE/SOL/XRP/ETH only)

1. **Buyer Count Trends** - Is the number of unique buyers increasing or decreasing? Does buyer count correlate with future price moves? Accumulation vibes?

2. **Buyer Concentration** - If most buying is coming from just a few addresses, that's different from broad-based buying. Does the concentration tell you anything?

3. **Buyers vs Price** - When buyer count goes up but price doesn't, what's happening? Vice versa? The relationship might be interesting.

---

## 16_depositors.py - All Hyperliquid Depositors

**Endpoint:** `/api/depositors.json`

1. **New User Growth** - Are new depositors joining Hyperliquid at an increasing or decreasing rate? Does user growth correlate with market conditions?

2. **Depositor Size Distribution** - Are the new depositors mostly small fish or big players? Does the composition of new users tell you anything about what's coming?

3. **Net Flow Direction** - Overall, is money flowing into Hyperliquid or out of it? Could be a macro indicator worth tracking.

---

## 17_hlp_sentiment.py - HLP Z-Score Signals

**Endpoint:** `/api/hlp/sentiment`

1. **Extreme Z-Scores** - The z-score shows how unusual HLP's positioning is. When it's way out there (very positive or very negative), does that mean retail is about to get squeezed? Maybe. Investigate.

2. **Mean Reversion Tendencies** - Extreme z-scores probably don't stay extreme forever. How quickly do they revert? What happens during the reversion?

3. **Multi-Timeframe Comparison** - Is the short-term z-score saying the same thing as the longer-term one? When they align vs diverge, does that matter?

---

## 18_hlp_analytics.py - HLP Deep Analytics

**Endpoint:** `/api/hlp/liquidators/status`, `/api/hlp/market-maker`, `/api/hlp/timing`

1. **Liquidator Status** - When HLP liquidators go active vs idle, what typically happens in the market? Is there a pattern worth knowing?

2. **Timing Patterns** - HLP timing data shows profitability by hour/session. Are there consistently good or bad times to trade? Maybe, maybe not. Look at the data.

3. **Market Maker Positioning** - How is the HLP market maker positioned? Does their positioning tell you anything about expected moves or volatility?

---

## 19_market_data.py - Rate-Limit-Free Market Data

**Endpoint:** `/api/prices`, `/api/orderbook/{coin}`, `/api/account/{address}`

1. **Orderbook Imbalances** - You can see orderbooks for all coins. When bids and asks are really unbalanced, does that predict short-term direction? Or is it just market maker games?

2. **Cross-Coin Correlations** - With all prices available, you can track correlations in real-time. When correlations break down, is that opportunity or noise?

3. **Account Watching** - No rate limits means you can watch multiple accounts' positions without getting throttled. What could you learn from that?

---

## 20_hip3_liquidations.py - TradFi Liquidations

**Endpoint:** `/api/hip3_liquidations/{timeframe}.json`

1. **Stock Liquidation Patterns** - TSLA, NVDA, and other stocks have liquidations on Hyperliquid now. Do liquidation spikes in stocks behave similarly to crypto? Or differently?

2. **TradFi-Crypto Relationship** - When stock positions are getting liquidated, does anything happen in crypto? Or vice versa? Cross-asset relationships could be interesting.

3. **Category Shifts** - Liquidations move between stocks, commodities, indices. When one category heats up, does it tell you anything about macro sentiment?

---

## 21_hip3_market_data.py - Multi-Dex TradFi Data

**Endpoint:** `/api/hip3_ticks/stats.json`, `/api/hip3_ticks/{dex}_{ticker}.json`

1. **Cross-Dex Price Differences** - Some assets trade on multiple dexes. Do prices diverge? If so, does convergence happen? Could be interesting to watch.

2. **Pre-IPO Activity** - OPENAI, ANTHROPIC, SPACEX trade as pre-IPO on Hyperliquid. What does activity in these markets tell you about sentiment? Anything?

3. **Trading Hours Patterns** - Stocks on Hyperliquid - do they behave differently during traditional market hours vs after hours? The tick data can show you.

---

## 22_hip3_dashboard.py - HIP3 Combined Dashboard

**Endpoint:** Multiple HIP3 endpoints combined

1. **Cross-Asset Momentum** - With all 58 HIP3 symbols visible, can you identify which sectors are gaining momentum? Is sector rotation a thing here?

2. **Liquidations vs Price Movement** - When a sector has heavy liquidations but prices haven't moved proportionally, is tension building? Or is it just noise?

3. **Combined Sentiment** - Could you build some kind of aggregate sentiment from all this HIP3 data? What would that even look like? Fun to explore.

---

## 29_btc_bulk_liquidations_csv.py - BTC Liquidation Monitor

**Endpoint:** `/api/all_liquidations/10m.json` (filtered to BTC, chopped to 5 min)

1. **5-Minute Liquidation Anticipation** - While the current 5-minute window is playing out, start anticipating the NEXT 5 minutes. If you see a cascade of long liquidations accelerating, the next 5 minutes likely has more long liquidations coming. Use the rate of change in liquidation volume to predict what's about to happen, not just what already happened.

2. **Liquidation Momentum Prediction** - Track liquidation volume per minute within your 5-minute window. If minute 4 has 3x the liquidations of minute 1, momentum is building and the next window will likely be even bigger. If it's decaying, the cascade is exhausting.

3. **Pre-Position for the Next Wave** - When BTC liquidations are one-sided (e.g., all longs getting rekt), the market is likely headed further in that direction short-term. Anticipate the next 5-minute window by looking at the current trend and positioning before the next wave hits.

---

## Moon Dev's 5-Minute BTC Trading Setup

**The Bot:**
```bash
python /Users/md/Dropbox/dev/github/Polymarket-Trading-Bots/poly_hyper/easy.py
```

**Data Sources (run these alongside the bot):**
```bash
# BTC positions close to liquidation (1% and 2% zones, refreshes 5s)
python 30_btc_near_liquidation.py

# BTC liquidation stream across all exchanges (refreshes 5s)
python 31_btc_liquidation_stream.py

# BTC liquidation monitor + CSV logger (5 min window, refreshes 5s)
python 29_btc_bulk_liquidations_csv.py

# BTC CVD scanner - order flow, imbalance, divergence alerts (refreshes 5s)
python examples/32_btc_cvd_scanner.py
```

---

## Final Thoughts

Look, all of these ideas might be garbage. Or some might be gold. The point is you have access to data that used to be hidden, and now you can actually test hypotheses instead of just guessing.

**The process:**
1. See an interesting idea
2. Pull the data
3. Look at it with your own eyes
4. If there's something there, backtest it properly
5. If it still looks good, paper trade it
6. Only then consider real money

Don't skip steps. Don't assume any of this works. Do the work.

The API gives you the data. What you do with it is up to you.

---

Built with love by Moon Dev | api.moondev.com

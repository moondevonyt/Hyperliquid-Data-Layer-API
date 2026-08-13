"""
🌙 Moon Dev's API Handler
Built with love by Moon Dev 🚀

API Documentation: https://moondev.com/docs

Available Endpoints:
-------------------
CORE:
- /health                               - Service health check (no auth)
- /api/liquidations/{timeframe}.json    - Liquidation data (10m, 1h, 4h, 12h, 24h, 2d, 7d, 14d, 30d)
- /api/liquidations/stats.json          - Aggregated liquidation stats
- /api/positions.json                   - Top 50 longs/shorts across ALL symbols (crypto + HIP-3 combined, updates every 1s)
- /api/positions/all.json               - All 182 symbols with top 50 positions each (crypto + HIP-3 combined, updates every 60s)
  SDK Methods for SEPARATE access:
  - get_crypto_positions()              - Crypto-only positions (BTC, ETH, SOL, HYPE, etc.)
  - get_hip3_positions()                - HIP-3-only positions (xyz:GOLD, cash:TSLA, etc.)
  - get_all_crypto_positions()          - All crypto symbols only (134 symbols)
  - get_all_hip3_positions()            - All HIP-3 symbols only (48 symbols)
- /api/whales.json                      - Recent whale trades ($25k+)
- /api/whale_addresses.txt              - Plain text whale address list
- /api/events.json                      - Real-time blockchain events
- /api/contracts.json                   - Contract registry with metadata

TICK DATA:
- /api/ticks/stats.json                 - Collection stats and summary
- /api/ticks/latest.json                - Current prices for all symbols
- /api/ticks/{symbol}_{timeframe}.json  - Historical ticks (symbols: btc, eth, hype, sol, xrp)
                                          (timeframes: 10m, 1h, 4h, 24h, 7d)
- /api/universe                         - Tracked perp universe + tick coverage metadata
- /api/bars                             - Bulk OHLCV-style bars for multiple symbols
- /api/bars/{symbol}                    - OHLCV-style bars for a single symbol

ORDER FLOW & TRADES (tracking: BTC, ETH, HYPE, SOL, XRP):
- /api/trades.json                      - Recent 500 trades (real-time)
- /api/large_trades.json                - Large trades >$100k (24h)
- /api/orderflow.json                   - Order flow imbalance by timeframe + per coin
- /api/orderflow/stats.json             - Service stats (uptime, trades/sec)
- /api/imbalance/5m.json                - 5-min buy/sell imbalance
- /api/imbalance/15m.json               - 15-min imbalance
- /api/imbalance/1h.json                - 1-hour imbalance
- /api/imbalance/4h.json                - 4-hour imbalance
- /api/imbalance/24h.json               - 24-hour imbalance

SMART MONEY:
- /api/smart_money/rankings.json        - Top 100 smart + Bottom 100 dumb money
- /api/smart_money/leaderboard.json     - Top 50 performers with details
- /api/smart_money/signals_10m.json     - Trading signals (10 min)
- /api/smart_money/signals_1h.json      - Trading signals (1 hour)
- /api/smart_money/signals_24h.json     - Trading signals (24 hour)

MULTI-EXCHANGE LIQUIDATIONS:
- /api/all_liquidations/{timeframe}.json     - Combined liquidations from ALL exchanges
- /api/all_liquidations/stats.json           - Combined stats across all exchanges
- /api/all_liquidations/totals.json          - Rolling totals w/ long/short split (5m, 15m, 1h, 2h, 3h, 4h)
- /api/binance_liquidations/{timeframe}.json - Binance Futures liquidations
- /api/bybit_liquidations/{timeframe}.json   - Bybit liquidations
- /api/okx_liquidations/{timeframe}.json     - OKX liquidations
  (timeframes: 10m, 1h, 4h, 12h, 24h, 2d, 7d, 14d, 30d)

HIP3 LIQUIDATIONS (Stocks, Commodities, Indices, FX):
- /api/hip3_liquidations/{timeframe}.json    - HIP3 liquidations (10m, 1h, 24h, 7d)
- /api/hip3_liquidations/stats.json          - HIP3 liquidation statistics
  Categories: Stocks (TSLA, NVDA, AAPL, etc.), Commodities (GOLD, SILVER, OIL),
              Indices (XYZ100), FX (EUR, JPY)

HIP3 MARKET DATA (Multi-Dex: Stocks, Commodities, Indices, FX, Crypto, Pre-IPO):
- /api/hip3/meta                             - All HIP3 symbols with current prices (auto-discovers new symbols)
- /api/hip3/prices                           - Latest prices for ALL 136+ tracked symbols (every dex)
- /api/hip3/price/{coin}                     - Single-symbol latest price (bare ticker or dex:ticker)
- /api/hip3/ticks/{coin}                     - Raw ticks for ANY HIP3 symbol (on-demand from tick DB)
- /api/hip3/candles/{coin}                   - OHLCV candles for ANY HIP3 symbol (computed live)
- /api/hip3/candles/symbols                  - List of all tracked HIP3 symbols (currently 136)
- /api/hip3_ticks/stats.json                 - Legacy collector stats
- /api/hip3_ticks/{dex}_{ticker}.json        - Legacy static-file ticks (top 10 only, kept for back-compat)
  Dexes: xyz, flx, vntl, hyna, km, cash, para (7 total — every HIP3 dex on HyperLiquid)

HYPERLIQUID USER DATA:
- get_user_positions(address)           - Get positions via Hyperliquid API (direct)

MOON DEV USER API (from local node - FAST!):
- /api/user/{address}/positions         - Get positions via Moon Dev API
- /api/user/{address}/fills             - Get historical fills (limit: 100-2000, -1 for all)

MARKET DATA (replaces Hyperliquid rate-limited calls!):
- /api/prices                           - All 224 coin prices + funding rates + open interest
- /api/price/{coin}                     - Quick price for single coin (best bid/ask/mid/spread)
- /api/orderbook/{coin}                 - Full L2 orderbook (~20 levels each side)
- /api/account/{address}                - Full account state (positions, margin, withdrawable)
- /api/fills/{address}                  - Trade fills in Hyperliquid-compatible format
- /api/candles/{coin}                   - OHLCV candles (1m, 5m, 15m, 1h, 4h, 1d)

HYPERLIQUID DIRECT-PROXY (drop-in for HL SDK - tries local node, falls back to public):
- /api/hl/clearinghouse/{address}       - Alias of /api/account - replaces info.user_state()
                                          (optional: ?dex=<name> for a perp dex; empty = main)
- /api/hl/open_orders/{address}         - Resting orders - replaces info.open_orders()
                                          (optional: ?coin=BTC server-side filter)

HLP (HYPERLIQUIDITY PROVIDER) DATA:
- /api/hlp/positions                    - All 7 HLP strategy positions + combined net exposure
                                          (optional: ?include_strategies=false for summary only)
- /api/hlp/positions/history            - Position snapshots over time
- /api/hlp/liquidators                  - Liquidator activation events
- /api/hlp/deltas                       - Net exposure changes over time
- /api/hlp/sentiment                    - THE BIG ONE! Net delta with z-scores and signals
- /api/hlp/liquidators/status           - Real-time liquidator status (active/idle + PnL)
- /api/hlp/market-maker                 - Strategy B tracker for BTC/ETH/SOL
- /api/hlp/timing                       - Hourly/session profitability analysis
- /api/hlp/correlation                  - Delta-price correlation by coin

RETIRED 2026-08-13 (these now return HTTP 410 Gone - use sentiment/positions instead):
- /api/hlp/funding, /api/hlp/funding/hip3, /api/hlp/trades, /api/hlp/trades/stats

POLYMARKET:
- /api/poly/profitable-traders          - Profitable Polymarket traders sorted by 7-day P&L ($300+ threshold)
- /api/poly/whales                      - Live whale trade log ($1,000+ fills, newest first)
- /api/poly/whales/top-traders          - Whale leaderboard by wallet
- /api/poly/whales/top-markets          - Whale leaderboard by market
- /api/poly/whales/daily                - Per-day rollup of whale activity (charting)
- /api/poly/whales/health               - Whale ingestion service status (no auth)
- /api/poly/health                      - Polymarket service health check (no auth)

Authentication:
--------------
- Header (recommended): X-API-Key: YOUR_API_KEY
- Query param: ?api_key=YOUR_API_KEY

Rate Limits: 3,600 requests/min | Data updates every 30 seconds | 60-day retention

Need an API key? https://moondev.com
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class MoonDevAPI:
    """🌙 Moon Dev's API Client"""

    def __init__(self, api_key=None, base_url="https://api.moondev.com"):
        self.api_key = api_key or os.getenv('MOONDEV_API_KEY')
        self.base_url = base_url
        self.headers = {'X-API-Key': self.api_key} if self.api_key else {}
        self.session = requests.Session()

    def _get(self, endpoint, auth_required=True, params=None):
        """Make GET request to API"""
        url = f"{self.base_url}{endpoint}"
        headers = self.headers if auth_required else {}

        response = self.session.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response

    # ==================== HEALTH ====================
    def health(self):
        """Check API health status (no auth required)"""
        response = self._get("/health", auth_required=False)
        return response.json()

    # ==================== LIQUIDATIONS ====================
    def get_liquidations(self, timeframe="1h"):
        """Get liquidation data for specified timeframe (10m, 1h, 4h, 12h, 24h, 2d, 7d, 14d, 30d)"""
        response = self._get(f"/api/liquidations/{timeframe}.json")
        return response.json()

    def get_liquidation_stats(self):
        """Get aggregated liquidation stats across all timeframes"""
        response = self._get("/api/liquidations/stats.json")
        return response.json()

    # ==================== POSITIONS ====================
    def get_positions(self):
        """Get large positions near liquidation ($200k+) - top 50 across ALL symbols (crypto + HIP-3 combined)"""
        response = self._get("/api/positions.json")
        return response.json()

    def get_all_positions(self):
        """Get ALL positions for all symbols - top 50 longs/shorts per symbol (crypto + HIP-3 combined)

        Returns dict with symbols key containing all symbol data.
        Access specific symbol: data['symbols']['BTC'], data['symbols']['HYPE'], etc.
        HIP-3 symbols have a colon prefix: data['symbols']['xyz:GOLD'], data['symbols']['cash:TSLA'], etc.
        """
        response = self._get("/api/positions/all.json")
        return response.json()

    def get_crypto_positions(self):
        """Get large CRYPTO-ONLY positions near liquidation - filters out HIP-3 symbols

        Moon Dev's separate crypto position feed - only Hyperliquid perp symbols like BTC, ETH, SOL, HYPE, etc.
        """
        data = self.get_positions()
        if not isinstance(data, dict):
            return data
        # Filter out HIP-3 symbols (they have ':' in the coin name like xyz:GOLD, cash:TSLA)
        data['longs'] = [p for p in data.get('longs', []) if ':' not in p.get('coin', '')]
        data['shorts'] = [p for p in data.get('shorts', []) if ':' not in p.get('coin', '')]
        data['total_longs'] = len(data['longs'])
        data['total_shorts'] = len(data['shorts'])
        data['total_positions'] = data['total_longs'] + data['total_shorts']
        return data

    def get_hip3_positions(self):
        """Get large HIP-3-ONLY positions near liquidation - stocks, commodities, indices, FX

        Moon Dev's separate HIP-3 position feed - only HIP-3 symbols like xyz:GOLD, cash:TSLA, xyz:NVDA, etc.
        Dex prefixes: xyz (stocks/commodities), cash (stocks/commodities), flx, hyna, km (indices)
        """
        data = self.get_positions()
        if not isinstance(data, dict):
            return data
        # Filter to only HIP-3 symbols (they have ':' in the coin name)
        data['longs'] = [p for p in data.get('longs', []) if ':' in p.get('coin', '')]
        data['shorts'] = [p for p in data.get('shorts', []) if ':' in p.get('coin', '')]
        data['total_longs'] = len(data['longs'])
        data['total_shorts'] = len(data['shorts'])
        data['total_positions'] = data['total_longs'] + data['total_shorts']
        return data

    def get_all_crypto_positions(self):
        """Get ALL crypto-only positions - filters out HIP-3, returns only Hyperliquid perp symbols

        Returns dict with symbols key containing only crypto symbol data (BTC, ETH, SOL, HYPE, etc.)
        """
        data = self.get_all_positions()
        if not isinstance(data, dict) or 'symbols' not in data:
            return data
        crypto_symbols = {k: v for k, v in data['symbols'].items() if ':' not in k}
        data['symbols'] = crypto_symbols
        data['total_symbols'] = len(crypto_symbols)
        return data

    def get_all_hip3_positions(self):
        """Get ALL HIP-3-only positions - stocks, commodities, indices, FX from all dexes

        Returns dict with symbols key containing only HIP-3 symbol data.
        Symbols use dex:ticker format: xyz:GOLD, cash:TSLA, xyz:NVDA, km:USA500, etc.
        """
        data = self.get_all_positions()
        if not isinstance(data, dict) or 'symbols' not in data:
            return data
        hip3_symbols = {k: v for k, v in data['symbols'].items() if ':' in k}
        data['symbols'] = hip3_symbols
        data['total_symbols'] = len(hip3_symbols)
        return data

    # ==================== WHALES ====================
    def get_whales(self):
        """Get recent whale trades ($25k+)"""
        response = self._get("/api/whales.json")
        return response.json()

    def get_whale_addresses(self):
        """Get plain text list of known whale addresses"""
        response = self._get("/api/whale_addresses.txt")
        addresses = response.text.strip().split('\n')
        return [addr.strip() for addr in addresses if addr.strip()]

    def get_buyers(self):
        """Get recent $5k+ buyers on HYPE/SOL/XRP/ETH (buyers only, no sells)"""
        response = self._get("/api/buyers.json")
        return response.json()

    def get_depositors(self):
        """Get all Hyperliquid depositors - canonical list of every address that bridged USDC"""
        response = self._get("/api/depositors.json")
        return response.json()

    # ==================== EVENTS ====================
    def get_events(self):
        """Get real-time blockchain events (Transfers, Swaps, Deposits, etc.)"""
        response = self._get("/api/events.json")
        return response.json()

    # ==================== CONTRACTS ====================
    def get_contracts(self):
        """Get contract registry with metadata and activity tracking"""
        response = self._get("/api/contracts.json")
        return response.json()

    # ==================== TICK DATA ====================
    def get_tick_stats(self):
        """Get tick data collection stats and summary"""
        response = self._get("/api/ticks/stats.json")
        return response.json()

    def get_tick_latest(self):
        """Get latest prices for all symbols"""
        response = self._get("/api/ticks/latest.json")
        return response.json()

    def get_ticks(self, symbol="BTC", duration="1h", limit=10000, start_time=None, end_time=None):
        """
        Get historical tick data for any of 80 tracked symbols.

        Args:
            symbol: Any tracked symbol (BTC, ETH, SOL, DOGE, FARTCOIN, TRUMP, etc.)
                   Use get_candle_symbols() to see all 80 available symbols
            duration: Time window - 10m, 1h, 4h, 24h, 7d (default: 1h)
            limit: Max ticks to return (default: 10000)
            start_time: Start time in Unix ms (optional, overrides duration)
            end_time: End time in Unix ms (optional)

        Returns:
            dict with:
                - symbol: Symbol queried
                - duration: Time window
                - tick_count: Number of ticks returned
                - latest_price: Most recent price
                - ticks: List of tick objects [{t, p, sz?, side?, dt}, ...]

        Tick payload notes:
            - Newer post-rollout rows may include real trade size in `sz`
            - `side` may be present when the upstream trade stream provides it
            - Older historical rows may be price-only and omit `sz` / `side`
        """
        params = [f"duration={duration}", f"limit={limit}"]
        if start_time is not None:
            params.append(f"startTime={start_time}")
        if end_time is not None:
            params.append(f"endTime={end_time}")
        query = "?" + "&".join(params)
        response = self._get(f"/api/ticks/{symbol.upper()}{query}")
        return response.json()

    def get_universe(self):
        """
        Get the tracked symbol universe and tick coverage metadata.

        Returns:
            dict from /api/universe with the active symbol list and metadata.
        """
        response = self._get("/api/universe")
        return response.json()

    def get_bars(self, symbols=None, interval="1h", start_time=None, end_time=None, limit=None):
        """
        Get OHLCV-style bars for one or more symbols from the new bars endpoint.

        Args:
            symbols: Optional list/tuple of symbols or comma-separated string
            interval: Bar interval, typically 1m/5m/15m/1h/4h/1d depending on service support
            start_time: Start timestamp in ms
            end_time: End timestamp in ms
            limit: Optional max bars to return

        Returns:
            dict from /api/bars

        Note:
            The server-side bars implementation currently derives bars from tick data.
            Volume is expected to be "0" for now, while "n" represents tick count.
        """
        params = [f"interval={interval}"]
        if symbols:
            if isinstance(symbols, (list, tuple, set)):
                symbol_str = ",".join(str(s).upper() for s in symbols)
            else:
                symbol_str = str(symbols)
            params.append(f"symbols={symbol_str}")
        if start_time is not None:
            params.append(f"startTime={start_time}")
        if end_time is not None:
            params.append(f"endTime={end_time}")
        if limit is not None:
            params.append(f"limit={limit}")
        query = "?" + "&".join(params) if params else ""
        response = self._get(f"/api/bars{query}")
        return response.json()

    def get_bars_symbol(self, symbol, interval="1h", start_time=None, end_time=None, limit=None):
        """
        Get OHLCV-style bars for a single symbol from /api/bars/{symbol}.

        Args:
            symbol: Requested symbol, e.g. BTC
            interval: Bar interval
            start_time: Start timestamp in ms
            end_time: End timestamp in ms
            limit: Optional max bars to return

        Returns:
            dict or list, depending on server response format.
        """
        params = [f"interval={interval}"]
        if start_time is not None:
            params.append(f"startTime={start_time}")
        if end_time is not None:
            params.append(f"endTime={end_time}")
        if limit is not None:
            params.append(f"limit={limit}")
        query = "?" + "&".join(params) if params else ""
        response = self._get(f"/api/bars/{symbol.upper()}{query}")
        return response.json()

    # ==================== ORDER FLOW & TRADES ====================
    def get_trades(self):
        """Get recent 500 trades (real-time)"""
        response = self._get("/api/trades.json")
        return response.json()

    def get_large_trades(self):
        """Get large trades >$100k (24h)"""
        response = self._get("/api/large_trades.json")
        return response.json()

    def get_orderflow(self):
        """Get order flow imbalance by timeframe + per coin"""
        response = self._get("/api/orderflow.json")
        return response.json()

    def get_orderflow_stats(self):
        """Get order flow service stats (uptime, trades/sec)"""
        response = self._get("/api/orderflow/stats.json")
        return response.json()

    def get_imbalance(self, timeframe="1h"):
        """Get buy/sell imbalance (5m, 15m, 1h, 4h, 24h)"""
        response = self._get(f"/api/imbalance/{timeframe}.json")
        return response.json()

    # ==================== USER POSITIONS (HYPERLIQUID) ====================
    def get_user_positions(self, address):
        """
        Get all open positions for a specific Hyperliquid wallet address.

        Args:
            address: Hyperliquid wallet address (e.g., "0x...")

        Returns:
            dict with 'assetPositions' list and 'marginSummary'

        Example response structure:
            {
                'assetPositions': [
                    {
                        'position': {
                            'coin': 'BTC',
                            'szi': '0.5',  # size (positive=long, negative=short)
                            'entryPx': '45000.0',
                            'positionValue': '22500.0',
                            'unrealizedPnl': '500.0',
                            'liquidationPx': '40000.0',
                            'leverage': {'value': 10}
                        }
                    }
                ],
                'marginSummary': {
                    'accountValue': '50000.0',
                    'totalNtlPos': '22500.0'
                }
            }
        """
        url = "https://api.hyperliquid.xyz/info"
        payload = {"type": "clearinghouseState", "user": address}

        print(f"📡 Moon Dev: Fetching positions for {address[:6]}...{address[-4:]}")
        response = self.session.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    # ==================== MOON DEV USER API (LOCAL NODE) ====================
    def get_user_positions_api(self, address):
        """
        Get all open positions for a Hyperliquid wallet via Moon Dev's API.

        This uses Moon Dev's local node data - faster and includes additional processing.

        Args:
            address: Hyperliquid wallet address (e.g., "0x...")

        Returns:
            dict with positions, margin summary, and account details
        """
        response = self._get(f"/api/user/{address}/positions")
        return response.json()

    def get_user_fills(self, address, limit=100):
        """
        Get historical fills/trades for a Hyperliquid wallet via Moon Dev's API.

        This uses Moon Dev's local node data - scans hourly fill archives.
        Extremely fast: ~300ms even for 32,000+ fills!

        Args:
            address: Hyperliquid wallet address (e.g., "0x...")
            limit: Number of fills to return (default: 100, max: 2000, use -1 for ALL fills)

        Returns:
            dict with:
                - fills: list of fill objects with trade details
                - total: total number of fills found
                - limit: limit that was applied
                - address: wallet address queried

        Example fill object:
            {
                'coin': 'BTC',
                'px': '45000.0',           # execution price
                'sz': '0.1',               # size
                'side': 'B',               # B=Buy, S=Sell
                'time': 1704067200000,     # timestamp ms
                'startPosition': '0.5',    # position before
                'dir': 'Open Long',        # direction description
                'closedPnl': '0',          # realized PnL if closing
                'hash': 'abc123...',       # transaction hash
                'tid': 12345,              # trade ID
                'fee': '1.5'               # fee paid
            }
        """
        params = f"?limit={limit}" if limit != 100 else ""
        response = self._get(f"/api/user/{address}/fills{params}")
        return response.json()

    # ==================== POSITION SNAPSHOTS ====================
    def get_position_snapshots(self, symbol, hours=24, limit=1000, min_distance_pct=None, max_distance_pct=None, side=None):
        """
        Get historical position snapshots for positions near liquidation.

        Tracks positions within 15% of liquidation price with minimum $10k value.
        Snapshots are taken every 1 minute.

        Args:
            symbol: Symbol to query (BTC, ETH, SOL, XRP, HYPE)
            hours: Lookback period in hours (default: 24)
            limit: Max records to return (default: 1000)
            min_distance_pct: Filter by minimum distance to liquidation %
            max_distance_pct: Filter by maximum distance to liquidation %
            side: Filter by position side ('long' or 'short')

        Returns:
            dict with snapshots and metadata
        """
        params = f"?hours={hours}&limit={limit}"
        if min_distance_pct is not None:
            params += f"&min_distance_pct={min_distance_pct}"
        if max_distance_pct is not None:
            params += f"&max_distance_pct={max_distance_pct}"
        if side is not None:
            params += f"&side={side}"
        response = self._get(f"/api/position_snapshots/symbol/{symbol}{params}")
        return response.json()

    def get_position_snapshot_stats(self, hours=24):
        """
        Get aggregate statistics for position snapshots across all tracked symbols.

        Args:
            hours: Lookback period in hours (default: 24)

        Returns:
            dict with:
                - overall: total snapshots, unique users, avg distance
                - by_symbol: per-symbol breakdown
                - top_10_closest: positions closest to liquidation
                - scan_metadata: recent scan info
        """
        params = f"?hours={hours}"
        response = self._get(f"/api/position_snapshots/stats{params}")
        return response.json()

    # ==================== MARKET DATA (NO RATE LIMITS!) ====================
    def get_prices(self):
        """
        Get all coin prices, funding rates, and open interest.

        This replaces Hyperliquid's rate-limited metaAndAssetCtxs call.
        No rate limits - goes through Moon Dev's node!

        Returns:
            dict with:
                - timestamp: When data was fetched
                - count: Number of coins (224)
                - prices: Dict of coin -> price (e.g., {"BTC": "93200.0", "ETH": "3175.0"})
                - funding_rates: Dict of coin -> funding rate
                - open_interest: Dict of coin -> open interest
        """
        response = self._get("/api/prices")
        return response.json()

    def get_price(self, coin):
        """
        Get quick price for a single coin.

        Args:
            coin: Coin symbol (e.g., "BTC", "ETH", "SOL")

        Returns:
            dict with:
                - coin: Symbol
                - timestamp: When data was fetched
                - best_bid: Best bid price
                - best_ask: Best ask price
                - best_bid_size: Size at best bid
                - best_ask_size: Size at best ask
                - mid_price: (bid + ask) / 2
                - spread: ask - bid
                - spread_bps: Spread in basis points
        """
        response = self._get(f"/api/price/{coin}")
        return response.json()

    def get_orderbook(self, coin):
        """
        Get full L2 orderbook for a coin (~20 levels each side).

        This replaces Hyperliquid's rate-limited l2Book call.
        No rate limits - goes through Moon Dev's node!

        Args:
            coin: Coin symbol (e.g., "BTC", "ETH", "SOL")

        Returns:
            dict with:
                - coin: Symbol
                - timestamp: When data was fetched
                - levels: [[bids], [asks]] - bids sorted high->low, asks sorted low->high
                  Each level: {"px": price, "sz": size, "n": order_count}
                - best_bid: Best bid price
                - best_ask: Best ask price
                - mid_price: (bid + ask) / 2
                - spread: ask - bid
                - spread_bps: Spread in basis points
                - bid_depth: Number of bid levels
                - ask_depth: Number of ask levels
        """
        response = self._get(f"/api/orderbook/{coin}")
        return response.json()

    def get_account(self, address):
        """
        Get full account state for any Hyperliquid wallet.

        This replaces Hyperliquid's rate-limited clearinghouseState call.
        No rate limits - goes through Moon Dev's node!

        Args:
            address: Wallet address (e.g., "0x...")

        Returns:
            dict with:
                - address: Wallet address
                - timestamp: When data was fetched
                - marginSummary: Account value, total position, margin used
                - crossMarginSummary: Cross margin details
                - assetPositions: List of all open positions with full details
                - withdrawable: Available to withdraw
        """
        response = self._get(f"/api/account/{address}")
        return response.json()

    def get_fills(self, address, limit=100):
        """
        Get trade fills for any wallet in Hyperliquid-compatible format.

        This is the DROP-IN REPLACEMENT for Hyperliquid's userFills call.
        Uses Moon Dev's local node - faster and no rate limits!

        Args:
            address: Wallet address (e.g., "0x...")
            limit: Number of fills to return (default: 100)

        Returns:
            list of fill objects in Hyperliquid format:
            [
                {
                    "tid": 293951512222,      # Trade ID
                    "time": 1768392000752,    # Timestamp (ms)
                    "coin": "BTC",            # Symbol
                    "side": "B" or "A",       # B=Buy, A=Sell (Ask)
                    "px": "94000.0",          # Price
                    "sz": "0.1",              # Size
                    "closedPnl": "100.50",    # Realized PnL
                    "dir": "Open Long",       # Direction description
                    "crossed": false,         # Whether crossed the spread
                    "fee": "1.5",             # Fee paid
                    "oid": 293951512222       # Order ID
                }
            ]
        """
        params = f"?limit={limit}" if limit != 100 else ""
        response = self._get(f"/api/fills/{address}{params}")
        return response.json()

    # ==================== HYPERLIQUID DIRECT-PROXY (drop-in for HL SDK) ====================
    def get_hl_clearinghouse(self, address, dex=""):
        """
        Moon Dev's drop-in replacement for Hyperliquid's info.user_state(address).

        Low-latency, retry-backed proxy to HL's /info clearinghouseState. Tries the
        local HL node first and transparently falls back to api.hyperliquid.xyz on
        failure - so a 200 ALWAYS means real data, never a silent zero from upstream.

        This is an alias of get_account() / /api/account/{address} - identical body.

        Args:
            address: Wallet / sub-account / vault. Case-insensitive, 0x optional.
            dex: Optional perp dex name. Empty string = main perp.

        Returns:
            dict with marginSummary, crossMarginSummary, assetPositions, withdrawable,
            timestamp (ms), and source ("local" or "public"). Numeric values are
            HL-native strings - cast client-side.
        """
        params = {"dex": dex} if dex else None
        response = self._get(f"/api/hl/clearinghouse/{address}", params=params)
        return response.json()

    def get_hl_open_orders(self, address, coin=""):
        """
        Moon Dev's drop-in replacement for Hyperliquid's info.open_orders(address).

        Returns all resting orders for the address. Tries the local HL node first and
        falls back to api.hyperliquid.xyz - a 200 with orders=[] means genuinely flat,
        never a silent [] on upstream failure. Use that as the signal to skip cancel loops.

        Args:
            address: Wallet / sub-account / vault. Case-insensitive, 0x optional.
            coin: Optional server-side coin filter (e.g. "BTC"). Case-insensitive.

        Returns:
            dict with:
                - address: the queried address
                - timestamp: ms since epoch
                - orders: list of resting orders (coin, oid, side, limitPx, sz,
                          origSz, reduceOnly, orderType, tif, cloid, ...)
                - source: "local" or "public"
        """
        params = {"coin": coin} if coin else None
        response = self._get(f"/api/hl/open_orders/{address}", params=params)
        return response.json()

    def get_candle_symbols(self):
        """
        Get list of all 80 tracked symbols available for candles/ticks.

        Symbols are selected based on $750k+ daily volume.

        Returns:
            dict with:
                - symbols: List of symbol strings (e.g., ["AAVE", "BTC", "DOGE", ...])
                - count: Number of tracked symbols (80)
                - volume_threshold: Minimum daily volume for inclusion ($750k)
                - intervals: Available candle intervals (1m, 5m, 15m, 1h, 4h, 1d)
                - symbol_details: Dict with per-symbol metadata
        """
        response = self._get("/api/candles/symbols")
        return response.json()

    def get_candles(self, coin, interval="5m", start_time=None, end_time=None):
        """
        Get OHLCV candles for any of 80 tracked symbols in Hyperliquid-compatible format.

        80 symbols tracked including majors, DeFi, L2s, and memes.
        Use get_candle_symbols() to see full list.

        Categories:
            - Major: BTC, ETH, SOL, XRP, DOGE, LTC, ADA, DOT, LINK, AVAX, BNB...
            - DeFi: AAVE, UNI, CRV, LDO, PENDLE, JUP, MORPHO, ONDO, ENA...
            - L2/Alt L1: ARB, OP, SUI, SEI, APT, NEAR, TON, TIA, MOVE, BERA...
            - Memes: HYPE, FARTCOIN, PUMP, WIF, POPCAT, PENGU, TRUMP...

        Args:
            coin: Any tracked symbol (use get_candle_symbols() for full list)
            interval: Candle interval - 1m, 5m, 15m, 1h, 4h, 1d (default: 5m)
            start_time: Start timestamp in ms (optional)
            end_time: End timestamp in ms (optional)

        Returns:
            list of candle objects:
            [
                {
                    "t": 1767787200000,    # Open time (ms)
                    "T": 1767790799999,    # Close time (ms)
                    "s": "BTC",            # Symbol
                    "i": "5m",             # Interval
                    "o": "92194.5",        # Open price
                    "h": "92232.5",        # High price
                    "l": "92049.5",        # Low price
                    "c": "92056.5",        # Close price
                    "v": "0",              # Volume (from ticks, may be 0)
                    "n": 239               # Number of price updates
                }
            ]
        """
        params = [f"interval={interval}"]
        if start_time is not None:
            params.append(f"startTime={start_time}")
        if end_time is not None:
            params.append(f"endTime={end_time}")
        query = "?" + "&".join(params) if params else ""
        response = self._get(f"/api/candles/{coin}{query}")
        return response.json()

    # ==================== HLP (HYPERLIQUIDITY PROVIDER) ====================
    def get_hlp_positions(self, include_strategies=True):
        """
        Get all HLP (HyperLiquidity Provider) positions across all 7 strategies.

        This endpoint provides a comprehensive view of Hyperliquid's market-making
        strategies including combined net exposure calculations.

        Args:
            include_strategies: If True, include individual strategy breakdowns.
                              If False, return summary only (faster response).

        Returns:
            dict with:
                - summary: Total account value (~$210M), position counts, net exposure
                - combined_positions: NET positions across all strategies (longs - shorts)
                - strategies: Individual HLP strategy details (if include_strategies=True)

        HLP Strategies tracked:
            - HLP Strategy A (main market maker)
            - HLP Strategy B (secondary market maker)
            - HLP Liquidator 1-4 (liquidation bots)
            - HLP Strategy X (experimental)

        Example combined_position:
            {
                'coin': 'BTC',
                'net_size': 10.5,           # positive=net long, negative=net short
                'net_value': 500000.0,      # USD value of net position
                'long_strategies': ['HLP Strategy A'],
                'short_strategies': ['HLP Strategy B'],
                'total_long': 15.0,
                'total_short': 4.5
            }
        """
        params = "" if include_strategies else "?include_strategies=false"
        response = self._get(f"/api/hlp/positions{params}")
        return response.json()

    # RETIRED 2026-08-13 - Moon Dev: get_hlp_trades() and get_hlp_trade_stats() are gone.
    # /api/hlp/trades and /api/hlp/trades/stats now return HTTP 410 Gone.
    # Use get_hlp_sentiment() or get_hlp_positions() instead.

    def get_hlp_position_history(self, hours=24):
        """
        Get historical position snapshots over time.

        Args:
            hours: Number of hours of history (default: 24)

        Returns:
            dict with:
                - snapshots: List of position snapshots with timestamps
                - interval: Time between snapshots
        """
        params = f"?hours={hours}" if hours != 24 else ""
        response = self._get(f"/api/hlp/positions/history{params}")
        return response.json()

    def get_hlp_liquidators(self):
        """
        Get HLP liquidator activation events.

        Monitors when liquidator accounts become active (non-idle).

        Returns:
            dict with:
                - events: List of liquidator activation events
                - liquidators: Current status of each liquidator account
        """
        response = self._get("/api/hlp/liquidators")
        return response.json()

    def get_hlp_deltas(self, hours=24):
        """
        Get HLP net exposure (delta) changes over time.

        Args:
            hours: Number of hours of history (default: 24)

        Returns:
            dict with:
                - deltas: Time series of net exposure values
                - current: Current net exposure
                - change_24h: 24-hour change in exposure
        """
        params = f"?hours={hours}" if hours != 24 else ""
        response = self._get(f"/api/hlp/deltas{params}")
        return response.json()

    def get_hlp_sentiment(self):
        """
        Get HLP sentiment indicator - THE BIG ONE!

        Returns z-scores showing how positioned HLP is vs historical norms.
        Z-score of 2.2 = HLP is 2.2σ more long than usual = retail heavily SHORT.

        Returns:
            dict with:
                - net_delta: Current net exposure
                - z_score: Standard deviations from mean
                - signal: Human readable signal (e.g., "Retail heavily SHORT")
                - percentile: Where current delta falls historically
        """
        response = self._get("/api/hlp/sentiment")
        return response.json()

    def get_hlp_liquidator_status(self):
        """
        Get real-time HLP liquidator status.

        Shows which liquidators are active/idle and their PnL.

        Returns:
            dict with liquidator addresses, status (active/idle), and PnL data
        """
        response = self._get("/api/hlp/liquidators/status")
        return response.json()

    def get_hlp_market_maker(self):
        """
        Get HLP Strategy B market maker tracker for BTC/ETH/SOL.

        Returns:
            dict with market maker positions and activity for major coins
        """
        response = self._get("/api/hlp/market-maker")
        return response.json()

    def get_hlp_timing(self):
        """
        Get HLP timing analysis - hourly/session profitability.

        Returns:
            dict with profitability breakdown by hour and trading session
        """
        response = self._get("/api/hlp/timing")
        return response.json()

    def get_hlp_correlation(self):
        """
        Get HLP delta-price correlation analysis by coin.

        Returns:
            dict with correlation data showing how HLP delta relates to price moves
        """
        response = self._get("/api/hlp/correlation")
        return response.json()

    def get_hlp_delta(self):
        """
        Get live HLP net delta calculation.

        Shows real-time HLP positioning across all vaults.
        Polls every 30 seconds, snapshots every 60 seconds.

        Returns:
            dict with:
                - net_delta: Current net exposure (positive=LONG, negative=SHORT)
                - long_exposure: Total long exposure in USD
                - short_exposure: Total short exposure in USD
                - position_count: Number of positions across vaults
                - timestamp: Last update time
        """
        response = self._get("/api/hlp/delta")
        return response.json()

    def get_hlp_flips(self):
        """
        Get historical HLP flip events (when delta crosses zero).

        A flip occurs when HLP's net delta crosses from long to short
        or vice versa. Each flip is recorded with BTC/ETH price context.

        Returns:
            list of flip events:
            [
                {
                    "datetime": "2026-01-14T15:30:00Z",
                    "from_direction": "long",
                    "to_direction": "short",
                    "from_delta": 500000,
                    "to_delta": -200000,
                    "hold_duration_hours": 4.5,
                    "btc_price": 95000,
                    "eth_price": 3300
                }
            ]
        """
        response = self._get("/api/hlp/flips")
        return response.json()

    def get_hlp_flip_stats(self):
        """
        Get aggregated HLP flip statistics.

        Provides analysis of historical flip patterns including
        average hold durations, flip frequency, and performance metrics.

        Returns:
            dict with:
                - total_flips: Number of recorded flips
                - avg_hold_duration_hours: Average time between flips
                - long_to_short_count: Number of long→short flips
                - short_to_long_count: Number of short→long flips
                - current_direction: Current HLP direction (long/short)
                - current_hold_hours: Hours in current direction
        """
        response = self._get("/api/hlp/flip-stats")
        return response.json()

    # RETIRED 2026-08-13 - Moon Dev: get_hlp_funding_hip3() is gone.
    # /api/hlp/funding and /api/hlp/funding/hip3 now return HTTP 410 Gone.
    # Use get_hlp_sentiment() or get_hlp_positions() instead.

    # ==================== SMART MONEY ====================
    def get_smart_money_rankings(self):
        """Get Top 100 smart money + Bottom 100 dumb money rankings"""
        response = self._get("/api/smart_money/rankings.json")
        return response.json()

    def get_smart_money_leaderboard(self):
        """Get Top 50 performers with details"""
        response = self._get("/api/smart_money/leaderboard.json")
        return response.json()

    def get_smart_money_signals(self, timeframe="1h"):
        """Get smart money trading signals (10m, 1h, 24h)"""
        response = self._get(f"/api/smart_money/signals_{timeframe}.json")
        return response.json()

    # ==================== MULTI-EXCHANGE LIQUIDATIONS ====================
    def get_all_liquidations(self, timeframe="1h"):
        """
        Get COMBINED liquidation data from ALL exchanges (Hyperliquid, Binance, Bybit, OKX).

        Args:
            timeframe: 10m, 1h, 4h, 12h, 24h, 2d, 7d, 14d, 30d

        Returns:
            dict with liquidation events from all exchanges, sorted by USD value
        """
        response = self._get(f"/api/all_liquidations/{timeframe}.json")
        return response.json()

    def get_all_liquidation_stats(self):
        """
        Get combined liquidation stats across ALL exchanges.

        Returns:
            dict with:
                - total_count: Total liquidations across all exchanges
                - total_volume: Combined USD volume
                - by_exchange: Breakdown by exchange (hyperliquid, binance, bybit, okx)
                - by_side: Long vs short breakdown
        """
        response = self._get("/api/all_liquidations/stats.json")
        return response.json()

    def get_all_liquidation_totals(self):
        """
        Get rolling liquidation totals across ALL exchanges with full long/short split.
        Updates every 20 seconds. 🌙 Moon Dev's favorite squeeze detector!

        Returns:
            dict with 'windows' (5m, 15m, 1h, 2h, 3h, 4h), each containing:
                - total_volume_usd / total_count
                - long_volume_usd / long_count
                - short_volume_usd / short_count
                - by_exchange: same breakdown per exchange (binance, bybit, okx, hyperliquid)
        """
        response = self._get("/api/all_liquidations/totals.json")
        return response.json()

    def get_binance_liquidations(self, timeframe="1h"):
        """
        Get Binance Futures liquidation data.

        Args:
            timeframe: 10m, 1h, 4h, 12h, 24h, 2d, 7d, 14d, 30d
        """
        response = self._get(f"/api/binance_liquidations/{timeframe}.json")
        return response.json()

    def get_binance_liquidation_stats(self):
        """
        Get aggregated Binance Futures liquidation statistics.

        Returns:
            dict with:
                - total_count: Total liquidations
                - total_volume: Total USD volume
                - long_count / short_count: By side
                - long_volume / short_volume: USD volume by side
        """
        response = self._get("/api/binance_liquidations/stats.json")
        return response.json()

    def get_bybit_liquidations(self, timeframe="1h"):
        """
        Get Bybit liquidation data.

        Args:
            timeframe: 10m, 1h, 4h, 12h, 24h, 2d, 7d, 14d, 30d
        """
        response = self._get(f"/api/bybit_liquidations/{timeframe}.json")
        return response.json()

    def get_okx_liquidations(self, timeframe="1h"):
        """
        Get OKX liquidation data.

        Args:
            timeframe: 10m, 1h, 4h, 12h, 24h, 2d, 7d, 14d, 30d
        """
        response = self._get(f"/api/okx_liquidations/{timeframe}.json")
        return response.json()

    # ==================== HIP3 LIQUIDATIONS ====================
    def get_hip3_liquidations(self, timeframe="1h"):
        """
        Get HIP3 liquidation data (Stocks, Commodities, Indices, FX).

        HIP3 covers traditional finance assets on Hyperliquid:
        - Stocks: TSLA, NVDA, AAPL, META, MSFT, GOOGL, AMZN, AMD, INTC, PLTR,
                  COIN, HOOD, MSTR, ORCL, MU, NFLX, RIVN, BABA
        - Commodities: GOLD, SILVER, COPPER, CL (Oil), NATGAS, URANIUM
        - Indices: XYZ100 (Nasdaq proxy)
        - FX: EUR, JPY

        Args:
            timeframe: 10m, 1h, 24h, 7d

        Returns:
            list of liquidation events with:
                - symbol: Asset symbol (TSLA, GOLD, etc.)
                - side: 'long' or 'short'
                - size: Position size
                - price: Liquidation price
                - value_usd: USD value of liquidation
                - category: 'stocks', 'commodities', 'indices', or 'fx'
                - timestamp: Event timestamp
        """
        response = self._get(f"/api/hip3_liquidations/{timeframe}.json")
        return response.json()

    def get_hip3_liquidation_stats(self):
        """
        Get HIP3 liquidation statistics.

        Returns:
            dict with:
                - total_count: Total liquidations
                - total_volume: Total USD volume liquidated
                - long_count: Number of long liquidations
                - short_count: Number of short liquidations
                - long_volume: USD volume of long liquidations
                - short_volume: USD volume of short liquidations
                - by_category: Breakdown by category (stocks, commodities, indices, fx)
                - by_symbol: Breakdown by individual symbol
                - top_symbols: Top symbols by liquidation volume
        """
        response = self._get("/api/hip3_liquidations/stats.json")
        return response.json()

    # ==================== HIP3 MARKET DATA (Multi-Dex) ====================
    def get_hip3_meta(self, include_delisted=False):
        """
        Get all HIP3 symbols across every dex with current prices.

        Auto-discovers symbols as HyperLiquid adds them. Currently 136+ symbols
        across 7 dexes:
            - xyz (XYZ): Stocks, commodities, FX, indices (TSLA, NVDA, GOLD, EUR)
            - flx (Felix): Stocks, commodities, crypto (XMR, GOLD, SILVER, OIL)
            - vntl (Ventuals): Pre-IPO + thematic baskets (OPENAI, ANTHROPIC, MAG7, SPACEX)
            - hyna (HyENA): Crypto perps (BTC, ETH, HYPE, SOL, PUMP, FARTCOIN)
            - km (Kinetiq): Asia / US indices (US500, USTECH, TENCENT, XIAOMI)
            - cash (dreamcash): Stocks, commodities, indices
            - para (Paragon): Specialty markets (TOTAL2, etc.)

        Args:
            include_delisted: If True, includes delisted symbols (default: False)

        Returns:
            dict with:
                - total_symbols: Total number of symbols
                - dexes: List of dex prefixes
                - dex_summary: Per-dex active/delisted counts
                - symbols: List of all symbol objects with prices

        Symbol format: {dex}:{ticker} (e.g., xyz:TSLA, hyna:BTC, cash:USA500)
        """
        params = "?include_delisted=true" if include_delisted else ""
        response = self._get(f"/api/hip3/meta{params}")
        return response.json()

    def get_hip3_tick_stats(self):
        """
        [LEGACY] Get HIP3 tick collector stats from the old static-file pipeline.

        Kept for backward compatibility with the top-10-by-volume static files.
        New consumers should use get_hip3_meta() / get_hip3_all_prices() instead.

        Returns:
            dict with total_symbols, total_ticks, by_dex, by_category, last_update
        """
        response = self._get("/api/hip3_ticks/stats.json")
        return response.json()

    def get_hip3_ticks(self, dex, ticker):
        """
        [LEGACY] Get raw tick data from the old static-file endpoint.

        Only top-10 symbols by volume are published this way. For full coverage
        of all 136+ HIP3 symbols, use get_hip3_raw_ticks() instead.

        Args:
            dex: Dex prefix (xyz, flx, hyna, km)
            ticker: Symbol ticker (tsla, btc, gold, us500, etc.) — case insensitive

        Returns:
            dict/list with tick data for the symbol

        Examples:
            get_hip3_ticks("xyz", "tsla")   # Tesla stock
            get_hip3_ticks("hyna", "btc")   # Bitcoin
            get_hip3_ticks("km", "us500")   # S&P 500 index
        """
        response = self._get(f"/api/hip3_ticks/{dex.lower()}_{ticker.lower()}.json")
        return response.json()

    # ==================== HIP3 ON-DEMAND (All Symbols, All Dexes) ====================
    # 🌙 Moon Dev — Full HIP3 coverage: 136+ symbols across 7 dexes, served live from
    # the tick DB. Auto-discovers new symbols as HyperLiquid adds them. 30-day retention.

    def get_hip3_candle_symbols(self):
        """
        List ALL tracked HIP3 symbols (currently 136 across 7 dexes).

        Auto-discovers new symbols as HyperLiquid lists them — no config needed.

        Returns:
            dict with:
                - symbols: List of dex-qualified symbols (e.g., 'xyz:TSLA', 'hyna:BTC')
                - count: Total tracked
                - intervals: Supported candle intervals
                - by_category: Symbols grouped by category (stocks, commodities,
                  indices, fx, crypto, pre_ipo, other)
        """
        response = self._get("/api/hip3/candles/symbols")
        return response.json()

    def get_hip3_raw_ticks(self, coin, duration="1h", limit=None,
                           start_time=None, end_time=None, order=None):
        """
        Get raw ticks for ANY HIP3 symbol — served live from the tick DB.

        Args:
            coin: Symbol — bare ticker (HIMS, TSLA, GOLD) or dex:ticker (xyz:HIMS,
                  cash:USA500, hyna:BTC). Bare tickers auto-resolve to the right dex.
            duration: Time window — 10m, 1h, 4h, 24h, 7d (default 1h)
            limit: Max ticks to return (default 10000)
            start_time: Optional explicit start (Unix ms) — overrides duration
            end_time: Optional explicit end (Unix ms)
            order: 'asc' (oldest-first, default) or 'desc' (newest-first)

        Returns:
            dict with symbol, category, market_type, duration, tick_count, order,
            ticks[]. Each tick has timestamp, price, size, side, datetime.

        Notes:
            - Sub-second freshness, 30-day retention, ~500ms tick resolution
            - 24/7 — HyperLiquid is always open, no market-hours gaps
        """
        params = {"duration": duration}
        if limit is not None: params["limit"] = limit
        if start_time is not None: params["startTime"] = start_time
        if end_time is not None: params["endTime"] = end_time
        if order is not None: params["order"] = order
        response = self._get(f"/api/hip3/ticks/{coin}", params=params)
        return response.json()

    def get_hip3_candles(self, coin, interval="5m", limit=None,
                         start_time=None, end_time=None):
        """
        OHLCV candles for ANY HIP3 symbol, computed live from stored ticks.

        Args:
            coin: Symbol — bare ticker (SILVER, NVDA) or dex:ticker (cash:USA500)
            interval: 1m, 5m, 15m, 1h, 4h, 1d
            limit: Max candles to return (default 200)
            start_time: Optional start (Unix ms)
            end_time: Optional end (Unix ms)

        Returns:
            list of candles in HL convention: {t, T, s, i, o, h, l, c, v, n}
            - t/T: candle start/end (ms)
            - s/i: symbol/interval
            - o/h/l/c: open/high/low/close
            - v: notional volume traded
            - n: tick count in interval
        """
        params = {"interval": interval}
        if limit is not None: params["limit"] = limit
        if start_time is not None: params["startTime"] = start_time
        if end_time is not None: params["endTime"] = end_time
        response = self._get(f"/api/hip3/candles/{coin}", params=params)
        return response.json()

    def get_hip3_price(self, coin):
        """
        Latest price for a single HIP3 symbol.

        Args:
            coin: Symbol — bare ticker (NVDA, HIMS) or dex:ticker (xyz:HIMS).
                  Bare tickers resolve automatically; for ambiguous tickers
                  (GOLD on xyz/flx/km) use the full dex:ticker form.

        Returns:
            dict with symbol, price, category, market_type, timestamp
        """
        response = self._get(f"/api/hip3/price/{coin}")
        return response.json()

    def get_hip3_all_prices(self):
        """
        Latest prices for ALL tracked HIP3 symbols (currently 136 across 7 dexes).

        Returns:
            dict with:
                - generated_at: ISO timestamp
                - market_type: 'HIP3'
                - mode: 'all_symbols_on_demand'
                - dexes: List of dexes covered
                - prices: { 'xyz:TSLA': {...}, 'hyna:BTC': {...}, ... }
        """
        response = self._get("/api/hip3/prices")
        return response.json()

    # ==================== POLYMARKET ====================
    def get_poly_profitable_traders(self):
        """
        Get profitable Polymarket traders sorted by 7-day P&L (highest first).

        Discovers traders from BTC 5-minute prediction markets and trending market
        big trades ($500+). Only traders with $300+ 7-day P&L are included.

        Access tiers:
            - Quant Elite (_qe) keys: Full list of all profitable traders
            - Standard keys: Top 25 traders only

        Returns:
            dict with:
                - total: Number of traders in response
                - full_list: True if showing all traders (QE key)
                - updated_at: ISO 8601 timestamp
                - stats: Service health (wallets_checked, queue_depth, uptime_minutes)
                - traders: List of trader dicts sorted by pnl_7d descending
                    Each trader has: wallet, polymarket_link, pnl_7d, volume_7d,
                    trades_7d, redeems_7d, discovered_at, source

        Note: As of 2026-04-14, `name` and `display_name` fields were removed
        (Polymarket pseudonyms were unreliable). Use `wallet` as the identifier.
        `polymarket_link` is now wallet-based: https://polymarket.com/<wallet>
        """
        response = self._get("/api/poly/profitable-traders")
        return response.json()

    def poly_health(self):
        """Check Polymarket service health (no auth required)"""
        response = self._get("/api/poly/health", auth_required=False)
        return response.json()

    # ==================== POLYMARKET WHALES ====================
    def get_poly_whales(self, min_usd=1000, days=1, wallet=None, market=None,
                        side=None, limit=250):
        """
        Get the live Polymarket whale trade log (individual fills, newest first).

        A background service holds a persistent WebSocket to Polymarket and
        records every trade with USD notional >= $1,000. Anything below $1,000
        is never collected, so min_usd has a hard floor of 1000.

        Args:
            min_usd: Minimum trade size in USD (floor $1,000). Default 1000.
            days:    Lookback window in days. Max 365. Default 1.
            wallet:  Filter to a single proxyWallet address. Default None.
            market:  Filter by market_slug or event_slug. Default None.
            side:    'BUY' or 'SELL'. Default None (both).
            limit:   Max rows. Standard keys capped at 250, _qe keys up to 5,000.

        Returns:
            dict with the whale fills. Each trade includes: ts, wallet,
            pseudonym, market_title, market_slug, event_slug, outcome, side,
            price, size, usd_amount, tx_hash.
        """
        params = {"min_usd": min_usd, "days": days, "limit": limit}
        if wallet:
            params["wallet"] = wallet
        if market:
            params["market"] = market
        if side:
            params["side"] = side
        response = self._get("/api/poly/whales", params=params)
        return response.json()

    def get_poly_whale_top_traders(self, min_usd=1000, days=7, limit=100):
        """
        Get the Polymarket whale leaderboard by wallet (sorted by volume desc).

        Args:
            min_usd: Minimum trade size in USD. Default 1000.
            days:    Lookback window in days. Default 7.
            limit:   Standard keys capped at 50, _qe keys up to 1,000. Default 100.

        Returns:
            dict with per-wallet aggregates: trade_count, total_volume,
            biggest_trade, markets_traded, last_trade_ts.
        """
        params = {"min_usd": min_usd, "days": days, "limit": limit}
        response = self._get("/api/poly/whales/top-traders", params=params)
        return response.json()

    def get_poly_whale_top_markets(self, min_usd=1000, days=7, limit=100):
        """
        Get the Polymarket whale leaderboard by market (sorted by volume desc).

        Args:
            min_usd: Minimum trade size in USD. Default 1000.
            days:    Lookback window in days. Default 7.
            limit:   Max rows. Default 100.

        Returns:
            dict with per-market aggregates: market_slug, event_slug,
            market_title, whale_trades, whale_volume, unique_whales,
            biggest_trade.
        """
        params = {"min_usd": min_usd, "days": days, "limit": limit}
        response = self._get("/api/poly/whales/top-markets", params=params)
        return response.json()

    def get_poly_whale_daily(self, min_usd=1000, days=30):
        """
        Get the per-day rollup of Polymarket whale activity (use for charting).

        Args:
            min_usd: Minimum trade size in USD. Default 1000.
            days:    Lookback window in days. Default 30.

        Returns:
            dict with one row per UTC day: trade_count, total_volume,
            biggest_trade, smallest_trade, avg_trade, unique_whales,
            unique_markets.
        """
        params = {"min_usd": min_usd, "days": days}
        response = self._get("/api/poly/whales/daily", params=params)
        return response.json()

    def poly_whales_health(self):
        """
        Check the Polymarket whale ingestion service status (no auth required).

        Returns live counters: trades_seen, whales_queued, whales_written,
        biggest_usd, biggest_market, ws_connects, ws_disconnects,
        last_trade_at, queue_depth, uptime_minutes. Useful for confirming the
        WebSocket is connected and ingestion is fresh.
        """
        response = self._get("/api/poly/whales/health", auth_required=False)
        return response.json()


# ==================== TEST SUITE ====================
def test_all():
    """🌙 Moon Dev API Mass Test Suite"""

    print("=" * 60)
    print("🌙 Moon Dev API Mass Test Suite 🚀")
    print("=" * 60)

    api = MoonDevAPI()

    if not api.api_key:
        print("❌ No API key found! Set MOONDEV_API_KEY in .env")
        return

    print(f"✅ API Key loaded (ends with ...{api.api_key[-4:]})")
    print()

    # ==================== 1. HEALTH CHECK ====================
    print("=" * 60)
    print("🏥 1. HEALTH CHECK")
    print("=" * 60)
    try:
        health = api.health()
        print(f"✅ Health: {health}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    print()

    # ==================== 2. LIQUIDATIONS ====================
    print("=" * 60)
    print("💥 2. LIQUIDATION DATA")
    print("=" * 60)
    timeframes = ["10m", "1h", "4h", "24h"]
    for tf in timeframes:
        try:
            data = api.get_liquidations(tf)
            if isinstance(data, dict):
                stats = data.get('stats', data)
                total_count = stats.get('total_count', 'N/A')
                total_usd = stats.get('total_value_usd', stats.get('total_usd', 'N/A'))
                if isinstance(total_usd, (int, float)):
                    print(f"✅ {tf}: {total_count:,} liqs | ${total_usd:,.0f}")
                else:
                    print(f"✅ {tf}: {total_count} liquidations")
        except Exception as e:
            print(f"❌ {tf} failed: {e}")
    print()

    # ==================== 3. POSITIONS ====================
    print("=" * 60)
    print("💰 3. LARGE POSITIONS ($200k+)")
    print("=" * 60)
    try:
        positions = api.get_positions()
        if isinstance(positions, dict):
            total = positions.get('total_positions', 0)
            print(f"✅ Found {total} positions tracked")
    except Exception as e:
        print(f"❌ Positions failed: {e}")
    print()

    # ==================== 4. WHALE ADDRESSES ====================
    print("=" * 60)
    print("🐋 4. WHALE ADDRESSES")
    print("=" * 60)
    try:
        addresses = api.get_whale_addresses()
        print(f"✅ Found {len(addresses)} whale addresses")
    except Exception as e:
        print(f"❌ Whale addresses failed: {e}")
    print()

    # ==================== 5. EVENTS ====================
    print("=" * 60)
    print("⚡ 5. BLOCKCHAIN EVENTS")
    print("=" * 60)
    try:
        events = api.get_events()
        if isinstance(events, dict):
            stats = events.get('stats', {})
            total = stats.get('total_events', 0)
            by_type = stats.get('events_by_type', {})
            print(f"✅ Found {total:,} total events")
            print(f"   📊 By type: {', '.join(f'{k}:{v}' for k,v in list(by_type.items())[:5])}")
    except Exception as e:
        print(f"❌ Events failed: {e}")
    print()

    # ==================== 6. CONTRACTS ====================
    print("=" * 60)
    print("📜 6. CONTRACT REGISTRY")
    print("=" * 60)
    try:
        contracts = api.get_contracts()
        if isinstance(contracts, dict):
            contract_list = contracts.get('contracts', [])
            high_value = contracts.get('high_value_count', 0)
            print(f"✅ Found {len(contract_list)} contracts ({high_value} high-value)")
    except Exception as e:
        print(f"❌ Contracts failed: {e}")
    print()

    # ==================== 7. TICK DATA ====================
    print("=" * 60)
    print("📈 7. TICK DATA")
    print("=" * 60)
    try:
        stats = api.get_tick_stats()
        symbols = stats.get('symbols', [])
        collector = stats.get('collector_stats', {})
        ticks = collector.get('ticks_collected', 0)
        print(f"✅ Tick Stats: {ticks:,} ticks collected for {symbols}")
    except Exception as e:
        print(f"⚠️  Tick stats: {e}")

    try:
        latest = api.get_tick_latest()
        print(f"✅ Latest prices:")
        for symbol, price in list(latest.items())[:5]:
            if isinstance(price, (int, float)):
                print(f"   {symbol}: ${price:,.2f}")
            elif isinstance(price, dict):
                p = price.get('price', price.get('last_price', 'N/A'))
                print(f"   {symbol}: ${p:,.2f}" if isinstance(p, (int, float)) else f"   {symbol}: {price}")
    except Exception as e:
        print(f"⚠️  Latest prices: {e}")

    for symbol in ["btc", "eth"]:
        try:
            ticks = api.get_ticks(symbol, "1h")
            if isinstance(ticks, list):
                print(f"✅ {symbol.upper()} 1h ticks: {len(ticks)} records")
            elif isinstance(ticks, dict):
                count = ticks.get('count', len(ticks.get('ticks', [])))
                print(f"✅ {symbol.upper()} 1h ticks: {count} records")
        except Exception as e:
            print(f"⚠️  {symbol} ticks: {e}")
    print()

    # ==================== 8. ORDER FLOW & TRADES ====================
    print("=" * 60)
    print("📊 8. ORDER FLOW & TRADES")
    print("=" * 60)
    try:
        stats = api.get_orderflow_stats()
        print(f"✅ Order Flow Stats: {stats}")
    except Exception as e:
        print(f"⚠️  Order flow stats: {e}")

    try:
        trades = api.get_trades()
        if isinstance(trades, list):
            print(f"✅ Recent trades: {len(trades)} trades")
            for t in trades[:3]:
                symbol = t.get('symbol', t.get('coin', '?'))
                side = t.get('side', '?')
                val = t.get('value', t.get('usd_value', t.get('sz', 0)))
                print(f"   {symbol} {side} ${val:,.0f}" if isinstance(val, (int, float)) else f"   {t}")
        elif isinstance(trades, dict):
            trade_list = trades.get('trades', [])
            print(f"✅ Recent trades: {len(trade_list)} trades")
    except Exception as e:
        print(f"⚠️  Recent trades: {e}")

    try:
        large = api.get_large_trades()
        if isinstance(large, list):
            print(f"✅ Large trades (>$100k): {len(large)} trades")
            for t in large[:3]:
                symbol = t.get('symbol', t.get('coin', '?'))
                side = t.get('side', '?')
                val = t.get('value', t.get('usd_value', 0))
                print(f"   {symbol} {side} ${val:,.0f}" if isinstance(val, (int, float)) else f"   {t}")
        elif isinstance(large, dict):
            trade_list = large.get('trades', [])
            print(f"✅ Large trades: {len(trade_list)} trades")
    except Exception as e:
        print(f"⚠️  Large trades: {e}")

    try:
        orderflow = api.get_orderflow()
        print(f"✅ Order flow: {orderflow}")
    except Exception as e:
        print(f"⚠️  Order flow: {e}")

    for tf in ["5m", "1h", "24h"]:
        try:
            imbalance = api.get_imbalance(tf)
            if isinstance(imbalance, dict):
                buy = imbalance.get('buy_volume', imbalance.get('buy', 0))
                sell = imbalance.get('sell_volume', imbalance.get('sell', 0))
                ratio = imbalance.get('ratio', imbalance.get('imbalance', 'N/A'))
                print(f"✅ {tf} imbalance: Buy ${buy:,.0f} | Sell ${sell:,.0f} | Ratio: {ratio}" if isinstance(buy, (int, float)) else f"✅ {tf} imbalance: {imbalance}")
        except Exception as e:
            print(f"⚠️  {tf} imbalance: {e}")
    print()

    # ==================== 9. SMART MONEY ====================
    print("=" * 60)
    print("🧠 9. SMART MONEY")
    print("=" * 60)
    try:
        rankings = api.get_smart_money_rankings()
        if isinstance(rankings, dict):
            smart = rankings.get('smart_money', rankings.get('top', []))
            dumb = rankings.get('dumb_money', rankings.get('bottom', []))
            print(f"✅ Rankings: {len(smart)} smart | {len(dumb)} dumb money wallets")
    except Exception as e:
        print(f"⚠️  Rankings: {e}")

    try:
        leaderboard = api.get_smart_money_leaderboard()
        if isinstance(leaderboard, dict):
            leaders = leaderboard.get('leaderboard', leaderboard.get('top', []))
            print(f"✅ Leaderboard: {len(leaders)} top performers")
            for l in leaders[:3]:
                addr = l.get('address', '')[:10] + '...' if l.get('address') else 'N/A'
                pnl = l.get('pnl', l.get('total_pnl', 0))
                print(f"   {addr} | PnL: ${pnl:,.0f}" if isinstance(pnl, (int, float)) else f"   {l}")
        elif isinstance(leaderboard, list):
            print(f"✅ Leaderboard: {len(leaderboard)} entries")
    except Exception as e:
        print(f"⚠️  Leaderboard: {e}")

    for tf in ["10m", "1h", "24h"]:
        try:
            signals = api.get_smart_money_signals(tf)
            if isinstance(signals, dict):
                signal_list = signals.get('signals', [])
                print(f"✅ Signals ({tf}): {len(signal_list)} trading signals")
            elif isinstance(signals, list):
                print(f"✅ Signals ({tf}): {len(signals)} trading signals")
        except Exception as e:
            print(f"⚠️  Signals ({tf}): {e}")
    print()

    # ==================== 10. USER POSITIONS (HYPERLIQUID) ====================
    print("=" * 60)
    print("📊 10. USER POSITIONS (HYPERLIQUID)")
    print("=" * 60)
    try:
        # Test with a known active address (HLP_LONG)
        test_address = "0x010461c14e146ac35fe42271bdc1134ee31c703a"
        positions = api.get_user_positions(test_address)
        if isinstance(positions, dict):
            asset_positions = positions.get('assetPositions', [])
            margin = positions.get('marginSummary', {})
            account_value = margin.get('accountValue', 'N/A')
            print(f"✅ Found {len(asset_positions)} positions for {test_address[:10]}...")
            if isinstance(account_value, (int, float, str)):
                print(f"   Account Value: ${float(account_value):,.2f}" if account_value != 'N/A' else f"   Account Value: {account_value}")
            for pos in asset_positions[:3]:
                if 'position' in pos:
                    p = pos['position']
                    coin = p.get('coin', '?')
                    size = float(p.get('szi', 0))
                    pnl = float(p.get('unrealizedPnl', 0))
                    direction = "LONG" if size > 0 else "SHORT"
                    print(f"   {coin} {direction} | PnL: ${pnl:,.2f}")
    except Exception as e:
        print(f"⚠️  User positions: {e}")
    print()

    # ==================== 11. USER FILLS (MOON DEV API) ====================
    print("=" * 60)
    print("📜 11. USER FILLS (MOON DEV LOCAL NODE)")
    print("=" * 60)
    try:
        test_address = "0x010461c14e146ac35fe42271bdc1134ee31c703a"
        fills = api.get_user_fills(test_address, limit=100)
        if isinstance(fills, dict):
            fill_list = fills.get('fills', [])
            total = fills.get('total', len(fill_list))
            print(f"✅ Found {total:,} total fills for {test_address[:10]}...")
            print(f"   Showing last {len(fill_list)} fills")
            for fill in fill_list[:5]:
                coin = fill.get('coin', '?')
                side = fill.get('side', '?')
                side_str = "BUY" if side == 'B' else "SELL"
                px = float(fill.get('px', 0))
                sz = float(fill.get('sz', 0))
                pnl = float(fill.get('closedPnl', 0))
                print(f"   {coin} {side_str} {sz:.4f} @ ${px:,.2f} | PnL: ${pnl:,.2f}")
    except Exception as e:
        print(f"⚠️  User fills: {e}")
    print()

    # ==================== 12. MARKET DATA (NO RATE LIMITS!) ====================
    print("=" * 60)
    print("📈 12. MARKET DATA (NO RATE LIMITS!)")
    print("=" * 60)

    # All Prices
    try:
        prices_data = api.get_prices()
        count = prices_data.get('count', 0)
        prices = prices_data.get('prices', {})
        funding = prices_data.get('funding_rates', {})
        oi = prices_data.get('open_interest', {})
        print(f"✅ All Prices: {count} coins")
        print(f"   BTC: ${prices.get('BTC', 'N/A')} | Funding: {funding.get('BTC', 'N/A')} | OI: {oi.get('BTC', 'N/A')}")
        print(f"   ETH: ${prices.get('ETH', 'N/A')} | Funding: {funding.get('ETH', 'N/A')}")
        print(f"   SOL: ${prices.get('SOL', 'N/A')} | Funding: {funding.get('SOL', 'N/A')}")
    except Exception as e:
        print(f"⚠️  All prices: {e}")

    # Quick Price
    try:
        price_data = api.get_price("BTC")
        print(f"✅ Quick Price (BTC):")
        print(f"   Best Bid: ${price_data.get('best_bid', 'N/A')}")
        print(f"   Best Ask: ${price_data.get('best_ask', 'N/A')}")
        print(f"   Mid Price: ${price_data.get('mid_price', 'N/A')}")
        print(f"   Spread: {price_data.get('spread_bps', 'N/A')} bps")
    except Exception as e:
        print(f"⚠️  Quick price: {e}")

    # Orderbook
    try:
        ob_data = api.get_orderbook("ETH")
        levels = ob_data.get('levels', [[], []])
        print(f"✅ Orderbook (ETH):")
        print(f"   Best Bid: ${ob_data.get('best_bid', 'N/A')} | Best Ask: ${ob_data.get('best_ask', 'N/A')}")
        print(f"   Spread: {ob_data.get('spread_bps', 'N/A')} bps")
        print(f"   Depth: {len(levels[0])} bids, {len(levels[1])} asks")
        if levels[0]:
            top_bid = levels[0][0]
            print(f"   Top Bid Level: ${top_bid.get('px', 'N/A')} x {top_bid.get('sz', 'N/A')} ({top_bid.get('n', 'N/A')} orders)")
    except Exception as e:
        print(f"⚠️  Orderbook: {e}")

    # Account State
    try:
        test_address = "0x010461c14e146ac35fe42271bdc1134ee31c703a"
        account_data = api.get_account(test_address)
        margin = account_data.get('marginSummary', {})
        positions = account_data.get('assetPositions', [])
        print(f"✅ Account State ({test_address[:10]}...):")
        print(f"   Account Value: ${float(margin.get('accountValue', 0)):,.2f}")
        print(f"   Total Position: ${float(margin.get('totalNtlPos', 0)):,.2f}")
        print(f"   Margin Used: ${float(margin.get('totalMarginUsed', 0)):,.2f}")
        print(f"   Positions: {len(positions)}")
        print(f"   Withdrawable: ${float(account_data.get('withdrawable', 0)):,.2f}")
    except Exception as e:
        print(f"⚠️  Account state: {e}")

    # Fills (Hyperliquid-compatible)
    try:
        test_address = "0x010461c14e146ac35fe42271bdc1134ee31c703a"
        fills = api.get_fills(test_address, limit=5)
        print(f"✅ Fills ({test_address[:10]}...): {len(fills)} fills")
        if fills:
            fill = fills[0]
            side = "BUY" if fill.get('side') == 'B' else "SELL"
            print(f"   Latest: {fill.get('coin')} {side} {fill.get('sz')} @ ${fill.get('px')} | PnL: ${fill.get('closedPnl')}")
    except Exception as e:
        print(f"⚠️  Fills: {e}")

    # Candles (OHLCV)
    try:
        candles = api.get_candles("BTC", interval="1h")
        print(f"✅ Candles (BTC 1h): {len(candles)} candles")
        if candles:
            latest = candles[-1]
            print(f"   Latest: O:${latest.get('o')} H:${latest.get('h')} L:${latest.get('l')} C:${latest.get('c')}")
    except Exception as e:
        print(f"⚠️  Candles: {e}")

    # Test all candle symbols
    for symbol in ["ETH", "SOL", "HYPE", "XRP"]:
        try:
            candles = api.get_candles(symbol, interval="1h")
            if candles:
                print(f"   ✅ {symbol}: {len(candles)} candles, close: ${candles[-1].get('c')}")
        except Exception as e:
            print(f"   ⚠️  {symbol}: {e}")

    print()

    # ==================== 13. HLP (HYPERLIQUIDITY PROVIDER) ====================
    print("=" * 60)
    print("🏦 13. HLP (HYPERLIQUIDITY PROVIDER)")
    print("=" * 60)

    # HLP Positions
    try:
        hlp_data = api.get_hlp_positions(include_strategies=False)
        if isinstance(hlp_data, dict):
            summary = hlp_data.get('summary', {})
            total_value = summary.get('total_account_value', 0)
            total_positions = summary.get('total_positions', 0)
            net_exposure = summary.get('net_exposure_delta', 0)
            print(f"✅ HLP Positions:")
            print(f"   Total Account Value: ${total_value:,.0f}")
            print(f"   Total Positions: {total_positions}")
            print(f"   Net Exposure Delta: ${net_exposure:,.0f}")

            combined = hlp_data.get('combined_positions', [])
            if combined:
                print(f"   Top Combined Net Positions:")
                for pos in combined[:3]:
                    coin = pos.get('coin', '?')
                    net_size = pos.get('net_size', 0)
                    net_value = pos.get('net_value', 0)
                    direction = "LONG" if net_size > 0 else "SHORT"
                    print(f"      {coin} NET {direction}: {abs(net_size):.4f} (${abs(net_value):,.0f})")
    except Exception as e:
        print(f"⚠️  HLP positions: {e}")

    # Moon Dev note: HLP trades + trade stats demos removed - endpoints retired 2026-08-13

    # HLP Liquidators
    try:
        liquidators = api.get_hlp_liquidators()
        if isinstance(liquidators, dict):
            liq_list = liquidators.get('liquidators', [])
            events = liquidators.get('events', [])
            active = sum(1 for l in liq_list if l.get('status') == 'active')
            print(f"✅ HLP Liquidators: {active}/{len(liq_list)} active, {len(events)} events")
    except Exception as e:
        print(f"⚠️  HLP liquidators: {e}")

    # HLP Deltas
    try:
        deltas = api.get_hlp_deltas(hours=24)
        if isinstance(deltas, dict):
            current = deltas.get('current', 0)
            change = deltas.get('change_24h', 0)
            delta_list = deltas.get('deltas', [])
            print(f"✅ HLP Deltas: Current ${current:,.0f}, 24h change ${change:,.0f}, {len(delta_list)} data points")
    except Exception as e:
        print(f"⚠️  HLP deltas: {e}")

    print()

    # ==================== 14. MULTI-EXCHANGE LIQUIDATIONS ====================
    print("=" * 60)
    print("🔥 14. MULTI-EXCHANGE LIQUIDATIONS")
    print("=" * 60)

    # Combined All Exchange Stats
    try:
        stats = api.get_all_liquidation_stats()
        if isinstance(stats, dict):
            total_count = stats.get('total_count', stats.get('count', 0))
            total_volume = stats.get('total_volume', stats.get('total_value_usd', 0))
            print(f"✅ Combined All Exchanges:")
            print(f"   Total Count: {total_count:,}")
            print(f"   Total Volume: ${total_volume:,.0f}")
            by_exchange = stats.get('by_exchange', {})
            if by_exchange:
                print(f"   By Exchange:")
                for ex, ex_stats in by_exchange.items():
                    if isinstance(ex_stats, dict):
                        ex_count = ex_stats.get('count', 0)
                        ex_vol = ex_stats.get('volume', 0)
                        print(f"      {ex}: {ex_count:,} liqs | ${ex_vol:,.0f}")
    except Exception as e:
        print(f"⚠️  All liquidation stats: {e}")

    # Per-exchange liquidations (1h sample)
    exchanges = [
        ("Binance", api.get_binance_liquidations),
        ("Bybit", api.get_bybit_liquidations),
        ("OKX", api.get_okx_liquidations),
    ]
    for name, func in exchanges:
        try:
            data = func("1h")
            if isinstance(data, list):
                print(f"✅ {name} 1h: {len(data)} liquidations")
            elif isinstance(data, dict):
                liq_list = data.get('liquidations', data.get('data', []))
                print(f"✅ {name} 1h: {len(liq_list)} liquidations")
        except Exception as e:
            print(f"⚠️  {name} 1h: {e}")

    print()

    print("=" * 60)
    print("🌙 Moon Dev API Test Complete! 🚀")
    print("=" * 60)


if __name__ == "__main__":
    test_all()

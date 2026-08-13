"""
Moon Dev's API Health Monitor
Runs every 15 minutes, tests ALL endpoints, collects errors,
prints them clearly, and sends alerts to Telegram.
Built by Moon Dev

Usage: python api_monitor.py

Requires in .env:
    MOONDEV_API_KEY=your_key
    TELEGRAM_BOT_TOKEN=your_bot_token
    TELEGRAM_CHAT_ID=your_chat_id
"""

import sys
import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from api import MoonDevAPI

# ==================== Moon Dev Config ====================
CHECK_INTERVAL_SECONDS = 900  # 15 minutes
TEST_WALLET = "0x010461c14e146ac35fe42271bdc1134ee31c703a"

# Telegram config - Moon Dev
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


# ==================== Telegram Alert - Moon Dev ====================
def send_telegram(message):
    """Send a message to Moon Dev's Telegram. Silently skips if not configured."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }

    resp = requests.post(url, json=payload, timeout=10)
    if resp.status_code != 200:
        print(f"  Moon Dev: Telegram send failed ({resp.status_code})")


# ==================== All Endpoints to Test ====================
def get_all_tests(api):
    """
    Returns list of (name, callable, validation_fn) tuples.
    Each test calls one endpoint and optionally validates the response.
    - Moon Dev
    """
    return [
        # --- CORE ---
        ("Health Check",
         lambda: api.health(),
         lambda r: isinstance(r, dict) and r.get('status') == 'ok'),

        ("Liquidations (1h)",
         lambda: api.get_liquidations("1h"),
         lambda r: r is not None),

        ("Liquidation Stats",
         lambda: api.get_liquidation_stats(),
         lambda r: isinstance(r, dict)),

        ("Positions",
         lambda: api.get_positions(),
         lambda r: r is not None),

        ("Whales",
         lambda: api.get_whales(),
         lambda r: r is not None),

        ("Whale Addresses",
         lambda: api.get_whale_addresses(),
         lambda r: isinstance(r, list) and len(r) > 0),

        ("Buyers",
         lambda: api.get_buyers(),
         lambda r: r is not None),

        ("Depositors",
         lambda: api.get_depositors(),
         lambda r: r is not None),

        ("Events",
         lambda: api.get_events(),
         lambda r: r is not None),

        ("Contracts",
         lambda: api.get_contracts(),
         lambda r: r is not None),

        # --- TICK DATA ---
        ("Tick Stats",
         lambda: api.get_tick_stats(),
         lambda r: isinstance(r, dict)),

        ("Tick Latest Prices",
         lambda: api.get_tick_latest(),
         lambda r: isinstance(r, dict)),

        ("Ticks (BTC 1h)",
         lambda: api.get_ticks("BTC", "1h"),
         lambda r: isinstance(r, dict) and len(r.get('ticks', [])) > 0),

        # --- ORDER FLOW & TRADES ---
        ("Trades (Recent 500)",
         lambda: api.get_trades(),
         lambda r: (isinstance(r, list) and len(r) > 0) or (isinstance(r, dict) and len(r.get('trades', [])) > 0)),

        ("Large Trades (>$100k)",
         lambda: api.get_large_trades(),
         lambda r: (isinstance(r, list) and len(r) > 0) or (isinstance(r, dict) and len(r.get('trades', [])) > 0)),

        ("Order Flow",
         lambda: api.get_orderflow(),
         lambda r: r is not None),

        ("Order Flow Stats",
         lambda: api.get_orderflow_stats(),
         lambda r: r is not None),

        ("Imbalance (1h)",
         lambda: api.get_imbalance("1h"),
         lambda r: r is not None),

        # --- SMART MONEY ---
        ("Smart Money Rankings",
         lambda: api.get_smart_money_rankings(),
         lambda r: r is not None),

        ("Smart Money Leaderboard",
         lambda: api.get_smart_money_leaderboard(),
         lambda r: r is not None),

        ("Smart Money Signals (1h)",
         lambda: api.get_smart_money_signals("1h"),
         lambda r: r is not None),

        # --- USER DATA ---
        ("User Positions (Moon Dev API)",
         lambda: api.get_user_positions_api(TEST_WALLET),
         lambda r: r is not None),

        ("User Fills",
         lambda: api.get_user_fills(TEST_WALLET, limit=10),
         lambda r: r is not None),

        # --- MARKET DATA ---
        ("All Prices",
         lambda: api.get_prices(),
         lambda r: isinstance(r, dict) and r.get('count', 0) > 0),

        ("Quick Price (BTC)",
         lambda: api.get_price("BTC"),
         lambda r: isinstance(r, dict) and r.get('mid_price') is not None),

        ("Orderbook (BTC)",
         lambda: api.get_orderbook("BTC"),
         lambda r: isinstance(r, dict) and r.get('best_bid') is not None),

        ("Account State",
         lambda: api.get_account(TEST_WALLET),
         lambda r: isinstance(r, dict)),

        ("Fills (Hyperliquid-compatible)",
         lambda: api.get_fills(TEST_WALLET, limit=5),
         lambda r: r is not None),

        ("Candles (BTC 1h)",
         lambda: api.get_candles("BTC", interval="1h"),
         lambda r: isinstance(r, list) and len(r) > 0),

        ("Candle Symbols",
         lambda: api.get_candle_symbols(),
         lambda r: isinstance(r, dict) and r.get('count', 0) > 0),

        # --- HLP ---
        ("HLP Positions",
         lambda: api.get_hlp_positions(include_strategies=False),
         lambda r: isinstance(r, dict)),

        # Moon Dev: HLP Trades + Trade Stats checks removed - endpoints retired 2026-08-13

        ("HLP Liquidators",
         lambda: api.get_hlp_liquidators(),
         lambda r: r is not None),

        ("HLP Deltas",
         lambda: api.get_hlp_deltas(hours=24),
         lambda r: r is not None),

        ("HLP Sentiment",
         lambda: api.get_hlp_sentiment(),
         lambda r: isinstance(r, dict)),

        ("HLP Liquidator Status",
         lambda: api.get_hlp_liquidator_status(),
         lambda r: r is not None),

        ("HLP Market Maker",
         lambda: api.get_hlp_market_maker(),
         lambda r: r is not None),

        ("HLP Timing",
         lambda: api.get_hlp_timing(),
         lambda r: r is not None),

        ("HLP Correlation",
         lambda: api.get_hlp_correlation(),
         lambda r: r is not None),

        ("HLP Live Delta",
         lambda: api.get_hlp_delta(),
         lambda r: isinstance(r, dict)),

        ("HLP Flips",
         lambda: api.get_hlp_flips(),
         lambda r: r is not None),

        ("HLP Flip Stats",
         lambda: api.get_hlp_flip_stats(),
         lambda r: isinstance(r, dict)),

        # --- MULTI-EXCHANGE LIQUIDATIONS ---
        ("All Exchange Liquidations (1h)",
         lambda: api.get_all_liquidations("1h"),
         lambda r: r is not None),

        ("All Exchange Liquidation Stats",
         lambda: api.get_all_liquidation_stats(),
         lambda r: isinstance(r, dict)),

        ("Binance Liquidations (1h)",
         lambda: api.get_binance_liquidations("1h"),
         lambda r: r is not None),

        ("Binance Liquidation Stats",
         lambda: api.get_binance_liquidation_stats(),
         lambda r: isinstance(r, dict)),

        ("Bybit Liquidations (1h)",
         lambda: api.get_bybit_liquidations("1h"),
         lambda r: r is not None),

        ("OKX Liquidations (1h)",
         lambda: api.get_okx_liquidations("1h"),
         lambda r: r is not None),

        # --- HIP3 ---
        ("HIP3 Liquidations (1h)",
         lambda: api.get_hip3_liquidations("1h"),
         lambda r: r is not None),

        ("HIP3 Liquidation Stats",
         lambda: api.get_hip3_liquidation_stats(),
         lambda r: isinstance(r, dict)),

        ("HIP3 Meta (All Symbols)",
         lambda: api.get_hip3_meta(),
         lambda r: isinstance(r, dict)),

        ("HIP3 Tick Stats",
         lambda: api.get_hip3_tick_stats(),
         lambda r: isinstance(r, dict)),

        # --- POSITION SNAPSHOTS ---
        ("Position Snapshot Stats",
         lambda: api.get_position_snapshot_stats(hours=24),
         lambda r: isinstance(r, dict)),

        ("Position Snapshots (BTC)",
         lambda: api.get_position_snapshots("BTC", hours=24, limit=10),
         lambda r: r is not None),
    ]


# ==================== Run All Tests ====================
def run_tests(api):
    """Run all endpoint tests, collect results - Moon Dev"""
    tests = get_all_tests(api)
    total = len(tests)
    passed = []
    failed = []

    print(f"\n{'='*80}")
    print(f"  MOON DEV API MONITOR - Testing {total} endpoints")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")

    for i, (name, call_fn, validate_fn) in enumerate(tests, 1):
        try:
            result = call_fn()
            if validate_fn(result):
                passed.append(name)
                print(f"  [{i:02d}/{total}] PASS  {name}")
            else:
                error_msg = f"Validation failed - response looks empty or wrong format"
                failed.append((name, error_msg, call_fn, validate_fn))
                print(f"  [{i:02d}/{total}] FAIL  {name} -> {error_msg}")
        except Exception as e:
            error_msg = str(e)
            failed.append((name, error_msg, call_fn, validate_fn))
            print(f"  [{i:02d}/{total}] FAIL  {name} -> {error_msg}")

    # ==================== RETRY FAILURES - Moon Dev ====================
    if failed:
        print(f"\n{'='*80}")
        print(f"  Moon Dev: {len(failed)} failure(s) detected - retrying before alerting...")
        print(f"{'='*80}\n")
        time.sleep(3)

        still_failed = []
        for name, prev_error, call_fn, validate_fn in failed:
            try:
                result = call_fn()
                if validate_fn(result):
                    passed.append(name)
                    print(f"  RETRY PASS  {name} (was a hiccup)")
                else:
                    still_failed.append((name, prev_error))
                    print(f"  RETRY FAIL  {name} -> still failing")
            except Exception as e:
                still_failed.append((name, str(e)))
                print(f"  RETRY FAIL  {name} -> {e}")

        failed = still_failed

    # ==================== RESULTS ====================
    print(f"\n{'='*80}")
    print(f"  MOON DEV API MONITOR - RESULTS")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}")
    print(f"\n  Total: {total}  |  Passed: {len(passed)}  |  Failed: {len(failed)}")
    print(f"{'='*80}")

    if failed:
        print(f"\n{'!'*80}")
        print(f"  ERRORS FOUND - {len(failed)} endpoint(s) failing")
        print(f"  Copy everything below this line and send to server AI")
        print(f"{'!'*80}")
        print()
        print(f"Moon Dev API Errors - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{len(failed)} endpoint(s) need fixing:\n")
        for i, (name, error) in enumerate(failed, 1):
            print(f"  {i}. [{name}]")
            print(f"     Error: {error}")
            print()
        print(f"{'!'*80}")

        # ==================== TELEGRAM ALERT - Moon Dev ====================
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        msg_lines = [
            f"<b>Moon Dev API Alert</b>",
            f"{timestamp}",
            f"",
            f"<b>{len(failed)}/{total} endpoints failing:</b>",
            f"",
        ]
        for i, (name, error) in enumerate(failed, 1):
            # Keep it short for Telegram - truncate long errors
            short_error = error[:100] + "..." if len(error) > 100 else error
            msg_lines.append(f"{i}. <b>{name}</b>")
            msg_lines.append(f"   {short_error}")
            msg_lines.append("")

        msg_lines.append(f"{len(passed)}/{total} endpoints healthy")
        send_telegram("\n".join(msg_lines))

    else:
        print(f"\n  ALL {total} ENDPOINTS HEALTHY - Moon Dev API running clean")
        # Only send Telegram on all-clear if there were errors last time
        # (we track this with a simple flag)

    print(f"\n{'='*80}\n")
    return failed


# ==================== Main Loop ====================
def main():
    print()
    print("  ================================================================")
    print("  =         MOON DEV API HEALTH MONITOR                         =")
    print("  =         Checking all endpoints every 15 minutes             =")
    print("  =         Built by Moon Dev                                   =")
    print("  ================================================================")
    print()

    api = MoonDevAPI()
    if not api.api_key:
        print("  ERROR: No API key found! Set MOONDEV_API_KEY in your .env file")
        return

    print(f"  API Key loaded: YES")
    print(f"  Check interval: {CHECK_INTERVAL_SECONDS}s ({CHECK_INTERVAL_SECONDS // 60} min)")

    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        print(f"  Telegram: ENABLED (alerts on errors only)")
    else:
        print(f"  Telegram: DISABLED (set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env)")

    print()

    run_count = 0
    had_errors = False

    while True:
        run_count += 1
        print(f"\n  >>> RUN #{run_count} starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        errors = run_tests(api)

        if errors:
            had_errors = True
            print(f"  Moon Dev: {len(errors)} error(s) detected. Fix them and they'll clear next run.")
        else:
            if had_errors:
                had_errors = False
            print(f"  Moon Dev: All clean. Next check in {CHECK_INTERVAL_SECONDS // 60} minutes.")

        next_run = datetime.fromtimestamp(time.time() + CHECK_INTERVAL_SECONDS).strftime('%H:%M:%S')
        print(f"  >>> Sleeping until {next_run}...")

        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()

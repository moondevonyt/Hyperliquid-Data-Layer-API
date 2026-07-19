"""
🌙 Moon Dev's Bulk Binance Liquidation Data Downloader
Built with love by Moon Dev 🚀

Downloads Binance Futures liquidation data — 35 million+ records dating back to June 2024,
plus the real-time feed. Requires a Quant Elite API key (must end in _qe).

⚠️  DATA GAP: 2026-04-23 → 2026-07-18. The dataset has two segments:
    - historical: 2024-06-04 → 2026-04-23 (frozen archive, final, never changes)
    - live:       2026-07-18 → now        (real-time feed, growing)
    No liquidations were collected in between and the gap is PERMANENT.
    This script hits the coverage endpoint first to get the exact, always-current
    segment boundaries instead of hardcoding dates.

Endpoints:
    GET /api/binance_liquidations/coverage.json  (standard key works)
    GET /api/bulk/binance_liquidations           (Quant Elite key only)

Response is paginated - this script auto-paginates through all data (100k records per page).
Supports filters: start, end, symbol, side, min_usd
"""

import sys
import os
import requests
import pandas as pd
from datetime import datetime

# Add parent directory to path for importing api.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIG ====================
BASE_URL = "https://api.moondev.com"
COVERAGE_ENDPOINT = "/api/binance_liquidations/coverage.json"
BULK_ENDPOINT = "/api/bulk/binance_liquidations"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

PAGE_SIZE = 100_000    # max allowed per page (default is 10k - crank it up for bulk pulls)

# Which segment to download: "all", "historical" (frozen archive), or "live" (real-time feed)
# Boundaries are pulled from the coverage endpoint automatically - no hardcoded dates
SEGMENT = "all"

# Optional filters - set to None to skip
SYMBOL = None          # e.g. "BTCUSDT", None for all
SIDE = None            # "BUY" (short liquidated) or "SELL" (long liquidated), None for all
MIN_USD = None         # minimum usd_size filter, e.g. 1000
START_DATE = None      # e.g. "2024-06-01" (overrides SEGMENT start)
END_DATE = None        # e.g. "2025-01-01" (overrides SEGMENT end)


def get_coverage(api_key):
    """🌙 Moon Dev: Check dataset coverage - segments, boundaries, and the gap"""
    print("🗺️  Moon Dev: Checking dataset coverage...")
    response = requests.get(f"{BASE_URL}{COVERAGE_ENDPOINT}", params={"api_key": api_key}, timeout=30)
    response.raise_for_status()
    coverage = response.json()

    segments = {}
    for seg in coverage["segments"]:
        segments[seg["name"]] = seg
        print(f"   📦 {seg['name']} ({seg['status']}): {seg['start']} → {seg['end']} | {seg['records']:,} records")

    gap = coverage.get("gap")
    if gap:
        print(f"   ⚠️  GAP: {gap['from']} → {gap['to']} - no data, permanent (cannot be recovered)")

    return segments


def main():
    """🌙 Moon Dev's Bulk Binance Liquidation Downloader"""
    print("🌙 Moon Dev's Bulk Binance Liquidation Downloader")
    print("=" * 60)

    api_key = os.getenv('MOONDEV_API_KEY')
    if not api_key:
        print("❌ Moon Dev says: No API key found! Set MOONDEV_API_KEY in your .env file")
        return

    if not api_key.endswith('_qe'):
        print("⚠️  Moon Dev Warning: The bulk endpoint requires a Quant Elite key (ending in _qe)")
        print(f"   Your key ends with: ...{api_key[-4:]}")
        print("   Standard keys get 403 Forbidden. Attempting anyway...\n")

    print(f"🔑 Moon Dev: API key loaded (...{api_key[-4:]})")

    # Step 1: coverage check - get exact segment boundaries before assuming a date range has data
    segments = get_coverage(api_key)

    # Step 2: build params (segment selection via date slicing - both segments live in one table)
    params = {"api_key": api_key, "limit": PAGE_SIZE}

    if SEGMENT == "historical":
        params["end"] = segments["historical"]["end"][:10]
        print(f"\n🎯 Moon Dev: Pulling HISTORICAL archive only (end={params['end']})")
    elif SEGMENT == "live":
        params["start"] = segments["live"]["start"][:10]
        print(f"\n🎯 Moon Dev: Pulling LIVE feed only (start={params['start']})")
    else:
        print(f"\n🎯 Moon Dev: Pulling EVERYTHING (gap rows simply don't exist)")

    if SYMBOL:
        params["symbol"] = SYMBOL
    if SIDE:
        params["side"] = SIDE
    if MIN_USD:
        params["min_usd"] = MIN_USD
    if START_DATE:
        params["start"] = START_DATE
    if END_DATE:
        params["end"] = END_DATE

    if any([SYMBOL, SIDE, MIN_USD, START_DATE, END_DATE]):
        print(f"🔍 Moon Dev: Extra filters applied: symbol={SYMBOL} side={SIDE} min_usd={MIN_USD} start={START_DATE} end={END_DATE}")

    print(f"📡 Moon Dev: Fetching bulk liquidation data (paginated, {PAGE_SIZE:,} per page)")

    # Step 3: paginate through all data - follow next_offset until has_more is false
    all_records = []
    offset = 0
    total_records = None

    while True:
        params["offset"] = offset
        url = f"{BASE_URL}{BULK_ENDPOINT}"

        response = requests.get(url, params=params, timeout=120)
        response.raise_for_status()
        result = response.json()

        if total_records is None:
            total_records = result.get("total_records", 0)
            print(f"📊 Moon Dev: Total records available: {total_records:,}")

        batch = result.get("data", [])
        if not batch:
            break

        all_records.extend(batch)
        returned = result.get("returned", len(batch))
        has_more = result.get("has_more", False)

        print(f"   📥 Page {offset // PAGE_SIZE + 1}: fetched {returned:,} records | total downloaded: {len(all_records):,} / {total_records:,}")

        if not has_more:
            break

        offset = result.get("next_offset", offset + PAGE_SIZE)

    print(f"\n✅ Moon Dev: All pages downloaded! Total records: {len(all_records):,}")

    # Convert to DataFrame
    df = pd.DataFrame(all_records)
    print(f"📊 Moon Dev: DataFrame shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")

    # Save to CSV
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = os.path.join(OUTPUT_DIR, f"bulk_binance_liquidations_{timestamp}.csv")
    df.to_csv(csv_file, index=False)

    size_mb = os.path.getsize(csv_file) / (1024 * 1024)
    print(f"\n💾 Moon Dev: Saved to {csv_file}")
    print(f"   📏 Size: {size_mb:.1f} MB")
    print(f"   📏 Rows: {len(df):,}")

    # Preview
    print(f"\n🔥 Moon Dev: First 10 rows:")
    print(df.head(10).to_string(index=False))

    # Quick stats
    if 'usd_size' in df.columns:
        print(f"\n📈 Moon Dev: Quick Stats:")
        print(f"   Total USD volume: ${df['usd_size'].sum():,.2f}")
        if 'side' in df.columns:
            for side in df['side'].unique():
                side_df = df[df['side'] == side]
                print(f"   {side}: {len(side_df):,} records, ${side_df['usd_size'].sum():,.2f}")
        if 'symbol' in df.columns:
            top_symbols = df.groupby('symbol')['usd_size'].sum().sort_values(ascending=False).head(10)
            print(f"\n   Top 10 symbols by USD volume:")
            for sym, vol in top_symbols.items():
                print(f"     {sym}: ${vol:,.2f}")

    print(f"\n🌙 Moon Dev: Bulk liquidation download complete! 🚀")


if __name__ == "__main__":
    main()

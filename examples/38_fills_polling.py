"""
Moon Dev's Fills Polling Demo - Time Windows Make Every Wallet Fast
===================================================================
Shows the RIGHT way to poll a wallet for new fills using time windows.

Built with love by Moon Dev

THE POINT:
    Pass a time window and ANY wallet answers in ~50ms, no matter how many
    fills it has. Skip the window and first contact with a fill-sparse wallet
    forces a full 3-day archive scan that can take ~30s. It still returns 200,
    it is just slow. So when you poll: ALWAYS pass a window.

Two ways to say the same thing:
    minutes=10          - last 10 minutes (0-4320, so up to 3 days)
    since_ms=1786...    - epoch milliseconds lower bound
    If you pass both, the later (narrower) one wins.

The response echoes back since_ms so you can check the server used your window.

Usage: python 38_fills_polling.py [address]
       python 38_fills_polling.py 0x010461c14e146ac35fe42271bdc1134ee31c703a

Data Source: Moon Dev's local Hyperliquid node (blazing fast!)
"""

import sys
import os
import time
from datetime import datetime

# Add parent directory to path to import api.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api import MoonDevAPI

import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

DEFAULT_ADDRESS = "0x010461c14e146ac35fe42271bdc1134ee31c703a"
POLL_SECONDS = 10       # how often we ask for new fills
WINDOW_MINUTES = 5      # how far back each poll looks


def fetch_recent_fills(api, address, minutes):
    """
    Fetch fills from the last N minutes.

    Moon Dev's error rule: a 503 fills_scanner_busy means RETRY OR FALL BACK.
    It does NOT mean the wallet has no fills. An empty list with HTTP 200 is
    the only thing that means "genuinely no fills".

    Returns (fills_list, since_ms) or (None, None) when the scanner was busy.
    """
    try:
        data = api.get_user_fills(address, limit=2000, minutes=minutes)
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 503:
            code = e.response.json().get('code', '')
            if code == 'fills_scanner_busy':
                console.print("[yellow]Scanner busy (fills_scanner_busy) - retrying next poll, NOT treating as empty[/yellow]")
                return None, None
        raise

    return data.get('fills', []), data.get('since_ms')


def show_speed_comparison(api, address):
    """Time a windowed call so Moon Dev can see the fast lane for himself"""
    console.print("\n[bold cyan]Moon Dev: timing a windowed call...[/bold cyan]")

    start = time.time()
    data = api.get_user_fills(address, limit=2000, minutes=WINDOW_MINUTES)
    elapsed = (time.time() - start) * 1000

    window_start = data.get('since_ms')
    readable = datetime.fromtimestamp(window_start / 1000).strftime("%Y-%m-%d %H:%M:%S") if window_start else "none"

    lines = [
        f"[bold cyan]minutes={WINDOW_MINUTES}[/bold cyan] took [bold green]{elapsed:.0f}ms[/bold green]",
        f"[bold cyan]fills returned:[/bold cyan] {data.get('count', 0)}",
        f"[bold cyan]since_ms echoed back:[/bold cyan] {window_start} ([dim]{readable}[/dim])",
        "",
        "[dim]No window would mean a possible ~30s cold archive scan.[/dim]",
    ]
    console.print(Panel("\n".join(lines), title="[bold white]FAST LANE[/bold white]  [dim cyan]GET /api/user/{address}/fills?minutes=N[/dim cyan]", border_style="green", padding=(0, 1)))


def show_hl_format(api, address):
    """The Hyperliquid-format endpoint takes startTime, exactly like userFillsByTime"""
    since_ms = int(time.time() * 1000) - (60 * 60 * 1000)  # 1 hour ago

    start = time.time()
    fills = api.get_fills(address, limit=100, start_time=since_ms)
    elapsed = (time.time() - start) * 1000

    console.print(Panel(
        f"[bold cyan]startTime={since_ms}[/bold cyan] took [bold green]{elapsed:.0f}ms[/bold green] and returned [yellow]{len(fills)}[/yellow] fills\n"
        "[dim]Same param name and units as Hyperliquid's userFillsByTime, so HL code ports straight over.[/dim]\n"
        "[dim]api.get_fills(addr, minutes=60) is the relative form of the same window.[/dim]",
        title="[bold white]HL-COMPATIBLE[/bold white]  [dim cyan]GET /api/fills/{address}?startTime=EPOCH_MS[/dim cyan]",
        border_style="magenta",
        padding=(0, 1)
    ))


def display_fills(fills, limit=10):
    """Print the newest fills in a compact table"""
    if not fills:
        console.print("[dim]No fills in this window (HTTP 200 + empty = genuinely none)[/dim]")
        return

    table = Table(box=box.SIMPLE_HEAD, border_style="cyan", header_style="bold magenta", padding=(0, 1), show_edge=False)
    table.add_column("Time", style="dim", width=19)
    table.add_column("Coin", style="white", width=8)
    table.add_column("Side", width=5)
    table.add_column("Size", justify="right", width=12)
    table.add_column("Price", style="yellow", justify="right", width=12)
    table.add_column("PnL", justify="right", width=12)

    for fill in fills[:limit]:
        ts = fill.get('time', 0)
        time_str = datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M:%S") if ts else "?"
        side = fill.get('side', '?')
        side_str = "[green]BUY[/green]" if side in ('B', 'b') else "[red]SELL[/red]"
        pnl = float(fill.get('closedPnl', 0) or 0)
        pnl_str = f"[green]+${pnl:,.2f}[/green]" if pnl > 0 else (f"[red]${pnl:,.2f}[/red]" if pnl < 0 else "[dim]$0.00[/dim]")

        table.add_row(
            time_str,
            str(fill.get('coin', '?'))[:8],
            side_str,
            f"{float(fill.get('sz', 0)):,.4f}",
            f"${float(fill.get('px', 0)):,.2f}",
            pnl_str
        )

    console.print(table)


def poll_loop(api, address):
    """
    Poll for new fills forever, deduping by trade id.

    This is the pattern Moon Dev wants bots to copy: small window, dedupe on tid,
    survive a busy scanner without dropping data.
    """
    console.print(f"\n[bold cyan]Polling every {POLL_SECONDS}s with a {WINDOW_MINUTES} minute window. Ctrl+C to stop.[/bold cyan]\n")

    seen_tids = set()
    first_pass = True

    while True:
        fills, since_ms = fetch_recent_fills(api, address, WINDOW_MINUTES)

        if fills is None:
            # Scanner was busy. Keep seen_tids so we do not re-print on recovery.
            time.sleep(POLL_SECONDS)
            continue

        new_fills = [f for f in fills if f.get('tid') not in seen_tids]
        for f in fills:
            seen_tids.add(f.get('tid'))

        stamp = datetime.now().strftime("%H:%M:%S")
        if first_pass:
            console.print(f"[dim]{stamp}[/dim] baseline: {len(fills)} fills already in the window")
            display_fills(fills, limit=5)
            first_pass = False
        elif new_fills:
            console.print(f"[bold green]{stamp} {len(new_fills)} NEW fill(s)![/bold green]")
            display_fills(new_fills, limit=10)
        else:
            console.print(f"[dim]{stamp} no new fills (window start {since_ms})[/dim]")

        time.sleep(POLL_SECONDS)


def main():
    """Main function - Moon Dev's fills polling demo"""
    address = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ADDRESS

    console.print(Panel(
        "[bold cyan]MOON DEV'S FILLS POLLING DEMO[/bold cyan]\n"
        "[dim]Time windows make every wallet answer in ~50ms[/dim]",
        border_style="bright_cyan",
        box=box.DOUBLE_EDGE,
        padding=(0, 1)
    ))
    console.print(f"[dim]Wallet: {address}[/dim]")

    api = MoonDevAPI()

    if not api.api_key:
        console.print(Panel(
            "[bold red]ERROR: No API key found![/bold red]\n"
            "Set MOONDEV_API_KEY in your .env file\n"
            "Get your API key at: [link=https://moondev.com]https://moondev.com[/link]",
            border_style="red",
            title="Authentication Required",
            padding=(0, 1)
        ))
        return

    show_speed_comparison(api, address)
    show_hl_format(api, address)

    try:
        poll_loop(api, address)
    except KeyboardInterrupt:
        console.print("\n[bold cyan]Moon Dev: polling stopped. Later![/bold cyan]")


if __name__ == "__main__":
    main()

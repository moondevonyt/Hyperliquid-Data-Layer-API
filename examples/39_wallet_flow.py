"""
Moon Dev's Wallet Flow Demo - Did This Wallet Net-Buy Or Net-Sell?
==================================================================
One call answers it, and the answer can never be truncated.

Built with love by Moon Dev

THE PROBLEM THIS SOLVES:
    /api/user/{address}/fills caps at 2,000 rows. On a busy wallet, a 24h window
    returns the newest 2,000 fills and sets truncated=true, so its page_summary
    describes maybe the last 15 minutes, NOT your 24 hours. Summing that page
    gives you a confidently wrong answer.

    /api/user/{address}/flow aggregates EVERY fill in the window server-side with
    no cap. truncated is always false. That is the number you trade on.

A time window is REQUIRED (minutes or since_ms). No window is a 400 window_required,
because "net flow since forever" is not a question with a useful answer.

Usage: python 39_wallet_flow.py [address] [minutes] [coin]
       python 39_wallet_flow.py                                    # defaults
       python 39_wallet_flow.py 0xYOUR_ADDRESS 60                  # per-coin breakdown
       python 39_wallet_flow.py 0xYOUR_ADDRESS 60 BTC              # single coin

Data Source: Moon Dev's local Hyperliquid node (blazing fast!)
"""

import sys
import os

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
DEFAULT_MINUTES = 60


def format_minutes(minutes):
    """Show 60 not 60.0, but keep 1.5 as 1.5"""
    return f"{int(minutes)}" if float(minutes).is_integer() else f"{minutes}"


def format_usd(value):
    """Format USD value with commas and dollar sign"""
    if value is None:
        return "$0"
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:,.2f}M"
    elif abs(value) >= 1_000:
        return f"${value/1_000:,.1f}K"
    return f"${value:,.2f}"


def color_signed(value, formatter=format_usd):
    """Green for net buying, red for net selling"""
    text = formatter(value)
    if value > 0:
        return f"[green]+{text}[/green]"
    if value < 0:
        return f"[red]{text}[/red]"
    return f"[dim]{text}[/dim]"


def show_single_coin(flow, minutes):
    """Show net flow for one coin - the direct answer"""
    net_sz = flow.get('net_sz', 0)
    net_usd = flow.get('net_usd', 0)
    coin = flow.get('coin', '?')

    verdict = "NET BUYER" if net_sz > 0 else ("NET SELLER" if net_sz < 0 else "FLAT")
    verdict_color = "green" if net_sz > 0 else ("red" if net_sz < 0 else "dim")

    lines = [
        f"[bold {verdict_color}]{verdict} of {coin}[/bold {verdict_color}]",
        "",
        f"[bold cyan]Net size:[/bold cyan]  {color_signed(net_sz, lambda v: f'{v:,.5f} {coin}')}",
        f"[bold cyan]Net USD:[/bold cyan]   {color_signed(net_usd)}",
        "",
        f"[dim]Bought {flow.get('bought_sz', 0):,.5f} ({format_usd(flow.get('bought_usd', 0))})[/dim]",
        f"[dim]Sold   {flow.get('sold_sz', 0):,.5f} ({format_usd(flow.get('sold_usd', 0))})[/dim]",
        "",
        f"[dim]{flow.get('count', 0):,} fills aggregated | truncated: {flow.get('truncated')}[/dim]",
    ]

    console.print(Panel(
        "\n".join(lines),
        title=f"[bold white]NET FLOW, LAST {format_minutes(minutes)} MIN[/bold white]  [dim cyan]GET /api/user/{{address}}/flow?coin={coin}[/dim cyan]",
        border_style=verdict_color if verdict_color != "dim" else "white",
        box=box.DOUBLE,
        padding=(1, 2)
    ))


def show_breakdown(flow, minutes, top=15):
    """Show the per-coin breakdown, biggest absolute USD flow first"""
    coins = flow.get('coins', {})
    if not coins:
        console.print("[dim]No fills in this window[/dim]")
        return

    ranked = sorted(coins.items(), key=lambda kv: abs(kv[1].get('net_usd', 0)), reverse=True)

    table = Table(box=box.SIMPLE_HEAD, border_style="cyan", header_style="bold magenta", padding=(0, 1), show_edge=False)
    table.add_column("Coin", style="bold white", width=10)
    table.add_column("Net USD", justify="right", width=14)
    table.add_column("Net Size", justify="right", width=18)
    table.add_column("Bought", style="dim green", justify="right", width=12)
    table.add_column("Sold", style="dim red", justify="right", width=12)
    table.add_column("Fills", style="yellow", justify="right", width=7)

    for coin, data in ranked[:top]:
        table.add_row(
            coin,
            color_signed(data.get('net_usd', 0)),
            color_signed(data.get('net_sz', 0), lambda v: f"{v:,.4f}"),
            format_usd(data.get('bought_usd', 0)),
            format_usd(data.get('sold_usd', 0)),
            f"{data.get('count', 0):,}"
        )

    net_usd = flow.get('net_usd', 0)
    header = (
        f"[bold cyan]NET FLOW BY COIN, LAST {format_minutes(minutes)} MIN[/bold cyan] │ "
        f"Total: {color_signed(net_usd)} │ {flow.get('count', 0):,} fills │ {len(coins)} coins"
    )
    console.print(Panel(table, title=header, subtitle="[dim cyan]GET /api/user/{address}/flow[/dim cyan]", border_style="cyan", padding=(0, 0)))

    if len(ranked) > top:
        console.print(f"[dim]... +{len(ranked) - top} more coins (showing top {top} by absolute USD flow)[/dim]")

    console.print("[dim]Top-level totals are USD only. Coin sizes are not comparable across coins,[/dim]")
    console.print("[dim]so there is no global size total. Use coin= for a size answer.[/dim]")


def show_truncation_trap(api, address, minutes):
    """
    Prove WHY /flow exists: compare it against the capped fills page.

    On a busy wallet the fills page covers a fraction of your window, so its
    page_summary is not a window answer. Moon Dev wants this seen, not assumed.
    """
    console.print("\n[bold cyan]Moon Dev: comparing /flow against a capped /fills page...[/bold cyan]")

    fills_data = api.get_user_fills(address, limit=2000, minutes=minutes)
    count = fills_data.get('count', 0)
    truncated = fills_data.get('truncated')
    newest_ms = fills_data.get('newest_ms')
    oldest_ms = fills_data.get('oldest_ms')
    page_summary = fills_data.get('page_summary', {})

    page_span_min = ((newest_ms - oldest_ms) / 60000) if (newest_ms and oldest_ms) else 0

    flow = api.get_user_flow(address, minutes=minutes)

    lines = [
        f"[bold]You asked for:[/bold] the last {format_minutes(minutes)} minutes",
        "",
        f"[bold yellow]/fills (limit 2000)[/bold yellow]",
        f"  returned [yellow]{count:,}[/yellow] fills, truncated=[bold]{truncated}[/bold]",
        f"  page actually covers [yellow]{page_span_min:,.1f}[/yellow] of your {format_minutes(minutes)} minutes",
        f"  page_summary volume: {format_usd(page_summary.get('total_volume', 0))}  [dim](this page only!)[/dim]",
        "",
        f"[bold green]/flow (no cap)[/bold green]",
        f"  aggregated [green]{flow.get('count', 0):,}[/green] fills, truncated=[bold]{flow.get('truncated')}[/bold]",
        f"  window volume: {format_usd(flow.get('bought_usd', 0) + flow.get('sold_usd', 0))}  [dim](the real answer)[/dim]",
        f"  net flow: {color_signed(flow.get('net_usd', 0))}",
    ]

    if truncated:
        lines += ["", "[bold red]The fills page is NOT your window. Use /flow for window aggregates.[/bold red]"]
    else:
        lines += ["", "[dim]This wallet is quiet enough that the page held the whole window.[/dim]",
                  "[dim]On a busy wallet the two numbers diverge hard.[/dim]"]

    console.print(Panel("\n".join(lines), title="[bold white]WHY /flow EXISTS[/bold white]", border_style="magenta", padding=(0, 1)))


def show_ordering_note():
    """The permanent ordering contract, worth knowing when you build recency signals"""
    console.print(Panel(
        "[bold]Fills always come back newest first.[/bold]\n"
        "When limit caps the result, the NEWEST fills are kept and the oldest dropped.\n"
        "This is a permanent API contract.\n\n"
        "[dim]It is deliberately the opposite of Hyperliquid's userFillsByTime, which returns\n"
        "ascending and keeps the OLDEST 2000 - silently blinding recency signals on busy\n"
        "wallets. Moon Dev's endpoint will not flip for HL parity, so build against it.[/dim]",
        title="[bold white]ORDERING GUARANTEE[/bold white]  [dim cyan]order: \"newest_first\"[/dim cyan]",
        border_style="bright_yellow",
        padding=(0, 1)
    ))


def main():
    """Main function - Moon Dev's wallet flow demo"""
    address = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ADDRESS
    minutes = float(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_MINUTES
    coin = sys.argv[3].upper() if len(sys.argv) > 3 else None

    console.print(Panel(
        "[bold cyan]MOON DEV'S WALLET FLOW[/bold cyan]\n"
        "[dim]Net-bought or net-sold since T, in one uncapped call[/dim]",
        border_style="bright_cyan",
        box=box.DOUBLE_EDGE,
        padding=(0, 1)
    ))
    console.print(f"[dim]Wallet: {address} | Window: {format_minutes(minutes)} min | Coin: {coin or 'ALL (breakdown)'}[/dim]\n")

    api = MoonDevAPI()

    if not api.api_key:
        console.print(Panel(
            "[bold red]ERROR: No API key found![/bold red]\n"
            "Set MOONDEV_API_KEY in your .env file\n"
            "Apply for an API key at: [link=https://moondev.com/apply]https://moondev.com/apply[/link]",
            border_style="red",
            title="Authentication Required",
            padding=(0, 1)
        ))
        return

    # A window is mandatory - the client catches this before the round trip
    try:
        api.get_user_flow(address)
    except ValueError as e:
        console.print(f"[dim]No-window check: {e}[/dim]\n")

    try:
        flow = api.get_user_flow(address, minutes=minutes, coin=coin)
    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None else 0
        if status == 503:
            console.print("[yellow]Fills scanner busy (fills_scanner_busy). Retry shortly or use your fallback.[/yellow]")
            return
        if status == 504:
            console.print(f"[yellow]Gateway timeout. {format_minutes(minutes)} min is too wide for this busy wallet.[/yellow]")
            console.print("[dim]Moon Dev tip: add up several narrower windows instead of one wide call.[/dim]")
            return
        raise

    if coin:
        show_single_coin(flow, minutes)
    else:
        show_breakdown(flow, minutes)

    show_truncation_trap(api, address, minutes)
    show_ordering_note()

    console.print("\n[dim cyan]Moon Dev's Wallet Flow | api.moondev.com | Built with love by Moon Dev[/dim cyan]")


if __name__ == "__main__":
    main()

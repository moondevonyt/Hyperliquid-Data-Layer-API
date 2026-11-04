"""
Moon Dev's Buyer Watcher Dashboard
===================================
Beautiful terminal dashboard for tracking $5k+ BUYERS on key coins

Built with love by Moon Dev
https://moondev.com

This script displays:
- Recent $5k+ buyers on HYPE, SOL, XRP, ETH
- Per-symbol buyer statistics
- Buyer-only tracking (no sells - these are accumulation signals!)

Difference from Whale Watcher:
- Whale Watcher: $25k+ threshold, BTC/ETH/SOL, both buys & sells
- Buyer Watcher: $5k+ threshold, HYPE/SOL/XRP/ETH, BUYERS ONLY

Usage: python 15_buyers.py
"""

import sys
import os
from datetime import datetime

# Add parent directory to path for API import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api import MoonDevAPI

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.align import Align
from rich import box

# Initialize Rich console
console = Console()

# Coin emojis - Moon Dev style
COIN_EMOJI = {
    'HYPE': '🔥',
    'SOL': '◎',
    'XRP': '✕',
    'ETH': 'Ξ',
}


def create_banner():
    """Create the Moon Dev buyer watcher banner"""
    banner = """██████╗ ██╗   ██╗██╗   ██╗███████╗██████╗ ███████╗
██╔══██╗██║   ██║╚██╗ ██╔╝██╔════╝██╔══██╗██╔════╝
██████╔╝██║   ██║ ╚████╔╝ █████╗  ██████╔╝███████╗
██╔══██╗██║   ██║  ╚██╔╝  ██╔══╝  ██╔══██╗╚════██║
██████╔╝╚██████╔╝   ██║   ███████╗██║  ██║███████║
╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝"""
    return Panel(
        Align.center(Text(banner, style="bold green")),
        title="🟢 [bold magenta]BUYER WATCHER[/bold magenta] 🟢",
        subtitle="[dim]$5k+ Buyers on HYPE/SOL/XRP/ETH | by Moon Dev[/dim]",
        border_style="bright_green",
        box=box.DOUBLE_EDGE,
        padding=(0, 1)
    )


def format_usd(value):
    """Format USD value with commas and dollar sign"""
    if value is None or value == 0:
        return "$0"
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    elif abs(value) >= 1_000:
        return f"${value/1_000:.1f}K"
    return f"${value:,.0f}"


def create_overview_panel(buyers_data):
    """Create overview stats panel"""
    if not isinstance(buyers_data, dict):
        return Panel("[dim]No data available[/dim]", title="Overview")

    total_buyers = len(buyers_data.get('buyers', []))
    stats = buyers_data.get('stats', {})

    # Build stats display
    lines = [
        f"[bold green]🟢 BUYERS ONLY[/bold green] (No sells tracked)",
        f"[bold cyan]Threshold:[/bold cyan] [yellow]$5,000+[/yellow]",
        f"[bold cyan]Total Buyers:[/bold cyan] [yellow]{total_buyers:,}[/yellow]",
        "",
        "[bold white]Tracked Symbols:[/bold white]",
        f"  🔥 HYPE  ◎ SOL  ✕ XRP  Ξ ETH",
    ]

    return Panel(
        "\n".join(lines),
        title="[bold green]📊 Buyer Watcher Overview[/bold green]  [dim cyan]GET https://api.moondev.com/api/buyers.json[/dim cyan]",
        border_style="green",
        padding=(1, 2)
    )


def create_symbol_stats_panel(buyers_data):
    """Create per-symbol statistics panel"""
    if not isinstance(buyers_data, dict):
        return Panel("[dim]No stats available[/dim]", title="Symbol Stats")

    stats = buyers_data.get('stats', {})
    by_symbol = stats.get('by_symbol', stats.get('symbols', {}))

    if not by_symbol:
        # Calculate from buyers list if stats not provided
        buyers = buyers_data.get('buyers', [])
        by_symbol = {}
        for buyer in buyers:
            symbol = buyer.get('coin', buyer.get('symbol', 'UNKNOWN'))
            if symbol not in by_symbol:
                by_symbol[symbol] = {'count': 0, 'volume': 0}
            by_symbol[symbol]['count'] += 1
            by_symbol[symbol]['volume'] += float(buyer.get('value', buyer.get('usd_value', 0)))

    lines = []
    for symbol in ['HYPE', 'SOL', 'XRP', 'ETH']:
        emoji = COIN_EMOJI.get(symbol, '🪙')
        data = by_symbol.get(symbol, by_symbol.get(f'{symbol}USDT', {}))

        if isinstance(data, dict):
            count = data.get('count', 0)
            volume = data.get('volume', data.get('total_volume', 0))
        else:
            count = 0
            volume = 0

        lines.append(f"{emoji} [bold white]{symbol:>4}[/bold white]  [green]{count:>4} buyers[/green]  [yellow]{format_usd(volume):>10}[/yellow]")

    return Panel(
        "\n".join(lines),
        title="[bold cyan]📈 Per-Symbol Stats[/bold cyan]  [dim cyan]GET https://api.moondev.com/api/buyers.json[/dim cyan]",
        border_style="cyan",
        padding=(1, 2)
    )


def create_buyers_table(buyers_data):
    """Create a beautiful table of recent buyers"""
    table = Table(
        title="🟢 [bold green]Recent $5k+ Buyers[/bold green] 🟢",
        show_header=True,
        header_style="bold magenta",
        border_style="green",
        box=box.ROUNDED,
        title_style="bold",
        padding=(0, 1)
    )

    table.add_column("Time", style="dim", width=11)
    table.add_column("Coin", style="bold", width=8, justify="center")
    table.add_column("Value", style="green", width=12, justify="right")
    table.add_column("Size", style="cyan", width=14, justify="right")
    table.add_column("Price", style="yellow", width=12, justify="right")
    table.add_column("Buyer Address", style="dim cyan", width=44)

    if not isinstance(buyers_data, dict):
        table.add_row("", "[dim]No data[/dim]", "", "", "", "")
        return table

    buyers = buyers_data.get('buyers', buyers_data.get('data', []))

    if not buyers:
        table.add_row("", "[dim]No recent buyers[/dim]", "", "", "", "")
        return table

    for buyer in buyers[:25]:  # Show max 25 buyers - Moon Dev
        # Time
        timestamp = buyer.get('time', buyer.get('timestamp', buyer.get('created_at', 'N/A')))
        if isinstance(timestamp, str) and len(timestamp) > 11:
            timestamp = timestamp[5:16].replace('T', ' ')
        elif isinstance(timestamp, (int, float)):
            if timestamp > 1e10:
                timestamp = timestamp / 1000
            try:
                timestamp = datetime.fromtimestamp(timestamp).strftime("%m-%d %H:%M")
            except:
                timestamp = str(timestamp)[:11]

        # Coin with emoji
        coin = buyer.get('coin', buyer.get('symbol', 'N/A'))
        coin_clean = coin.replace('USDT', '').replace('USD', '')
        emoji = COIN_EMOJI.get(coin_clean.upper(), '🪙')
        coin_display = f"{emoji} {coin_clean}"

        # Value
        value = buyer.get('value', buyer.get('usd_value', buyer.get('notional', 0)))
        if isinstance(value, (int, float)):
            value_display = f"[bold green]{format_usd(value)}[/bold green]"
        else:
            value_display = str(value)

        # Size
        size = buyer.get('sz', buyer.get('size', buyer.get('quantity', 'N/A')))
        if isinstance(size, (int, float)):
            size_str = f"{size:,.4f}" if size < 100 else f"{size:,.2f}"
        else:
            size_str = str(size)

        # Price
        price = buyer.get('px', buyer.get('price', 0))
        if isinstance(price, (int, float)) and price > 0:
            price_str = f"${price:,.2f}"
        else:
            price_str = "N/A"

        # Address
        address = buyer.get('address', buyer.get('user', buyer.get('wallet', 'N/A')))

        table.add_row(
            str(timestamp),
            coin_display,
            value_display,
            size_str,
            price_str,
            str(address)
        )

    return table


def create_comparison_panel():
    """Create panel comparing Whale vs Buyer watcher"""
    content = """[bold white]Whale Watcher vs Buyer Watcher[/bold white]

[bold cyan]Whale Watcher[/bold cyan] (/api/whales.json)
  • Threshold: [yellow]$25,000+[/yellow]
  • Symbols: BTC, ETH, SOL
  • Tracks: [green]Buys[/green] & [red]Sells[/red]

[bold green]Buyer Watcher[/bold green] (/api/buyers.json)
  • Threshold: [yellow]$5,000+[/yellow]
  • Symbols: HYPE, SOL, XRP, ETH
  • Tracks: [green]BUYERS ONLY[/green]

[dim]Buyer-only signals = accumulation detection[/dim]"""

    return Panel(
        content,
        title="[bold magenta]📋 Service Comparison[/bold magenta]  [dim cyan]GET https://api.moondev.com/api/buyers.json[/dim cyan]",
        border_style="magenta",
        padding=(1, 2)
    )


def create_footer():
    """Create footer with timestamp and branding"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return Text(
        f"━━━ 🌙 Moon Dev's Buyer Watcher | {now} | api.moondev.com | Tracking accumulation! ━━━",
        style="dim green",
        justify="center"
    )


def main():
    """Main function - Moon Dev's Buyer Watcher Dashboard"""
    console.clear()
    console.print(create_banner())

    # Initialize API - Moon Dev
    console.print("[dim]🌙 Connecting to Moon Dev API...[/dim]")
    api = MoonDevAPI()

    if not api.api_key:
        console.print(Panel(
            "[bold red]ERROR:[/bold red] No API key found!\n"
            "Set MOONDEV_API_KEY in .env | Apply for a key at: [cyan]moondev.com/apply[/cyan]",
            title="[red]Auth Error[/red]",
            border_style="red",
            padding=(0, 1)
        ))
        return

    console.print("[dim green]✅ API connected[/dim green]")
    console.print()

    # Fetch buyers data - Moon Dev
    console.print("[bold green]🟢 Fetching $5k+ buyers on HYPE/SOL/XRP/ETH...[/bold green]")

    try:
        buyers_data = api.get_buyers()
    except AttributeError:
        # If get_buyers doesn't exist yet, try direct API call
        import requests
        headers = {'X-API-Key': api.api_key}
        response = requests.get(f"{api.base_url}/api/buyers.json", headers=headers)
        buyers_data = response.json() if response.status_code == 200 else {}
    except Exception as e:
        console.print(f"[red]Error fetching buyers: {e}[/red]")
        buyers_data = {}

    # Display panels side by side
    overview = create_overview_panel(buyers_data)
    symbol_stats = create_symbol_stats_panel(buyers_data)
    console.print(Columns([overview, symbol_stats], equal=True, expand=True))

    console.print()

    # Display buyers table
    console.print(create_buyers_table(buyers_data))

    console.print()

    # Display comparison panel
    console.print(create_comparison_panel())

    # Summary
    if isinstance(buyers_data, dict):
        buyer_count = len(buyers_data.get('buyers', []))
    else:
        buyer_count = 0

    summary = (
        f"🟢 [green]{buyer_count}[/green] recent buyers | "
        f"🔥 HYPE ◎ SOL ✕ XRP Ξ ETH | "
        f"💰 [yellow]$5k+ threshold[/yellow] | "
        f"📈 [green]Accumulation signals![/green]"
    )
    console.print(Panel(summary, title="[bold green]Summary[/bold green]  [dim cyan]GET https://api.moondev.com/api/buyers.json[/dim cyan]", border_style="green", padding=(0, 1)))

    console.print()
    console.print(create_footer())


if __name__ == "__main__":
    main()

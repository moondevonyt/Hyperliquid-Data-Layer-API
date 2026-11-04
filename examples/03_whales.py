"""
🌙 Moon Dev's Whale Watcher Dashboard 🐋
=========================================
A beautiful terminal dashboard for tracking whale activity

Built with love by Moon Dev
https://moondev.com

This script displays:
- Total whale address count
- Sample whale addresses
- Recent whale trades ($25k+)
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
from rich.layout import Layout
from rich import box


# Initialize Rich console
console = Console()


def create_banner():
    """Create the Moon Dev whale watcher banner"""
    banner = """███╗   ███╗ ██████╗  ██████╗ ███╗   ██╗    ██████╗ ███████╗██╗   ██╗
████╗ ████║██╔═══██╗██╔═══██╗████╗  ██║    ██╔══██╗██╔════╝██║   ██║
██╔████╔██║██║   ██║██║   ██║██╔██╗ ██║    ██║  ██║█████╗  ██║   ██║
██║╚██╔╝██║██║   ██║██║   ██║██║╚██╗██║    ██║  ██║██╔══╝  ╚██╗ ██╔╝
██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██║ ╚████║    ██████╔╝███████╗ ╚████╔╝
╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝    ╚═════╝ ╚══════╝  ╚═══╝"""
    return Panel(
        Align.center(Text(banner, style="bold cyan")),
        title="🌙 [bold magenta]WHALE WATCHER[/bold magenta] 🐋",
        subtitle="[dim]Tracking the biggest players by Moon Dev[/dim]",
        border_style="bright_cyan",
        box=box.DOUBLE_EDGE,
        padding=(0, 1)
    )


def create_stats_panel(whale_count):
    """Create a big number display for whale count"""
    stats_content = f"🐋 Total Tracked Whales: [bold yellow]{whale_count:,}[/bold yellow] | Verified $25k+ traders on Hyperliquid"
    return Panel(
        stats_content,
        title="[bold green]📊 Statistics[/bold green]  [dim cyan]GET https://api.moondev.com/api/whale_addresses.txt[/dim cyan]",
        border_style="green",
        padding=(0, 1)
    )


def create_addresses_table(addresses, limit=20):
    """Create a beautiful table of whale addresses"""
    table = Table(
        title="🐋 [bold cyan]Sample Whale Addresses[/bold cyan]",
        show_header=True,
        header_style="bold magenta",
        border_style="cyan",
        box=box.SIMPLE,
        title_style="bold",
        padding=(0, 1)
    )
    table.add_column("#", style="dim", width=3, justify="right")
    table.add_column("Whale Address", style="cyan", width=44)
    table.add_column("Status", style="green", width=8, justify="center")
    for idx, addr in enumerate(addresses[:limit], 1):
        # Show full address - the main event! - Moon Dev
        table.add_row(str(idx), addr, "🐋")
    return table


def create_trades_table(trades):
    """Create a beautiful table of recent whale trades"""
    table = Table(
        title="💵 [bold yellow]Recent Whale Trades ($25k+)[/bold yellow]",
        show_header=True,
        header_style="bold magenta",
        border_style="yellow",
        box=box.SIMPLE,
        title_style="bold",
        padding=(0, 1)
    )
    table.add_column("Time", style="dim", width=11)
    table.add_column("Coin", style="cyan", width=6, justify="center")
    table.add_column("Side", width=6, justify="center")
    table.add_column("Size", style="magenta", width=12, justify="right")
    table.add_column("Value", style="green", width=12, justify="right")
    table.add_column("Whale", style="dim cyan", width=44)
    if not trades:
        table.add_row("", "[dim]No trades[/dim]", "", "", "", "")
        return table
    for trade in trades[:15]:  # Show max 15 trades - Moon Dev
        timestamp = trade.get('time', trade.get('timestamp', trade.get('created_at', 'N/A')))
        if isinstance(timestamp, str) and len(timestamp) > 11:
            timestamp = timestamp[:11]
        coin = trade.get('coin', trade.get('symbol', 'N/A'))
        side = trade.get('side', 'N/A')
        if side.lower() in ('buy', 'b'):
            side_display = "[bold green]BUY[/bold green]"
        elif side.lower() in ('sell', 's'):
            side_display = "[bold red]SELL[/bold red]"
        else:
            side_display = side
        size = trade.get('sz', trade.get('size', trade.get('quantity', 'N/A')))
        if isinstance(size, (int, float)):
            size = f"{size:,.2f}"
        value = trade.get('value', trade.get('usd_value', trade.get('notional', 0)))
        if isinstance(value, (int, float)):
            value_display = f"[green]${value:,.0f}[/green]"
        else:
            value_display = str(value)
        address = trade.get('address', trade.get('user', trade.get('wallet', 'N/A')))
        table.add_row(str(timestamp), str(coin), side_display, str(size), value_display, str(address))
    return table


def create_footer():
    """Create footer with timestamp and branding"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return Text(f"━━━ 🌙 Moon Dev | {now} | api.moondev.com ━━━", style="dim magenta", justify="center")


def main():
    """Main function - Moon Dev's Whale Watcher Dashboard"""
    console.clear()
    console.print(create_banner())
    # Initialize API - Moon Dev
    console.print("[dim]🌙 Connecting to Moon Dev API...[/dim]")
    api = MoonDevAPI()
    if not api.api_key:
        console.print(Panel(
            "[bold red]ERROR:[/bold red] No API key found!\nSet MOONDEV_API_KEY in .env | Apply for a key at: [cyan]moondev.com/apply[/cyan]",
            title="[red]Auth Error[/red]",
            border_style="red",
            padding=(0, 1)
        ))
        return
    console.print("[dim green]✅ API connected[/dim green]")
    # Fetch whale addresses - Moon Dev
    addresses = api.get_whale_addresses()
    whale_count = len(addresses)
    console.print(create_stats_panel(whale_count))
    console.print(create_addresses_table(addresses, limit=20))
    # Fetch whale trades - Moon Dev
    trades_data = api.get_whales()
    if isinstance(trades_data, dict):
        trades = trades_data.get('trades', trades_data.get('data', []))
        if not trades and 'whales' in trades_data:
            trades = trades_data.get('whales', [])
    elif isinstance(trades_data, list):
        trades = trades_data
    else:
        trades = []
    console.print(create_trades_table(trades))
    # Summary - Moon Dev
    summary = f"🐋 [cyan]{whale_count:,}[/cyan] whales | 💵 [yellow]{len(trades)}[/yellow] trades | 📊 [green]Live[/green] | 🌙 [magenta]Watch for big moves![/magenta]"
    console.print(Panel(summary, title="[bold cyan]Summary[/bold cyan]  [dim cyan]GET https://api.moondev.com/api/whales.json[/dim cyan]", border_style="cyan", padding=(0, 1)))
    console.print(create_footer())


if __name__ == "__main__":
    main()

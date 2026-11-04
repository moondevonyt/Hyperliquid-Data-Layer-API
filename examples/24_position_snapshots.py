"""
Moon Dev's Position Snapshot Dashboard - Track Positions Near Liquidation
Built with love by Moon Dev | Run with: python examples/24_position_snapshots.py

Tracks positions within 15% of liquidation on HyperLiquid.
Symbols: BTC, ETH, SOL, XRP, HYPE
Minimum position value: $10k
Snapshot frequency: 1 minute

Use cases:
- Identify potential liquidation cascades
- Spot short/long squeeze setups
- Monitor at-risk whale positions
"""

import sys
import os

# Add parent directory to path for importing api.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import MoonDevAPI
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich import box

# Initialize Rich console
console = Console()

# Tracked symbols
TRACKED_SYMBOLS = ['BTC', 'ETH', 'SOL', 'XRP', 'HYPE']

# ==================== BANNER ====================
def print_banner():
    """Print the Moon Dev banner"""
    banner = """██████╗  ██████╗ ███████╗    ███████╗███╗   ██╗ █████╗ ██████╗ ███████╗
██╔══██╗██╔═══██╗██╔════╝    ██╔════╝████╗  ██║██╔══██╗██╔══██╗██╔════╝
██████╔╝██║   ██║███████╗    ███████╗██╔██╗ ██║███████║██████╔╝███████╗
██╔═══╝ ██║   ██║╚════██║    ╚════██║██║╚██╗██║██╔══██║██╔═══╝ ╚════██║
██║     ╚██████╔╝███████║    ███████║██║ ╚████║██║  ██║██║     ███████║
╚═╝      ╚═════╝ ╚══════╝    ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝"""
    console.print(Panel(
        Align.center(Text(banner, style="bold cyan")),
        title="[bold red]POSITION SNAPSHOT TRACKER[/bold red]",
        subtitle="[dim]Positions Near Liquidation - by Moon Dev[/dim]",
        border_style="red",
        box=box.DOUBLE_EDGE,
        padding=(0, 1)
    ))

# ==================== HELPER FUNCTIONS ====================
def format_usd(value):
    """Format USD value with commas and dollar sign"""
    if value is None:
        return "$0"
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    elif abs(value) >= 1_000:
        return f"${value/1_000:.1f}K"
    return f"${value:,.0f}"

def format_pct(value):
    """Format percentage value"""
    if value is None:
        return "N/A"
    return f"{value:.2f}%"

def get_risk_color(distance_pct):
    """Get color based on distance to liquidation"""
    if distance_pct < 2:
        return "bold red"
    elif distance_pct < 5:
        return "red"
    elif distance_pct < 10:
        return "yellow"
    return "green"

# ==================== AGGREGATE STATS ====================
def display_aggregate_stats(api, hours=24):
    """Display aggregate statistics for all tracked symbols"""
    console.print(Panel(
        f"[bold yellow]POSITION SNAPSHOT STATISTICS ({hours}H)[/bold yellow]  [dim cyan]GET https://api.moondev.com/api/position_snapshots/stats[/dim cyan]",
        border_style="yellow",
        padding=(0, 1)
    ))

    try:
        stats = api.get_position_snapshot_stats(hours=hours)

        if not stats or 'error' in stats:
            console.print(f"[red]Moon Dev: Error fetching stats: {stats.get('error', 'Unknown error')}[/red]")
            return

        # Overall stats panel
        overall = stats.get('overall', {})
        panels = []

        panels.append(Panel(
            f"[bold white]TOTAL SNAPSHOTS[/bold white]\n[bold cyan]{overall.get('total_snapshots', 0):,}[/bold cyan]",
            border_style="cyan", width=22, padding=(0, 1)
        ))

        panels.append(Panel(
            f"[bold white]UNIQUE USERS[/bold white]\n[bold magenta]{overall.get('unique_users', 0):,}[/bold magenta]",
            border_style="magenta", width=22, padding=(0, 1)
        ))

        avg_dist = overall.get('avg_distance_pct', 0)
        panels.append(Panel(
            f"[bold white]AVG DISTANCE[/bold white]\n[bold {get_risk_color(avg_dist)}]{format_pct(avg_dist)}[/bold {get_risk_color(avg_dist)}]",
            border_style="yellow", width=22, padding=(0, 1)
        ))

        console.print(Columns(panels, equal=True, expand=True))

        # Per-symbol breakdown
        by_symbol = stats.get('by_symbol', {})
        if by_symbol:
            console.print()
            table = Table(box=box.ROUNDED, border_style="cyan", header_style="bold magenta", padding=(0, 1))
            table.add_column("Symbol", style="cyan", justify="center", width=10)
            table.add_column("Snapshots", style="white", justify="right", width=12)
            table.add_column("Unique Users", style="magenta", justify="right", width=14)
            table.add_column("Avg Distance", justify="right", width=14)
            table.add_column("Longs", style="green", justify="right", width=10)
            table.add_column("Shorts", style="red", justify="right", width=10)

            for symbol in TRACKED_SYMBOLS:
                sym_data = by_symbol.get(symbol, {})
                if sym_data:
                    avg_d = sym_data.get('avg_distance_pct', 0)
                    table.add_row(
                        f"[bold]{symbol}[/bold]",
                        f"{sym_data.get('snapshots', 0):,}",
                        f"{sym_data.get('unique_users', 0):,}",
                        f"[{get_risk_color(avg_d)}]{format_pct(avg_d)}[/{get_risk_color(avg_d)}]",
                        f"[green]{sym_data.get('longs', 0):,}[/green]",
                        f"[red]{sym_data.get('shorts', 0):,}[/red]"
                    )

            console.print(table)

        # Top 10 closest to liquidation
        top_10 = stats.get('top_10_closest', [])
        if top_10:
            console.print()
            display_top_at_risk(top_10)

    except Exception as e:
        console.print(f"[red]Moon Dev: Error fetching aggregate stats: {e}[/red]")

# ==================== TOP AT RISK ====================
def display_top_at_risk(positions):
    """Display top positions closest to liquidation"""
    console.print(Panel(
        "[bold red]TOP 10 CLOSEST TO LIQUIDATION[/bold red]",
        border_style="red",
        padding=(0, 1)
    ))

    table = Table(box=box.ROUNDED, border_style="red", header_style="bold yellow", padding=(0, 1))
    table.add_column("#", style="dim", width=3)
    table.add_column("Symbol", style="cyan", justify="center", width=8)
    table.add_column("Side", justify="center", width=8)
    table.add_column("Position Value", style="yellow", justify="right", width=16)
    table.add_column("Entry Price", style="white", justify="right", width=14)
    table.add_column("Liq Price", style="red", justify="right", width=14)
    table.add_column("Distance", justify="right", width=12)
    table.add_column("Address", style="dim", width=14)

    for i, pos in enumerate(positions[:10], 1):
        distance = pos.get('distance_pct', pos.get('liquidation_distance_pct', 0))
        side = pos.get('side', 'unknown')

        # Format side
        if side.lower() == 'long':
            side_display = "[green]LONG[/green]"
        else:
            side_display = "[red]SHORT[/red]"

        # Rank emoji
        rank_display = "" if i == 1 else "" if i == 2 else "" if i == 3 else str(i)

        # Truncate address
        address = pos.get('user', pos.get('address', ''))
        addr_short = f"{address[:6]}...{address[-4:]}" if len(address) > 12 else address

        table.add_row(
            rank_display,
            pos.get('symbol', pos.get('coin', '?')),
            side_display,
            format_usd(pos.get('position_value', pos.get('value_usd', 0))),
            f"${pos.get('entry_price', pos.get('entry_px', 0)):,.2f}",
            f"${pos.get('liquidation_price', pos.get('liq_px', 0)):,.2f}",
            f"[{get_risk_color(distance)}]{format_pct(distance)}[/{get_risk_color(distance)}]",
            addr_short
        )

    console.print(table)

# ==================== SYMBOL SNAPSHOTS ====================
def display_symbol_snapshots(api, symbol, hours=24, max_distance=None):
    """Display position snapshots for a specific symbol"""
    console.print(Panel(
        f"[bold cyan]{symbol} POSITION SNAPSHOTS ({hours}H)[/bold cyan]  [dim cyan]GET https://api.moondev.com/api/position_snapshots/symbol/{symbol}[/dim cyan]",
        border_style="cyan",
        padding=(0, 1)
    ))

    try:
        params = {'hours': hours, 'limit': 50}
        if max_distance:
            params['max_distance_pct'] = max_distance

        data = api.get_position_snapshots(symbol, **params)

        if not data or 'error' in data:
            console.print(f"[red]Moon Dev: Error fetching {symbol} snapshots: {data.get('error', 'No data')}[/red]")
            return

        snapshots = data.get('snapshots', data.get('data', data if isinstance(data, list) else []))

        if not snapshots:
            console.print(f"[dim]No snapshots found for {symbol}[/dim]")
            return

        # Summary stats
        long_count = sum(1 for s in snapshots if s.get('side', '').lower() == 'long')
        short_count = len(snapshots) - long_count
        avg_distance = sum(s.get('distance_pct', s.get('liquidation_distance_pct', 0)) for s in snapshots) / len(snapshots) if snapshots else 0
        total_value = sum(s.get('position_value', s.get('value_usd', 0)) for s in snapshots)

        panels = [
            Panel(f"[bold white]POSITIONS[/bold white]\n[bold cyan]{len(snapshots)}[/bold cyan]", border_style="cyan", width=18),
            Panel(f"[bold green]LONGS[/bold green]\n[bold green]{long_count}[/bold green]", border_style="green", width=18),
            Panel(f"[bold red]SHORTS[/bold red]\n[bold red]{short_count}[/bold red]", border_style="red", width=18),
            Panel(f"[bold white]AVG DIST[/bold white]\n[bold {get_risk_color(avg_distance)}]{format_pct(avg_distance)}[/bold {get_risk_color(avg_distance)}]", border_style="yellow", width=18),
            Panel(f"[bold white]TOTAL VALUE[/bold white]\n[bold yellow]{format_usd(total_value)}[/bold yellow]", border_style="magenta", width=18),
        ]
        console.print(Columns(panels, equal=True, expand=True))
        console.print()

        # Position table
        table = Table(box=box.ROUNDED, border_style="cyan", header_style="bold magenta", padding=(0, 1))
        table.add_column("#", style="dim", width=3)
        table.add_column("Side", justify="center", width=8)
        table.add_column("Position Value", style="yellow", justify="right", width=16)
        table.add_column("Entry Price", style="white", justify="right", width=14)
        table.add_column("Liq Price", style="red", justify="right", width=14)
        table.add_column("Distance", justify="right", width=12)
        table.add_column("Leverage", style="cyan", justify="right", width=10)
        table.add_column("Address", style="dim", width=14)

        # Sort by distance (closest first)
        sorted_snaps = sorted(snapshots, key=lambda x: x.get('distance_pct', x.get('liquidation_distance_pct', 100)))

        for i, pos in enumerate(sorted_snaps[:25], 1):
            distance = pos.get('distance_pct', pos.get('liquidation_distance_pct', 0))
            side = pos.get('side', 'unknown')

            side_display = "[green]LONG[/green]" if side.lower() == 'long' else "[red]SHORT[/red]"
            rank_display = "" if i == 1 else "" if i == 2 else "" if i == 3 else str(i)

            address = pos.get('user', pos.get('address', ''))
            addr_short = f"{address[:6]}...{address[-4:]}" if len(address) > 12 else address

            leverage = pos.get('leverage', pos.get('lev', 'N/A'))
            lev_display = f"{leverage}x" if leverage != 'N/A' else 'N/A'

            table.add_row(
                rank_display,
                side_display,
                format_usd(pos.get('position_value', pos.get('value_usd', 0))),
                f"${pos.get('entry_price', pos.get('entry_px', 0)):,.2f}",
                f"${pos.get('liquidation_price', pos.get('liq_px', 0)):,.2f}",
                f"[{get_risk_color(distance)}]{format_pct(distance)}[/{get_risk_color(distance)}]",
                lev_display,
                addr_short
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Moon Dev: Error fetching {symbol} snapshots: {e}[/red]")

# ==================== FOOTER ====================
def print_footer():
    """Print footer with timestamp and branding"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(f"[dim yellow]{'─'*95}[/dim yellow]")
    console.print(f"[dim yellow]Moon Dev's Position Snapshot Dashboard | {now} | api.moondev.com | Built with love by Moon Dev[/dim yellow]")

# ==================== MAIN ====================
def main():
    """Main function - Moon Dev's Position Snapshot Dashboard"""
    import argparse

    parser = argparse.ArgumentParser(description="Moon Dev's Position Snapshot Dashboard")
    parser.add_argument('symbol', nargs='?', default=None, help='Symbol to filter (BTC, ETH, SOL, XRP, HYPE)')
    parser.add_argument('--hours', type=int, default=24, help='Lookback hours (default: 24)')
    parser.add_argument('--max-distance', type=float, default=None, help='Max distance to liquidation %')
    args = parser.parse_args()

    console.clear()
    print_banner()

    console.print("[bold cyan]Moon Dev: Initializing API connection...[/bold cyan]")
    api = MoonDevAPI()

    if not api.api_key:
        console.print(Panel(
            "[bold red]ERROR: No API key found![/bold red]\n\n"
            "Please set MOONDEV_API_KEY in your .env file:\n"
            "[dim]MOONDEV_API_KEY=your_key_here[/dim]\n\n"
            "Apply for an API key at: [link=https://moondev.com/apply]https://moondev.com/apply[/link]",
            border_style="red",
            title="Authentication Required",
            padding=(0, 1)
        ))
        return

    console.print(f"[green]API key loaded (...{api.api_key[-4:]})[/green]")

    with console.status("[bold yellow]Moon Dev: Fetching position snapshot data...[/bold yellow]"):
        pass

    if args.symbol:
        # Show specific symbol
        symbol = args.symbol.upper()
        if symbol not in TRACKED_SYMBOLS:
            console.print(f"[red]Moon Dev: Invalid symbol '{symbol}'. Available: {', '.join(TRACKED_SYMBOLS)}[/red]")
            return
        display_symbol_snapshots(api, symbol, hours=args.hours, max_distance=args.max_distance)
    else:
        # Show aggregate stats for all symbols
        display_aggregate_stats(api, hours=args.hours)
        console.print()

        # Show brief for each symbol
        for symbol in TRACKED_SYMBOLS:
            display_symbol_snapshots(api, symbol, hours=args.hours, max_distance=args.max_distance)
            console.print()

    print_footer()

if __name__ == "__main__":
    main()

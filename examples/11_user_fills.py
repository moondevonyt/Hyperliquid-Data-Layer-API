"""
Moon Dev's Trade History Dashboard
===================================
Beautiful terminal dashboard for viewing Hyperliquid wallet fill/trade history

Built with love by Moon Dev

Usage: python 11_user_fills.py [address] [limit] [minutes]
       python 11_user_fills.py 0x010461c14e146ac35fe42271bdc1134ee31c703a 500
       python 11_user_fills.py 0x010461c14e146ac35fe42271bdc1134ee31c703a -1  # ALL fills
       python 11_user_fills.py 0x010461c14e146ac35fe42271bdc1134ee31c703a 2000 60  # last 60 min

Moon Dev tip: passing minutes puts you on the fast lane (~50ms for ANY wallet).
Without a window, first contact with a fill-sparse wallet can take ~30s.
See 38_fills_polling.py for the polling pattern.

Data Source: Moon Dev's local Hyperliquid node (blazing fast!)
"""

import sys
import os
from datetime import datetime
from collections import defaultdict

import requests

# Add parent directory to path to import api.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api import MoonDevAPI

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.columns import Columns
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

# ==================== BANNER ====================
def create_banner():
    """Create the Moon Dev branded header banner"""
    banner = """
 _____ ___  ___   ____  _____
|_   _| _ \\/ _ \\ |  _ \\| ____|
  | | |   / /_\\ \\| | | |  _|
  | | | |\\ \\  _  | |_| | |___
  |_| |_| \\_\\| |_|____/|_____|
 _   _ ___ ____ _____ ___  ______   __
| | | |_ _/ ___|_   _/ _ \\|  _ \\ \\ / /
| |_| || |\\___ \\ | || | | | |_) \\ V /
|  _  || | ___) || || |_| |  _ < | |
|_| |_|___|____/ |_| \\___/|_| \\_\\|_|
"""
    return Panel(
        Align.center(Text(banner, style="bold cyan")),
        title="[bold magenta]MOON DEV'S HYPERLIQUID TRADE HISTORY[/bold magenta]",
        subtitle="[dim]Powered by Moon Dev's Local Node - Blazing Fast![/dim]",
        border_style="bright_cyan",
        box=box.DOUBLE_EDGE,
        padding=(0, 1)
    )


# ==================== HELPER FUNCTIONS ====================
def format_usd(value):
    """Format USD value with commas and dollar sign"""
    if value is None:
        return "$0"
    if isinstance(value, str):
        value = float(value.replace(',', '').replace('$', ''))
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:,.2f}M"
    elif abs(value) >= 1_000:
        return f"${value/1_000:,.1f}K"
    return f"${value:,.2f}"


def format_pnl(value):
    """Format PnL with color coding"""
    if value is None:
        return Text("$0.00", style="white")
    if isinstance(value, str):
        value = float(value.replace(',', '').replace('$', ''))

    if value > 0:
        return Text(f"+${value:,.2f}", style="bold green")
    elif value < 0:
        return Text(f"-${abs(value):,.2f}", style="bold red")
    else:
        return Text("$0.00", style="dim white")


def format_timestamp(ts):
    """Format timestamp to readable string"""
    if not ts:
        return "N/A"
    if isinstance(ts, (int, float)):
        # Convert from ms if needed
        if ts > 1e12:
            ts = ts / 1000
        dt = datetime.fromtimestamp(ts)
        return dt.strftime("%m-%d %H:%M:%S")
    return str(ts)[:19]


# ==================== STATS CALCULATION ====================
def calculate_fill_stats(fills):
    """Calculate comprehensive stats from fills data"""
    stats = {
        'total_fills': len(fills),
        'total_volume': 0,
        'total_pnl': 0,
        'total_fees': 0,
        'winning_trades': 0,
        'losing_trades': 0,
        'buys': 0,
        'sells': 0,
        'buy_volume': 0,
        'sell_volume': 0,
        'coins': defaultdict(lambda: {'count': 0, 'volume': 0, 'pnl': 0}),
        'directions': defaultdict(int),
        'largest_win': 0,
        'largest_loss': 0,
        'first_fill': None,
        'last_fill': None,
    }

    for fill in fills:
        px = float(fill.get('px', 0))
        sz = float(fill.get('sz', 0))
        volume = px * sz
        pnl = float(fill.get('closedPnl', 0))
        fee = float(fill.get('fee', 0))
        coin = fill.get('coin', 'UNKNOWN')
        side = fill.get('side', '?')
        direction = fill.get('dir', 'Unknown')
        ts = fill.get('time', 0)

        stats['total_volume'] += volume
        stats['total_pnl'] += pnl
        stats['total_fees'] += fee

        if pnl > 0:
            stats['winning_trades'] += 1
            if pnl > stats['largest_win']:
                stats['largest_win'] = pnl
        elif pnl < 0:
            stats['losing_trades'] += 1
            if pnl < stats['largest_loss']:
                stats['largest_loss'] = pnl

        if side == 'B':
            stats['buys'] += 1
            stats['buy_volume'] += volume
        else:
            stats['sells'] += 1
            stats['sell_volume'] += volume

        stats['coins'][coin]['count'] += 1
        stats['coins'][coin]['volume'] += volume
        stats['coins'][coin]['pnl'] += pnl

        stats['directions'][direction] += 1

        if stats['first_fill'] is None or (ts and ts < stats['first_fill']):
            stats['first_fill'] = ts
        if stats['last_fill'] is None or (ts and ts > stats['last_fill']):
            stats['last_fill'] = ts

    return stats


# ==================== DISPLAY FUNCTIONS ====================
def display_summary_panels(stats, address, total_available):
    """Display summary stat panels"""
    # Calculate win rate
    total_closed = stats['winning_trades'] + stats['losing_trades']
    win_rate = (stats['winning_trades'] / total_closed * 100) if total_closed > 0 else 0

    pnl_color = "green" if stats['total_pnl'] >= 0 else "red"
    pnl_sign = "+" if stats['total_pnl'] >= 0 else ""

    # Panel 1: Trade Overview
    panel1_lines = [
        f"[bold cyan]Wallet:[/bold cyan] [dim]{address[:16]}...{address[-8:]}[/dim]",
        f"[bold cyan]Total Fills:[/bold cyan] [yellow]{stats['total_fills']:,}[/yellow] / [dim]{total_available:,} available[/dim]",
        f"[bold cyan]Total Volume:[/bold cyan] [yellow]{format_usd(stats['total_volume'])}[/yellow]",
        f"[bold cyan]Total Fees:[/bold cyan] [red]{format_usd(stats['total_fees'])}[/red]",
    ]

    if stats['first_fill'] and stats['last_fill']:
        panel1_lines.append(f"[bold cyan]Date Range:[/bold cyan] [dim]{format_timestamp(stats['first_fill'])} - {format_timestamp(stats['last_fill'])}[/dim]")

    panel1 = Panel(
        "\n".join(panel1_lines),
        title="[bold white]Trade Overview[/bold white]",
        border_style="bright_cyan",
        box=box.ROUNDED,
        padding=(0, 1)
    )

    # Panel 2: PnL Summary
    panel2_lines = [
        f"[bold cyan]Realized PnL:[/bold cyan] [{pnl_color}]{pnl_sign}{format_usd(stats['total_pnl'])}[/{pnl_color}]",
        f"[bold cyan]Winning Trades:[/bold cyan] [green]{stats['winning_trades']:,}[/green]",
        f"[bold cyan]Losing Trades:[/bold cyan] [red]{stats['losing_trades']:,}[/red]",
        f"[bold cyan]Win Rate:[/bold cyan] [{'green' if win_rate >= 50 else 'red'}]{win_rate:.1f}%[/{'green' if win_rate >= 50 else 'red'}]",
        f"[bold cyan]Largest Win:[/bold cyan] [green]+{format_usd(stats['largest_win'])}[/green]",
        f"[bold cyan]Largest Loss:[/bold cyan] [red]{format_usd(stats['largest_loss'])}[/red]",
    ]

    panel2 = Panel(
        "\n".join(panel2_lines),
        title="[bold white]PnL Summary[/bold white]",
        border_style="bright_green" if stats['total_pnl'] >= 0 else "bright_red",
        box=box.ROUNDED,
        padding=(0, 1)
    )

    # Panel 3: Buy/Sell Breakdown
    total_trades = stats['buys'] + stats['sells']
    buy_pct = (stats['buys'] / total_trades * 100) if total_trades > 0 else 0

    panel3_lines = [
        f"[bold green]Buys:[/bold green] [green]{stats['buys']:,}[/green] ({buy_pct:.1f}%)",
        f"[bold red]Sells:[/bold red] [red]{stats['sells']:,}[/red] ({100-buy_pct:.1f}%)",
        f"[bold green]Buy Volume:[/bold green] [green]{format_usd(stats['buy_volume'])}[/green]",
        f"[bold red]Sell Volume:[/bold red] [red]{format_usd(stats['sell_volume'])}[/red]",
        "",
        f"[dim]{'[green]' + '█' * int(buy_pct/5) + '[/green]' + '[red]' + '█' * int((100-buy_pct)/5) + '[/red]'}[/dim]",
    ]

    panel3 = Panel(
        "\n".join(panel3_lines),
        title="[bold white]Buy/Sell Ratio[/bold white]",
        border_style="bright_yellow",
        box=box.ROUNDED,
        padding=(0, 1)
    )

    console.print(Columns([panel1, panel2, panel3], equal=True, expand=True))


def display_coin_breakdown(stats):
    """Display breakdown by coin"""
    console.print(Panel(
        "📊 [bold white]COIN BREAKDOWN[/bold white]  [dim cyan]GET https://api.moondev.com/api/user/{address}/fills[/dim cyan]",
        border_style="magenta",
        padding=(0, 1)
    ))

    table = Table(box=box.ROUNDED, border_style="magenta", header_style="bold cyan", padding=(0, 1))
    table.add_column("Coin", style="bold white", justify="center", width=10)
    table.add_column("Trades", style="yellow", justify="right", width=10)
    table.add_column("Volume", style="cyan", justify="right", width=14)
    table.add_column("Realized PnL", justify="right", width=14)
    table.add_column("Avg Trade Size", style="dim", justify="right", width=14)

    coin_emoji = {
        'BTC': '₿', 'ETH': 'Ξ', 'SOL': '◎', 'HYPE': '🔥', 'XRP': '✕',
        'SUI': '💧', 'AVAX': '🔺', 'ARB': '🔵', 'DOGE': '🐕', 'PEPE': '🐸',
        'WIF': '🐶', 'BONK': '🦴', 'LINK': '🔗', 'OP': '🔴', 'MATIC': '💜'
    }

    # Sort coins by volume
    sorted_coins = sorted(stats['coins'].items(), key=lambda x: x[1]['volume'], reverse=True)

    for coin, data in sorted_coins[:15]:
        emoji = coin_emoji.get(coin.upper(), '🪙')
        count = data['count']
        volume = data['volume']
        pnl = data['pnl']
        avg_size = volume / count if count > 0 else 0

        pnl_text = format_pnl(pnl)

        table.add_row(
            f"{emoji} {coin}",
            f"{count:,}",
            format_usd(volume),
            pnl_text,
            format_usd(avg_size)
        )

    console.print(table)


def display_direction_breakdown(stats):
    """Display breakdown by trade direction"""
    console.print(Panel(
        "📊 [bold white]TRADE DIRECTION BREAKDOWN[/bold white]  [dim cyan]GET https://api.moondev.com/api/user/{address}/fills[/dim cyan]",
        border_style="yellow",
        padding=(0, 1)
    ))

    table = Table(box=box.SIMPLE_HEAD, border_style="yellow", header_style="bold white", padding=(0, 1))
    table.add_column("Direction", style="bold", width=20)
    table.add_column("Count", style="cyan", justify="right", width=12)
    table.add_column("% of Total", justify="right", width=12)

    total = sum(stats['directions'].values())
    sorted_dirs = sorted(stats['directions'].items(), key=lambda x: x[1], reverse=True)

    direction_colors = {
        'Open Long': 'green',
        'Open Short': 'red',
        'Close Long': 'bright_green',
        'Close Short': 'bright_red',
        'Buy': 'green',
        'Sell': 'red',
    }

    for direction, count in sorted_dirs:
        pct = (count / total * 100) if total > 0 else 0
        color = direction_colors.get(direction, 'white')
        table.add_row(
            f"[{color}]{direction}[/{color}]",
            f"{count:,}",
            f"{pct:.1f}%"
        )

    console.print(table)


def display_recent_fills(fills, limit=25):
    """Display recent fills in a beautiful table"""
    console.print(Panel(
        f"📊 [bold white]RECENT TRADES (Last {min(len(fills), limit)})[/bold white]  [dim cyan]GET https://api.moondev.com/api/user/{{address}}/fills[/dim cyan]",
        border_style="cyan",
        padding=(0, 1)
    ))

    table = Table(box=box.ROUNDED, border_style="cyan", header_style="bold magenta", padding=(0, 1))
    table.add_column("Time", style="dim", width=14)
    table.add_column("Coin", style="bold white", justify="center", width=8)
    table.add_column("Side", justify="center", width=6)
    table.add_column("Direction", width=14)
    table.add_column("Size", style="cyan", justify="right", width=12)
    table.add_column("Price", style="yellow", justify="right", width=12)
    table.add_column("Value", style="white", justify="right", width=12)
    table.add_column("PnL", justify="right", width=12)
    table.add_column("Fee", style="dim", justify="right", width=8)

    coin_emoji = {
        'BTC': '₿', 'ETH': 'Ξ', 'SOL': '◎', 'HYPE': '🔥', 'XRP': '✕',
        'SUI': '💧', 'AVAX': '🔺', 'ARB': '🔵', 'DOGE': '🐕', 'PEPE': '🐸'
    }

    for fill in fills[:limit]:
        ts = fill.get('time', 0)
        coin = fill.get('coin', '?')
        side = fill.get('side', '?')
        direction = fill.get('dir', 'Unknown')
        sz = float(fill.get('sz', 0))
        px = float(fill.get('px', 0))
        pnl = float(fill.get('closedPnl', 0))
        fee = float(fill.get('fee', 0))
        value = sz * px

        # Time formatting
        time_str = format_timestamp(ts)

        # Side with color
        if side == 'B':
            side_text = Text("BUY", style="bold green")
        else:
            side_text = Text("SELL", style="bold red")

        # Direction with color
        if 'Long' in direction and 'Open' in direction:
            dir_text = Text(direction, style="green")
        elif 'Short' in direction and 'Open' in direction:
            dir_text = Text(direction, style="red")
        elif 'Long' in direction and 'Close' in direction:
            dir_text = Text(direction, style="bright_green")
        elif 'Short' in direction and 'Close' in direction:
            dir_text = Text(direction, style="bright_red")
        else:
            dir_text = Text(direction, style="white")

        # Coin with emoji
        emoji = coin_emoji.get(coin.upper(), '')
        coin_str = f"{emoji}{coin}" if emoji else coin

        # Size formatting
        size_str = f"{sz:,.4f}" if sz < 100 else f"{sz:,.2f}"

        # Price formatting
        price_str = f"${px:,.2f}" if px < 10000 else f"${px:,.0f}"

        # Value formatting
        value_str = format_usd(value)

        # PnL with color
        pnl_text = format_pnl(pnl)

        # Fee
        fee_str = f"${fee:.2f}"

        table.add_row(
            time_str,
            coin_str,
            side_text,
            dir_text,
            size_str,
            price_str,
            value_str,
            pnl_text,
            fee_str
        )

    console.print(table)


def display_win_streak_analysis(fills):
    """Analyze and display win/loss streaks"""
    console.print(Panel(
        "📊 [bold white]WIN/LOSS STREAK ANALYSIS[/bold white]  [dim cyan]GET https://api.moondev.com/api/user/{address}/fills[/dim cyan]",
        border_style="green",
        padding=(0, 1)
    ))

    current_streak = 0
    max_win_streak = 0
    max_loss_streak = 0
    current_type = None

    for fill in fills:
        pnl = float(fill.get('closedPnl', 0))
        if pnl == 0:
            continue

        if pnl > 0:
            if current_type == 'win':
                current_streak += 1
            else:
                current_streak = 1
                current_type = 'win'
            max_win_streak = max(max_win_streak, current_streak)
        else:
            if current_type == 'loss':
                current_streak += 1
            else:
                current_streak = 1
                current_type = 'loss'
            max_loss_streak = max(max_loss_streak, current_streak)

    lines = [
        f"[bold green]Max Winning Streak:[/bold green] [green]{max_win_streak}[/green] trades in a row",
        f"[bold red]Max Losing Streak:[/bold red] [red]{max_loss_streak}[/red] trades in a row",
        f"[bold cyan]Current Streak:[/bold cyan] [{'green' if current_type == 'win' else 'red'}]{current_streak} {'wins' if current_type == 'win' else 'losses'}[/{'green' if current_type == 'win' else 'red'}]",
    ]

    console.print("\n".join(lines))


# ==================== FOOTER ====================
def print_footer():
    """Print footer with timestamp and branding"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(f"\n[dim cyan]{'─' * 100}[/dim cyan]")
    console.print(f"[dim cyan]Moon Dev's Trade History Dashboard | {now} | api.moondev.com | Built with love by Moon Dev[/dim cyan]")


# ==================== MAIN ====================
def main():
    """Main function - Moon Dev's Trade History Dashboard"""
    console.clear()
    console.print(create_banner())

    # Parse command line args
    if len(sys.argv) > 1:
        address = sys.argv[1]
    else:
        # Default to HLP_LONG for demo
        address = "0x010461c14e146ac35fe42271bdc1134ee31c703a"
        console.print(f"[dim]No address provided, using default: {address[:10]}...[/dim]")

    limit = 100
    if len(sys.argv) > 2:
        limit = int(sys.argv[2])

    # Optional time window - Moon Dev: this is the fast lane, ~50ms for ANY wallet
    minutes = None
    if len(sys.argv) > 3:
        minutes = float(sys.argv[3])

    console.print(f"[bold cyan]Moon Dev: Fetching trade history for {address[:10]}...{address[-6:]}[/bold cyan]")
    console.print(f"[dim]Limit: {limit if limit > 0 else 'ALL'} fills[/dim]")
    if minutes:
        console.print(f"[dim]Window: last {minutes} minutes (fast lane, ~50ms)[/dim]")
    else:
        console.print("[dim]No time window. First contact with a fill-sparse wallet can take ~30s.[/dim]")
        console.print("[dim]Tip: pass minutes as the 3rd arg to use the fast lane.[/dim]")
    console.print()

    # Initialize API
    api = MoonDevAPI()

    if not api.api_key:
        console.print(Panel(
            "[bold red]ERROR: No API key found![/bold red]\n"
            "Please set MOONDEV_API_KEY in your .env file\n"
            "[dim]MOONDEV_API_KEY=your_key_here[/dim]\n\n"
            "Get your API key at: [link=https://moondev.com]https://moondev.com[/link]",
            border_style="red",
            title="Authentication Required",
            padding=(0, 1)
        ))
        return

    # Fetch fills
    with console.status("[bold cyan]Moon Dev: Scanning local node for fills...[/bold cyan]"):
        try:
            fills_data = api.get_user_fills(address, limit=limit, minutes=minutes)
        except requests.HTTPError as e:
            # 503 fills_scanner_busy means RETRY OR FALL BACK, never "no fills"
            if e.response is not None and e.response.status_code == 503:
                console.print(Panel(
                    "[bold yellow]Fills scanner is busy (fills_scanner_busy)[/bold yellow]\n"
                    "[dim]Retry shortly or use your fallback source. This is NOT an empty result.[/dim]",
                    border_style="yellow",
                    title="Service Busy",
                    padding=(0, 1)
                ))
                return
            raise

    if not isinstance(fills_data, dict):
        console.print("[red]Error: Invalid response from API[/red]")
        return

    fills = fills_data.get('fills', [])
    total_available = fills_data.get('count', len(fills))

    if not fills:
        # HTTP 200 with an empty list always means genuinely no fills
        console.print(Panel(
            f"[yellow]No fills found for address {address}[/yellow]\n"
            "[dim]This wallet has no trading history in this window on Hyperliquid.[/dim]",
            border_style="yellow",
            title="No Data",
            padding=(0, 1)
        ))
        return

    console.print(f"[green]Found {total_available:,} total fills! Analyzing {len(fills):,}...[/green]")
    console.print()

    # Calculate stats
    stats = calculate_fill_stats(fills)

    # Display everything!
    display_summary_panels(stats, address, total_available)
    console.print()

    display_coin_breakdown(stats)
    console.print()

    display_direction_breakdown(stats)
    console.print()

    display_win_streak_analysis(fills)
    console.print()

    display_recent_fills(fills, limit=30)

    print_footer()


if __name__ == "__main__":
    main()

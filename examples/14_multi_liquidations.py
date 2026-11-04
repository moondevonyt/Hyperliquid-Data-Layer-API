"""
🌙 Moon Dev's Multi-Exchange Liquidation Dashboard
===================================================
Beautiful terminal dashboard for liquidations across ALL exchanges:
- Hyperliquid
- Binance Futures
- Bybit
- OKX

Built with love by Moon Dev 🚀 | Run with: python -m api_examples.14_multi_liquidations
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
from rich.layout import Layout
from rich.live import Live
from rich import box
import time

# Initialize Rich console
console = Console()

# Exchange colors and emojis
EXCHANGE_STYLE = {
    'hyperliquid': {'color': 'cyan', 'emoji': '💎', 'name': 'Hyperliquid'},
    'binance': {'color': 'yellow', 'emoji': '🟡', 'name': 'Binance'},
    'bybit': {'color': 'orange1', 'emoji': '🟠', 'name': 'Bybit'},
    'okx': {'color': 'bright_white', 'emoji': '⚪', 'name': 'OKX'},
}

# ==================== BANNER ====================
def print_banner():
    """Print the Moon Dev banner"""
    banner = """███╗   ███╗██╗   ██╗██╗  ████████╗██╗    ██╗     ██╗ ██████╗
████╗ ████║██║   ██║██║  ╚══██╔══╝██║    ██║     ██║██╔═══██╗
██╔████╔██║██║   ██║██║     ██║   ██║    ██║     ██║██║   ██║
██║╚██╔╝██║██║   ██║██║     ██║   ██║    ██║     ██║██║▄▄ ██║
██║ ╚═╝ ██║╚██████╔╝███████╗██║   ██║    ███████╗██║╚██████╔╝
╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝    ╚══════╝╚═╝ ╚══▀▀═╝"""
    console.print(Panel(
        Align.center(Text(banner, style="bold red")),
        title="🔥 [bold yellow]MULTI-EXCHANGE LIQUIDATION DASHBOARD[/bold yellow] 🔥",
        subtitle="[dim]💥 Hyperliquid • Binance • Bybit • OKX | by Moon Dev 💥[/dim]",
        border_style="red",
        box=box.DOUBLE_EDGE,
        padding=(0, 1)
    ))

# ==================== HELPER FUNCTIONS ====================
def format_usd(value):
    """Format USD value with commas and dollar sign"""
    if value is None or value == 0:
        return "$0"
    if abs(value) >= 1_000_000_000:
        return f"${value/1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    elif abs(value) >= 1_000:
        return f"${value/1_000:.1f}K"
    return f"${value:,.0f}"

def format_count(value):
    """Format count with K/M suffixes"""
    if value is None or value == 0:
        return "0"
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    return f"{value:,}"

def get_exchange_style(exchange):
    """Get style info for an exchange"""
    ex_lower = exchange.lower()
    return EXCHANGE_STYLE.get(ex_lower, {'color': 'white', 'emoji': '🔹', 'name': exchange})

# ==================== COMBINED STATS DASHBOARD ====================
def display_combined_stats(api):
    """Display combined stats across all exchanges"""
    console.print(Panel(
        "📊 [bold white]COMBINED STATS (24H)[/bold white]  [dim cyan]GET https://api.moondev.com/api/all_liquidations/stats.json[/dim cyan]",
        border_style="bright_white",
        padding=(0, 1)
    ))

    try:
        stats = api.get_all_liquidation_stats()

        if not isinstance(stats, dict):
            console.print("[dim]No combined stats available[/dim]")
            return

        # Main stats
        total_count = stats.get('total_count', stats.get('count', 0))
        total_volume = stats.get('total_volume', stats.get('total_value_usd', 0))

        # Create main stats panel
        main_panel = Panel(
            f"[bold white]🔥 TOTAL LIQUIDATIONS[/bold white]\n\n"
            f"[bold cyan]{format_count(total_count)}[/bold cyan] liquidations\n"
            f"[bold yellow]{format_usd(total_volume)}[/bold yellow] volume",
            border_style="red",
            width=35,
            padding=(1, 2)
        )

        # Long/Short breakdown
        long_count = stats.get('long_count', stats.get('longs', 0))
        short_count = stats.get('short_count', stats.get('shorts', 0))
        long_volume = stats.get('long_volume', 0)
        short_volume = stats.get('short_volume', 0)

        ls_panel = Panel(
            f"[bold green]📈 LONGS[/bold green]\n"
            f"[green]{format_count(long_count)}[/green] liqs | [yellow]{format_usd(long_volume)}[/yellow]\n\n"
            f"[bold red]📉 SHORTS[/bold red]\n"
            f"[red]{format_count(short_count)}[/red] liqs | [yellow]{format_usd(short_volume)}[/yellow]",
            border_style="magenta",
            width=35,
            padding=(1, 2)
        )

        console.print(Columns([main_panel, ls_panel], equal=True, expand=True))

    except Exception as e:
        console.print(f"[red]🌙 Moon Dev: Error fetching combined stats: {e}[/red]")

# ==================== EXCHANGE BREAKDOWN ====================
def display_exchange_breakdown(api):
    """Display breakdown by exchange"""
    console.print(Panel(
        "🏦 [bold cyan]EXCHANGE BREAKDOWN (24H)[/bold cyan]  [dim cyan]GET https://api.moondev.com/api/all_liquidations/stats.json[/dim cyan]",
        border_style="cyan",
        padding=(0, 1)
    ))

    try:
        stats = api.get_all_liquidation_stats()

        if not isinstance(stats, dict):
            console.print("[dim]No exchange breakdown available[/dim]")
            return

        by_exchange = stats.get('by_exchange', stats.get('exchanges', {}))

        # Also try to get from nested structure
        if not by_exchange and 'stats' in stats:
            by_exchange = stats['stats'].get('by_exchange', {})

        # Calculate totals for percentage
        total_vol = sum(
            ex.get('volume', ex.get('total_volume', 0)) if isinstance(ex, dict) else 0
            for ex in by_exchange.values()
        )
        total_count = sum(
            ex.get('count', ex.get('total_count', 0)) if isinstance(ex, dict) else 0
            for ex in by_exchange.values()
        )

        table = Table(
            box=box.DOUBLE_EDGE,
            border_style="cyan",
            header_style="bold magenta",
            padding=(0, 1),
            expand=True
        )
        table.add_column("🏦 Exchange", style="bold", justify="left", width=18)
        table.add_column("💥 Liquidations", justify="right", width=14)
        table.add_column("💰 Volume", style="yellow", justify="right", width=14)
        table.add_column("📊 % of Total", justify="center", width=12)
        table.add_column("📈 Share", width=25)

        # Sort by volume descending
        sorted_exchanges = sorted(
            by_exchange.items(),
            key=lambda x: x[1].get('volume', x[1].get('total_volume', 0)) if isinstance(x[1], dict) else 0,
            reverse=True
        )

        for exchange, ex_stats in sorted_exchanges:
            if not isinstance(ex_stats, dict):
                continue

            style = get_exchange_style(exchange)
            ex_count = ex_stats.get('count', ex_stats.get('total_count', 0))
            ex_volume = ex_stats.get('volume', ex_stats.get('total_volume', 0))

            # Calculate percentage
            vol_pct = (ex_volume / total_vol * 100) if total_vol > 0 else 0

            # Create visual bar
            bar_width = int(vol_pct / 5)  # 20 chars = 100%
            bar = f"[{style['color']}]{'█' * bar_width}{'░' * (20 - bar_width)}[/{style['color']}]"

            table.add_row(
                f"{style['emoji']} [{style['color']}]{style['name']}[/{style['color']}]",
                f"{format_count(ex_count)}",
                f"[bold]{format_usd(ex_volume)}[/bold]",
                f"{vol_pct:.1f}%",
                bar
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]🌙 Moon Dev: Error fetching exchange breakdown: {e}[/red]")

# ==================== TIMEFRAME COMPARISON ====================
def display_timeframe_comparison(api):
    """Display liquidations across different timeframes"""
    console.print(Panel(
        "⏰ [bold yellow]LIQUIDATIONS BY TIMEFRAME[/bold yellow]  [dim cyan]GET https://api.moondev.com/api/all_liquidations/{timeframe}.json[/dim cyan]",
        border_style="yellow",
        padding=(0, 1)
    ))

    table = Table(
        box=box.DOUBLE_EDGE,
        border_style="yellow",
        header_style="bold cyan",
        padding=(0, 1),
        expand=True
    )
    table.add_column("⏰ TF", style="bold cyan", justify="center", width=8)
    table.add_column("💎 Hyperliquid", style="cyan", justify="right", width=14)
    table.add_column("🟡 Binance", style="yellow", justify="right", width=14)
    table.add_column("🟠 Bybit", style="orange1", justify="right", width=14)
    table.add_column("⚪ OKX", style="white", justify="right", width=14)
    table.add_column("🔥 TOTAL", style="bold red", justify="right", width=14)

    timeframes = ["10m", "1h", "4h", "24h"]

    for tf in timeframes:
        row = [f"[bold]{tf}[/bold]"]

        total_for_tf = 0

        # Hyperliquid
        try:
            data = api.get_liquidations(tf)
            if isinstance(data, dict):
                count = data.get('stats', data).get('total_count', 0)
            elif isinstance(data, list):
                count = len(data)
            else:
                count = 0
            row.append(format_count(count))
            total_for_tf += count
        except:
            row.append("[dim]--[/dim]")

        # Binance
        try:
            data = api.get_binance_liquidations(tf)
            count = len(data) if isinstance(data, list) else len(data.get('liquidations', data.get('data', []))) if isinstance(data, dict) else 0
            row.append(format_count(count))
            total_for_tf += count
        except:
            row.append("[dim]--[/dim]")

        # Bybit
        try:
            data = api.get_bybit_liquidations(tf)
            count = len(data) if isinstance(data, list) else len(data.get('liquidations', data.get('data', []))) if isinstance(data, dict) else 0
            row.append(format_count(count))
            total_for_tf += count
        except:
            row.append("[dim]--[/dim]")

        # OKX
        try:
            data = api.get_okx_liquidations(tf)
            count = len(data) if isinstance(data, list) else len(data.get('liquidations', data.get('data', []))) if isinstance(data, dict) else 0
            row.append(format_count(count))
            total_for_tf += count
        except:
            row.append("[dim]--[/dim]")

        # Total
        row.append(f"[bold red]{format_count(total_for_tf)}[/bold red]")

        table.add_row(*row)

    console.print(table)

# ==================== TOP LIQUIDATIONS ====================
def display_top_liquidations(api):
    """Display top liquidations from all exchanges combined"""
    console.print(Panel(
        "🏆 [bold red]TOP LIQUIDATIONS (1H)[/bold red]  [dim cyan]GET https://api.moondev.com/api/all_liquidations/1h.json[/dim cyan]",
        border_style="red",
        padding=(0, 1)
    ))

    try:
        data = api.get_all_liquidations("1h")

        # Handle different response formats
        if isinstance(data, list):
            liq_list = data
        elif isinstance(data, dict):
            liq_list = data.get('liquidations', data.get('data', []))
        else:
            liq_list = []

        if not liq_list:
            console.print("[dim]No recent liquidations found[/dim]")
            return

        # Sort by value
        try:
            liq_list = sorted(
                liq_list,
                key=lambda x: float(x.get('value', x.get('usd_value', x.get('value_usd', x.get('quantity', 0))))),
                reverse=True
            )
        except:
            pass

        table = Table(
            box=box.ROUNDED,
            border_style="red",
            header_style="bold yellow",
            padding=(0, 1),
            expand=True
        )
        table.add_column("#", style="dim", width=3)
        table.add_column("🏦 Exchange", justify="center", width=14)
        table.add_column("🪙 Symbol", style="cyan", justify="center", width=10)
        table.add_column("💰 Value", style="yellow", justify="right", width=14)
        table.add_column("📊 Side", justify="center", width=10)
        table.add_column("💵 Price", style="white", justify="right", width=12)
        table.add_column("⏰ Time", style="dim", width=12)

        for i, liq in enumerate(liq_list[:20], 1):
            # Extract fields with fallbacks
            exchange = liq.get('exchange', liq.get('source', 'unknown'))
            symbol = liq.get('symbol', liq.get('coin', '?'))
            value = float(liq.get('value', liq.get('usd_value', liq.get('value_usd', liq.get('quantity', 0)))))
            side = liq.get('side', liq.get('direction', '?'))
            price = float(liq.get('price', liq.get('px', 0)))
            timestamp = liq.get('timestamp', liq.get('time', ''))

            # Format exchange
            style = get_exchange_style(exchange)
            ex_display = f"{style['emoji']} [{style['color']}]{style['name'][:8]}[/{style['color']}]"

            # Format side
            if str(side).lower() in ['long', 'buy', 'b']:
                side_display = "[green]📈 LONG[/green]"
            else:
                side_display = "[red]📉 SHORT[/red]"

            # Format time
            if timestamp:
                try:
                    if isinstance(timestamp, (int, float)):
                        dt = datetime.fromtimestamp(timestamp / 1000 if timestamp > 1e10 else timestamp)
                        time_str = dt.strftime("%H:%M:%S")
                    else:
                        time_str = str(timestamp)[11:19]
                except:
                    time_str = str(timestamp)[:10]
            else:
                time_str = "N/A"

            # Rank emoji
            rank = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else str(i)

            # Clean symbol (remove USDT/USD suffix)
            symbol_clean = symbol.replace("USDT", "").replace("USD", "").replace("-SWAP", "")[:8]

            table.add_row(
                rank,
                ex_display,
                symbol_clean,
                f"[bold]{format_usd(value)}[/bold]",
                side_display,
                f"${price:,.2f}" if price else "N/A",
                time_str
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]🌙 Moon Dev: Error fetching top liquidations: {e}[/red]")

# ==================== COIN BREAKDOWN ====================
def display_coin_breakdown(api):
    """Display liquidations broken down by coin across all exchanges"""
    console.print(Panel(
        "🪙 [bold magenta]LIQUIDATIONS BY COIN (24H)[/bold magenta]  [dim cyan]GET https://api.moondev.com/api/all_liquidations/stats.json[/dim cyan]",
        border_style="magenta",
        padding=(0, 1)
    ))

    try:
        stats = api.get_all_liquidation_stats()

        if not isinstance(stats, dict):
            console.print("[dim]No coin breakdown available[/dim]")
            return

        by_coin = stats.get('by_coin', stats.get('coins', {}))

        if not by_coin:
            # Try nested structure
            if 'stats' in stats:
                by_coin = stats['stats'].get('by_coin', {})

        if not by_coin:
            console.print("[dim]No coin breakdown in stats[/dim]")
            return

        table = Table(
            box=box.SIMPLE_HEAD,
            border_style="magenta",
            header_style="bold cyan",
            padding=(0, 1)
        )
        table.add_column("🪙 Coin", style="bold", width=10)
        table.add_column("💥 Count", justify="right", width=12)
        table.add_column("💰 Volume", style="yellow", justify="right", width=14)
        table.add_column("📈 Long $", style="green", justify="right", width=12)
        table.add_column("📉 Short $", style="red", justify="right", width=12)

        # Coin emojis
        coin_emoji = {
            'BTC': '₿', 'ETH': 'Ξ', 'SOL': '◎', 'HYPE': '🔥',
            'XRP': '✕', 'SUI': '💧', 'AVAX': '🔺', 'ARB': '🔵',
            'DOGE': '🐕', 'PEPE': '🐸', 'WIF': '🐶', 'LINK': '🔗'
        }

        # Sort by volume
        sorted_coins = sorted(
            by_coin.items(),
            key=lambda x: x[1].get('volume', x[1].get('total_value', 0)) if isinstance(x[1], dict) else 0,
            reverse=True
        )

        for coin, coin_data in sorted_coins[:15]:
            if not isinstance(coin_data, dict):
                continue

            count = coin_data.get('count', 0)
            volume = coin_data.get('volume', coin_data.get('total_value', 0))
            long_vol = coin_data.get('long_volume', coin_data.get('long_value', 0))
            short_vol = coin_data.get('short_volume', coin_data.get('short_value', 0))

            emoji = coin_emoji.get(coin.upper().replace("USDT", "").replace("USD", ""), '🪙')
            coin_clean = coin.replace("USDT", "").replace("USD", "")[:8]

            table.add_row(
                f"{emoji} {coin_clean}",
                f"{format_count(count)}",
                format_usd(volume),
                format_usd(long_vol),
                format_usd(short_vol)
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]🌙 Moon Dev: Error fetching coin breakdown: {e}[/red]")

# ==================== EXCHANGE STATUS ====================
def display_exchange_status(api):
    """Display connection status for each exchange"""
    console.print(Panel(
        "📡 [bold green]EXCHANGE STATUS[/bold green]  [dim cyan]GET https://api.moondev.com/api/all_liquidations/10m.json[/dim cyan]",
        border_style="green",
        padding=(0, 1)
    ))

    exchanges = [
        ("Hyperliquid", "💎", "cyan", api.get_liquidations),
        ("Binance", "🟡", "yellow", api.get_binance_liquidations),
        ("Bybit", "🟠", "orange1", api.get_bybit_liquidations),
        ("OKX", "⚪", "white", api.get_okx_liquidations),
    ]

    panels = []
    for name, emoji, color, func in exchanges:
        try:
            data = func("10m")
            if isinstance(data, list):
                count = len(data)
            elif isinstance(data, dict):
                count = len(data.get('liquidations', data.get('data', [])))
            else:
                count = 0

            status = "[green]✅ CONNECTED[/green]"
            data_info = f"{count} liqs (10m)"
        except Exception as e:
            status = "[red]❌ ERROR[/red]"
            data_info = str(e)[:30]

        panels.append(Panel(
            f"[bold {color}]{emoji} {name}[/bold {color}]\n{status}\n[dim]{data_info}[/dim]",
            border_style=color,
            width=20,
            padding=(0, 1)
        ))

    console.print(Columns(panels, equal=True, expand=True))

# ==================== FOOTER ====================
def print_footer():
    """Print footer with timestamp and branding"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(f"[dim red]─────────────────────────────────────────────────────────────────────────────────────────────[/dim red]")
    console.print(f"[dim red]🌙 Moon Dev's Multi-Exchange Liquidation Dashboard | {now} | 📡 api.moondev.com | Built with 💜 by Moon Dev[/dim red]")

# ==================== MAIN ====================
def main():
    """Main function - Moon Dev's Multi-Exchange Liquidation Dashboard"""
    console.clear()
    print_banner()

    console.print("[bold cyan]🌙 Moon Dev: Initializing API connection...[/bold cyan]")
    api = MoonDevAPI()

    if not api.api_key:
        console.print(Panel(
            "[bold red]❌ ERROR: No API key found![/bold red]\n\n"
            "Please set MOONDEV_API_KEY in your .env file:\n"
            "[dim]MOONDEV_API_KEY=your_key_here[/dim]\n\n"
            "🌙 Apply for an API key at: [link=https://moondev.com/apply]https://moondev.com/apply[/link]",
            border_style="red",
            title="🔑 Authentication Required",
            padding=(0, 1)
        ))
        return

    console.print(f"[green]✅ API key loaded (...{api.api_key[-4:]})[/green]")
    console.print()

    with console.status("[bold red]🌙 Fetching multi-exchange liquidation data...[/bold red]"):
        time.sleep(0.5)

    # Display all sections
    display_exchange_status(api)
    console.print()
    display_combined_stats(api)
    console.print()
    display_exchange_breakdown(api)
    console.print()
    display_timeframe_comparison(api)
    console.print()
    display_top_liquidations(api)
    console.print()
    display_coin_breakdown(api)

    print_footer()

if __name__ == "__main__":
    main()

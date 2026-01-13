"""
🌙 Moon Dev's Liquidation Dashboard - Beautiful Terminal Dashboard for Hyperliquid Liquidation Data
Built with love by Moon Dev 🚀 | Run with: python -m API_examples.01_liquidations
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

# ==================== BANNER ====================
def print_banner():
    """Print the Moon Dev banner"""
    banner = """███╗   ███╗ ██████╗  ██████╗ ███╗   ██╗    ██████╗ ███████╗██╗   ██╗
████╗ ████║██╔═══██╗██╔═══██╗████╗  ██║    ██╔══██╗██╔════╝██║   ██║
██╔████╔██║██║   ██║██║   ██║██╔██╗ ██║    ██║  ██║█████╗  ██║   ██║
██║╚██╔╝██║██║   ██║██║   ██║██║╚██╗██║    ██║  ██║██╔══╝  ╚██╗ ██╔╝
██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██║ ╚████║    ██████╔╝███████╗ ╚████╔╝
╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝    ╚═════╝ ╚══════╝  ╚═══╝"""
    console.print(Panel(
        Align.center(Text(banner, style="bold cyan")),
        title="🌙 [bold magenta]LIQUIDATION DASHBOARD[/bold magenta] 🌙",
        subtitle="[dim]💥 Real-Time Liquidation Intelligence by Moon Dev 💥[/dim]",
        border_style="bright_cyan",
        box=box.DOUBLE_EDGE,
        padding=(0, 1)
    ))

# ==================== HELPER FUNCTIONS ====================
def format_usd(value):
    """Format USD value with commas and dollar sign"""
    if value is None:
        return "$0"
    if value >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"${value/1_000:.1f}K"
    return f"${value:,.0f}"

def format_address(address):
    """Format wallet address for display - Moon Dev wants FULL addresses!"""
    if not address:
        return "Unknown"
    return address

def create_progress_bar(value, total, color="cyan"):
    """Create a simple text-based progress bar"""
    if total == 0:
        return "[dim]No data[/dim]"
    percentage = min(value / total * 100, 100)
    filled = int(percentage / 5)  # 20 chars total
    empty = 20 - filled
    bar = f"[{color}]{'█' * filled}{'░' * empty}[/{color}]"
    return f"{bar} {percentage:.1f}%"

# ==================== TIMEFRAME LIQUIDATIONS TABLE ====================
def display_timeframe_liquidations(api):
    """Display liquidations across different timeframes"""
    console.print(Panel("💥 [bold yellow]LIQUIDATION OVERVIEW BY TIMEFRAME[/bold yellow]  [dim cyan]GET https://api.moondev.com/api/liquidations/{timeframe}.json[/dim cyan]", border_style="yellow", padding=(0, 1)))
    table = Table(box=box.DOUBLE_EDGE, border_style="cyan", header_style="bold magenta", padding=(0, 1))
    table.add_column("⏰ Timeframe", style="cyan", justify="center", width=12)
    table.add_column("💥 Total Count", style="white", justify="right", width=14)
    table.add_column("💰 Total USD", style="yellow", justify="right", width=16)
    table.add_column("📈 Longs (Count)", style="green", justify="right", width=16)
    table.add_column("📉 Shorts (Count)", style="red", justify="right", width=16)
    table.add_column("📊 Long/Short Ratio", justify="center", width=20)
    for tf in ["10m", "1h", "4h", "24h"]:
        try:
            data = api.get_liquidations(tf)
            if isinstance(data, dict):
                stats = data.get('stats', data)
                total_count = stats.get('total_count', 0)
                total_usd = stats.get('total_value_usd', stats.get('total_usd', 0))
                long_count = stats.get('long_count', stats.get('longs', 0))
                short_count = stats.get('short_count', stats.get('shorts', 0))
                total_ls = long_count + short_count if (long_count + short_count) > 0 else 1
                long_pct = (long_count / total_ls) * 100
                if long_pct > 60:
                    ratio_bar = f"[green]{'█' * int(long_pct/5)}[/green][red]{'█' * int((100-long_pct)/5)}[/red] {long_pct:.0f}% L"
                elif long_pct < 40:
                    ratio_bar = f"[green]{'█' * int(long_pct/5)}[/green][red]{'█' * int((100-long_pct)/5)}[/red] {100-long_pct:.0f}% S"
                else:
                    ratio_bar = f"[green]{'█' * int(long_pct/5)}[/green][red]{'█' * int((100-long_pct)/5)}[/red] Balanced"
                table.add_row(f"[bold]{tf}[/bold]", f"{total_count:,}", format_usd(total_usd), f"[green]{long_count:,}[/green]", f"[red]{short_count:,}[/red]", ratio_bar)
            else:
                table.add_row(tf, "N/A", "N/A", "N/A", "N/A", "N/A")
        except Exception as e:
            table.add_row(tf, "[dim]Error[/dim]", "", "", "", "")
    console.print(table)

# ==================== LIQUIDATION STATS ====================
def display_liquidation_stats(api):
    """Display aggregated liquidation statistics"""
    console.print(Panel("📊 [bold cyan]AGGREGATED LIQUIDATION STATISTICS (24H)[/bold cyan]  [dim cyan]GET https://api.moondev.com/api/liquidations/stats.json[/dim cyan]", border_style="cyan", padding=(0, 1)))
    try:
        stats = api.get_liquidation_stats()
        if isinstance(stats, dict):
            windows = stats.get('windows', {})
            window_24h = windows.get('24h', windows.get('4h', {}))
            panels = []
            total_count = window_24h.get('total_count', 0)
            total_usd = window_24h.get('total_value_usd', 0)
            panels.append(Panel(
                f"[bold white]💥 TOTAL LIQUIDATIONS[/bold white]\n[bold cyan]{total_count:,}[/bold cyan] events | [bold yellow]{format_usd(total_usd)}[/bold yellow]",
                border_style="cyan", width=30, padding=(0, 1)
            ))
            long_count = window_24h.get('long_count', 0)
            long_usd = window_24h.get('long_value_usd', 0)
            panels.append(Panel(
                f"[bold green]📈 LONG LIQUIDATIONS[/bold green]\n[bold green]{long_count:,}[/bold green] events | [bold yellow]{format_usd(long_usd)}[/bold yellow]",
                border_style="green", width=30, padding=(0, 1)
            ))
            short_count = window_24h.get('short_count', 0)
            short_usd = window_24h.get('short_value_usd', 0)
            panels.append(Panel(
                f"[bold red]📉 SHORT LIQUIDATIONS[/bold red]\n[bold red]{short_count:,}[/bold red] events | [bold yellow]{format_usd(short_usd)}[/bold yellow]",
                border_style="red", width=30, padding=(0, 1)
            ))
            console.print(Columns(panels, equal=True, expand=True))
            total_ls = long_count + short_count if (long_count + short_count) > 0 else 1
            long_pct, short_pct = (long_count / total_ls) * 100, (short_count / total_ls) * 100
            ratio_text = Text()
            ratio_text.append("📈 LONGS ", style="bold green")
            ratio_text.append("█" * int(long_pct / 2), style="green")
            ratio_text.append("░" * int(short_pct / 2), style="red")
            ratio_text.append(" 📉 SHORTS", style="bold red")
            console.print(Panel(Align.center(ratio_text), title=f"[bold white]Long/Short Ratio: {long_pct:.1f}% / {short_pct:.1f}%[/bold white]", border_style="magenta", padding=(0, 1)))
    except Exception as e:
        console.print(f"[red]🌙 Moon Dev: Error fetching stats: {e}[/red]")

# ==================== TOP LIQUIDATIONS ====================
def display_top_liquidations(api):
    """Display top 10 largest liquidations from stats endpoint"""
    console.print(Panel("🔥 [bold red]TOP 10 LARGEST LIQUIDATIONS (24H)[/bold red]  [dim cyan]GET https://api.moondev.com/api/liquidations/stats.json[/dim cyan]", border_style="red", padding=(0, 1)))
    try:
        stats = api.get_liquidation_stats()
        if isinstance(stats, dict):
            windows = stats.get('windows', {})
            window_24h = windows.get('24h', windows.get('4h', {}))
            largest = window_24h.get('largest', [])
            if isinstance(largest, list) and len(largest) > 0:
                table = Table(box=box.ROUNDED, border_style="red", header_style="bold yellow", padding=(0, 1))
                table.add_column("#", style="dim", width=3)
                table.add_column("💰 Value", style="yellow", justify="right", width=14)
                table.add_column("🪙 Coin", style="cyan", justify="center", width=8)
                table.add_column("📊 Side", justify="center", width=10)
                table.add_column("💵 Price", style="white", justify="right", width=12)
                table.add_column("🔗 Wallet", style="dim", width=44)
                table.add_column("⏰ Time", style="dim", width=18)
                for i, liq in enumerate(largest[:10], 1):
                    value = liq.get('value_usd', liq.get('usd', liq.get('value', 0)))
                    coin = liq.get('coin', liq.get('symbol', 'N/A'))
                    side = liq.get('side', liq.get('direction', 'N/A'))
                    wallet = liq.get('address', liq.get('wallet', liq.get('user', '')))
                    price = liq.get('price', 0)
                    timestamp = liq.get('timestamp', liq.get('time', ''))
                    side_display = "[green]📈 LONG[/green]" if side.lower() in ['long', 'buy'] else "[red]📉 SHORT[/red]"
                    if timestamp:
                        try:
                            if isinstance(timestamp, (int, float)):
                                dt = datetime.fromtimestamp(timestamp / 1000 if timestamp > 1e10 else timestamp)
                                time_str = dt.strftime("%m-%d %H:%M")
                            else:
                                time_str = str(timestamp)[5:16].replace('T', ' ')
                        except:
                            time_str = str(timestamp)[:16]
                    else:
                        time_str = "N/A"
                    rank_display = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else str(i)
                    price_str = f"${price:,.2f}" if price else "N/A"
                    table.add_row(rank_display, f"[bold]{format_usd(value)}[/bold]", coin, side_display, price_str, format_address(wallet), time_str)
                console.print(table)
            else:
                console.print("[dim]No individual liquidation data available[/dim]")
    except Exception as e:
        console.print(f"[red]🌙 Moon Dev: Error fetching top liquidations: {e}[/red]")

# ==================== PER-COIN BREAKDOWN ====================
def display_coin_breakdown(api):
    """Display liquidations broken down by coin using stats endpoint"""
    console.print(Panel("🪙 [bold magenta]LIQUIDATIONS BY COIN (24H)[/bold magenta]  [dim cyan]GET https://api.moondev.com/api/liquidations/stats.json[/dim cyan]", border_style="magenta", padding=(0, 1)))
    try:
        stats = api.get_liquidation_stats()
        if isinstance(stats, dict):
            windows = stats.get('windows', {})
            window_24h = windows.get('24h', windows.get('4h', {}))
            by_coin = window_24h.get('by_coin', {})
            if isinstance(by_coin, dict) and len(by_coin) > 0:
                table = Table(box=box.SIMPLE_HEAD, border_style="magenta", header_style="bold cyan", padding=(0, 1))
                table.add_column("🪙 Coin", style="bold", width=12)
                table.add_column("💥 Count", justify="right", width=10)
                table.add_column("💰 Total Value", style="yellow", justify="right", width=14)
                table.add_column("📈 Long $", style="green", justify="right", width=12)
                table.add_column("📉 Short $", style="red", justify="right", width=12)
                table.add_column("📊 Long/Short", width=24)
                sorted_coins = sorted(by_coin.items(), key=lambda x: x[1].get('total_value_usd', x[1].get('total_value', x[1].get('count', 0))) if isinstance(x[1], dict) else 0, reverse=True)
                coin_emoji = {'BTC': '₿', 'ETH': 'Ξ', 'SOL': '◎', 'HYPE': '🔥', 'XRP': '✕', 'SUI': '💧', 'AVAX': '🔺', 'ARB': '🔵'}
                for coin, coin_data in sorted_coins[:10]:
                    if isinstance(coin_data, dict):
                        count = coin_data.get('count', coin_data.get('total_count', 0))
                        total_value = coin_data.get('total_value_usd', coin_data.get('total_value', coin_data.get('total_usd', 0)))
                        long_value = coin_data.get('long_value_usd', coin_data.get('long_value', coin_data.get('long_usd', 0)))
                        short_value = coin_data.get('short_value_usd', coin_data.get('short_value', coin_data.get('short_usd', 0)))
                        total = long_value + short_value if (long_value + short_value) > 0 else 1
                        long_pct = long_value / total
                        green_bars, red_bars = int(long_pct * 20), 20 - int(long_pct * 20)
                        dist_bar = f"[green]{'█' * green_bars}[/green][red]{'█' * red_bars}[/red]"
                        emoji = coin_emoji.get(coin.upper(), '🪙')
                        table.add_row(f"{emoji} {coin}", f"{count:,}", format_usd(total_value), format_usd(long_value), format_usd(short_value), dist_bar)
                console.print(table)
            else:
                console.print("[dim]No per-coin breakdown available[/dim]")
    except Exception as e:
        console.print(f"[red]🌙 Moon Dev: Error fetching coin breakdown: {e}[/red]")

# ==================== FOOTER ====================
def print_footer():
    """Print footer with timestamp and branding"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(f"[dim cyan]─────────────────────────────────────────────────────────────────────────────────────────────[/dim cyan]")
    console.print(f"[dim cyan]🌙 Moon Dev's Liquidation Dashboard | {now} | 📡 api.moondev.com | Built with 💜 by Moon Dev[/dim cyan]")

# ==================== MAIN ====================
def main():
    """Main function - Moon Dev's Liquidation Dashboard"""
    console.clear()
    print_banner()
    console.print("[bold cyan]🌙 Moon Dev: Initializing API connection...[/bold cyan]")
    api = MoonDevAPI()
    if not api.api_key:
        console.print(Panel(
            "[bold red]❌ ERROR: No API key found![/bold red]\nPlease set MOONDEV_API_KEY in your .env file: [dim]MOONDEV_API_KEY=your_key_here[/dim]\n🌙 Get your API key at: [link=https://moondev.com]https://moondev.com[/link]",
            border_style="red", title="🔑 Authentication Required", padding=(0, 1)
        ))
        return
    console.print(f"[green]✅ API key loaded (...{api.api_key[-4:]})[/green]")
    with console.status("[bold cyan]🌙 Fetching liquidation data...[/bold cyan]"):
        pass
    display_timeframe_liquidations(api)
    display_liquidation_stats(api)
    display_top_liquidations(api)
    display_coin_breakdown(api)
    print_footer()

if __name__ == "__main__":
    main()

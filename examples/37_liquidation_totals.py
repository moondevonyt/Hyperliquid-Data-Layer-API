"""
🌙 Moon Dev's Liquidation Totals Dashboard (Long vs Short)
===========================================================
Rolling liquidation totals across ALL exchanges with the FULL long/short split:
- 6 windows: 5m, 15m, 1h, 2h, 3h, 4h
- Long vs Short volume + count per window
- Per-exchange breakdown (Binance, Bybit, OKX, Hyperliquid)
- Squeeze detector: spots when one side is getting wrecked

Endpoint: https://api.moondev.com/api/all_liquidations/totals.json (updates every 20s)

Built with love by Moon Dev 🚀 | Run with: python examples/37_liquidation_totals.py
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
from rich import box

console = Console()

# Window order for display
WINDOWS = ["5m", "15m", "1h", "2h", "3h", "4h"]

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
        title="⚔️ [bold yellow]LIQUIDATION TOTALS — LONG vs SHORT[/bold yellow] ⚔️",
        subtitle="[dim]💥 5m • 15m • 1h • 2h • 3h • 4h rolling windows | by Moon Dev 💥[/dim]",
        border_style="red",
        box=box.DOUBLE_EDGE,
        padding=(0, 1)
    ))

# ==================== HELPERS ====================
def format_usd(value):
    """Format USD value with K/M/B suffixes"""
    if value is None or value == 0:
        return "$0"
    if abs(value) >= 1_000_000_000:
        return f"${value/1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"${value/1_000:.1f}K"
    return f"${value:,.0f}"

def format_count(value):
    """Format count with commas"""
    if not value:
        return "0"
    return f"{value:,}"

def get_exchange_style(exchange):
    """Get style info for an exchange"""
    return EXCHANGE_STYLE.get(exchange.lower(), {'color': 'white', 'emoji': '🔹', 'name': exchange})

# ==================== LONG VS SHORT BY WINDOW ====================
def display_window_totals(windows):
    """Display long/short totals for every rolling window"""
    console.print(Panel(
        "⚔️ [bold white]LONG vs SHORT LIQUIDATIONS BY WINDOW[/bold white]  "
        "[dim cyan]GET https://api.moondev.com/api/all_liquidations/totals.json[/dim cyan]",
        border_style="bright_white",
        padding=(0, 1)
    ))

    table = Table(
        box=box.DOUBLE_EDGE,
        border_style="red",
        header_style="bold cyan",
        padding=(0, 1),
        expand=True
    )
    table.add_column("⏰ Window", style="bold cyan", justify="center", width=9)
    table.add_column("📈 Long Liq'd", style="green", justify="right", width=14)
    table.add_column("# Longs", style="green", justify="right", width=9)
    table.add_column("📉 Short Liq'd", style="red", justify="right", width=14)
    table.add_column("# Shorts", style="red", justify="right", width=9)
    table.add_column("🔥 Total", style="bold yellow", justify="right", width=12)
    table.add_column("⚖️ Balance", justify="center", width=24)

    for tf in WINDOWS:
        w = windows.get(tf)
        if not w:
            continue

        long_vol = w.get('long_volume_usd', 0)
        short_vol = w.get('short_volume_usd', 0)
        total_vol = w.get('total_volume_usd', long_vol + short_vol)

        # Balance bar: green = longs liquidated, red = shorts liquidated
        bar_len = 20
        if total_vol > 0:
            long_chars = round(long_vol / total_vol * bar_len)
        else:
            long_chars = bar_len // 2
        bar = f"[green]{'█' * long_chars}[/green][red]{'█' * (bar_len - long_chars)}[/red]"

        table.add_row(
            f"[bold]{tf}[/bold]",
            format_usd(long_vol),
            format_count(w.get('long_count', 0)),
            format_usd(short_vol),
            format_count(w.get('short_count', 0)),
            format_usd(total_vol),
            bar
        )

    console.print(table)

# ==================== SQUEEZE DETECTOR ====================
def display_squeeze_signal(windows):
    """🌙 Moon Dev's squeeze detector - who's getting wrecked?"""
    signals = []
    for tf in WINDOWS:
        w = windows.get(tf)
        if not w:
            continue
        long_vol = w.get('long_volume_usd', 0)
        short_vol = w.get('short_volume_usd', 0)
        total = long_vol + short_vol
        if total < 1_000_000:  # not enough action to call it
            continue
        if short_vol > long_vol * 3:
            signals.append(f"[green]🚀 {tf}: SHORT SQUEEZE — {format_usd(short_vol)} shorts vs {format_usd(long_vol)} longs liquidated (price ripping UP)[/green]")
        elif long_vol > short_vol * 3:
            signals.append(f"[red]💀 {tf}: LONG FLUSH — {format_usd(long_vol)} longs vs {format_usd(short_vol)} shorts liquidated (price dumping DOWN)[/red]")

    if signals:
        console.print(Panel(
            "\n".join(signals),
            title="🚨 [bold yellow]MOON DEV'S SQUEEZE DETECTOR[/bold yellow] 🚨",
            border_style="yellow",
            padding=(0, 1)
        ))
    else:
        console.print(Panel(
            "[dim]⚖️ No major squeeze detected — longs and shorts getting liquidated evenly[/dim]",
            title="🚨 [bold yellow]MOON DEV'S SQUEEZE DETECTOR[/bold yellow] 🚨",
            border_style="yellow",
            padding=(0, 1)
        ))

# ==================== EXCHANGE BREAKDOWN ====================
def display_exchange_breakdown(windows, tf="1h"):
    """Display per-exchange long/short breakdown for one window"""
    w = windows.get(tf)
    if not w:
        console.print(f"[dim]No {tf} window data available[/dim]")
        return

    console.print(Panel(
        f"🏦 [bold cyan]EXCHANGE BREAKDOWN — {tf.upper()} WINDOW[/bold cyan]  "
        "[dim]same long/short split, per exchange[/dim]",
        border_style="cyan",
        padding=(0, 1)
    ))

    by_exchange = w.get('by_exchange', {})

    table = Table(
        box=box.ROUNDED,
        border_style="cyan",
        header_style="bold magenta",
        padding=(0, 1),
        expand=True
    )
    table.add_column("🏦 Exchange", style="bold", justify="left", width=16)
    table.add_column("💰 Volume", style="yellow", justify="right", width=12)
    table.add_column("💥 Count", justify="right", width=9)
    table.add_column("📈 Long $", style="green", justify="right", width=12)
    table.add_column("# L", style="green", justify="right", width=7)
    table.add_column("📉 Short $", style="red", justify="right", width=12)
    table.add_column("# S", style="red", justify="right", width=7)

    # Sort by volume descending
    sorted_exchanges = sorted(
        by_exchange.items(),
        key=lambda x: x[1].get('volume_usd', 0),
        reverse=True
    )

    for exchange, ex in sorted_exchanges:
        style = get_exchange_style(exchange)
        table.add_row(
            f"{style['emoji']} [{style['color']}]{style['name']}[/{style['color']}]",
            f"[bold]{format_usd(ex.get('volume_usd', 0))}[/bold]",
            format_count(ex.get('count', 0)),
            format_usd(ex.get('long_volume_usd', 0)),
            format_count(ex.get('long_count', 0)),
            format_usd(ex.get('short_volume_usd', 0)),
            format_count(ex.get('short_count', 0)),
        )

    console.print(table)

# ==================== FOOTER ====================
def print_footer():
    """Print footer with timestamp and branding"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(f"[dim red]─────────────────────────────────────────────────────────────────────────────────────────────[/dim red]")
    console.print(f"[dim red]🌙 Moon Dev's Liquidation Totals Dashboard | {now} | 📡 api.moondev.com (updates every 20s) | Built with 💜 by Moon Dev[/dim red]")

# ==================== MAIN ====================
def main():
    """Main function - Moon Dev's Liquidation Totals Dashboard"""
    console.clear()
    print_banner()

    console.print("[bold cyan]🌙 Moon Dev: Initializing API connection...[/bold cyan]")
    api = MoonDevAPI()

    if not api.api_key:
        console.print(Panel(
            "[bold red]❌ ERROR: No API key found![/bold red]\n\n"
            "Please set MOONDEV_API_KEY in your .env file:\n"
            "[dim]MOONDEV_API_KEY=your_key_here[/dim]\n\n"
            "🌙 Get your API key at: [link=https://moondev.com]https://moondev.com[/link]",
            border_style="red",
            title="🔑 Authentication Required",
            padding=(0, 1)
        ))
        return

    console.print(f"[green]✅ API key loaded (...{api.api_key[-4:]})[/green]")
    console.print()

    data = api.get_all_liquidation_totals()
    windows = data.get('windows', {})

    if not windows:
        console.print("[red]🌙 Moon Dev: No windows in response — check the endpoint![/red]")
        return

    display_window_totals(windows)
    console.print()
    display_squeeze_signal(windows)
    console.print()
    display_exchange_breakdown(windows, "1h")
    console.print()
    display_exchange_breakdown(windows, "4h")

    print_footer()

if __name__ == "__main__":
    main()

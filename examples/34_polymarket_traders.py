"""
🌙 Moon Dev's Polymarket Profitable Traders Dashboard
Built with love by Moon Dev 🚀

Discovers the most profitable traders on Polymarket by scanning BTC 5-minute
prediction markets and trending market big trades ($500+). Shows traders
with $300+ 7-day P&L, sorted by profitability.

Usage:
    python 34_polymarket_traders.py

Author: Moon Dev
"""

import sys, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api import MoonDevAPI

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.align import Align
from rich.columns import Columns

console = Console()


def create_banner():
    """Moon Dev branded banner"""
    banner = """    ███╗   ███╗ ██████╗  ██████╗ ███╗   ██╗    ██████╗ ███████╗██╗   ██╗
    ████╗ ████║██╔═══██╗██╔═══██╗████╗  ██║    ██╔══██╗██╔════╝██║   ██║
    ██╔████╔██║██║   ██║██║   ██║██╔██╗ ██║    ██║  ██║█████╗  ██║   ██║
    ██║╚██╔╝██║██║   ██║██║   ██║██║╚██╗██║    ██║  ██║██╔══╝  ╚██╗ ██╔╝
    ██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██║ ╚████║    ██████╔╝███████╗ ╚████╔╝
    ╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝    ╚═════╝ ╚══════╝  ╚═══╝"""
    return Panel(
        Align.center(Text(banner, style="bold cyan")),
        title="🌙 [bold magenta]POLYMARKET PROFITABLE TRADERS[/bold magenta] 🌙",
        subtitle="[dim]Prediction Market Alpha by Moon Dev[/dim]",
        border_style="bright_cyan",
        box=box.DOUBLE_EDGE,
        padding=(0, 1)
    )


def fmt_usd(value):
    """Moon Dev - Format dollar values"""
    if value >= 1_000_000:
        return f"${value / 1_000_000:,.2f}M"
    if value >= 1_000:
        return f"${value / 1_000:,.1f}K"
    return f"${value:,.2f}"


def fmt_pnl(value):
    """Moon Dev - Color-coded P&L"""
    color = "bright_green" if value >= 0 else "bright_red"
    return f"[bold {color}]{fmt_usd(value)}[/]"


def source_badge(source):
    """Moon Dev - Format discovery source"""
    if source == "btc_5m":
        return "[bold bright_cyan]BTC 5m[/]"
    elif source == "trending":
        return "[bold bright_yellow]TRENDING[/]"
    return f"[dim]{source}[/]"


def main():
    """🌙 Moon Dev's Polymarket Profitable Traders Dashboard"""
    console.print(create_banner())
    console.print()

    # ==================== INITIALIZE ====================
    api = MoonDevAPI()
    if not api.api_key:
        console.print("[bold red]No API key found! Set MOONDEV_API_KEY in .env[/]")
        console.print("[dim]Apply for an API key at https://moondev.com/apply[/]")
        return

    console.print("[bold bright_cyan]  🌙 Moon Dev[/] | Fetching Polymarket profitable traders...\n")

    # ==================== FETCH DATA ====================
    data = api.get_poly_profitable_traders()

    total = data.get("total", 0)
    full_list = data.get("full_list", False)
    updated_at = data.get("updated_at", "unknown")
    stats = data.get("stats", {})
    traders = data.get("traders", [])

    # ==================== STATS PANEL ====================
    tier_label = "[bold bright_green]FULL LIST (Quant Elite)[/]" if full_list else "[bold bright_yellow]TOP 25 (Standard)[/]"
    stats_text = Text()
    stats_text.append(f"  Traders: {total}", style="bold white")
    stats_text.append(f"  |  Wallets Scanned: {stats.get('wallets_checked', 0):,}", style="dim")
    stats_text.append(f"  |  Queue: {stats.get('queue_depth', 0)}", style="dim")
    stats_text.append(f"  |  Uptime: {stats.get('uptime_minutes', 0):.0f}m", style="dim")

    console.print(Panel(
        stats_text,
        title=f"🌙 [bold bright_magenta]MOON DEV[/] | {tier_label}",
        subtitle=f"[dim]Updated: {updated_at}[/]",
        border_style="bright_magenta",
        box=box.ROUNDED,
        padding=(0, 1)
    ))
    console.print()

    if not traders:
        console.print("[bold yellow]  No profitable traders found yet. Service may still be scanning.[/]")
        return

    # ==================== LEADERBOARD TABLE ====================
    # Top 10 traders in detail
    top_table = Table(
        title="[bold bright_green]💰 TOP PROFITABLE TRADERS 💰[/]",
        box=box.HEAVY_EDGE,
        border_style="bright_green",
        header_style="bold bright_white on dark_green",
        show_lines=True,
        padding=(0, 1),
        expand=True,
    )
    top_table.add_column("#", style="bold bright_yellow", justify="center", width=4)
    top_table.add_column("WALLET", style="bold bright_cyan", width=16)
    top_table.add_column("7D P&L", justify="right", width=14)
    top_table.add_column("7D VOLUME", justify="right", width=14)
    top_table.add_column("TRADES", justify="center", width=8)
    top_table.add_column("WINS", justify="center", width=6)
    top_table.add_column("SOURCE", justify="center", width=10)

    for i, t in enumerate(traders[:10], 1):
        wallet = t.get("wallet", "")
        wallet_short = f"{wallet[:6]}...{wallet[-4:]}" if wallet else "unknown"
        top_table.add_row(
            str(i),
            wallet_short,
            fmt_pnl(t.get("pnl_7d", 0)),
            fmt_usd(t.get("volume_7d", 0)),
            str(t.get("trades_7d", 0)),
            str(t.get("redeems_7d", 0)),
            source_badge(t.get("source", "")),
        )

    console.print(top_table)
    console.print()

    # ==================== FULL LIST (compact) ====================
    if len(traders) > 10:
        full_table = Table(
            title=f"[bold bright_magenta]📊 ALL {total} PROFITABLE TRADERS 📊[/]",
            box=box.SIMPLE,
            border_style="bright_magenta",
            header_style="bold bright_white",
            padding=(0, 1),
            expand=True,
        )
        full_table.add_column("#", style="dim", justify="right", width=4)
        full_table.add_column("WALLET", style="bright_cyan", width=16)
        full_table.add_column("7D P&L", justify="right", width=12)
        full_table.add_column("VOLUME", justify="right", width=12)
        full_table.add_column("TRADES", justify="center", width=7)
        full_table.add_column("PROFILE", style="dim", width=50)

        for i, t in enumerate(traders, 1):
            wallet = t.get("wallet", "")
            wallet_short = f"{wallet[:6]}...{wallet[-4:]}" if wallet else "unknown"
            full_table.add_row(
                str(i),
                wallet_short,
                fmt_pnl(t.get("pnl_7d", 0)),
                fmt_usd(t.get("volume_7d", 0)),
                str(t.get("trades_7d", 0)),
                t.get("polymarket_link", ""),
            )

        console.print(full_table)
        console.print()

    # ==================== SUMMARY STATS ====================
    total_pnl = sum(t.get("pnl_7d", 0) for t in traders)
    total_vol = sum(t.get("volume_7d", 0) for t in traders)
    total_trades = sum(t.get("trades_7d", 0) for t in traders)
    btc_5m_count = sum(1 for t in traders if t.get("source") == "btc_5m")
    trending_count = sum(1 for t in traders if t.get("source") == "trending")

    summary_parts = [
        Panel(f"[bold bright_green]{fmt_usd(total_pnl)}[/]\n[dim]Combined P&L[/]", border_style="bright_green", box=box.ROUNDED, expand=True),
        Panel(f"[bold bright_cyan]{fmt_usd(total_vol)}[/]\n[dim]Combined Volume[/]", border_style="bright_cyan", box=box.ROUNDED, expand=True),
        Panel(f"[bold bright_yellow]{total_trades:,}[/]\n[dim]Total Trades[/]", border_style="bright_yellow", box=box.ROUNDED, expand=True),
        Panel(f"[bold bright_cyan]{btc_5m_count}[/] BTC 5m  [bold bright_yellow]{trending_count}[/] Trending\n[dim]Discovery Sources[/]", border_style="bright_magenta", box=box.ROUNDED, expand=True),
    ]
    console.print(Columns(summary_parts, equal=True, expand=True))
    console.print()

    # ==================== FOOTER ====================
    console.print(Panel(
        "[dim]  🌙 Moon Dev | Polymarket Profitable Traders | moondev.com/docs[/]",
        border_style="dim",
        box=box.ROUNDED,
        padding=(0, 0),
    ))


if __name__ == "__main__":
    print("🌙 Moon Dev's Polymarket Profitable Traders Dashboard - Loading...")
    print("🌙 Moon Dev says: Follow the smart money in prediction markets.\n")
    main()

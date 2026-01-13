"""
Moon Dev's HLP Analytics Dashboard
===================================
Advanced analytics for Hyperliquid's HLP (HyperLiquidity Provider)

Built with love by Moon Dev
https://moondev.com

This dashboard shows:
- Liquidator Status: Active/idle liquidators with PnL
- Market Maker: Strategy B tracking for BTC/ETH/SOL
- Timing Analysis: Hourly/session profitability
- Correlation: Delta-price correlation by coin

Usage: python 18_hlp_analytics.py
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


def create_banner():
    """Create the Moon Dev HLP Analytics banner"""
    banner = """██╗  ██╗██╗     ██████╗      █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗████████╗██╗ ██████╗███████╗
██║  ██║██║     ██╔══██╗    ██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝╚══██╔══╝██║██╔════╝██╔════╝
███████║██║     ██████╔╝    ███████║██╔██╗ ██║███████║██║   ╚████╔╝    ██║   ██║██║     ███████╗
██╔══██║██║     ██╔═══╝     ██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝     ██║   ██║██║     ╚════██║
██║  ██║███████╗██║         ██║  ██║██║ ╚████║██║  ██║███████╗██║      ██║   ██║╚██████╗███████║
╚═╝  ╚═╝╚══════╝╚═╝         ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝      ╚═╝   ╚═╝ ╚═════╝╚══════╝"""
    return Panel(
        Align.center(Text(banner, style="bold cyan")),
        title="📊 [bold magenta]HLP ANALYTICS DASHBOARD[/bold magenta] 📊",
        subtitle="[dim]Liquidators • Market Maker • Timing • Correlation | by Moon Dev[/dim]",
        border_style="bright_cyan",
        box=box.DOUBLE_EDGE,
        padding=(0, 1)
    )


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


def format_pnl(value):
    """Format PnL with color"""
    if value is None:
        return "[dim]N/A[/dim]"
    if value > 0:
        return f"[green]+{format_usd(value)}[/green]"
    elif value < 0:
        return f"[red]{format_usd(value)}[/red]"
    return "[dim]$0[/dim]"


# ==================== LIQUIDATOR STATUS ====================
def display_liquidator_status(api):
    """Display real-time liquidator status"""
    console.print(Panel(
        "⚡ [bold yellow]LIQUIDATOR STATUS[/bold yellow]  [dim cyan]GET https://api.moondev.com/api/hlp/liquidators/status[/dim cyan]",
        border_style="yellow",
        padding=(0, 1)
    ))

    try:
        status_data = api.get_hlp_liquidator_status()
    except Exception as e:
        console.print(f"[red]Error fetching liquidator status: {e}[/red]")
        return

    if not isinstance(status_data, dict):
        console.print("[dim]No liquidator status data available[/dim]")
        return

    liquidators = status_data.get('liquidators', status_data.get('data', []))

    if isinstance(liquidators, list) and len(liquidators) > 0:
        table = Table(
            box=box.ROUNDED,
            border_style="yellow",
            header_style="bold magenta",
            padding=(0, 1)
        )

        table.add_column("Liquidator", style="cyan", width=44)
        table.add_column("Status", justify="center", width=10)
        table.add_column("PnL", justify="right", width=14)
        table.add_column("Last Active", style="dim", width=16)

        for liq in liquidators[:10]:
            address = liq.get('address', liq.get('wallet', 'Unknown'))
            status = liq.get('status', 'unknown')
            pnl = liq.get('pnl', liq.get('profit', 0))
            last_active = liq.get('last_active', liq.get('timestamp', 'N/A'))

            if isinstance(last_active, (int, float)):
                if last_active > 1e10:
                    last_active = last_active / 1000
                try:
                    last_active = datetime.fromtimestamp(last_active).strftime("%m-%d %H:%M")
                except:
                    last_active = str(last_active)[:16]
            elif isinstance(last_active, str) and len(last_active) > 16:
                last_active = last_active[5:16].replace('T', ' ')

            status_display = "[green]✅ ACTIVE[/green]" if status.lower() == 'active' else "[dim]💤 IDLE[/dim]"

            table.add_row(address, status_display, format_pnl(pnl), str(last_active))

        console.print(table)
    else:
        # Maybe it's a summary format
        active = status_data.get('active_count', status_data.get('active', 0))
        idle = status_data.get('idle_count', status_data.get('idle', 0))
        total_pnl = status_data.get('total_pnl', 0)

        content = f"""[bold white]Liquidator Overview[/bold white]

[green]✅ Active:[/green] {active}
[dim]💤 Idle:[/dim] {idle}
[bold yellow]💰 Total PnL:[/bold yellow] {format_pnl(total_pnl)}
"""
        console.print(Panel(content, border_style="yellow", padding=(0, 1)))


# ==================== MARKET MAKER ====================
def display_market_maker(api):
    """Display Strategy B market maker tracking"""
    console.print(Panel(
        "🏦 [bold blue]MARKET MAKER (STRATEGY B)[/bold blue]  [dim cyan]GET https://api.moondev.com/api/hlp/market-maker[/dim cyan]",
        border_style="blue",
        padding=(0, 1)
    ))

    try:
        mm_data = api.get_hlp_market_maker()
    except Exception as e:
        console.print(f"[red]Error fetching market maker data: {e}[/red]")
        return

    if not isinstance(mm_data, dict):
        console.print("[dim]No market maker data available[/dim]")
        return

    coins = mm_data.get('coins', mm_data.get('symbols', mm_data.get('data', {})))

    if isinstance(coins, dict):
        table = Table(
            box=box.ROUNDED,
            border_style="blue",
            header_style="bold magenta",
            padding=(0, 1)
        )

        table.add_column("Coin", style="cyan", justify="center", width=8)
        table.add_column("Position", justify="right", width=14)
        table.add_column("Side", justify="center", width=10)
        table.add_column("Entry", justify="right", width=12)
        table.add_column("Mark", justify="right", width=12)
        table.add_column("PnL", justify="right", width=12)

        coin_emoji = {'BTC': '₿', 'ETH': 'Ξ', 'SOL': '◎'}

        for coin in ['BTC', 'ETH', 'SOL']:
            data = coins.get(coin, coins.get(coin.lower(), {}))
            if isinstance(data, dict):
                emoji = coin_emoji.get(coin, '🪙')
                position = data.get('position', data.get('size', 0))
                side = 'LONG' if position > 0 else 'SHORT' if position < 0 else 'FLAT'
                entry = data.get('entry_price', data.get('entry', 0))
                mark = data.get('mark_price', data.get('mark', 0))
                pnl = data.get('pnl', data.get('unrealized_pnl', 0))

                side_display = f"[green]{side}[/green]" if side == 'LONG' else f"[red]{side}[/red]" if side == 'SHORT' else "[dim]FLAT[/dim]"

                table.add_row(
                    f"{emoji} {coin}",
                    format_usd(abs(position)) if position else "[dim]--[/dim]",
                    side_display,
                    f"${entry:,.2f}" if entry else "[dim]--[/dim]",
                    f"${mark:,.2f}" if mark else "[dim]--[/dim]",
                    format_pnl(pnl)
                )

        console.print(table)
    elif isinstance(coins, list):
        for item in coins[:5]:
            console.print(f"  {item}")


# ==================== TIMING ANALYSIS ====================
def display_timing_analysis(api):
    """Display hourly/session profitability analysis"""
    console.print(Panel(
        "⏰ [bold green]TIMING ANALYSIS[/bold green]  [dim cyan]GET https://api.moondev.com/api/hlp/timing[/dim cyan]",
        border_style="green",
        padding=(0, 1)
    ))

    try:
        timing_data = api.get_hlp_timing()
    except Exception as e:
        console.print(f"[red]Error fetching timing data: {e}[/red]")
        return

    if not isinstance(timing_data, dict):
        console.print("[dim]No timing data available[/dim]")
        return

    # Hourly breakdown
    hourly = timing_data.get('hourly', timing_data.get('by_hour', {}))
    sessions = timing_data.get('sessions', timing_data.get('by_session', {}))

    panels = []

    # Session panel
    if isinstance(sessions, dict) and sessions:
        session_lines = ["[bold white]📅 SESSION PROFITABILITY[/bold white]\n"]
        session_emoji = {'asia': '🌏', 'europe': '🌍', 'us': '🌎', 'london': '🇬🇧', 'new_york': '🗽', 'tokyo': '🗼'}

        for session, data in sessions.items():
            if isinstance(data, dict):
                pnl = data.get('pnl', data.get('profit', 0))
                trades = data.get('trades', data.get('count', 0))
                emoji = session_emoji.get(session.lower(), '📊')
                pnl_display = format_pnl(pnl)
                session_lines.append(f"{emoji} [cyan]{session.upper():>8}[/cyan]: {pnl_display} ({trades} trades)")

        panels.append(Panel("\n".join(session_lines), border_style="green", padding=(0, 1)))

    # Best/worst hours
    if isinstance(hourly, dict) and hourly:
        # Sort by PnL
        sorted_hours = sorted(
            [(h, d.get('pnl', 0) if isinstance(d, dict) else 0) for h, d in hourly.items()],
            key=lambda x: x[1],
            reverse=True
        )

        hour_lines = ["[bold white]🕐 BEST/WORST HOURS (UTC)[/bold white]\n"]
        hour_lines.append("[green]Best:[/green]")
        for hour, pnl in sorted_hours[:3]:
            hour_lines.append(f"  {hour}:00 → {format_pnl(pnl)}")

        hour_lines.append("\n[red]Worst:[/red]")
        for hour, pnl in sorted_hours[-3:]:
            hour_lines.append(f"  {hour}:00 → {format_pnl(pnl)}")

        panels.append(Panel("\n".join(hour_lines), border_style="green", padding=(0, 1)))

    if panels:
        console.print(Columns(panels, equal=True, expand=True))
    else:
        console.print("[dim]No detailed timing data available[/dim]")


# ==================== CORRELATION ====================
def display_correlation(api):
    """Display delta-price correlation by coin"""
    console.print(Panel(
        "📈 [bold magenta]DELTA-PRICE CORRELATION[/bold magenta]  [dim cyan]GET https://api.moondev.com/api/hlp/correlation[/dim cyan]",
        border_style="magenta",
        padding=(0, 1)
    ))

    try:
        corr_data = api.get_hlp_correlation()
    except Exception as e:
        console.print(f"[red]Error fetching correlation data: {e}[/red]")
        return

    if not isinstance(corr_data, dict):
        console.print("[dim]No correlation data available[/dim]")
        return

    coins = corr_data.get('coins', corr_data.get('correlations', corr_data.get('data', {})))

    if isinstance(coins, dict) and coins:
        table = Table(
            box=box.ROUNDED,
            border_style="magenta",
            header_style="bold cyan",
            padding=(0, 1)
        )

        table.add_column("Coin", style="cyan", justify="center", width=8)
        table.add_column("Correlation", justify="center", width=12)
        table.add_column("Strength", justify="center", width=20)
        table.add_column("Interpretation", width=30)

        coin_emoji = {'BTC': '₿', 'ETH': 'Ξ', 'SOL': '◎', 'HYPE': '🔥', 'XRP': '✕'}

        for coin, data in coins.items():
            if isinstance(data, dict):
                corr = data.get('correlation', data.get('corr', 0))
                emoji = coin_emoji.get(coin.upper(), '🪙')

                # Visual bar for correlation
                abs_corr = abs(corr) if corr else 0
                bar_len = int(abs_corr * 10)
                if corr and corr > 0:
                    bar = f"[green]{'█' * bar_len}[/green]{'░' * (10 - bar_len)}"
                    color = "green"
                elif corr and corr < 0:
                    bar = f"[red]{'█' * bar_len}[/red]{'░' * (10 - bar_len)}"
                    color = "red"
                else:
                    bar = "░" * 10
                    color = "dim"

                # Interpretation
                if abs_corr >= 0.7:
                    strength = "Strong"
                elif abs_corr >= 0.4:
                    strength = "Moderate"
                elif abs_corr >= 0.2:
                    strength = "Weak"
                else:
                    strength = "None"

                if corr and corr > 0.4:
                    interp = "Delta follows price"
                elif corr and corr < -0.4:
                    interp = "Delta inverse to price"
                else:
                    interp = "No clear relationship"

                table.add_row(
                    f"{emoji} {coin}",
                    f"[{color}]{corr:+.3f}[/{color}]" if corr else "[dim]N/A[/dim]",
                    bar,
                    f"{strength}: {interp}"
                )

        console.print(table)
    else:
        console.print("[dim]No correlation data available[/dim]")


def create_footer():
    """Create footer with timestamp and branding"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return Text(
        f"━━━ 🌙 Moon Dev's HLP Analytics | {now} | api.moondev.com | Deep HLP Insights ━━━",
        style="dim cyan",
        justify="center"
    )


def main():
    """Main function - Moon Dev's HLP Analytics Dashboard"""
    console.clear()
    console.print(create_banner())

    # Initialize API - Moon Dev
    console.print("[dim]🌙 Connecting to Moon Dev API...[/dim]")
    api = MoonDevAPI()

    if not api.api_key:
        console.print(Panel(
            "[bold red]ERROR:[/bold red] No API key found!\n"
            "Set MOONDEV_API_KEY in .env | Get key at: [cyan]moondev.com[/cyan]",
            title="[red]Auth Error[/red]",
            border_style="red",
            padding=(0, 1)
        ))
        return

    console.print("[dim green]✅ API connected[/dim green]")
    console.print()

    # Display all analytics sections
    display_liquidator_status(api)
    console.print()

    display_market_maker(api)
    console.print()

    display_timing_analysis(api)
    console.print()

    display_correlation(api)
    console.print()

    # Summary
    summary = (
        "⚡ [yellow]Liquidators[/yellow] | "
        "🏦 [blue]Market Maker[/blue] | "
        "⏰ [green]Timing[/green] | "
        "📈 [magenta]Correlation[/magenta] | "
        "🌙 [cyan]Moon Dev Analytics[/cyan]"
    )
    console.print(Panel(summary, title="[bold cyan]HLP Analytics Summary[/bold cyan]", border_style="cyan", padding=(0, 1)))

    console.print()
    console.print(create_footer())


if __name__ == "__main__":
    main()

"""
Moon Dev's HLP Dashboard - Complete HyperLiquidity Provider Analysis
=====================================================================
Beautiful terminal dashboard for all HLP data: positions, liquidators, deltas

Built with love by Moon Dev

HLP is Hyperliquid's native market-making protocol with ~$210M+ in positions.
This dashboard shows all 7 HLP strategies, liquidator events, and exposure tracking.

RETIRED 2026-08-13: the trade history sections are gone. /api/hlp/trades and
/api/hlp/trades/stats now return HTTP 410 Gone. Use /api/hlp/sentiment and
/api/hlp/positions instead.

Usage: python 12_hlp_positions.py [mode]
       python 12_hlp_positions.py              # Full dashboard (all sections)
       python 12_hlp_positions.py --positions  # Positions only
       python 12_hlp_positions.py --summary    # Quick summary only

Data Source: Moon Dev's local Hyperliquid node (blazing fast!)
"""

import sys
import os
from datetime import datetime
from collections import defaultdict

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
from rich.tree import Tree

console = Console()

# ==================== BANNER ====================
def create_banner():
    """Create the Moon Dev branded header banner"""
    banner = """
 _   _ _     ____
| | | | |   |  _ \\
| |_| | |   | |_) |
|  _  | |___|  __/
|_| |_|_____|_|
 ____    _    ____  _   _ ____   ___    _    ____  ____
|  _ \\  / \\  / ___|| | | | __ ) / _ \\  / \\  |  _ \\|  _ \\
| | | |/ _ \\ \\___ \\| |_| |  _ \\| | | |/ _ \\ | |_) | | | |
| |_| / ___ \\ ___) |  _  | |_) | |_| / ___ \\|  _ <| |_| |
|____/_/   \\_\\____/|_| |_|____/ \\___/_/   \\_\\_| \\_\\____/
"""
    return Panel(
        Align.center(Text(banner, style="bold cyan")),
        title="[bold magenta]MOON DEV'S HLP REVERSE ENGINEERING DASHBOARD[/bold magenta]",
        subtitle="[dim]All 7 HLP Strategies | Liquidators | Delta Tracking | ~$210M+ AUM[/dim]",
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
    if abs(value) >= 1_000_000_000:
        return f"${value/1_000_000_000:,.2f}B"
    elif abs(value) >= 1_000_000:
        return f"${value/1_000_000:,.2f}M"
    elif abs(value) >= 1_000:
        return f"${value/1_000:,.1f}K"
    return f"${value:,.2f}"


def format_size(value, coin=''):
    """Format position size"""
    if value is None:
        return "0"
    if isinstance(value, str):
        value = float(value)
    if abs(value) >= 1000:
        return f"{value:,.2f}"
    elif abs(value) >= 1:
        return f"{value:,.4f}"
    else:
        return f"{value:,.6f}"


def format_timestamp(ts):
    """Format timestamp to readable string"""
    if not ts:
        return "N/A"
    if isinstance(ts, (int, float)):
        if ts > 1e12:
            ts = ts / 1000
        dt = datetime.fromtimestamp(ts)
        return dt.strftime("%m-%d %H:%M:%S")
    return str(ts)[:19]


# ==================== DISPLAY FUNCTIONS ====================
def display_summary_panels(summary, exposure=None, strategies=None):
    """Display HLP summary statistics"""
    total_value = summary.get('total_account_value', 0)
    total_positions = summary.get('total_positions', 0)
    total_pnl = summary.get('total_pnl', 0)
    total_strategies = summary.get('strategy_count', 7)

    # Get net exposure from exposure dict
    if exposure and isinstance(exposure, dict):
        net_exposure = exposure.get('net_delta', 0)
    else:
        net_exposure = 0

    # Count active strategies (those with positions)
    active_strategies = 0
    if strategies:
        if isinstance(strategies, dict):
            for name, data in strategies.items():
                if isinstance(data, dict) and data.get('position_count', 0) > 0:
                    active_strategies += 1
        elif isinstance(strategies, list):
            active_strategies = len([s for s in strategies if isinstance(s, dict) and s.get('position_count', 0) > 0])

    # Main stats panel
    panel1_lines = [
        f"[bold yellow]Total Account Value[/bold yellow]",
        f"[bold white]{format_usd(total_value)}[/bold white]",
        "",
        f"[bold cyan]Active Strategies:[/bold cyan] [green]{active_strategies}[/green] / {total_strategies}",
        f"[bold cyan]Total Positions:[/bold cyan] [yellow]{total_positions:,}[/yellow]",
    ]

    panel1 = Panel(
        Align.center("\n".join(panel1_lines)),
        title="[bold white]HLP OVERVIEW[/bold white]  [dim cyan]GET https://api.moondev.com/api/hlp/positions[/dim cyan]",
        border_style="bright_yellow",
        box=box.DOUBLE,
        padding=(1, 2)
    )

    # Net exposure panel
    exposure_color = "green" if net_exposure >= 0 else "red"
    exposure_sign = "+" if net_exposure >= 0 else ""
    exposure_direction = "NET LONG" if net_exposure >= 0 else "NET SHORT"

    panel2_lines = [
        f"[bold {exposure_color}]{exposure_direction}[/bold {exposure_color}]",
        f"[bold white]{exposure_sign}{format_usd(net_exposure)}[/bold white]",
        "",
        f"[dim]Combined delta exposure[/dim]",
        f"[dim]across all strategies[/dim]",
    ]

    panel2 = Panel(
        Align.center("\n".join(panel2_lines)),
        title="[bold white]NET EXPOSURE[/bold white]  [dim cyan]GET https://api.moondev.com/api/hlp/deltas[/dim cyan]",
        border_style=f"bright_{exposure_color}",
        box=box.DOUBLE,
        padding=(1, 2)
    )

    # Strategy status panel (trade stats panel removed - endpoint retired 2026-08-13)
    panel3_lines = [
        "[bold white]Strategy Status[/bold white]",
        "",
        "[green]● Active[/green] HLP Strategy A",
        "[green]● Active[/green] HLP Strategy B",
        "[dim]○ Idle[/dim]   HLP Liquidators",
        "[dim]○ Idle[/dim]   HLP Strategy X",
    ]

    panel3 = Panel(
        "\n".join(panel3_lines),
        title="[bold white]STRATEGIES[/bold white]  [dim cyan]GET https://api.moondev.com/api/hlp/positions[/dim cyan]",
        border_style="bright_magenta",
        box=box.DOUBLE,
        padding=(1, 2)
    )

    console.print(Columns([panel1, panel2, panel3], equal=True, expand=True))


def display_combined_positions(combined_positions):
    """Display combined NET positions in compact format"""
    if not combined_positions:
        return

    # Sort by absolute net value
    sorted_positions = sorted(
        combined_positions,
        key=lambda x: abs(x.get('net_value', 0)),
        reverse=True
    )

    # Calculate totals
    total_long = sum(p.get('long_value', 0) for p in combined_positions)
    total_short = sum(p.get('short_value', 0) for p in combined_positions)
    net_delta = total_long - total_short

    # Create compact table - top 15 positions
    table = Table(
        box=box.SIMPLE_HEAD,
        border_style="cyan",
        header_style="bold magenta",
        padding=(0, 1),
        show_edge=False
    )

    table.add_column("Coin", style="bold white", width=8)
    table.add_column("Dir", justify="center", width=5)
    table.add_column("Value", style="yellow", justify="right", width=10)
    table.add_column("Coin", style="bold white", width=8)
    table.add_column("Dir", justify="center", width=5)
    table.add_column("Value", style="yellow", justify="right", width=10)
    table.add_column("Coin", style="bold white", width=8)
    table.add_column("Dir", justify="center", width=5)
    table.add_column("Value", style="yellow", justify="right", width=10)

    coin_emoji = {'BTC': '₿', 'ETH': 'Ξ', 'SOL': '◎', 'HYPE': '🔥', 'XRP': '✕', 'SUI': '💧'}

    # Display in 3 columns, 5 rows = 15 positions
    for i in range(0, 15, 3):
        row = []
        for j in range(3):
            idx = i + j
            if idx < len(sorted_positions):
                pos = sorted_positions[idx]
                coin = pos.get('coin', '?')
                net_size = pos.get('net_size', 0)
                net_value = pos.get('net_value', 0)
                emoji = coin_emoji.get(coin.upper(), '')
                direction = Text("L", style="green") if net_size > 0 else Text("S", style="red")
                row.extend([f"{emoji}{coin}"[:8], direction, format_usd(abs(net_value))])
            else:
                row.extend(["", "", ""])
        table.add_row(*row)

    # Header with totals
    delta_color = "green" if net_delta >= 0 else "red"
    header = f"[bold cyan]TOP 15 NET POSITIONS[/bold cyan]  [dim cyan]GET https://api.moondev.com/api/hlp/positions[/dim cyan] │ [green]Long: {format_usd(total_long)}[/green] │ [red]Short: {format_usd(total_short)}[/red] │ [{delta_color}]Delta: {'+' if net_delta >= 0 else ''}{format_usd(net_delta)}[/{delta_color}]"
    console.print(Panel(table, title=header, border_style="cyan", padding=(0, 0)))


# Moon Dev: display_hlp_trades() and display_trade_stats() removed - endpoints retired 2026-08-13


def display_liquidators(liquidators_data):
    """Display liquidator status - compact inline"""
    if not liquidators_data:
        return

    liquidators = liquidators_data.get('liquidators', [])
    events = liquidators_data.get('events', [])

    # Build compact status line
    liq_parts = []
    for liq in liquidators:
        name = liq.get('name', 'Unknown').replace("HLP ", "")
        status = liq.get('status', 'unknown')
        icon = "[green]●[/green]" if status == 'active' else "[dim]○[/dim]"
        liq_parts.append(f"{icon} {name}")

    event_count = len(events)
    event_str = f" │ [yellow]{event_count} events[/yellow]" if event_count > 0 else ""

    console.print(f"[bold red]LIQUIDATORS[/bold red] {' │ '.join(liq_parts)}{event_str}")


def display_deltas(deltas_data):
    """Display net exposure delta - compact with sparkline"""
    if not deltas_data:
        return

    current = deltas_data.get('current', 0)
    change_24h = deltas_data.get('change_24h', 0)
    deltas = deltas_data.get('deltas', [])

    current_color = "green" if current >= 0 else "red"
    change_color = "green" if change_24h >= 0 else "red"

    # Build sparkline
    sparkline = ""
    if deltas and len(deltas) >= 5:
        values = []
        for d in deltas[-24:]:
            if isinstance(d, dict):
                val = d.get('net_delta', d.get('delta', 0))
                values.append(float(val) if val else 0)
            elif isinstance(d, (int, float)):
                values.append(float(d))
            else:
                values.append(0)

        min_val, max_val = min(values), max(values)
        range_val = max_val - min_val if max_val != min_val else 1
        chars = " ▁▂▃▄▅▆▇█"
        for v in values:
            idx = int((v - min_val) / range_val * 8)
            sparkline += f"[{'green' if v >= 0 else 'red'}]{chars[idx]}[/]"

    console.print(f"[bold magenta]24H DELTA[/bold magenta] [{current_color}]Now: {format_usd(current)}[/{current_color}] │ [{change_color}]Chg: {'+' if change_24h >= 0 else ''}{format_usd(change_24h)}[/{change_color}] │ {sparkline}")


def display_exposure_visualization(combined_positions):
    """Display compact exposure bar"""
    if not combined_positions:
        return

    # Calculate totals
    total_long = sum(pos.get('long_value', 0) for pos in combined_positions)
    total_short = sum(pos.get('short_value', 0) for pos in combined_positions)
    total = total_long + total_short

    if total == 0:
        return

    long_pct = (total_long / total) * 100
    short_pct = (total_short / total) * 100

    # Create visual bar
    bar_width = 50
    long_bars = int((long_pct / 100) * bar_width)
    short_bars = bar_width - long_bars

    bar = f"[green]{'█' * long_bars}[/green][red]{'█' * short_bars}[/red]"

    # Top 5 in compact format
    sorted_by_value = sorted(combined_positions, key=lambda x: abs(x.get('net_value', 0)), reverse=True)[:5]
    top5 = " │ ".join([
        f"[{'green' if p.get('net_value', 0) > 0 else 'red'}]{p.get('coin', '?')} {format_usd(abs(p.get('net_value', 0)))}[/]"
        for p in sorted_by_value
    ])

    console.print(f"[green]L {format_usd(total_long)} ({long_pct:.0f}%)[/green] {bar} [red]S {format_usd(total_short)} ({short_pct:.0f}%)[/red]")
    console.print(f"[dim]Top 5:[/dim] {top5}")


def display_strategy_details(strategies):
    """Display individual strategy breakdown - compact side-by-side"""
    if not strategies:
        return

    # Handle strategies as dict (API format) or list
    if isinstance(strategies, dict):
        strategy_items = list(strategies.items())
    elif isinstance(strategies, list):
        if all(isinstance(s, str) for s in strategies):
            names = [s.replace("HLP ", "") for s in strategies]
            console.print(f"[dim]Strategies: {' | '.join(names)}[/dim]")
            return
        strategy_items = [(s.get('name', f'Strategy {i}'), s) for i, s in enumerate(strategies) if isinstance(s, dict)]
    else:
        return

    if not strategy_items:
        return

    # Separate active and idle strategies
    active_strategies = []
    idle_strategies = []

    for name, data in strategy_items:
        if isinstance(data, dict) and data.get('position_count', 0) > 0:
            active_strategies.append((name, data))
        else:
            idle_strategies.append((name, data))

    # Create panels for active strategies (side by side)
    active_panels = []
    for name, data in active_strategies:
        account_value = float(data.get('account_value', 0))
        total_pnl = float(data.get('total_pnl', 0))
        position_count = data.get('position_count', 0)
        positions = data.get('positions', [])

        pnl_color = "green" if total_pnl >= 0 else "red"
        pnl_sign = "+" if total_pnl >= 0 else ""

        # Build compact position list
        lines = []
        if positions:
            sorted_pos = sorted(positions, key=lambda x: abs(float(x.get('position_value', 0) if isinstance(x, dict) else 0)), reverse=True)
            for pos in sorted_pos[:8]:
                if not isinstance(pos, dict):
                    continue
                coin = pos.get('coin', '?')[:6]
                size = float(pos.get('size', 0))
                value = float(pos.get('position_value', 0))
                pnl = float(pos.get('unrealized_pnl', 0))
                side_char = "[green]L[/green]" if size > 0 else "[red]S[/red]"
                pnl_str = f"[green]+{pnl/1000:.1f}K[/green]" if pnl >= 0 else f"[red]{pnl/1000:.1f}K[/red]"
                lines.append(f"{side_char} [white]{coin:>6}[/white] [yellow]{format_usd(value):>8}[/yellow] {pnl_str:>8}")

            if len(positions) > 8:
                lines.append(f"[dim]... +{len(positions) - 8} more positions[/dim]")

        content = "\n".join(lines) if lines else "[dim]No positions[/dim]"
        short_name = name.replace("HLP ", "")
        title = f"[green]●[/green] [bold]{short_name}[/bold] │ {format_usd(account_value)} │ [{pnl_color}]{pnl_sign}{format_usd(total_pnl)}[/{pnl_color}]"

        active_panels.append(Panel(content, title=title, border_style="green", padding=(0, 1)))

    # Show active strategies side by side
    if active_panels:
        console.print(Columns(active_panels, equal=True, expand=True))

    # Show idle strategies in a single compact line
    if idle_strategies:
        idle_parts = []
        for name, data in idle_strategies:
            short_name = name.replace("HLP ", "")
            acct_val = float(data.get('account_value', 0)) if isinstance(data, dict) else 0
            idle_parts.append(f"[dim]○ {short_name}[/dim] [yellow]{format_usd(acct_val)}[/yellow]")
        console.print(f"[dim]Idle:[/dim] " + " │ ".join(idle_parts))


# ==================== FOOTER ====================
def print_footer():
    """Print footer with timestamp and branding"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(f"\n[dim cyan]{'─' * 100}[/dim cyan]")
    console.print(f"[dim cyan]Moon Dev's HLP Dashboard | {now} | api.moondev.com | Built with love by Moon Dev[/dim cyan]")


# ==================== MAIN ====================
def main():
    """Main function - Moon Dev's HLP Dashboard"""
    console.clear()
    console.print(create_banner())

    # Parse command line args
    args = sys.argv[1:]
    mode = "full"
    if "--positions" in args:
        mode = "positions"
    elif "--summary" in args:
        mode = "summary"

    console.print(f"[bold cyan]Moon Dev: Fetching HLP data from local node...[/bold cyan]")
    console.print(f"[dim]Mode: {mode}[/dim]")
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

    # Fetch data based on mode
    with console.status("[bold cyan]Moon Dev: Loading HLP data...[/bold cyan]"):
        hlp_data = api.get_hlp_positions(include_strategies=(mode in ["full", "positions"]))
        liquidators = None
        deltas = None

        if mode == "full":
            try:
                liquidators = api.get_hlp_liquidators()
            except Exception as e:
                console.print(f"[dim]Note: Liquidators endpoint unavailable[/dim]")

            try:
                deltas = api.get_hlp_deltas(hours=24)
            except Exception as e:
                console.print(f"[dim]Note: Deltas endpoint unavailable[/dim]")

    if not isinstance(hlp_data, dict):
        console.print("[red]Error: Invalid response from API[/red]")
        return

    # Use correct field names from API
    summary = hlp_data.get('hlp_summary', hlp_data.get('summary', {}))
    combined_positions = hlp_data.get('combined_net_positions', hlp_data.get('combined_positions', []))
    strategies = hlp_data.get('strategies', [])
    exposure = hlp_data.get('exposure', {})

    console.print(f"[green]HLP data loaded successfully![/green]")
    console.print()

    # Display based on mode
    if mode == "summary":
        display_summary_panels(summary, exposure=exposure, strategies=strategies)
        display_exposure_visualization(combined_positions)

    elif mode == "positions":
        display_summary_panels(summary, exposure=exposure, strategies=strategies)
        console.print()
        display_combined_positions(combined_positions)
        console.print()
        display_exposure_visualization(combined_positions)
        console.print()
        if strategies:
            display_strategy_details(strategies)

    else:  # full mode
        display_summary_panels(summary, exposure=exposure, strategies=strategies)
        console.print()

        display_combined_positions(combined_positions)
        console.print()

        display_exposure_visualization(combined_positions)
        console.print()

        if liquidators:
            display_liquidators(liquidators)
            console.print()

        if deltas:
            display_deltas(deltas)
            console.print()

        if strategies:
            display_strategy_details(strategies)

    print_footer()


if __name__ == "__main__":
    main()

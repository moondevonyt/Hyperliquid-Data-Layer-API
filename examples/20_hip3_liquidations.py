"""
Moon Dev's HIP3 Liquidation Dashboard - Stocks, Commodities, Indices & FX Liquidations
Built with love by Moon Dev | Run with: python examples/20_hip3_liquidations.py

HIP3 Categories:
- Stocks: TSLA, NVDA, AAPL, META, MSFT, GOOGL, AMZN, AMD, INTC, PLTR, COIN, HOOD, MSTR, ORCL, MU, NFLX, RIVN, BABA
- Commodities: GOLD, SILVER, COPPER, CL (Oil), NATGAS, URANIUM (~$125M OI)
- Indices: XYZ100 (Nasdaq proxy, ~$120M OI)
- FX: EUR, JPY (~$3M OI)
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

# Category colors and emojis
CATEGORY_STYLES = {
    'stocks': {'color': 'cyan', 'emoji': ''},
    'commodities': {'color': 'yellow', 'emoji': ''},
    'indices': {'color': 'magenta', 'emoji': ''},
    'fx': {'color': 'green', 'emoji': ''}
}

# ==================== BANNER ====================
def print_banner():
    """Print the Moon Dev banner"""
    banner = """██╗  ██╗██╗██████╗ ██████╗     ██╗     ██╗ ██████╗ ███████╗
██║  ██║██║██╔══██╗╚════██╗    ██║     ██║██╔═══██╗██╔════╝
███████║██║██████╔╝ █████╔╝    ██║     ██║██║   ██║███████╗
██╔══██║██║██╔═══╝  ╚═══██╗    ██║     ██║██║▄▄ ██║╚════██║
██║  ██║██║██║     ██████╔╝    ███████╗██║╚██████╔╝███████║
╚═╝  ╚═╝╚═╝╚═╝     ╚═════╝     ╚══════╝╚═╝ ╚══▀▀═╝ ╚══════╝"""
    console.print(Panel(
        Align.center(Text(banner, style="bold yellow")),
        title="[bold red]HIP3 LIQUIDATION TRACKER[/bold red]",
        subtitle="[dim]Stocks | Commodities | Indices | FX - by Moon Dev[/dim]",
        border_style="red",
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

def get_category_style(category):
    """Get color and emoji for category"""
    return CATEGORY_STYLES.get(category.lower(), {'color': 'white', 'emoji': ''})

def categorize_symbol(symbol):
    """Categorize a symbol into its asset class"""
    stocks = ['TSLA', 'NVDA', 'AAPL', 'META', 'MSFT', 'GOOGL', 'AMZN', 'AMD', 'INTC', 'PLTR',
              'COIN', 'HOOD', 'MSTR', 'ORCL', 'MU', 'NFLX', 'RIVN', 'BABA']
    commodities = ['GOLD', 'SILVER', 'COPPER', 'CL', 'NATGAS', 'URANIUM']
    indices = ['XYZ100']
    fx = ['EUR', 'JPY']

    if symbol in stocks:
        return 'stocks'
    elif symbol in commodities:
        return 'commodities'
    elif symbol in indices:
        return 'indices'
    elif symbol in fx:
        return 'fx'
    return 'other'

# ==================== HIP3 LIQUIDATION STATS ====================
def display_hip3_stats(api):
    """Display aggregated HIP3 liquidation statistics"""
    console.print(Panel(
        "[bold yellow]HIP3 LIQUIDATION STATISTICS[/bold yellow]  [dim cyan]GET https://api.moondev.com/api/hip3_liquidations/stats.json[/dim cyan]",
        border_style="yellow",
        padding=(0, 1)
    ))

    try:
        stats = api.get_hip3_liquidation_stats()
        if isinstance(stats, dict):
            panels = []

            # Total stats
            total_count = stats.get('total_count', stats.get('count', 0))
            total_volume = stats.get('total_volume', stats.get('total_value_usd', 0))
            panels.append(Panel(
                f"[bold white]TOTAL LIQUIDATIONS[/bold white]\n[bold cyan]{total_count:,}[/bold cyan] events\n[bold yellow]{format_usd(total_volume)}[/bold yellow]",
                border_style="cyan", width=28, padding=(0, 1)
            ))

            # Long stats
            long_count = stats.get('long_count', stats.get('longs', 0))
            long_volume = stats.get('long_volume', stats.get('long_value_usd', 0))
            panels.append(Panel(
                f"[bold green]LONG LIQUIDATIONS[/bold green]\n[bold green]{long_count:,}[/bold green] events\n[bold yellow]{format_usd(long_volume)}[/bold yellow]",
                border_style="green", width=28, padding=(0, 1)
            ))

            # Short stats
            short_count = stats.get('short_count', stats.get('shorts', 0))
            short_volume = stats.get('short_volume', stats.get('short_value_usd', 0))
            panels.append(Panel(
                f"[bold red]SHORT LIQUIDATIONS[/bold red]\n[bold red]{short_count:,}[/bold red] events\n[bold yellow]{format_usd(short_volume)}[/bold yellow]",
                border_style="red", width=28, padding=(0, 1)
            ))

            console.print(Columns(panels, equal=True, expand=True))

            # Long/Short Ratio Bar
            total_ls = long_count + short_count if (long_count + short_count) > 0 else 1
            long_pct, short_pct = (long_count / total_ls) * 100, (short_count / total_ls) * 100
            ratio_text = Text()
            ratio_text.append("LONGS ", style="bold green")
            ratio_text.append("" * int(long_pct / 2), style="green")
            ratio_text.append("" * int(short_pct / 2), style="red")
            ratio_text.append(" SHORTS", style="bold red")
            console.print(Panel(
                Align.center(ratio_text),
                title=f"[bold white]Long/Short Ratio: {long_pct:.1f}% / {short_pct:.1f}%[/bold white]",
                border_style="magenta", padding=(0, 1)
            ))

            # Category breakdown
            by_category = stats.get('by_category', {})
            if by_category:
                console.print()
                cat_table = Table(box=box.ROUNDED, border_style="cyan", header_style="bold magenta", padding=(0, 1))
                cat_table.add_column("Category", style="cyan", justify="center", width=15)
                cat_table.add_column("Count", style="white", justify="right", width=10)
                cat_table.add_column("Volume", style="yellow", justify="right", width=15)

                for cat_name, cat_data in by_category.items():
                    if isinstance(cat_data, dict):
                        cat_count = cat_data.get('count', 0)
                        cat_vol = cat_data.get('volume', cat_data.get('total_volume', 0))
                    else:
                        cat_count = cat_data
                        cat_vol = 0
                    style = get_category_style(cat_name)
                    cat_table.add_row(
                        f"[{style['color']}]{style['emoji']} {cat_name.upper()}[/{style['color']}]",
                        f"{cat_count:,}",
                        format_usd(cat_vol)
                    )
                console.print(cat_table)

    except Exception as e:
        console.print(f"[red]Moon Dev: Error fetching HIP3 stats: {e}[/red]")

# ==================== TIMEFRAME LIQUIDATIONS ====================
def display_timeframe_liquidations(api):
    """Display HIP3 liquidations across different timeframes"""
    console.print(Panel(
        "[bold cyan]HIP3 LIQUIDATIONS BY TIMEFRAME[/bold cyan]  [dim cyan]GET https://api.moondev.com/api/hip3_liquidations/{timeframe}.json[/dim cyan]",
        border_style="cyan",
        padding=(0, 1)
    ))

    table = Table(box=box.DOUBLE_EDGE, border_style="yellow", header_style="bold magenta", padding=(0, 1))
    table.add_column("Timeframe", style="cyan", justify="center", width=12)
    table.add_column("Count", style="white", justify="right", width=12)
    table.add_column("Volume", style="yellow", justify="right", width=14)
    table.add_column("Longs", style="green", justify="right", width=10)
    table.add_column("Shorts", style="red", justify="right", width=10)

    for tf in ["10m", "1h", "24h"]:
        try:
            data = api.get_hip3_liquidations(tf)

            if isinstance(data, list):
                count = len(data)
                total_volume = sum(float(liq.get('value_usd', liq.get('value', liq.get('usd_value', 0)))) for liq in data)
                long_count = sum(1 for liq in data if liq.get('side', '').lower() in ['long', 'buy'])
                short_count = count - long_count

                table.add_row(
                    f"[bold]{tf}[/bold]",
                    f"{count:,}",
                    format_usd(total_volume),
                    f"[green]{long_count:,}[/green]",
                    f"[red]{short_count:,}[/red]"
                )
            elif isinstance(data, dict):
                stats = data.get('stats', data)
                count = stats.get('total_count', stats.get('count', len(data.get('liquidations', []))))
                volume = stats.get('total_value_usd', stats.get('total_volume', 0))
                longs = stats.get('long_count', 0)
                shorts = stats.get('short_count', 0)

                table.add_row(
                    f"[bold]{tf}[/bold]",
                    f"{count:,}",
                    format_usd(volume),
                    f"[green]{longs:,}[/green]",
                    f"[red]{shorts:,}[/red]"
                )
            else:
                table.add_row(tf, "N/A", "N/A", "N/A", "N/A")

        except Exception as e:
            table.add_row(tf, f"[dim]Error[/dim]", "", "", "")

    console.print(table)
    console.print("[dim]NOTE: Other timeframe available: 7d - use api.get_hip3_liquidations('7d')[/dim]")

# ==================== RECENT LIQUIDATIONS ====================
def display_recent_liquidations(api):
    """Display most recent HIP3 liquidation events"""
    console.print(Panel(
        "[bold red]RECENT HIP3 LIQUIDATIONS (24H)[/bold red]  [dim cyan]GET https://api.moondev.com/api/hip3_liquidations/24h.json[/dim cyan]",
        border_style="red",
        padding=(0, 1)
    ))

    try:
        data = api.get_hip3_liquidations("24h")

        # Handle list response
        if isinstance(data, list):
            liq_list = data
        elif isinstance(data, dict):
            liq_list = data.get('liquidations', data.get('data', []))
        else:
            liq_list = []

        if len(liq_list) > 0:
            # Sort by value descending
            try:
                liq_list = sorted(liq_list, key=lambda x: float(x.get('value_usd', x.get('value', x.get('usd_value', 0)))), reverse=True)
            except:
                pass

            table = Table(box=box.ROUNDED, border_style="red", header_style="bold yellow", padding=(0, 1))
            table.add_column("#", style="dim", width=3)
            table.add_column("Symbol", style="cyan", justify="center", width=12)
            table.add_column("Category", justify="center", width=12)
            table.add_column("Value", style="yellow", justify="right", width=14)
            table.add_column("Side", justify="center", width=10)
            table.add_column("Price", style="white", justify="right", width=14)
            table.add_column("Time", style="dim", width=14)

            for i, liq in enumerate(liq_list[:20], 1):
                symbol = liq.get('symbol', liq.get('coin', '?'))
                value = float(liq.get('value_usd', liq.get('value', liq.get('usd_value', 0))))
                side = liq.get('side', liq.get('direction', '?'))
                price = float(liq.get('price', liq.get('px', 0)))
                timestamp = liq.get('timestamp', liq.get('time', ''))
                category = liq.get('category', categorize_symbol(symbol))

                # Format side
                if side.lower() in ['long', 'buy', 'b']:
                    side_display = "[green]LONG[/green]"
                else:
                    side_display = "[red]SHORT[/red]"

                # Format category
                cat_style = get_category_style(category)
                cat_display = f"[{cat_style['color']}]{cat_style['emoji']} {category.upper()}[/{cat_style['color']}]"

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
                rank_display = "" if i == 1 else "" if i == 2 else "" if i == 3 else str(i)

                table.add_row(
                    rank_display,
                    symbol,
                    cat_display,
                    f"[bold]{format_usd(value)}[/bold]",
                    side_display,
                    f"${price:,.2f}" if price else "N/A",
                    time_str
                )

            console.print(table)
        else:
            console.print("[dim]No recent liquidations found[/dim]")

    except Exception as e:
        console.print(f"[red]Moon Dev: Error fetching recent liquidations: {e}[/red]")

# ==================== CATEGORY BREAKDOWN ====================
def display_category_breakdown(api):
    """Display liquidations breakdown by category"""
    console.print(Panel(
        "[bold magenta]LIQUIDATIONS BY ASSET CLASS[/bold magenta]",
        border_style="magenta",
        padding=(0, 1)
    ))

    try:
        data = api.get_hip3_liquidations("24h")

        if isinstance(data, list):
            liq_list = data
        elif isinstance(data, dict):
            liq_list = data.get('liquidations', data.get('data', []))
        else:
            liq_list = []

        if not liq_list:
            console.print("[dim]No liquidation data available[/dim]")
            return

        # Group by category
        categories = {}
        for liq in liq_list:
            symbol = liq.get('symbol', liq.get('coin', '?'))
            category = liq.get('category', categorize_symbol(symbol))
            value = float(liq.get('value_usd', liq.get('value', liq.get('usd_value', 0))))

            if category not in categories:
                categories[category] = {'count': 0, 'volume': 0, 'symbols': {}}
            categories[category]['count'] += 1
            categories[category]['volume'] += value

            if symbol not in categories[category]['symbols']:
                categories[category]['symbols'][symbol] = {'count': 0, 'volume': 0}
            categories[category]['symbols'][symbol]['count'] += 1
            categories[category]['symbols'][symbol]['volume'] += value

        # Display panels for each category
        panels = []
        for cat_name, cat_data in sorted(categories.items(), key=lambda x: x[1]['volume'], reverse=True):
            style = get_category_style(cat_name)

            # Get top 3 symbols
            top_symbols = sorted(cat_data['symbols'].items(), key=lambda x: x[1]['volume'], reverse=True)[:3]
            symbol_text = "\n".join([f"  {sym}: {format_usd(data['volume'])}" for sym, data in top_symbols])

            panel_text = f"[bold]{style['emoji']} {cat_name.upper()}[/bold]\n"
            panel_text += f"[white]{cat_data['count']}[/white] liqs | [yellow]{format_usd(cat_data['volume'])}[/yellow]\n"
            panel_text += f"[dim]Top Symbols:[/dim]\n{symbol_text}"

            panels.append(Panel(
                panel_text,
                border_style=style['color'],
                width=25,
                padding=(0, 1)
            ))

        if panels:
            console.print(Columns(panels, equal=False, expand=True))

    except Exception as e:
        console.print(f"[red]Moon Dev: Error displaying category breakdown: {e}[/red]")

# ==================== FOOTER ====================
def print_footer():
    """Print footer with timestamp and branding"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(f"[dim yellow]{'─'*95}[/dim yellow]")
    console.print(f"[dim yellow]Moon Dev's HIP3 Liquidation Dashboard | {now} | api.moondev.com | Built with love by Moon Dev[/dim yellow]")

# ==================== MAIN ====================
def main():
    """Main function - Moon Dev's HIP3 Liquidation Dashboard"""
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

    with console.status("[bold yellow]Moon Dev: Fetching HIP3 liquidation data...[/bold yellow]"):
        pass

    display_hip3_stats(api)
    console.print()
    display_timeframe_liquidations(api)
    console.print()
    display_category_breakdown(api)
    console.print()
    display_recent_liquidations(api)
    print_footer()

if __name__ == "__main__":
    main()

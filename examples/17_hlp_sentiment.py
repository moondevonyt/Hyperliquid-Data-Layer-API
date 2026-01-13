"""
Moon Dev's HLP Sentiment Dashboard
===================================
THE BIG ONE! Track what HLP is doing to understand retail positioning.

Built with love by Moon Dev
https://moondev.com

When HLP is long, retail is short (and vice versa).
Z-scores show how extreme the current positioning is vs historical norms.

Key Insight:
- Z-Score > 2.0 = HLP unusually LONG = Retail heavily SHORT = Potential short squeeze
- Z-Score < -2.0 = HLP unusually SHORT = Retail heavily LONG = Potential long squeeze

Usage: python 17_hlp_sentiment.py
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
    """Create the Moon Dev HLP Sentiment banner"""
    banner = """███████╗███████╗███╗   ██╗████████╗██╗███╗   ███╗███████╗███╗   ██╗████████╗
██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗ ████║██╔════╝████╗  ██║╚══██╔══╝
███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔████╔██║█████╗  ██╔██╗ ██║   ██║
╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║
███████║███████╗██║ ╚████║   ██║   ██║██║ ╚═╝ ██║███████╗██║ ╚████║   ██║
╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝"""
    return Panel(
        Align.center(Text(banner, style="bold magenta")),
        title="🧠 [bold cyan]HLP SENTIMENT INDICATOR[/bold cyan] 🧠",
        subtitle="[dim]THE BIG ONE - What is retail actually doing? | by Moon Dev[/dim]",
        border_style="bright_magenta",
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


def get_z_score_color(z_score):
    """Get color based on z-score magnitude"""
    if z_score is None:
        return "white"
    abs_z = abs(z_score)
    if abs_z >= 3:
        return "bold red" if z_score > 0 else "bold green"
    elif abs_z >= 2:
        return "red" if z_score > 0 else "green"
    elif abs_z >= 1:
        return "yellow"
    return "white"


def get_signal_color(signal):
    """Get color based on signal text"""
    if not signal:
        return "white"
    # Handle if signal is a dict
    if isinstance(signal, dict):
        signal = signal.get('text', signal.get('message', signal.get('signal', str(signal))))
    signal_lower = str(signal).lower()
    if 'short squeeze' in signal_lower or 'retail short' in signal_lower:
        return "bold green"
    elif 'long squeeze' in signal_lower or 'retail long' in signal_lower:
        return "bold red"
    elif 'neutral' in signal_lower:
        return "yellow"
    return "cyan"


def create_main_signal_panel(sentiment_data):
    """Create the main signal panel - THE BIG ONE"""
    if not isinstance(sentiment_data, dict):
        return Panel("[dim]No sentiment data available[/dim]", title="Signal")

    z_score = sentiment_data.get('z_score', sentiment_data.get('zscore', 0))
    signal_raw = sentiment_data.get('signal', sentiment_data.get('interpretation', 'Unknown'))
    net_delta = sentiment_data.get('net_delta', sentiment_data.get('delta', 0))
    percentile = sentiment_data.get('percentile', sentiment_data.get('pct', 50))

    # Handle signal if it's a dict
    if isinstance(signal_raw, dict):
        signal = signal_raw.get('text', signal_raw.get('message', signal_raw.get('signal', str(signal_raw))))
    else:
        signal = signal_raw

    z_color = get_z_score_color(z_score)
    signal_color = get_signal_color(signal)

    # Create z-score visual bar
    z_normalized = max(-3, min(3, z_score)) if z_score else 0
    bar_pos = int((z_normalized + 3) / 6 * 40)  # Map -3 to +3 to 0-40
    bar = "░" * bar_pos + "█" + "░" * (40 - bar_pos - 1)

    # Color the bar
    if z_score and z_score > 0:
        bar_display = f"[green]{bar[:20]}[/green][{z_color}]{bar[20:]}[/{z_color}]"
    else:
        bar_display = f"[{z_color}]{bar[:20]}[/{z_color}][red]{bar[20:]}[/red]"

    content = f"""
[bold white]🎯 CURRENT SIGNAL[/bold white]

[{signal_color}]{signal}[/{signal_color}]

[bold white]📊 Z-SCORE[/bold white]
[{z_color}]{z_score:+.2f}σ[/{z_color}] from mean

SHORT ◄─────────────────────────────────────────► LONG
      {bar_display}

[bold white]📈 NET DELTA[/bold white]: [{z_color}]{format_usd(net_delta)}[/{z_color}]
[bold white]📉 PERCENTILE[/bold white]: {percentile:.1f}%
"""

    return Panel(
        content,
        title="🧠 [bold magenta]HLP SENTIMENT[/bold magenta]  [dim cyan]GET https://api.moondev.com/api/hlp/sentiment[/dim cyan]",
        border_style="magenta",
        padding=(1, 2)
    )


def create_interpretation_panel(sentiment_data):
    """Create panel explaining what the signal means"""
    if not isinstance(sentiment_data, dict):
        return Panel("[dim]No data[/dim]", title="Interpretation")

    z_score = sentiment_data.get('z_score', sentiment_data.get('zscore', 0))

    if z_score is None:
        interpretation = "Unable to calculate sentiment"
        action = "Wait for data"
    elif z_score >= 2.5:
        interpretation = "🚀 EXTREME: HLP is heavily LONG\n   Retail is heavily SHORT\n   High probability of SHORT SQUEEZE"
        action = "Consider LONG positions"
    elif z_score >= 2.0:
        interpretation = "📈 BULLISH: HLP more long than usual\n   Retail leaning short\n   Potential short squeeze brewing"
        action = "Lean LONG, watch for squeeze"
    elif z_score >= 1.0:
        interpretation = "↗️ SLIGHTLY BULLISH: HLP slightly long\n   Retail slightly short\n   Mild bullish bias"
        action = "Slight long bias"
    elif z_score <= -2.5:
        interpretation = "💥 EXTREME: HLP is heavily SHORT\n   Retail is heavily LONG\n   High probability of LONG SQUEEZE"
        action = "Consider SHORT positions"
    elif z_score <= -2.0:
        interpretation = "📉 BEARISH: HLP more short than usual\n   Retail leaning long\n   Potential long squeeze brewing"
        action = "Lean SHORT, watch for squeeze"
    elif z_score <= -1.0:
        interpretation = "↘️ SLIGHTLY BEARISH: HLP slightly short\n   Retail slightly long\n   Mild bearish bias"
        action = "Slight short bias"
    else:
        interpretation = "⚖️ NEUTRAL: HLP near historical average\n   No strong retail bias\n   Market in equilibrium"
        action = "No clear directional bias"

    content = f"""[bold white]📖 INTERPRETATION[/bold white]

{interpretation}

[bold yellow]💡 SUGGESTED ACTION[/bold yellow]
{action}

[dim]Remember: HLP takes the opposite side of retail.
When HLP is long, retail is short (and getting squeezed).[/dim]
"""

    return Panel(
        content,
        title="[bold cyan]What This Means[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    )


def create_z_score_guide():
    """Create a guide explaining z-scores"""
    content = """[bold white]📊 Z-SCORE GUIDE[/bold white]

[bold green]Z > +2.0[/bold green]  HLP unusually LONG → Retail SHORT → Buy signal
[yellow]Z = 0[/yellow]      HLP at average → Neutral
[bold red]Z < -2.0[/bold red]  HLP unusually SHORT → Retail LONG → Sell signal

[bold white]🎯 QUICK REFERENCE[/bold white]

  +3σ ████████████ Extreme long (rare)
  +2σ ████████░░░░ Heavily long (buy zone)
  +1σ █████░░░░░░░ Slightly long
   0σ ░░░░░░░░░░░░ Neutral
  -1σ ░░░░░░░█████ Slightly short
  -2σ ░░░░████████ Heavily short (sell zone)
  -3σ ████████████ Extreme short (rare)

[dim]Updates every 5 minutes | Historical data: 60 days[/dim]
"""

    return Panel(
        content,
        title="[bold yellow]Understanding Z-Scores[/bold yellow]",
        border_style="yellow",
        padding=(1, 2)
    )


def create_historical_context(sentiment_data):
    """Create panel with historical context"""
    if not isinstance(sentiment_data, dict):
        return Panel("[dim]No historical data[/dim]", title="History")

    # Try to get historical stats
    stats = sentiment_data.get('stats', sentiment_data.get('historical', {}))
    mean_delta = stats.get('mean', stats.get('avg_delta', 0))
    std_delta = stats.get('std', stats.get('std_delta', 0))
    max_delta = stats.get('max', stats.get('max_delta', 0))
    min_delta = stats.get('min', stats.get('min_delta', 0))

    current = sentiment_data.get('net_delta', sentiment_data.get('delta', 0))

    content = f"""[bold white]📜 HISTORICAL CONTEXT[/bold white]

[cyan]Current Delta:[/cyan]   {format_usd(current)}
[cyan]Historical Mean:[/cyan] {format_usd(mean_delta)}
[cyan]Std Deviation:[/cyan]   {format_usd(std_delta)}

[bold white]📈 RANGE (60 days)[/bold white]
[green]Max (Most Long):[/green]  {format_usd(max_delta)}
[red]Min (Most Short):[/red] {format_usd(min_delta)}

[dim]Z-score = (Current - Mean) / StdDev[/dim]
"""

    return Panel(
        content,
        title="[bold white]Historical Data[/bold white]",
        border_style="white",
        padding=(1, 2)
    )


def create_footer():
    """Create footer with timestamp and branding"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return Text(
        f"━━━ 🌙 Moon Dev's HLP Sentiment | {now} | api.moondev.com | THE BIG ONE! ━━━",
        style="dim magenta",
        justify="center"
    )


def main():
    """Main function - Moon Dev's HLP Sentiment Dashboard"""
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

    # Fetch sentiment data - THE BIG ONE
    console.print("[bold magenta]🧠 Fetching HLP Sentiment (THE BIG ONE)...[/bold magenta]")

    try:
        sentiment_data = api.get_hlp_sentiment()
    except Exception as e:
        console.print(f"[red]Error fetching sentiment: {e}[/red]")
        sentiment_data = {}

    console.print()

    # Main signal panel - THE BIG ONE
    main_panel = create_main_signal_panel(sentiment_data)
    interpretation_panel = create_interpretation_panel(sentiment_data)
    console.print(Columns([main_panel, interpretation_panel], equal=True, expand=True))

    console.print()

    # Guide and historical context
    guide_panel = create_z_score_guide()
    history_panel = create_historical_context(sentiment_data)
    console.print(Columns([guide_panel, history_panel], equal=True, expand=True))

    # Summary
    z_score = sentiment_data.get('z_score', sentiment_data.get('zscore', 0)) if isinstance(sentiment_data, dict) else 0
    signal_raw = sentiment_data.get('signal', 'Unknown') if isinstance(sentiment_data, dict) else 'Unknown'
    # Handle signal if it's a dict
    if isinstance(signal_raw, dict):
        signal = signal_raw.get('text', signal_raw.get('message', signal_raw.get('signal', str(signal_raw))))
    else:
        signal = signal_raw
    z_color = get_z_score_color(z_score)

    summary = (
        f"🧠 Z-Score: [{z_color}]{z_score:+.2f}σ[/{z_color}] | "
        f"📊 Signal: [bold]{signal}[/bold] | "
        f"🎯 [magenta]THE BIG ONE - Moon Dev[/magenta]"
    )
    console.print(Panel(summary, title="[bold magenta]Summary[/bold magenta]  [dim cyan]GET https://api.moondev.com/api/hlp/sentiment[/dim cyan]", border_style="magenta", padding=(0, 1)))

    console.print()
    console.print(create_footer())


if __name__ == "__main__":
    main()

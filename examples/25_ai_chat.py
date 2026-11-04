"""
Moon Dev's AI Chat API - OpenAI-Compatible Drop-in Replacement
Built with love by Moon Dev | Run with: python examples/25_ai_chat.py

This example shows how to use Moon Dev's AI API as a drop-in replacement for OpenAI.
No need for OpenAI or Anthropic API keys - just use your Moon Dev API key!

Features:
- OpenAI SDK compatible (just change base_url)
- Simple chat endpoint for quick queries
- Works with any OpenAI-compatible library

Full docs: https://moondev.com/docs
"""

import sys
import os

# Add parent directory to path for importing api.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
import requests
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.markdown import Markdown
from rich import box

# Load environment variables
load_dotenv()

# Initialize Rich console
console = Console()

# API Configuration
BASE_URL = "https://api.moondev.com/api/ai"
API_KEY = os.getenv("MOONDEV_API_KEY", "")

# ==================== BANNER ====================
def print_banner():
    """Print the Moon Dev banner"""
    banner = """███╗   ███╗ ██████╗  ██████╗ ███╗   ██╗    ██████╗ ███████╗██╗   ██╗
████╗ ████║██╔═══██╗██╔═══██╗████╗  ██║    ██╔══██╗██╔════╝██║   ██║
██╔████╔██║██║   ██║██║   ██║██╔██╗ ██║    ██║  ██║█████╗  ██║   ██║
██║╚██╔╝██║██║   ██║██║   ██║██║╚██╗██║    ██║  ██║██╔══╝  ╚██╗ ██╔╝
██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██║ ╚████║    ██████╔╝███████╗ ╚████╔╝
╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝    ╚═════╝ ╚══════╝  ╚═══╝
                         █████╗ ██╗
                        ██╔══██╗██║
                        ███████║██║
                        ██╔══██║██║
                        ██║  ██║██║
                        ╚═╝  ╚═╝╚═╝"""
    console.print(Panel(
        Align.center(Text(banner, style="bold cyan")),
        title="[bold red]MOON DEV AI API[/bold red]",
        subtitle="[dim]OpenAI-Compatible Drop-in Replacement - by Moon Dev[/dim]",
        border_style="red",
        box=box.DOUBLE_EDGE,
        padding=(0, 1)
    ))

# ==================== SIMPLE CHAT ====================
def simple_chat(message, max_tokens=500):
    """
    Use the simple chat endpoint for quick AI queries.

    POST https://api.moondev.com/api/ai/chat
    """
    url = f"{BASE_URL}/chat"

    payload = {
        "messages": [{"role": "user", "content": message}],
        "max_tokens": max_tokens
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    return response.json()

# ==================== OPENAI-COMPATIBLE CHAT ====================
def openai_compatible_chat(messages, max_tokens=500, model="moondev-ai"):
    """
    Use the OpenAI-compatible endpoint.

    POST https://api.moondev.com/api/ai/v1/chat/completions

    This endpoint is compatible with the OpenAI SDK - just change base_url!
    """
    url = f"{BASE_URL}/v1/chat/completions"

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    return response.json()

# ==================== OPENAI SDK EXAMPLE ====================
def openai_sdk_example(message, max_tokens=500):
    """
    Example using the official OpenAI SDK with Moon Dev's API.

    This is a drop-in replacement - just change the base_url!
    """
    try:
        from openai import OpenAI

        client = OpenAI(
            base_url=f"{BASE_URL}/v1",
            api_key=API_KEY
        )

        response = client.chat.completions.create(
            model="moondev-ai",
            messages=[{"role": "user", "content": message}],
            max_tokens=max_tokens
        )

        return response.choices[0].message.content
    except ImportError:
        return None  # OpenAI SDK not installed

# ==================== HEALTH CHECK ====================
def check_health():
    """Check if the AI API is healthy"""
    url = f"{BASE_URL}/health"
    response = requests.get(url)
    return response.json()

# ==================== DEMO FUNCTIONS ====================
def demo_simple_chat():
    """Demonstrate the simple chat endpoint"""
    console.print(Panel(
        "[bold yellow]SIMPLE CHAT ENDPOINT[/bold yellow]  [dim cyan]POST https://api.moondev.com/api/ai/chat[/dim cyan]",
        border_style="yellow",
        padding=(0, 1)
    ))

    question = "What is Hyperliquid and why is it important for crypto trading?"

    console.print(f"\n[bold cyan]Question:[/bold cyan] {question}\n")

    try:
        response = simple_chat(question, max_tokens=300)

        # Extract the response content
        if isinstance(response, dict):
            if 'choices' in response:
                content = response['choices'][0]['message']['content']
            elif 'response' in response:
                content = response['response']
            elif 'content' in response:
                content = response['content']
            else:
                content = str(response)
        else:
            content = str(response)

        console.print(Panel(
            Markdown(content),
            title="[bold green]Moon Dev AI Response[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def demo_openai_compatible():
    """Demonstrate the OpenAI-compatible endpoint"""
    console.print(Panel(
        "[bold magenta]OPENAI-COMPATIBLE ENDPOINT[/bold magenta]  [dim cyan]POST https://api.moondev.com/api/ai/v1/chat/completions[/dim cyan]",
        border_style="magenta",
        padding=(0, 1)
    ))

    messages = [
        {"role": "system", "content": "You are a helpful trading assistant created by Moon Dev."},
        {"role": "user", "content": "Give me 3 tips for managing risk in crypto trading."}
    ]

    console.print(f"\n[bold cyan]System:[/bold cyan] {messages[0]['content']}")
    console.print(f"[bold cyan]User:[/bold cyan] {messages[1]['content']}\n")

    try:
        response = openai_compatible_chat(messages, max_tokens=400)

        # Extract the response content
        if 'choices' in response:
            content = response['choices'][0]['message']['content']
        else:
            content = str(response)

        console.print(Panel(
            Markdown(content),
            title="[bold green]Moon Dev AI Response[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def demo_openai_sdk():
    """Demonstrate using the official OpenAI SDK"""
    console.print(Panel(
        "[bold blue]OPENAI SDK DROP-IN[/bold blue]  [dim cyan]from openai import OpenAI[/dim cyan]",
        border_style="blue",
        padding=(0, 1)
    ))

    console.print("\n[bold cyan]Code Example:[/bold cyan]")
    code = '''
from openai import OpenAI

client = OpenAI(
    base_url="https://api.moondev.com/api/ai/v1",
    api_key="YOUR_MOONDEV_API_KEY"
)

response = client.chat.completions.create(
    model="moondev-ai",
    messages=[{"role": "user", "content": "Your question here"}],
    max_tokens=500
)
print(response.choices[0].message.content)
'''
    console.print(Panel(code, border_style="dim", padding=(0, 1)))

    question = "What makes Moon Dev's data layer unique?"
    console.print(f"\n[bold cyan]Testing with:[/bold cyan] {question}\n")

    try:
        result = openai_sdk_example(question, max_tokens=300)
        if result:
            console.print(Panel(
                Markdown(result),
                title="[bold green]OpenAI SDK Response[/bold green]",
                border_style="green",
                padding=(1, 2)
            ))
        else:
            console.print("[yellow]OpenAI SDK not installed. Install with: pip install openai[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

# ==================== MAIN ====================
def main():
    """Main function - Moon Dev's AI Chat API Demo"""
    console.clear()
    print_banner()

    console.print("[bold cyan]Moon Dev: Initializing AI API connection...[/bold cyan]")

    if not API_KEY:
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

    console.print(f"[green]API key loaded (...{API_KEY[-4:]})[/green]")

    # Health check
    console.print("\n[bold cyan]Moon Dev: Checking AI API health...[/bold cyan]")
    try:
        health = check_health()
        console.print(f"[green]AI API Status: {health.get('status', 'OK')}[/green]")
    except Exception as e:
        console.print(f"[yellow]Health check: {e}[/yellow]")

    console.print()

    # Demo 1: Simple Chat
    demo_simple_chat()
    console.print()

    # Demo 2: OpenAI-Compatible
    demo_openai_compatible()
    console.print()

    # Demo 3: OpenAI SDK
    demo_openai_sdk()

    # Footer
    console.print(f"\n[dim yellow]{'─'*80}[/dim yellow]")
    console.print("[dim yellow]Moon Dev's AI Chat API | https://moondev.com/docs | Built with love by Moon Dev[/dim yellow]")

if __name__ == "__main__":
    main()

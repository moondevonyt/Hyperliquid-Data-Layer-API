"""
🌙 Moon Dev's Director Agent
Chat about Hyperliquid APIs, propose plans, execute with AI swarm

Built with love by Moon Dev 🚀

Usage:
    python -m ai_agents.director_agent

The Director:
    1. Understands all 40+ Hyperliquid API endpoints
    2. Chats with you about what's available
    3. Proposes analysis plans using specific API calls
    4. Executes plans and distributes data to 6+ AI models
    5. Returns multi-perspective analysis from the swarm
"""

import os
import sys
import json

# Add parent directory to path for api.py import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from openai import OpenAI
from termcolor import cprint

# Load environment variables
load_dotenv()

# Import after path setup
from api import MoonDevAPI
from ai_agents.swarm_agent import SwarmAgent

# ============================================
# 🎯 API KNOWLEDGE - What the Director knows
# ============================================

API_KNOWLEDGE = """
AVAILABLE HYPERLIQUID API ENDPOINTS (Moon Dev's Data Layer):

== LIQUIDATIONS ==
• get_liquidations(timeframe) - Liquidation data
  Timeframes: 10m, 1h, 4h, 12h, 24h, 2d, 7d, 14d, 30d
  Returns: total_count, total_usd, long_count, short_count, top liquidations

• get_all_liquidations(timeframe) - Multi-exchange combined liquidations
  Exchanges: Hyperliquid + Binance + Bybit + OKX

• get_all_liquidation_stats() - Stats across all exchanges
  Returns: total_count, total_volume, by_exchange breakdown

• get_binance_liquidations(timeframe) - Binance Futures liquidations
• get_bybit_liquidations(timeframe) - Bybit liquidations
• get_okx_liquidations(timeframe) - OKX liquidations

== POSITIONS ==
• get_positions() - Top 50 whale positions across ALL 148 symbols
  Updates every 1 second, shows positions near liquidation

• get_all_positions() - All 148 symbols, top 50 longs/shorts each
  500KB response, updates every 60 seconds

== HLP SENTIMENT (THE BIG ONE!) ==
• get_hlp_sentiment() - Z-scores showing retail positioning
  Z > +2.0 = HLP is LONG = Retail is SHORT = Potential BUY signal
  Z < -2.0 = HLP is SHORT = Retail is LONG = Potential SELL signal
  This is institutional-grade sentiment data!

== HLP ANALYTICS (Hyperliquidity Provider ~$210M+) ==
• get_hlp_positions() - All 7 HLP strategy positions + combined net exposure
• get_hlp_trades(limit) - Historical HLP trade fills (5,000+ tracked)
• get_hlp_trade_stats() - Volume and fee statistics
• get_hlp_position_history(hours) - Position snapshots over time
• get_hlp_liquidators() - Liquidator activation events
• get_hlp_deltas(hours) - Net exposure changes over time
• get_hlp_liquidator_status() - Real-time liquidator status (active/idle + PnL)
• get_hlp_market_maker() - Strategy B tracker for BTC/ETH/SOL
• get_hlp_timing() - Hourly/session profitability analysis
• get_hlp_correlation() - Delta-price correlation by coin

== SMART MONEY ==
• get_smart_money_rankings() - Top 100 smart money + Bottom 100 dumb money
• get_smart_money_leaderboard() - Top 50 performers with details
• get_smart_money_signals(timeframe) - Trading signals (10m, 1h, 24h)

== ORDER FLOW ==
• get_orderflow() - Buy/sell pressure by timeframe + per coin
• get_imbalance(timeframe) - Buy/sell imbalance (5m, 15m, 1h, 4h, 24h)
• get_trades() - Recent 500 trades (real-time)
• get_large_trades() - Large trades >$100k (24h)

== TICK DATA ==
• get_tick_latest() - Current prices for all symbols
• get_tick_stats() - Collection stats
• get_ticks(symbol, timeframe) - Historical ticks
  Symbols: btc, eth, hype, sol, xrp
  Timeframes: 10m, 1h, 4h, 24h, 7d

== USER DATA (ANY Hyperliquid wallet!) ==
• get_user_positions(address) - Positions for ANY wallet address
• get_user_fills(address, limit) - Trade history for ANY wallet (up to ALL fills!)

== WHALE TRACKING ==
• get_whales() - Recent whale trades ($25k+, buys & sells)
• get_buyers() - $5k+ buyers on HYPE/SOL/XRP/ETH (buyers only!)
• get_depositors() - All addresses that ever bridged to Hyperliquid
• get_whale_addresses() - Plain text list of whale addresses

== BLOCKCHAIN DATA ==
• get_events() - Real-time blockchain events (transfers, swaps, deposits)
• get_contracts() - Contract registry with metadata
"""

# Director model (Grok 4 Fast via OpenRouter for SPEED!)
DIRECTOR_MODEL = "x-ai/grok-4-fast"  # Fast reasoning model via OpenRouter


class DirectorAgent:
    """
    🌙 Moon Dev's Director Agent

    Chats about Hyperliquid APIs, proposes analysis plans,
    executes with AI swarm for multi-perspective insights.
    """

    def __init__(self):
        cprint("\n" + "=" * 60, "cyan")
        cprint("🌙 Moon Dev's Director Agent", "cyan", attrs=['bold'])
        cprint("=" * 60, "cyan")

        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if not openrouter_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment!")

        # OpenRouter client for Director (Grok 4 Fast - SPEED!)
        self.client = OpenAI(
            api_key=openrouter_key,
            base_url="https://openrouter.ai/api/v1"
        )

        # MoonDevAPI for data fetching
        cprint("\n📡 Connecting to Moon Dev API...", "yellow")
        self.api = MoonDevAPI()

        if not self.api.api_key:
            cprint("⚠️  MOONDEV_API_KEY not found - API calls will fail", "yellow")
        else:
            cprint("✅ Moon Dev API connected", "green")

        # Swarm for multi-model analysis
        self.swarm = SwarmAgent()

        cprint("\n✅ Director ready!", "green")
        cprint("\n" + "-" * 60, "cyan")
        cprint("🎬 DIRECTOR MODE - I know all 40+ Hyperliquid APIs!", "cyan", attrs=['bold'])
        cprint("   Ask me anything, I'll propose a plan to fetch data", "grey")
        cprint("   Type 'quit' to exit", "grey")
        cprint("-" * 60, "cyan")

    def chat(self, user_message):
        """Chat with Director about API capabilities"""
        system_prompt = f"""You are Moon Dev's Director Agent for Hyperliquid data analysis.

{API_KNOWLEDGE}

INSTRUCTIONS:
1. Help users understand what they can analyze with these APIs
2. When they ask for analysis, propose which API calls to make
3. Format your plan with [PLAN] tag when proposing API calls
4. Be concise, direct, and helpful
5. Use Moon Dev branding

Example plan format:
[PLAN]
1. get_hlp_sentiment() - Check retail positioning
2. get_liquidations("24h") - Recent liquidation pressure
3. get_smart_money_signals("1h") - Smart money activity

When user asks "what can I do" or similar, give a helpful overview.
When user asks for specific analysis, propose a concrete plan with [PLAN] tag.
"""

        response = self.client.chat.completions.create(
            model=DIRECTOR_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1024,
            temperature=0.7
        )

        return response.choices[0].message.content

    def execute_plan(self, plan_text, original_question):
        """Execute API calls from plan and send to swarm"""
        # Parse API calls from plan
        api_calls = self._parse_plan(plan_text)

        if not api_calls:
            cprint("❌ No API calls found in plan", "red")
            return None, None

        # Execute API calls
        cprint("\n📡 Fetching data from Moon Dev API...", "yellow")
        data = {}
        for call in api_calls:
            cprint(f"   → {call}", "cyan")
            result = self._execute_api_call(call)
            if result is not None:
                data[call] = result
                cprint(f"   ✅ {call}", "green")
            else:
                cprint(f"   ❌ {call} - failed", "red")

        if not data:
            cprint("❌ No data retrieved from APIs", "red")
            return None, None

        # Format data for swarm
        data_summary = self._format_data(data)

        # Build swarm prompt
        swarm_prompt = f"""
QUESTION: {original_question}

DATA FROM HYPERLIQUID APIs (Moon Dev's Data Layer):
{data_summary}

Analyze this data and provide your perspective on the question.
Be specific about what the data tells us. Include actionable insights.
Keep your response concise but thorough.
"""

        system_prompt = """You are an expert crypto analyst reviewing Hyperliquid exchange data.
This is institutional-grade data from Moon Dev's Data Layer API.
Provide clear, actionable analysis based on the data provided.
Focus on what the numbers mean for trading decisions."""

        cprint("\n🌊 Sending to AI Swarm for analysis...", "cyan")
        results = self.swarm.query(swarm_prompt, system_prompt)
        return results, data_summary

    def _parse_plan(self, plan_text):
        """Extract API calls from plan text"""
        calls = []
        for line in plan_text.split('\n'):
            if 'get_' in line:
                # Extract method call including arguments
                start = line.find('get_')
                end = line.find(')', start) + 1
                if end > start:
                    call = line[start:end]
                    # Handle calls without closing paren
                    if ')' not in call:
                        # Try to find the method name at least
                        paren = call.find('(')
                        if paren == -1:
                            call = call.split()[0] + "()"
                    calls.append(call)
        return calls

    def _execute_api_call(self, call):
        """Execute a single API call dynamically"""
        try:
            # Parse method name and arguments
            if '(' in call:
                method_name = call.split('(')[0]
                args_str = call[call.find('(')+1:call.find(')')]
            else:
                method_name = call.strip()
                args_str = ""

            # Get method from API
            method = getattr(self.api, method_name, None)
            if not method:
                cprint(f"      ⚠️  Method {method_name} not found", "yellow")
                return None

            # Execute with or without args
            if args_str:
                # Clean up argument string
                args_str = args_str.strip().strip('"').strip("'")
                return method(args_str)
            else:
                return method()

        except Exception as e:
            cprint(f"      ⚠️  Error: {str(e)[:50]}", "yellow")
            return None

    def _format_data(self, data):
        """Format API data for swarm prompt"""
        formatted = []
        for call, result in data.items():
            # Truncate large responses
            result_str = json.dumps(result, indent=2, default=str)
            if len(result_str) > 3000:
                result_str = result_str[:3000] + "\n... [truncated]"
            formatted.append(f"\n=== {call} ===\n{result_str}")
        return "\n".join(formatted)

    def _display_results(self, results, original_data):
        """Display swarm results beautifully - FULL responses, no truncation!"""
        cprint("\n" + "=" * 60, "green")
        cprint("🤖 AI SWARM RESPONSES", "green", attrs=['bold'])
        cprint("=" * 60, "green")

        for model, data in results.items():
            if data["success"]:
                cprint(f"\n💡 {model}:", "yellow", attrs=['bold'])
                cprint("-" * 40, "yellow")
                cprint(data["response"], "white")
            else:
                cprint(f"\n❌ {model}: {data['response']}", "red")

        cprint("\n" + "=" * 60, "green")
        cprint("🌙 Analysis complete! - Moon Dev", "cyan", attrs=['bold'])

        # Swarm follow-up loop - returns "exit" or "director"
        return self._swarm_loop(original_data)

    def _swarm_loop(self, data_summary):
        """Continue chatting with the swarm or go back to Director"""
        cprint("\n" + "-" * 60, "cyan")
        cprint("🌊 SWARM MODE - Ask the swarm anything about this data!", "cyan", attrs=['bold'])
        cprint("   Type 'd' to go back to Director", "grey")
        cprint("   Type 'quit' to exit", "grey")
        cprint("-" * 60, "cyan")

        system_prompt = """You are an expert crypto analyst reviewing Hyperliquid exchange data.
This is institutional-grade data from Moon Dev's Data Layer API.
Provide clear, actionable analysis based on the data provided.
Focus on what the numbers mean for trading decisions."""

        while True:
            try:
                user_input = input("\n🌊 > ").strip()
            except (EOFError, KeyboardInterrupt):
                cprint("\n\n👋 Moon Dev says goodbye!", "cyan")
                return "exit"

            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit', 'q']:
                cprint("\n👋 Moon Dev says goodbye!", "cyan")
                return "exit"

            if user_input.lower() == 'd':
                cprint("\n🎬 Back to Director mode!", "cyan")
                return "director"

            # Ask the swarm with the data context
            swarm_prompt = f"""
CONTEXT - DATA FROM HYPERLIQUID APIs:
{data_summary}

USER QUESTION: {user_input}

Analyze the data and answer the user's question.
Be specific and actionable.
"""
            cprint("\n🌊 Asking the swarm...", "cyan")
            results = self.swarm.query(swarm_prompt, system_prompt)

            # Display results
            cprint("\n" + "=" * 60, "green")
            cprint("🤖 AI SWARM RESPONSES", "green", attrs=['bold'])
            cprint("=" * 60, "green")

            for model, response_data in results.items():
                if response_data["success"]:
                    cprint(f"\n💡 {model}:", "yellow", attrs=['bold'])
                    cprint("-" * 40, "yellow")
                    cprint(response_data["response"], "white")
                else:
                    cprint(f"\n❌ {model}: {response_data['response']}", "red")

            cprint("\n" + "=" * 60, "green")
            cprint("🌙 Analysis complete! - Moon Dev", "cyan", attrs=['bold'])

    def run(self):
        """Interactive chat loop"""
        while True:
            try:
                user_input = input("\n🌙 > ").strip()
            except (EOFError, KeyboardInterrupt):
                cprint("\n\n👋 Moon Dev says goodbye!", "cyan")
                break

            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit', 'q']:
                cprint("\n👋 Moon Dev says goodbye!", "cyan")
                break

            # Get Director response
            cprint("\n🤔 Director is thinking...", "grey")
            response = self.chat(user_input)
            cprint(f"\n{response}\n", "white")

            # Check if response contains a plan
            if "[PLAN]" in response:
                try:
                    confirm = input("📋 Proceed with this plan? [y/n] > ").strip().lower()
                except (EOFError, KeyboardInterrupt):
                    cprint("\n\n👋 Moon Dev says goodbye!", "cyan")
                    break

                if confirm == 'y':
                    results, data_summary = self.execute_plan(response, user_input)
                    if results and data_summary:
                        exit_status = self._display_results(results, data_summary)
                        if exit_status == "exit":
                            break
                        # Back to Director mode
                        cprint("\n" + "-" * 60, "cyan")
                        cprint("🎬 DIRECTOR MODE - Ask me another question!", "cyan", attrs=['bold'])
                        cprint("-" * 60, "cyan")
                else:
                    cprint("Plan cancelled. Ask me something else!", "grey")
            else:
                # No plan in response - give clear options in a loop
                while True:
                    cprint("-" * 60, "yellow")
                    cprint("What's next?", "yellow", attrs=['bold'])
                    cprint("   's' = Send Director's response to Swarm for multi-AI analysis", "white")
                    cprint("   Or type anything else to keep chatting with Director", "white")
                    cprint("-" * 60, "yellow")

                    try:
                        next_action = input("\n🌙 > ").strip()
                    except (EOFError, KeyboardInterrupt):
                        cprint("\n\n👋 Moon Dev says goodbye!", "cyan")
                        return  # Exit run() entirely

                    if next_action.lower() == 's':
                        # Send Director's response to swarm for analysis
                        cprint("\n🌊 Sending Director's response to Swarm...", "cyan")

                        swarm_prompt = f"""
The Director provided this analysis about Hyperliquid:

{response}

Please review this analysis and provide your perspective.
Add any additional insights, correct any errors, or expand on key points.
"""
                        system_prompt = """You are an expert crypto analyst reviewing another AI's analysis of Hyperliquid data.
Provide your own perspective, add insights, and highlight what's most actionable."""

                        results = self.swarm.query(swarm_prompt, system_prompt)

                        # Display results
                        cprint("\n" + "=" * 60, "green")
                        cprint("🤖 AI SWARM RESPONSES", "green", attrs=['bold'])
                        cprint("=" * 60, "green")

                        for model, data in results.items():
                            if data["success"]:
                                cprint(f"\n💡 {model}:", "yellow", attrs=['bold'])
                                cprint("-" * 40, "yellow")
                                cprint(data["response"], "white")
                            else:
                                cprint(f"\n❌ {model}: {data['response']}", "red")

                        cprint("\n" + "=" * 60, "green")
                        cprint("🌙 Analysis complete! - Moon Dev", "cyan", attrs=['bold'])

                        # Back to Director - break inner loop
                        cprint("\n" + "-" * 60, "cyan")
                        cprint("🎬 DIRECTOR MODE - Ask me another question!", "cyan", attrs=['bold'])
                        cprint("-" * 60, "cyan")
                        break

                    elif next_action.lower() in ['quit', 'exit', 'q']:
                        cprint("\n👋 Moon Dev says goodbye!", "cyan")
                        return  # Exit run() entirely

                    elif next_action:
                        # They typed a new question - process it
                        cprint("\n🤔 Director is thinking...", "grey")
                        response = self.chat(next_action)
                        cprint(f"\n{response}\n", "white")

                        # Check if THIS response has a plan
                        if "[PLAN]" in response:
                            try:
                                confirm = input("📋 Proceed with this plan? [y/n] > ").strip().lower()
                            except (EOFError, KeyboardInterrupt):
                                cprint("\n\n👋 Moon Dev says goodbye!", "cyan")
                                return

                            if confirm == 'y':
                                results, data_summary = self.execute_plan(response, next_action)
                                if results and data_summary:
                                    exit_status = self._display_results(results, data_summary)
                                    if exit_status == "exit":
                                        return
                                # Break to go back to Director mode
                                cprint("\n" + "-" * 60, "cyan")
                                cprint("🎬 DIRECTOR MODE - Ask me another question!", "cyan", attrs=['bold'])
                                cprint("-" * 60, "cyan")
                                break
                            else:
                                cprint("Plan cancelled.", "grey")
                        # If no plan, loop continues and shows options again


def main():
    """Main entry point"""
    try:
        director = DirectorAgent()
        director.run()
    except ValueError as e:
        cprint(f"\n❌ Error: {e}", "red")
        cprint("Make sure OPENROUTER_API_KEY is set in your .env file", "yellow")
    except Exception as e:
        cprint(f"\n❌ Unexpected error: {e}", "red")


if __name__ == "__main__":
    main()

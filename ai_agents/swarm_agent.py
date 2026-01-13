"""
🌙 Moon Dev's Swarm Agent - OpenRouter Edition
Query multiple AI models in parallel via OpenRouter (one API key!)

Built with love by Moon Dev 🚀

Usage:
    from ai_agents.swarm_agent import SwarmAgent

    swarm = SwarmAgent()
    results = swarm.query("Should I buy BTC now?")

    for model, data in results.items():
        if data["success"]:
            print(f"{model}: {data['response']}")
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from termcolor import cprint

# Load environment variables
load_dotenv()

# ============================================
# 🎯 SWARM CONFIGURATION - Moon Dev
# ============================================

# OpenRouter models to use in swarm (name, model_id)
# All accessed via single OPENROUTER_API_KEY!
# See https://openrouter.ai/models for latest model IDs
SWARM_MODELS = [
    ("Claude Sonnet 4", "anthropic/claude-sonnet-4"),
    ("GPT-4o", "openai/gpt-4o"),
    ("Qwen Max", "qwen/qwen-max"),
    ("GLM-4.7", "z-ai/glm-4.7"),
    ("Gemini 3 Flash", "google/gemini-3-flash-preview"),
    ("DeepSeek R1", "deepseek/deepseek-r1"),
]

# Model parameters
DEFAULT_MAX_TOKENS = 2048
DEFAULT_TEMPERATURE = 0.7
MODEL_TIMEOUT = 120  # seconds

# ============================================


class SwarmAgent:
    """
    🌙 Moon Dev's Swarm Agent

    Queries multiple AI models in parallel via OpenRouter and returns
    responses from each model. Perfect for getting diverse AI perspectives
    on trading decisions.
    """

    def __init__(self, custom_models=None):
        """
        Initialize the Swarm Agent

        Args:
            custom_models: Optional list of (name, model_id) tuples to override defaults
        """
        self.models = custom_models or SWARM_MODELS

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment!")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )

        cprint("\n🌙 Moon Dev's Swarm Agent Initialized", "cyan", attrs=['bold'])
        cprint(f"   📡 {len(self.models)} AI models ready via OpenRouter", "green")
        for name, model_id in self.models:
            cprint(f"      • {name}", "white")

    def _query_model(self, model_name, model_id, prompt, system_prompt):
        """Query a single model via OpenRouter"""
        try:
            response = self.client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=DEFAULT_MAX_TOKENS,
                temperature=DEFAULT_TEMPERATURE
            )

            content = response.choices[0].message.content

            # Strip <think> tags from reasoning models
            import re
            content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()

            return model_name, content, True

        except Exception as e:
            return model_name, str(e), False

    def query(self, prompt, system_prompt="You are a helpful trading analyst."):
        """
        Query all models in parallel

        Args:
            prompt: The question/prompt to send to all models
            system_prompt: System prompt for context

        Returns:
            Dict mapping model names to response dicts:
            {
                "Claude Opus 4.5": {"response": "...", "success": True},
                "GPT-5 Mini": {"response": "...", "success": True},
                ...
            }
        """
        cprint(f"\n🌊 Querying {len(self.models)} AI models in parallel...", "cyan", attrs=['bold'])

        results = {}

        with ThreadPoolExecutor(max_workers=len(self.models)) as executor:
            # Submit all queries in parallel
            futures = {
                executor.submit(
                    self._query_model, name, model_id, prompt, system_prompt
                ): name
                for name, model_id in self.models
            }

            # Collect results as they complete
            try:
                for future in as_completed(futures, timeout=MODEL_TIMEOUT):
                    name, response, success = future.result()
                    results[name] = {"response": response, "success": success}

                    status = "✅" if success else "❌"
                    color = "green" if success else "red"
                    cprint(f"   {status} {name}", color)

            except TimeoutError:
                cprint("   ⏰ Some models timed out", "yellow")
                # Mark remaining as failed
                for future, name in futures.items():
                    if name not in results:
                        results[name] = {"response": "Timeout", "success": False}

        successful = sum(1 for r in results.values() if r["success"])
        cprint(f"\n✨ {successful}/{len(self.models)} models responded - Moon Dev", "cyan")

        return results


def main():
    """Simple test of the Swarm Agent"""
    cprint("\n" + "=" * 60, "cyan")
    cprint("🌙 Moon Dev's Swarm Agent Test", "cyan", attrs=['bold'])
    cprint("=" * 60, "cyan")

    swarm = SwarmAgent()

    cprint("\n💭 Enter a question to ask the AI swarm:", "yellow")
    prompt = input("🌙 > ").strip()

    if not prompt:
        cprint("❌ No prompt provided. Exiting.", "red")
        return

    results = swarm.query(prompt)

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

    cprint("\n✨ Swarm query complete! - Moon Dev 🌙\n", "cyan", attrs=['bold'])


if __name__ == "__main__":
    main()

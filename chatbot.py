"""CLI customer support chatbot."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from support.bot import SupportBot


def main() -> None:
    bot = SupportBot()
    mode = "DEMO" if bot.demo_mode() else "LIVE (Groq)"
    print("=" * 50)
    print("  AI Customer Support Bot · NovaGear")
    print(f"  Mode: {mode}")
    print("  Type 'quit' to exit  |  'save' to save chat  |  'reset' to clear memory")
    print("=" * 50)
    print()

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("\nGoodbye! Have a great day.")
            break
        if user_input.lower() == "save":
            path = bot.save_log()
            print(f"\nChat saved to {path}\n")
            continue
        if user_input.lower() == "reset":
            bot.reset()
            print("\nMemory cleared.\n")
            continue
        reply = bot.ask(user_input)
        print(f"\nBot: {reply}\n")


if __name__ == "__main__":
    main()

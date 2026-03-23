import os
import json
from datetime import datetime
import requests

# ── config ──────────────────────────────────────────────────────────────────
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-groq-api-key-here")
MODEL        = "llama3-8b-8192"   # free & fast on Groq

SYSTEM_PROMPT = """
You are a helpful customer support assistant for a tech company.
Your job is to help users with questions about products, orders, and technical issues.
Keep your answers short, clear, and friendly.
If you don't know something, say so honestly instead of guessing.
"""

# ── conversation memory ──────────────────────────────────────────────────────
# We store the full chat history so the bot remembers context
chat_history = []

def ask_bot(user_message):
    """Send a message to the AI and get a reply back."""

    # Add user message to history
    chat_history.append({
        "role": "user",
        "content": user_message
    })

    # Build the full request payload
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history,
        "temperature": 0.7,
        "max_tokens": 500
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()
        bot_reply = data["choices"][0]["message"]["content"]

        # Save bot reply to history too
        chat_history.append({
            "role": "assistant",
            "content": bot_reply
        })

        return bot_reply

    except requests.exceptions.RequestException as error:
        return f"Connection error: {error}"
    except KeyError:
        return "Unexpected response from the API. Please try again."


def save_chat_log():
    """Save the conversation to a JSON file for later review."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename   = f"chat_log_{timestamp}.json"

    with open(filename, "w") as file:
        json.dump(chat_history, file, indent=2)

    print(f"\nChat saved to {filename}")


def run_chatbot():
    """Main loop — keeps the conversation going until the user types 'quit'."""
    print("=" * 50)
    print("  AI Customer Support Bot")
    print("  Type 'quit' to exit  |  Type 'save' to save chat")
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
            save_chat_log()
            continue

        reply = ask_bot(user_input)
        print(f"\nBot: {reply}\n")


if __name__ == "__main__":
    run_chatbot()

"""Conversation memory + Groq / demo replies."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

from .knowledge import FAQ, SYSTEM_PROMPT

load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


class SupportBot:
    def __init__(self) -> None:
        self.history: list[dict[str, str]] = []
        self.memory: dict[str, str] = {}

    def demo_mode(self) -> bool:
        if os.getenv("SUPPORT_DEMO_MODE", "0") == "1":
            return True
        key = os.getenv("GROQ_API_KEY", "").strip()
        return not key or key == "your-groq-api-key-here"

    def _extract_order(self, text: str) -> None:
        import re

        m = re.search(r"#?\d{4,}", text)
        if m and ("order" in text.lower() or text.strip().startswith("#") or "it's" in text.lower() or "its" in text.lower()):
            self.memory["order_id"] = m.group(0) if m.group(0).startswith("#") else f"#{m.group(0)}"

    def _demo_reply(self, user_message: str) -> str:
        self._extract_order(user_message)
        lower = user_message.lower()
        if "escalate" in lower:
            return (
                "I've flagged this for a human specialist. Please reply with your account email "
                "and a short summary — they'll follow up during support hours."
            )
        for item in FAQ:
            if any(k in lower for k in item["keywords"]):
                extra = ""
                if self.memory.get("order_id") and item["id"] == "shipping":
                    extra = f" I still have your order {self.memory['order_id']} on file for this chat."
                return item["answer"] + extra
        if self.memory.get("order_id") and any(w in lower for w in ("status", "where", "update")):
            return (
                f"For order {self.memory['order_id']}, typical transit is 3–5 business days. "
                "If it has been longer, reply with 'escalate' and your email."
            )
        return (
            "I can help with shipping, returns, billing, password resets, and support hours. "
            "Ask about one of those, or share an order number like #12345."
        )

    def ask(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": user_message})
        if self.demo_mode():
            reply = self._demo_reply(user_message)
        else:
            self._extract_order(user_message)
            payload = {
                "model": MODEL,
                "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + self.history,
                "temperature": 0.7,
                "max_tokens": 500,
            }
            headers = {
                "Authorization": f"Bearer {os.getenv('GROQ_API_KEY', '').strip()}",
                "Content-Type": "application/json",
            }
            try:
                response = requests.post(
                    GROQ_API_URL, headers=headers, json=payload, timeout=60
                )
                response.raise_for_status()
                reply = response.json()["choices"][0]["message"]["content"]
            except requests.exceptions.RequestException as error:
                reply = f"Connection error: {error}"
            except (KeyError, IndexError):
                reply = "Unexpected response from the API. Please try again."

        self.history.append({"role": "assistant", "content": reply})
        return reply

    def save_log(self, directory: Path | None = None) -> Path:
        directory = directory or Path.cwd()
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = directory / f"chat_log_{stamp}.json"
        path.write_text(
            json.dumps({"memory": self.memory, "history": self.history}, indent=2),
            encoding="utf-8",
        )
        return path

    def reset(self) -> None:
        self.history.clear()
        self.memory.clear()

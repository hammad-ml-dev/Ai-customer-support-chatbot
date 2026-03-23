# AI Customer Support Chatbot

A simple but functional AI chatbot built with Python and Groq's free LLM API.
It remembers the conversation history, so replies feel natural and connected.

## What it does

- Answers customer support questions using an LLM (Llama 3)
- Remembers previous messages in the conversation
- Saves the full chat log to a JSON file on request
- Runs fully in the terminal — no web server needed

## How to run it

**Step 1 — Install the only dependency:**
```bash
pip install requests
```

**Step 2 — Get a free Groq API key:**
Go to https://console.groq.com and sign up (free, no credit card needed)

**Step 3 — Add your key:**
```bash
export GROQ_API_KEY="your-key-here"
```

**Step 4 — Run it:**
```bash
python chatbot.py
```

## Example conversation

```
You: My order hasn't arrived yet
Bot: I'm sorry to hear that. Can you share your order number?

You: It's #12345
Bot: Thank you. Orders typically take 3-5 business days...

You: save
Chat saved to chat_log_20250823_142301.json
```

## Skills demonstrated

- Python functions and loops
- Working with REST APIs using `requests`
- Handling JSON data
- Managing conversation state (memory)
- Error handling with try/except
- LLM integration (Groq / Llama 3)

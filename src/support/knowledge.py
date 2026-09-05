"""FAQ knowledge for demo / grounding."""

FAQ = [
    {
        "id": "shipping",
        "keywords": ["ship", "delivery", "arrive", "tracking", "order"],
        "answer": (
            "Orders typically arrive in 3–5 business days within the UAE and 7–12 days internationally. "
            "Share your order number (e.g. #12345) and I can explain the next status check steps."
        ),
    },
    {
        "id": "returns",
        "keywords": ["return", "refund", "exchange"],
        "answer": (
            "You can return unused items within 30 days of delivery. Start a return from your account → Orders → Return. "
            "Refunds post to the original payment method in 5–7 business days after we receive the item."
        ),
    },
    {
        "id": "password",
        "keywords": ["password", "login", "reset", "account"],
        "answer": (
            "Use Forgot password on the sign-in page. We'll email a reset link that expires in 30 minutes. "
            "If you don't see it, check spam or ask me to walk through verifying your email."
        ),
    },
    {
        "id": "billing",
        "keywords": ["bill", "charge", "invoice", "payment", "card"],
        "answer": (
            "Billing invoices are under Account → Billing. Failed charges are usually an expired card or bank decline — "
            "update the card and retry, or tell me the last four digits and approx. charge date for troubleshooting tips."
        ),
    },
    {
        "id": "hours",
        "keywords": ["hour", "support", "open", "contact", "human"],
        "answer": (
            "Human support is available Sun–Thu, 9:00–18:00 GST. For urgent outages, reply with 'escalate' and your account email."
        ),
    },
]

SYSTEM_PROMPT = """
You are a helpful customer support assistant for NovaGear, a fictional consumer electronics brand.
Help with products, orders, shipping, returns, billing, and account access.
Keep answers short, clear, and friendly. If you don't know something, say so honestly.
When the user shares an order number, acknowledge it and keep it in mind for follow-ups.
"""

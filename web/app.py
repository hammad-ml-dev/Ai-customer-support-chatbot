"""Flask UI for the support chatbot."""

from __future__ import annotations

import sys
from pathlib import Path

from flask import Flask, jsonify, render_template_string, request, session

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from support.bot import SupportBot

app = Flask(__name__)
app.secret_key = "portfolio-demo-not-for-production"
bots: dict[str, SupportBot] = {}

PAGE = """
<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>AI Customer Support Chatbot</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&family=Fraunces:opsz,wght@9..144,700&display=swap" rel="stylesheet"/>
<style>
:root{--bg:#10151c;--text:#eef3fa;--muted:#9aabbf;--accent:#f0a05a;--panel:#1a2330}
*{box-sizing:border-box}body{margin:0;font-family:DM Sans,system-ui;color:var(--text);min-height:100vh;
background:radial-gradient(700px 400px at 100% 0%,rgba(240,160,90,.16),transparent),var(--bg)}
.wrap{max-width:640px;margin:0 auto;padding:36px 18px}h1{font-family:Fraunces,serif;margin:0 0 6px}
.lead{color:var(--muted)}.badge{display:inline-block;margin:12px 0;padding:4px 10px;border-radius:999px;background:var(--accent);color:#10151c;font-size:12px;font-weight:700}
#log{background:var(--panel);border:1px solid rgba(255,255,255,.08);border-radius:16px;min-height:320px;padding:16px;overflow:auto}
.msg{margin:10px 0;padding:10px 12px;border-radius:12px;max-width:85%;line-height:1.45;font-size:14px}
.user{background:rgba(240,160,90,.18);margin-left:auto}.bot{background:rgba(255,255,255,.05)}
.row{display:flex;gap:8px;margin-top:12px}input{flex:1;padding:12px;border-radius:10px;border:1px solid rgba(255,255,255,.14);background:#121a24;color:var(--text);font:inherit}
button{padding:12px 16px;border:0;border-radius:10px;background:var(--accent);color:#10151c;font-weight:700;cursor:pointer}
</style></head><body><div class="wrap">
<h1>NovaGear Support</h1>
<p class="lead">Customer support chatbot with conversation memory. Demo mode uses FAQ grounding — no API key required.</p>
<span class="badge">{{ mode }}</span>
<div id="log"></div>
<div class="row"><input id="q" placeholder="My order hasn't arrived yet…"/><button id="send">Send</button></div>
</div>
<script>
const log=document.getElementById('log');
const add=(who,text)=>{const d=document.createElement('div');d.className='msg '+who;d.textContent=text;log.appendChild(d);log.scrollTop=log.scrollHeight;};
document.getElementById('send').onclick=async()=>{
  const q=document.getElementById('q').value.trim(); if(!q) return;
  document.getElementById('q').value=''; add('user',q);
  const res=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:q})});
  const data=await res.json(); add('bot', data.reply);
};
</script></div></body></html>
"""


def get_bot() -> SupportBot:
    sid = session.get("sid")
    if not sid:
        import uuid

        sid = str(uuid.uuid4())
        session["sid"] = sid
    if sid not in bots:
        bots[sid] = SupportBot()
    return bots[sid]


@app.get("/")
def home():
    bot = get_bot()
    mode = "DEMO" if bot.demo_mode() else "LIVE (Groq)"
    return render_template_string(PAGE, mode=mode)


@app.post("/api/chat")
def api_chat():
    bot = get_bot()
    body = request.get_json(force=True)
    reply = bot.ask(body.get("message", ""))
    return jsonify({"reply": reply, "memory": bot.memory})


def main():
    print("Open http://127.0.0.1:5056")
    app.run(host="127.0.0.1", port=5056, debug=False)


if __name__ == "__main__":
    main()

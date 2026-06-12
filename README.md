# 🤖 CLI Chatbot with Context (Gemini)

> A terminal-based conversational AI chatbot powered by Google Gemini that maintains full conversation context with smart history truncation.

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![Gemini](https://img.shields.io/badge/Google-Gemini_API-orange?logo=google)
![Day](https://img.shields.io/badge/Day-01%2F30-purple)

---

## 📸 Demo

```
╔══════════════════════════════════╗
║      CLI Chatbot (Gemini) 🤖     ║
╚══════════════════════════════════╝
Model : gemini-3.5-flash
Commands: exit · clear · stats

You: Hii what's my name
Assistant: Hi there! Since we just started our conversation, I don't know your name yet. What would you like me to call you?

You: My name is Parth
Assistant: Nice to meet you, Parth! How can I help you today?
```

---

## 🧠 What Problem Does This Solve?

Most beginners who call an LLM API send only the **latest message** — so the model has no memory of what was said before. Every reply feels disconnected, and the assistant can't reference anything from earlier in the conversation.

This project solves that by **maintaining a running conversation history** and sending it with every API call — exactly how ChatGPT and similar products work under the hood. It also solves the **context window overflow problem**: if a long conversation exceeds the model's token budget, the chatbot intelligently trims the oldest messages instead of crashing.

---

## 🎯 Purpose & Goals

- Understand how **multi-turn conversation** works with LLM APIs
- Learn to manage **context windows** — the limited memory LLMs have
- Build a **production-style CLI tool** with error handling and user commands
- Explore the Google Gemini API (`google-genai` SDK) and its `types.Content` message format
- Write clean, modular Python with separated concerns (`chatbot.py`, `config.py`, `history_manager.py`)

---

## ✨ Features

| Feature | Details |
|---|---|
| 💬 Multi-turn memory | Full conversation history sent with every request |
| ✂️ Smart truncation | Oldest messages dropped first when history exceeds `MAX_HIST_CHARS` |
| 🚫 Orphan guard | Never starts history with a model turn (Gemini rejects it) |
| 📊 Stats command | Shows message count, estimated chars and tokens live |
| 🗑️ Clear command | Wipes history to start a fresh conversation |
| 🎨 Colour output | ANSI-coloured terminal UI (cyan, green, yellow, red) |
| ⚠️ Smart errors | Distinct messages for auth errors, rate limits, and safety blocks |
| 🔐 Env-based config | API key loaded from `.env`, never hardcoded |

---

## 🗂️ Project Structure

```
01_Context_CLI_Chatbot/
├── chatbot.py          # Main loop, UI, input handling
├── config.py           # API key, model name, and constants
├── history_manager.py  # Truncation logic and token stats
├── requirements.txt    # Dependencies
└── .env                # Your API key (never commit this!)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- A [Google AI Studio](https://aistudio.google.com/) account (free)
- Your `GOOGLE_API_KEY`

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/30_Days_AI_Apps_Challenge.git
cd 30_Days_AI_Apps_Challenge/01_Context_CLI_Chatbot

# 2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install google-generativeai python-dotenv

# 4. Create your .env file
echo GOOGLE_API_KEY=your_key_here > .env

# 5. Run the chatbot
python chatbot.py
```

### Available Commands (in chat)

| Command | Action |
|---|---|
| `exit` / `quit` | End the session |
| `clear` | Wipe conversation history |
| `stats` | Show message count and estimated token usage |

---

## ⚙️ Configuration

Edit `config.py` to customise the chatbot:

```python
MODEL          = "gemini-3.5-flash"   # Gemini model to use
MAX_TOKENS     = 1024                 # Max tokens per response
MAX_HIST_CHARS = 24000                # Context window budget (~6k tokens)
SYSTEM_PROMPT  = "You are a helpful, concise assistant..."
```

---

## 🧩 How Context Management Works

```
Each turn, history looks like:
[user_msg_1, model_msg_1, user_msg_2, model_msg_2, ..., current_user_msg]

When total chars > MAX_HIST_CHARS:
  → Drop oldest messages from the front
  → Always keep the current user message (last item)
  → Remove any leading model message (Gemini API requirement)
```

This is a simplified version of what production chatbot services do — a sliding window over the conversation.

---

## 📚 What I Learned

- **How LLM APIs handle multi-turn conversations** — the model has no built-in memory; you reconstruct the conversation from scratch on every call.
- **Context window management** — every token costs money and has a hard limit. Blindly appending messages will eventually crash your app.
- **Google Gemini SDK (`google-genai`)** — the new `genai.Client()` style, `types.Content`, `types.Part`, and `GenerateContentConfig`.
- **Modular Python design** — separating config, business logic, and UI into distinct files makes the code much easier to extend.
- **ANSI escape codes** — how to add colour and bold formatting to terminal output without any third-party library.
- **Error handling in production** — distinguishing between auth errors, rate limits, and safety blocks instead of showing a generic traceback.

---

## ⚖️ Tradeoffs & Limitations

| Decision | Tradeoff |
|---|---|
| **Char-based truncation** | Simple and fast, but not perfectly aligned with actual token counts (1 token ≈ 4 chars is a rough estimate) |
| **Drop-oldest strategy** | Easy to implement, but can lose important early context (e.g., the user's name introduced at the start) |
| **In-memory history** | No persistence — closing the terminal wipes the conversation. A SQLite/JSON file could fix this. |
| **No streaming** | Replies appear all at once. The Gemini SDK supports streaming; adding it would feel more responsive. |
| **Single system prompt** | The persona is fixed in `config.py`. A proper app would let users set this dynamically. |
| **CLI only** | Not shareable with non-technical users. A simple Flask/FastAPI web wrapper would fix this. |

---

## 🔮 Possible Extensions

- [ ] Save/load conversation history to a JSON file
- [ ] Add streaming responses (`generate_content_stream`)
- [ ] Let users set a custom system prompt at startup
- [ ] Wrap in a minimal Flask UI for browser access
- [ ] Add a `/summarize` command that condenses old history instead of dropping it
- [ ] Support multiple chat sessions / named conversations

---

## 🛠️ Tech Stack

- **Python 3.12**
- **Google Gemini API** via `google-generativeai`
- **python-dotenv** for environment variable management

---


## 🙌 Acknowledgements

Built as part of my personal challenge: **30 Days AI Apps Challenge** — 15 AI-powered projects in 30 days.


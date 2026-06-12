# history_manager.py
"""
Truncation strategy:
  - Walk backwards through history keeping the most recent messages
  - Always keep the latest user message
  - Drop oldest messages first when budget is exceeded
  - Never leave an orphaned assistant message at the start
"""


def estimate_chars(message: dict) -> int:
    """Rough size estimate for a message dict."""
    return len(message.get("parts", [""])[0]) + 10   # +10 role overhead


def truncate_history(history: list, max_chars: int) -> list:
    """
    Return a trimmed copy of history that fits within max_chars.
    history format: [{"role": "user"|"model", "parts": ["text"]}, ...]
    """
    if not history:
        return []

    # Always keep the last message (current user input)
    last  = history[-1]
    rest  = history[:-1]
    used  = estimate_chars(last)
    kept  = []

    for msg in reversed(rest):
        cost = estimate_chars(msg)
        if used + cost <= max_chars:
            kept.insert(0, msg)
            used += cost
        else:
            break   # oldest messages dropped first

    # Never start with a model (assistant) turn — Gemini rejects it
    while kept and kept[0]["role"] == "model":
        kept.pop(0)

    kept.append(last)
    return kept


def get_stats(history: list) -> dict:
    total_chars = sum(estimate_chars(m) for m in history)
    return {
        "messages" : len(history),
        "est_chars": total_chars,
        "est_tokens": total_chars // 4,
    }
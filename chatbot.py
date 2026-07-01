# chatbot.py
import sys
import os
from google import genai
from google.genai import types
from config import API_KEY, MODEL, MAX_TOKENS, MAX_HIST_CHARS, SYSTEM_PROMPT
from history_manager import truncate_history, get_stats

# ── Terminal colours ──────────────────────────────────────────────────────────
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

def validate():
    if not API_KEY:
        print(f"{RED}Error: GOOGLE_API_KEY not found in .env{RESET}")
        print("Make sure your .env file contains: GOOGLE_API_KEY=AIza-your-key-here")
        sys.exit(1)


def send_message(client, history: list) -> str:
    """Truncate history and send to Gemini API."""
    trimmed  = truncate_history(history, MAX_HIST_CHARS)

    # Build contents list for the new SDK format
    contents = []
    for msg in trimmed:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part(text=msg["parts"][0])]
            )
        )

    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=MAX_TOKENS,
        ),
    )
    return response.text


def print_banner():
    print(f"\n{BOLD}{CYAN}╔══════════════════════════════════╗{RESET}")
    print(f"{BOLD}{CYAN}║      CLI Chatbot (Gemini) 🤖     ║{RESET}")
    print(f"{BOLD}{CYAN}╚══════════════════════════════════╝{RESET}")
    print(f"{DIM}Model : {MODEL}{RESET}")
    print(f"{DIM}Commands: exit · clear · stats{RESET}\n")


def print_stats(history):
    s = get_stats(history)
    print(
        f"\n{YELLOW}📊 {s['messages']} messages · "
        f"~{s['est_tokens']} tokens · "
        f"{s['est_chars']} chars{RESET}\n"
    )


def main():
    validate()
    client  = genai.Client(api_key=API_KEY)
    history = []

    print_banner()

    while True:
        try:
            user_input = input(f"{GREEN}You:{RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}Goodbye!{RESET}")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print(f"{DIM}Goodbye!{RESET}")
            break

        if user_input.lower() == "clear":
            history = []
            print(f"{YELLOW}🗑  History cleared.{RESET}\n")
            continue

        if user_input.lower() == "stats":
            print_stats(history)
            continue

        # ── Send message ──────────────────────────────────────────────────
        history.append({"role": "user", "parts": [user_input]})

        try:
            print(f"{CYAN}Assistant:{RESET} ", end="", flush=True)
            reply = send_message(client, history)
            print(reply)
            print()
            history.append({"role": "model", "parts": [reply]})

        except Exception as e:
            error = str(e)
            if "API_KEY" in error or "credentials" in error.lower():
                print(f"{RED}Invalid API key. Check your .env file.{RESET}")
            elif "429" in error or "quota" in error.lower():
                print(f"{RED}Rate limit hit. Wait a moment and try again.{RESET}")
            elif "safety" in error.lower():
                print(f"{YELLOW}Response blocked by safety filter. Try rephrasing.{RESET}")
            else:
                print(f"{RED}Error: {error}{RESET}")
            history.pop()


if __name__ == "__main__":
    main()
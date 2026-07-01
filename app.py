import streamlit as st
from google import genai
from google.genai import types
from config import MODEL, MAX_TOKENS, MAX_HIST_CHARS, SYSTEM_PROMPT
from history_manager import truncate_history
import os

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

st.title("🤖 CLI Chatbot (Gemini)")

if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    role = "user" if msg["role"] == "user" else "assistant"
    st.chat_message(role).write(msg["parts"][0])

if prompt := st.chat_input("Type a message..."):
    st.session_state.history.append({"role": "user", "parts": [prompt]})
    st.chat_message("user").write(prompt)

    trimmed = truncate_history(st.session_state.history, MAX_HIST_CHARS)
    contents = [
        types.Content(role="user" if m["role"]=="user" else "model",
                      parts=[types.Part(text=m["parts"][0])])
        for m in trimmed
    ]
    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=MAX_TOKENS,
        ),
    )
    reply = response.text
    st.session_state.history.append({"role": "model", "parts": [reply]})
    st.chat_message("assistant").write(reply)
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY        = os.getenv("GOOGLE_API_KEY")
MODEL          = "gemini-3.5-flash"
MAX_TOKENS     = 1024
MAX_HIST_CHARS = 24000
SYSTEM_PROMPT  = (
    "You are a helpful, concise assistant. "
    "You maintain context across the conversation and give clear answers."
)


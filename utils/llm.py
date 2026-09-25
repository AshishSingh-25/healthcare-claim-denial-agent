"""
utils/llm.py

Loads environment variables and creates the LLM client used
throughout the app. Uses Groq as the inference provider (switched
from OpenAI after hitting a 429 insufficient_quota error).
"""

import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set. Add it to your .env file, e.g.:\n"
        "GROQ_API_KEY=your_key_here"
    )

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0.2,
)

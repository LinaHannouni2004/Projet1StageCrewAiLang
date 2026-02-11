import os
from crewai import LLM

def build_llm():
    api_key = os.getenv("GEMINI_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_KEY is missing. Set it in your environment variables.")
    return LLM(
        model="google/gemini-2.5-flash",
        api_key=api_key
    )

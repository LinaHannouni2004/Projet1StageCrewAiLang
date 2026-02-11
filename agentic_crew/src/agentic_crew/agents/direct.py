import os
import requests

GEMINI_API_KEY = os.getenv("GEMINI_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


class DirectAgent:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found")

    def run(self, query: str) -> str:
        prompt = f"""
You are an intelligent AI assistant.

Answer the following question clearly and accurately.
If the question is technical, provide a structured explanation.
If the question is simple, answer concisely.

User question:
{query}
"""

        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {"parts": [{"text": prompt}]}
                ]
            },
            timeout=30
        )

        if response.status_code != 200:
            return "Error contacting Gemini."

        return response.json()["candidates"][0]["content"]["parts"][0]["text"]

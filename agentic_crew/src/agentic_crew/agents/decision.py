import os
import requests
import json

GEMINI_API_KEY = os.getenv("GEMINI_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


class DecisionAgent:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment")

    def analyze_query_with_llm(self, query: str) -> dict:
        prompt = f"""
You are an AI Decision Agent for a multi-agent system.

Your job is to analyze the user query and decide the best reasoning strategy:

RAG → if the question relates to internal documents, PDF, reports, or files.
RESEARCH → if the question requires external, recent, or web-based information.
DIRECT → if the question is general knowledge or explanation.

Return STRICT JSON format:
{{
  "decision": "RAG | RESEARCH | DIRECT",
  "reason": "short explanation",
  "confidence": 0-1
}}

User query:
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
            timeout=30,
        )

        if response.status_code != 200:
            raise Exception(f"Gemini API error: {response.text}")

        text = response.json()["candidates"][0]["content"]["parts"][0]["text"]

        # Extraire JSON
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            decision_json = json.loads(text[start:end])
            return decision_json
        except Exception:
            return {
                "decision": "DIRECT",
                "reason": "Fallback due to parsing error",
                "confidence": 0.5
            }

    def run(self, query: str) -> dict:
        result = self.analyze_query_with_llm(query)
        return result

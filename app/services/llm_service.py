import requests
import os


class LLMService:   

    @staticmethod
    def get_llm_response(message: str, context: str) -> str | None:
        try:
            print("🚀 GEMINI CALLED:", message)

            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"

            api_key = os.getenv("GEMINI_API_KEY")

            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"""
You are AP RERA Assistant.

STRICT RULES:
- Answer ONLY from CONTEXT
- Do NOT guess
- Do NOT hallucinate

CONTEXT:
{context}

USER QUESTION:
{message}

ANSWER:
"""
                            }
                        ]
                    }
                ]
            }

            response = requests.post(
                url,
                headers={
                    "Content-Type": "application/json",
                    "X-goog-api-key": api_key
                },
                json=payload,
                timeout=60
            )

            print("🔥 STATUS:", response.status_code)
            print("🔥 RAW:", response.text)

            data = response.json()

            # ✅ correct parsing
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()

        except Exception as e:
            print("❌ GEMINI ERROR:", e)
            return None
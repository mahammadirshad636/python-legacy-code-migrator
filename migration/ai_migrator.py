import requests
from config import LM_STUDIO_URL, LM_MODEL, MAX_TOKENS

def migrate_with_ai(code):
    payload = {
        "model": LM_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a senior software architect modernizing legacy Python code."
            },
            {
                "role": "user",
                "content": f"""
Migrate the following legacy Python code to modern Python:
- Use dataclasses
- Type hints
- Remove unsafe patterns
- Improve readability

CODE:
{code}
"""
            }
        ],
        "max_tokens": MAX_TOKENS,
        "temperature": 0.2
    }

    response = requests.post(LM_STUDIO_URL, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

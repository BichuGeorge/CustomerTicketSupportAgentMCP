import os
import requests
from dotenv import load_dotenv
load_dotenv()
import sys
sys.stdout.reconfigure(encoding='utf-8')

EURI_API_URL = "https://api.euron.one/api/v1/euri/alpha/chat/completions"
EURI_API_KEY = os.getenv("EURI_API_KEY")

def generate_reply(text):
    prompt = f"""
You are a friendly and professional customer support agent.print

Respond to the following issue with empathy, clear explanation, and helpful advice.

Issue:
\"\"\"{text}\"\"\"

Only return the final response message.
"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {EURI_API_KEY}"
    }
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": "gpt-4.1-nano",
        "max_tokens": 500,
        "temperature": 0.5
    }
    try:
        response = requests.post(EURI_API_URL, headers=headers, json=payload)
        result = response.json()  # Raise an error for bad responses
        print(f"Euri Raw Response: {result}")
        content = result["choices"][0]["message"]["content"]
        return content.strip()
    except Exception as e:
        print(f"Error generating reply: {e}")
        return "We are currently experiencing high demand. Please try again later or contact support directly."

import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()
import sys
sys.stdout.reconfigure(encoding='utf-8')

EURI_API_URL = "https://api.euron.one/api/v1/euri/alpha/chat/completions"
EURI_API_KEY = os.getenv("EURI_API_KEY")

def classify_ticket(text):
    prompt = f"""
You are a smar support ticket classifier.

Given a customer ticket, classify it into:
- Sentiment: Positive, Negative, Neutral
- Issue Type: Billing, Technical, General, Other

Respond ONLY with a JSON object like this:
{{
    "Sentiment": "Negative",
    "IssueType": "Billing"
}}

Customer Ticket:
\"\"\"{text}\"\"\"
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
        "temperature": 0.3
    }
    try:
        response = requests.post(EURI_API_URL, headers=headers, json=payload)
        result = response.json()  # Raise an error for bad responses
        print(f"Euri Raw Response: {result}")
        content = result["choices"][0]["message"]["content"]

        parsed = json.loads(content)
        return {
            "sentiment": parsed.get("Sentiment", "Unknown"),
            "issue_type": parsed.get("IssueType", "General")
        }
    except Exception as e:
        print(f"Error classifying ticket: {e}")
        return {
            "sentiment": "Unknown",
            "issue_type": "General"
        }
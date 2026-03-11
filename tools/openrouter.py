"""
tools/openrouter.py — AI lead qualification via OpenRouter (MiniMax)
"""

import json
import sys
import os
import http.client
from urllib.parse import urlparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_ENDPOINT,
    OPENROUTER_MODEL,
    OPENROUTER_MAX_TOKENS,
    OPENROUTER_TEMPERATURE,
    LEAD_QUALIFY_PROMPT,
)


def chat(messages: list[dict], system_prompt: str = None) -> str:
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "YOUR_OPENROUTER_API_KEY":
        raise RuntimeError(
            "OpenRouter API key not set. Open config.py and replace "
            "YOUR_OPENROUTER_API_KEY with your real key from https://openrouter.ai"
        )

    parsed = urlparse(OPENROUTER_ENDPOINT)

    try:
        conn = http.client.HTTPSConnection(parsed.netloc, timeout=30)
    except Exception:
        raise RuntimeError(
            "Could not connect to OpenRouter. Check your internet connection."
        )

    full_messages = []
    if system_prompt:
        full_messages.append({"role": "system", "content": system_prompt})
    full_messages.extend(messages)

    payload = json.dumps({
        "model":       OPENROUTER_MODEL,
        "messages":    full_messages,
        "max_tokens":  OPENROUTER_MAX_TOKENS,
        "temperature": OPENROUTER_TEMPERATURE,
    })

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type":  "application/json",
    }

    try:
        conn.request("POST", parsed.path, payload, headers)
        response = conn.getresponse()
        raw      = response.read().decode("utf-8")
        conn.close()
    except Exception as e:
        raise RuntimeError(
            f"Could not reach OpenRouter. Check your internet connection. ({e})"
        )

    if response.status == 401 or response.status == 403:
        raise RuntimeError(
            "OpenRouter API key is invalid. Double-check your key in config.py. "
            "Get a key at https://openrouter.ai"
        )

    if response.status != 200:
        raise RuntimeError(f"OpenRouter returned error {response.status}: {raw}")

    data = json.loads(raw)

    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise RuntimeError(
            f"Unexpected response from OpenRouter. The model may be unavailable. "
            f"Response: {raw[:300]}"
        )


def qualify_lead(lead: dict) -> str:
    lead_text = (
        f"Business: {lead.get('title', 'Unknown')}\n"
        f"URL:      {lead.get('link', 'N/A')}\n"
        f"Snippet:  {lead.get('snippet', 'No description.')}\n"
        f"Query:    {lead.get('source_query', 'N/A')}"
    )
    return chat([{"role": "user", "content": LEAD_QUALIFY_PROMPT.format(lead_data=lead_text)}])


def qualify_leads_batch(leads: list[dict]) -> list[dict]:
    for i, lead in enumerate(leads, 1):
        print(f"  Qualifying {i}/{len(leads)}: {lead['title']}")
        try:
            lead["ai_summary"] = qualify_lead(lead)
        except RuntimeError as e:
            print(f"  [!] Failed: {e}")
            lead["ai_summary"] = "Error: could not qualify this lead."
    return leads
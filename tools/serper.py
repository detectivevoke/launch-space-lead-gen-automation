"""
tools/serper.py — Google Search via Serper API
"""

import json
import sys
import os
import http.client
from urllib.parse import urlparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import SERPER_API_KEY, SERPER_ENDPOINT, SERPER_NUM_RESULTS, SERPER_COUNTRY, SERPER_LANGUAGE


def search(query: str, num_results: int = None) -> dict:
    if not SERPER_API_KEY or SERPER_API_KEY == "YOUR_SERPER_API_KEY":
        raise RuntimeError(
            "Serper API key not set. Open config.py and replace YOUR_SERPER_API_KEY "
            "with your real key from https://serper.dev"
        )

    parsed = urlparse(SERPER_ENDPOINT)

    try:
        conn = http.client.HTTPSConnection(parsed.netloc, timeout=15)
    except Exception:
        raise RuntimeError(
            "Could not connect to Serper. Check your internet connection."
        )

    payload = json.dumps({
        "q":   query,
        "num": num_results or SERPER_NUM_RESULTS,
        "gl":  SERPER_COUNTRY,
        "hl":  SERPER_LANGUAGE,
    })

    headers = {
        "X-API-KEY":    SERPER_API_KEY,
        "Content-Type": "application/json",
    }

    try:
        conn.request("POST", parsed.path, payload, headers)
        response = conn.getresponse()
        raw      = response.read().decode("utf-8")
        conn.close()
    except Exception as e:
        raise RuntimeError(
            f"Could not reach Serper. Check your internet connection. ({e})"
        )

    if response.status == 401 or response.status == 403:
        raise RuntimeError(
            "Serper API key is invalid. Double-check your key in config.py. "
            "Get a key at https://serper.dev"
        )

    if response.status != 200:
        raise RuntimeError(f"Serper returned error {response.status}: {raw}")

    return json.loads(raw)


def extract_organic(results: dict) -> list[dict]:
    return [
        {
            "title":   item.get("title", ""),
            "link":    item.get("link", ""),
            "snippet": item.get("snippet", ""),
        }
        for item in results.get("organic", [])
    ]


def search_leads(queries: list[str]) -> list[dict]:
    seen      = set()
    all_leads = []

    for query in queries:
        print(f"  Searching: {query}")
        try:
            results = search(query)
            for lead in extract_organic(results):
                if lead["link"] not in seen:
                    seen.add(lead["link"])
                    lead["source_query"] = query
                    all_leads.append(lead)
        except RuntimeError as e:
            print(f"  [!] Error: {e}")

    print(f"\n  {len(all_leads)} unique results found")
    return all_leads
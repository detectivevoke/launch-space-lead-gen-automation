"""
scripts/find_poc.py — Find the Point of Contact for a company
Uses Companies House officers API (real directors) + Google search.
Edit POC_COMPANIES in config.py
Run: python scripts/find_poc.py
"""

import sys
import os
import json
import http.client
import base64
from urllib.parse import quote

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import POC_COMPANIES, CH_API_KEY
from tools.serper import search, extract_organic
from tools.companies_house import get_officers

GOOGLE_QUERIES = [
    "{company} owner",
    "{company} director",
    "{company} founder LinkedIn",
    "{company} contact",
]


def _ch_find_company_number(company_name):
    """Search Companies House by name and return the first match's number."""
    if not CH_API_KEY or CH_API_KEY == "YOUR_CH_API_KEY":
        return None

    conn = http.client.HTTPSConnection("api.company-information.service.gov.uk", timeout=15)
    token = base64.b64encode(f"{CH_API_KEY}:".encode()).decode()

    try:
        conn.request(
            "GET",
            f"/search/companies?q={quote(company_name)}&items_per_page=3",
            headers={"Authorization": f"Basic {token}"},
        )
        resp = conn.getresponse()
        raw = resp.read().decode("utf-8")
        conn.close()

        if resp.status != 200:
            return None

        items = json.loads(raw).get("items", [])
        if items:
            top = items[0]
            return top.get("company_number"), top.get("title", company_name)
    except Exception:
        pass
    return None


def find_poc(company):
    print(f"\n  Looking up: {company}")
    print("  " + "-" * 40)

    has_ch = CH_API_KEY and CH_API_KEY != "YOUR_CH_API_KEY"

    # ── Companies House: find real directors ────────────────────
    if has_ch:
        print(f"  [CH] Searching for registered company...")
        try:
            result = _ch_find_company_number(company)
            if result:
                number, matched_name = result
                print(f"  [CH] Found: {matched_name} (#{number})")
                officers = get_officers(number)
                if officers:
                    print(f"  [CH] Directors/officers:")
                    for o in officers:
                        print(f"       {o['name']} — {o['role']} (since {o['appointed']})")
                else:
                    print(f"  [CH] No active officers found")
            else:
                print(f"  [CH] No match on Companies House")
        except Exception as e:
            print(f"  [!] Companies House lookup failed: {e}")

    # ── Google: supplementary search ────────────────────────────
    print(f"  [Google] Searching for contact info...")

    seen    = set()
    results = []

    for template in GOOGLE_QUERIES:
        query = template.format(company=company)
        try:
            for lead in extract_organic(search(query, num_results=5)):
                if lead["link"] not in seen:
                    seen.add(lead["link"])
                    results.append(lead)
        except Exception as e:
            print(f"  [!] Search failed for '{query}': {e}")
            continue

    if results:
        print(f"  [Google] Top results:")
        for r in results[:6]:
            print(f"       {r['title']}")
            print(f"       {r['link']}")
            print(f"       {r['snippet']}\n")
    else:
        print(f"  [Google] No results found.")


def find_all_pocs():
    print(f"Looking up {len(POC_COMPANIES)} companies...\n")
    print("=" * 55)

    for company in POC_COMPANIES:
        find_poc(company)

    print("\nDone.")


if __name__ == "__main__":
    try:
        find_all_pocs()
    except KeyboardInterrupt:
        print("\n\nStopped by user.")
    except Exception as e:
        print(f"\n[!] Something went wrong: {e}")
        print("    Check your config.py settings and internet connection.")

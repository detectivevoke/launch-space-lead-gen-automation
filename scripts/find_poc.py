"""
scripts/find_poc.py — Find the Point of Contact for a company
Edit POC_COMPANIES in config.py
Run: python scripts/find_poc.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import POC_COMPANIES
from tools.serper import search, extract_organic

POC_QUERIES = [
    "{company} owner",
    "{company} director",
    "{company} founder LinkedIn",
    "{company} contact",
]


def find_poc(company: str):
    print(f"\n  Looking up: {company}")
    print("  " + "-" * 40)

    seen    = set()
    results = []

    for template in POC_QUERIES:
        query = template.format(company=company)
        try:
            for lead in extract_organic(search(query, num_results=5)):
                if lead["link"] not in seen:
                    seen.add(lead["link"])
                    results.append(lead)
        except Exception as e:
            print(f"  [!] Search failed for '{query}': {e}")
            continue

    if not results:
        print("  No results found.")
    else:
        for r in results[:6]:
            print(f"  • {r['title']}")
            print(f"    {r['link']}")
            print(f"    {r['snippet']}\n")


def find_all_pocs():
    print(f"Looking up {len(POC_COMPANIES)} companies...\n")
    print("=" * 55)

    for company in POC_COMPANIES:
        find_poc(company)

    print("\n✓ Done.")


if __name__ == "__main__":
    try:
        find_all_pocs()
    except KeyboardInterrupt:
        print("\n\nStopped by user.")
    except Exception as e:
        print(f"\n[!] Something went wrong: {e}")
        print("    Check your config.py settings and internet connection.")
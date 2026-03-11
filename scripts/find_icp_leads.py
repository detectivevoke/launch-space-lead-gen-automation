"""
scripts/find_icp_leads.py — Find businesses that match your ICP
Edit ICP_INDUSTRIES, ICP_LOCATIONS, ICP_SIGNALS in config.py
Run: python scripts/find_icp_leads.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import ICP_INDUSTRIES, ICP_LOCATIONS, ICP_SIGNALS
from tools.serper import search, extract_organic


def find_icp_leads():
    queries = [
        f"{industry} in {location}"
        for industry in ICP_INDUSTRIES
        for location in ICP_LOCATIONS
    ]

    seen    = set()
    matches = []

    print(f"Running {len(queries)} searches...\n")

    for query in queries:
        print(f"  Searching: {query}")
        try:
            results = search(query)
        except Exception as e:
            print(f"  [!] Search failed: {e}")
            continue

        for lead in extract_organic(results):
            if lead["link"] in seen:
                continue
            seen.add(lead["link"])

            text = (lead["title"] + " " + lead["snippet"]).lower()
            if not ICP_SIGNALS or any(s.lower() in text for s in ICP_SIGNALS):
                lead["source_query"] = query
                matches.append(lead)

    print(f"\n✓ {len(matches)} ICP-matching leads found\n")
    print("=" * 55)

    for i, lead in enumerate(matches, 1):
        print(f"{i}. {lead['title']}")
        print(f"   {lead['link']}")
        print(f"   {lead['snippet']}\n")


if __name__ == "__main__":
    try:
        find_icp_leads()
    except KeyboardInterrupt:
        print("\n\nStopped by user.")
    except Exception as e:
        print(f"\n[!] Something went wrong: {e}")
        print("    Check your config.py settings and internet connection.")
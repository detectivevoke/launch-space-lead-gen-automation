"""
scripts/find_icp_leads.py — Find businesses that match your ICP
Uses Companies House (real registered companies) + Google search.
Edit ICP_INDUSTRIES, ICP_LOCATIONS, ICP_SIGNALS in config.py
Run: python scripts/find_icp_leads.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import ICP_INDUSTRIES, ICP_LOCATIONS, ICP_SIGNALS, CH_API_KEY
from tools.serper import search, extract_organic
from tools.companies_house import find_companies_by_industry


def find_icp_leads():
    seen    = set()
    matches = []

    # ── Companies House search ──────────────────────────────────
    has_ch = CH_API_KEY and CH_API_KEY != "YOUR_CH_API_KEY"

    if has_ch:
        print("Step 1: Searching Companies House...\n")
        for industry in ICP_INDUSTRIES:
            for location in ICP_LOCATIONS:
                try:
                    companies = find_companies_by_industry(industry, location, size=5)
                except Exception as e:
                    print(f"  [!] CH search failed: {e}")
                    continue

                for c in companies:
                    if c["number"] in seen:
                        continue
                    seen.add(c["number"])

                    text = (c["name"] + " " + c["address"]).lower()
                    if not ICP_SIGNALS or any(s.lower() in text for s in ICP_SIGNALS):
                        matches.append({
                            "title":   c["name"],
                            "link":    f"https://find-and-update.company-information.service.gov.uk/company/{c['number']}",
                            "snippet": c["address"],
                            "source":  "Companies House",
                        })

        print(f"\n  {len(matches)} companies from Companies House\n")
    else:
        print("[i] Companies House key not set — using Google only.\n")

    # ── Google search ───────────────────────────────────────────
    print("Step 2: Searching Google...\n")
    queries = [
        f"{industry} in {location}"
        for industry in ICP_INDUSTRIES
        for location in ICP_LOCATIONS
    ]

    google_count = 0
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
                lead["source"] = "Google"
                matches.append(lead)
                google_count += 1

    print(f"\n  {google_count} leads from Google")

    # ── Results ─────────────────────────────────────────────────
    print(f"\n{'=' * 55}")
    print(f"  {len(matches)} total ICP-matching leads")
    print(f"{'=' * 55}\n")

    for i, lead in enumerate(matches, 1):
        source_tag = f" [{lead.get('source', '')}]" if lead.get("source") else ""
        print(f"{i}. {lead['title']}{source_tag}")
        print(f"   {lead['link']}")
        print(f"   {lead.get('snippet', '')}\n")


if __name__ == "__main__":
    try:
        find_icp_leads()
    except KeyboardInterrupt:
        print("\n\nStopped by user.")
    except Exception as e:
        print(f"\n[!] Something went wrong: {e}")
        print("    Check your config.py settings and internet connection.")

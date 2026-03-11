"""
main.py — Full AI lead gen pipeline
  Step 1: Find real companies via Companies House (optional)
  Step 2: Search Google for more leads
  Step 3: Qualify all leads with AI
Edit config.py only. Run: python main.py
"""

import sys

from config import (
    LEAD_SEARCH_QUERIES, SERPER_API_KEY, OPENROUTER_API_KEY, CH_API_KEY,
    ICP_INDUSTRIES, ICP_LOCATIONS,
)
from tools.serper import search_leads
from tools.openrouter import qualify_leads_batch
from tools.companies_house import find_companies_by_industry


def check_keys():
    ok = True
    if not SERPER_API_KEY or SERPER_API_KEY == "YOUR_SERPER_API_KEY":
        print("[!] SERPER_API_KEY is not set.")
        print("    Open config.py and paste your key from https://serper.dev")
        ok = False
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "YOUR_OPENROUTER_API_KEY":
        print("[!] OPENROUTER_API_KEY is not set.")
        print("    Open config.py and paste your key from https://openrouter.ai")
        ok = False
    return ok


def run():
    print("=" * 55)
    print("  LEAD GEN WORKSHOP — AI Pipeline")
    print("=" * 55)

    if not check_keys():
        print("\nFix the above, save config.py, and run this again.")
        sys.exit(1)

    all_leads = []
    step = 1

    # ── Step 1: Companies House (if key is set) ─────────────────
    has_ch = CH_API_KEY and CH_API_KEY != "YOUR_CH_API_KEY"

    if has_ch:
        print(f"\n[{step}/3] Finding real companies via Companies House...\n")
        for industry in ICP_INDUSTRIES:
            for location in ICP_LOCATIONS:
                companies = find_companies_by_industry(industry, location, size=5)
                for c in companies:
                    all_leads.append({
                        "title":        c["name"],
                        "link":         f"https://find-and-update.company-information.service.gov.uk/company/{c['number']}",
                        "snippet":      f"{c['address']} | SIC: {', '.join(c.get('sic_codes', []))}",
                        "source_query": f"Companies House: {industry} in {location}",
                        "company_number": c["number"],
                    })
        print(f"\n  {len(all_leads)} companies found on Companies House")
        step += 1
    else:
        print("\n[i] Companies House key not set — skipping (optional).")
        print("    Add CH_API_KEY in config.py to enable.")

    # ── Step 2: Google search via Serper ────────────────────────
    total_steps = 3 if has_ch else 2
    print(f"\n[{step}/{total_steps}] Searching Google for leads...\n")
    google_leads = search_leads(LEAD_SEARCH_QUERIES)
    step += 1

    # Merge, deduplicating by title similarity
    seen_titles = {lead["title"].lower() for lead in all_leads}
    for lead in google_leads:
        if lead["title"].lower() not in seen_titles:
            seen_titles.add(lead["title"].lower())
            all_leads.append(lead)

    if not all_leads:
        print("[!] No leads found. Check your config.py settings.")
        return

    print(f"\n  {len(all_leads)} total unique leads")

    # ── Step 3: AI qualification ────────────────────────────────
    print(f"\n[{step}/{total_steps}] Qualifying {len(all_leads)} leads with AI...\n")
    qualified = qualify_leads_batch(all_leads)

    # ── Results ─────────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  RESULTS")
    print("=" * 55)

    for lead in qualified:
        source = ""
        if lead.get("company_number"):
            source = " [Companies House]"
        print(f"\n  {lead['title']}{source}")
        print(f"  {lead['link']}")
        print(f"  {lead.get('ai_summary', 'No summary')}")

    print(f"\nDone. {len(qualified)} leads qualified.")


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\n\nStopped by user.")
    except Exception as e:
        print(f"\n[!] Something went wrong: {e}")
        print("    Check your config.py settings and internet connection.")
        sys.exit(1)

"""
main.py — Full AI lead gen pipeline (search → qualify → print)
Edit config.py only. Run: python main.py
"""

import sys

from config import LEAD_SEARCH_QUERIES, SERPER_API_KEY, OPENROUTER_API_KEY
from tools.serper import search_leads
from tools.openrouter import qualify_leads_batch


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

    print("\n[1/2] Searching for leads...\n")
    leads = search_leads(LEAD_SEARCH_QUERIES)

    if not leads:
        print("[!] No leads found. Check your queries in config.py.")
        return

    print(f"\n[2/2] Qualifying {len(leads)} leads with AI...\n")
    qualified = qualify_leads_batch(leads)

    print("\n" + "=" * 55)
    print("  RESULTS")
    print("=" * 55)

    for lead in qualified:
        print(f"\n  {lead['title']}")
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

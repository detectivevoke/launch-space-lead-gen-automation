"""
tools/companies_house.py — UK Companies House API
Free API key: https://developer.company-information.service.gov.uk
"""

import json
import sys
import os
import http.client
import base64

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import CH_API_KEY, CH_API_URL


# SIC codes for common small business types
SIC_CODES = {
    "plumbers":         ["43220"],
    "electricians":     ["43210"],
    "estate agents":    ["68310"],
    "accountants":      ["69201", "69202"],
    "marketing agency": ["73110", "73120"],
    "web design":       ["62012", "62020"],
    "builders":         ["41201", "43390"],
    "cleaners":         ["81210"],
    "hairdressers":     ["96021"],
    "restaurants":      ["56101"],
    "cafes":            ["56102"],
    "gyms":             ["93130"],
    "dentists":         ["86230"],
    "vets":             ["75000"],
    "landscapers":      ["81300"],
    "mechanics":        ["45200"],
}


def _auth_header():
    token = base64.b64encode(f"{CH_API_KEY}:".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def search_companies(sic_code, location, size=10):
    """Search Companies House for active companies by SIC code + location."""
    if not CH_API_KEY or CH_API_KEY == "YOUR_CH_API_KEY":
        raise RuntimeError(
            "Companies House API key not set. Open config.py and replace "
            "YOUR_CH_API_KEY with your key from "
            "https://developer.company-information.service.gov.uk"
        )

    conn = http.client.HTTPSConnection("api.company-information.service.gov.uk", timeout=15)
    path = (
        f"/advanced-search/companies"
        f"?location={location}"
        f"&sic_codes={sic_code}"
        f"&company_status=active"
        f"&size={size}"
    )

    try:
        conn.request("GET", path, headers=_auth_header())
        resp = conn.getresponse()
        raw = resp.read().decode("utf-8")
        conn.close()
    except Exception as e:
        raise RuntimeError(f"Could not reach Companies House API. ({e})")

    if resp.status == 401:
        raise RuntimeError(
            "Companies House API key is invalid. Check config.py. "
            "Get a key at https://developer.company-information.service.gov.uk"
        )

    if resp.status != 200:
        raise RuntimeError(f"Companies House returned {resp.status}: {raw[:200]}")

    return json.loads(raw).get("items", [])


def get_company_profile(company_number):
    """Get full profile for a company by its number."""
    if not CH_API_KEY or CH_API_KEY == "YOUR_CH_API_KEY":
        raise RuntimeError("Companies House API key not set in config.py")

    conn = http.client.HTTPSConnection("api.company-information.service.gov.uk", timeout=15)

    try:
        conn.request("GET", f"/company/{company_number}", headers=_auth_header())
        resp = conn.getresponse()
        raw = resp.read().decode("utf-8")
        conn.close()
    except Exception as e:
        raise RuntimeError(f"Could not reach Companies House API. ({e})")

    if resp.status != 200:
        return None

    return json.loads(raw)


def get_officers(company_number):
    """Get officers (directors, secretaries) for a company."""
    if not CH_API_KEY or CH_API_KEY == "YOUR_CH_API_KEY":
        raise RuntimeError("Companies House API key not set in config.py")

    conn = http.client.HTTPSConnection("api.company-information.service.gov.uk", timeout=15)

    try:
        conn.request("GET", f"/company/{company_number}/officers", headers=_auth_header())
        resp = conn.getresponse()
        raw = resp.read().decode("utf-8")
        conn.close()
    except Exception as e:
        raise RuntimeError(f"Could not reach Companies House API. ({e})")

    if resp.status != 200:
        return []

    data = json.loads(raw)
    officers = []
    for item in data.get("items", []):
        if item.get("resigned_on"):
            continue
        officers.append({
            "name":       item.get("name", ""),
            "role":       item.get("officer_role", ""),
            "appointed":  item.get("appointed_on", ""),
        })
    return officers


def find_companies_by_industry(industry, location, size=10):
    """Find companies by industry name (looks up SIC codes automatically).

    Returns a list of dicts with: name, number, address, sic_codes.
    """
    industry_lower = industry.lower().strip()

    # Find matching SIC codes
    sic_codes = SIC_CODES.get(industry_lower)
    if not sic_codes:
        # Try partial match
        for key, codes in SIC_CODES.items():
            if industry_lower in key or key in industry_lower:
                sic_codes = codes
                break

    if not sic_codes:
        print(f"  [!] No SIC codes mapped for '{industry}'. Using Google search instead.")
        return []

    all_results = []
    seen = set()

    for sic in sic_codes:
        print(f"  [CH] Searching SIC {sic} in {location}...")
        try:
            items = search_companies(sic, location, size=size)
        except Exception as e:
            print(f"  [!] Companies House search failed: {e}")
            continue

        for company in items:
            number = company.get("company_number", "")
            if not number or number in seen:
                continue
            seen.add(number)

            if company.get("company_status") != "active":
                continue

            # Build address
            addr = company.get("registered_office_address", {})
            addr_parts = [
                addr.get("address_line_1", ""),
                addr.get("address_line_2", ""),
                addr.get("locality", ""),
                addr.get("postal_code", ""),
            ]
            address = ", ".join(p for p in addr_parts if p)

            # Check location actually matches
            loc_lower = location.lower().split()[0]
            if loc_lower not in address.lower() and loc_lower not in company.get("company_name", "").lower():
                continue

            name = company.get("company_name", "").strip().title()
            all_results.append({
                "name":      name,
                "number":    number,
                "address":   address,
                "sic_codes": company.get("sic_codes", []),
            })

    return all_results

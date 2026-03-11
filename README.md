# Lead Gen Workshop

AI-powered lead generation pipeline for finding and qualifying small business prospects.

## What It Does

1. **Find companies** — Searches Companies House (real UK registered companies) and Google
2. **Qualify with AI** — Sends each lead to an AI model for scoring and analysis
3. **Find decision makers** — Looks up real directors via Companies House + Google

## Files

```
workshop/
  config.py                    <- Edit this (API keys, search settings, prompts)
  main.py                      <- Full pipeline: find → qualify → results
  GUIDE.md                     <- Step-by-step setup guide (start here)
  tools/
    serper.py                  <- Google Search via Serper API
    openrouter.py              <- AI model via OpenRouter API
    companies_house.py         <- UK Companies House API
  scripts/
    find_icp_leads.py          <- Find businesses matching your ICP
    find_poc.py                <- Find point of contact for a company
```

## Quick Start

1. Install Python from https://www.python.org/downloads/ (tick "Add to PATH")
2. Get API keys (see below)
3. Paste keys into `config.py`
4. Open a terminal in this folder
5. Run `python main.py`

See **GUIDE.md** for detailed step-by-step instructions.

## API Keys

| Service | Purpose | Required | Free? | Link |
|---------|---------|----------|-------|------|
| Serper | Google search | Yes | 2,500 free searches | https://serper.dev |
| OpenRouter | AI qualification | Yes | Pay-as-you-go ($5 is plenty) | https://openrouter.ai |
| Companies House | UK company data | No | Completely free | https://developer.company-information.service.gov.uk |

## Scripts

### `python main.py`
Full pipeline — finds companies (Companies House + Google), qualifies each one with AI, prints results.

### `python scripts/find_icp_leads.py`
Finds businesses matching your Ideal Customer Profile. Edit `ICP_INDUSTRIES`, `ICP_LOCATIONS`, and `ICP_SIGNALS` in `config.py`.

### `python scripts/find_poc.py`
Finds the point of contact (directors, owners) for specific companies. Edit `POC_COMPANIES` in `config.py`.

## Supported Industries (Companies House)

The following industries have SIC codes mapped and work with Companies House search:

plumbers, electricians, estate agents, accountants, marketing agency, web design, builders, cleaners, hairdressers, restaurants, cafes, gyms, dentists, vets, landscapers, mechanics

For other industries, the pipeline falls back to Google search.

## No Dependencies

Everything uses Python's built-in libraries. No `pip install` needed.

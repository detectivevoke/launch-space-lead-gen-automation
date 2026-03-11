# ============================================================
#  LEAD GEN WORKSHOP — CONFIG
#  This is the only file you need to edit.
# ============================================================

# --- API KEYS -----------------------------------------------
SERPER_API_KEY     = "YOUR_SERPER_API_KEY"       # https://serper.dev
OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"   # https://openrouter.ai
CH_API_KEY         = "YOUR_CH_API_KEY"           # https://developer.company-information.service.gov.uk

# --- COMPANIES HOUSE SETTINGS --------------------------------
CH_API_URL         = "https://api.company-information.service.gov.uk"

# --- SERPER SETTINGS ----------------------------------------
SERPER_ENDPOINT    = "https://google.serper.dev/search"
SERPER_NUM_RESULTS = 10
SERPER_COUNTRY     = "gb"
SERPER_LANGUAGE    = "en"

# --- OPENROUTER / MODEL SETTINGS ----------------------------
OPENROUTER_MODEL       = "minimax/minimax-m2.5"
OPENROUTER_ENDPOINT    = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MAX_TOKENS  = 2048
OPENROUTER_TEMPERATURE = 0.7

# --- ICP LEAD FINDER ----------------------------------------
ICP_INDUSTRIES = ["plumbers", "electricians", "estate agents", "accountants"]
ICP_LOCATIONS  = ["Bristol", "Bath", "Somerset"]
ICP_SIGNALS    = ["owner", "family run", "independent", "established"]

# --- POC FINDER ---------------------------------------------
POC_COMPANIES = [
    "Apex Plumbing Bristol",
    "Clifton Estate Agents",
    "Smith & Co Accountants Bath",
]

# --- AI QUALIFY PIPELINE ------------------------------------
LEAD_SEARCH_QUERIES = [
    "plumbers in Bristol",
    "estate agents in Bath",
    "accountants in Bristol",
    "electricians in Somerset",
]

LEAD_QUALIFY_PROMPT = """
You are a lead qualification assistant. Analyse the following business information
extracted from a search result and return a structured summary.

Lead data:
{lead_data}

Return:
- Business name
- Location
- What they do (1 sentence)
- Why they could be a good automation/AI prospect (1–2 sentences)
- Confidence score: Low / Medium / High
"""
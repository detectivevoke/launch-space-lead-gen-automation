# Lead Gen Workshop — Setup Guide

This guide walks you through everything from scratch. No coding experience needed.

---

## Step 1: Install Python

1. Go to **https://www.python.org/downloads/**
2. Click the yellow **"Download Python 3.x.x"** button
3. Run the installer
4. **IMPORTANT:** Tick the box that says **"Add Python to PATH"** at the bottom of the first screen
5. Click **Install Now**
6. When it finishes, click **Close**

### Check it worked

Open a terminal:
- **Windows:** Press `Win + R`, type `cmd`, press Enter
- **Mac:** Press `Cmd + Space`, type `terminal`, press Enter

Type this and press Enter:

```
python --version
```

You should see something like `Python 3.12.x`. If you get an error, restart your computer and try again.

> **Mac users:** If `python` doesn't work, try `python3` instead. Use `python3` everywhere this guide says `python`.

---

## Step 2: Get Your API Keys

You need two API keys (required) and one optional key. All take about 60 seconds each.

### Serper (Google Search) — Required

1. Go to **https://serper.dev**
2. Click **Sign Up** and create an account
3. You get **2,500 free searches** (more than enough)
4. Once logged in, your API key is on the dashboard — copy it

### OpenRouter (AI Model) — Required

1. Go to **https://openrouter.ai**
2. Click **Sign Up** and create an account
3. Go to **https://openrouter.ai/keys**
4. Click **Create Key**, give it any name, click **Create**
5. Copy the key (starts with `sk-or-...`)
6. You will need to add a small amount of credit ($5 is plenty) — go to **https://openrouter.ai/credits**

### Companies House (UK Company Data) — Optional

This gives you access to real registered UK company data — directors' names, addresses, SIC codes. The pipeline works without it (Google only), but it's a big upgrade.

1. Go to **https://developer.company-information.service.gov.uk**
2. Click **Register** and create an account (you'll need to verify your email)
3. Once logged in, go to **Manage Applications** → **Create an application**
4. Give it any name and description
5. Under **API Key**, click **Create** — copy the key
6. This is completely free with no limits

---

## Step 3: Add Your API Keys

1. Open the `config.py` file in any text editor (Notepad, VS Code, whatever you have)
2. Find these two lines near the top:

```python
SERPER_API_KEY     = "YOUR_SERPER_API_KEY"
OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"
CH_API_KEY         = "YOUR_CH_API_KEY"
```

3. Replace the placeholder text with your real keys. For example:

```python
SERPER_API_KEY     = "a1b2c3d4e5f6..."
OPENROUTER_API_KEY = "sk-or-v1-abc123..."
CH_API_KEY         = "abc123-def456-..."
```

> **Note:** The Companies House key is optional. If you leave it as `YOUR_CH_API_KEY`, everything still works — it just uses Google only.

4. **Save the file** (Ctrl+S)

> **Important:** Keep the quote marks around your keys. Don't delete them.

---

## Step 4: Open a Terminal in the Workshop Folder

### Windows

1. Open File Explorer and navigate to the `workshop` folder
2. Click in the address bar at the top, type `cmd`, press Enter
3. A terminal window will open, already in the right folder

### Mac

1. Open Terminal
2. Type `cd ` (with a space after it), then drag the `workshop` folder into the terminal window
3. Press Enter

### Check you're in the right place

Type `dir` (Windows) or `ls` (Mac) and press Enter. You should see `config.py` and `main.py` in the list.

---

## Step 5: Run the Pipeline

Type this and press Enter:

```
python main.py
```

This will:
1. Search Companies House for real registered companies (if CH key is set)
2. Search Google for more leads
3. Send all leads to AI for qualification
4. Print the results

You should see output like:

```
=======================================================
  LEAD GEN WORKSHOP — AI Pipeline
=======================================================

[1/3] Finding real companies via Companies House...

  [CH] Searching SIC 43220 in Bristol...
  [CH] Searching SIC 43210 in Bath...
  ...
  12 companies found on Companies House

[2/3] Searching Google for leads...

  Searching: plumbers in Bristol
  Searching: estate agents in Bath
  ...
  35 total unique leads

[3/3] Qualifying 35 leads with AI...

  Qualifying 1/35: Bristol Plumbing Services Ltd [Companies House]
  Qualifying 2/35: ...
```

---

## Step 6: Try the Other Scripts

### Find ICP Leads

Searches Companies House + Google for businesses that match your Ideal Customer Profile:

```
python scripts/find_icp_leads.py
```

Edit these in `config.py` to change what it searches for:

```python
ICP_INDUSTRIES = ["plumbers", "electricians", "estate agents", "accountants"]
ICP_LOCATIONS  = ["Bristol", "Bath", "Somerset"]
ICP_SIGNALS    = ["owner", "family run", "independent", "established"]
```

### Find Point of Contact

Finds real directors via Companies House + searches Google for contact details:

```
python scripts/find_poc.py
```

Edit this in `config.py` to change which companies it looks up:

```python
POC_COMPANIES = [
    "Apex Plumbing Bristol",
    "Clifton Estate Agents",
    "Smith & Co Accountants Bath",
]
```

---

## Customising

Everything you need to change is in **`config.py`**. You don't need to touch any other file.

### Change what you search for

Edit `LEAD_SEARCH_QUERIES` — add or remove search queries:

```python
LEAD_SEARCH_QUERIES = [
    "plumbers in Bristol",
    "estate agents in Bath",
    "dentists in London",        # add your own
]
```

### Change how AI qualifies leads

Edit `LEAD_QUALIFY_PROMPT` — this is the instruction sent to the AI for each lead:

```python
LEAD_QUALIFY_PROMPT = """
You are a lead qualification assistant. Analyse the following business...
...
"""
```

### Change the AI model

Edit `OPENROUTER_MODEL` — browse models at https://openrouter.ai/models:

```python
OPENROUTER_MODEL = "minimax/minimax-m2.5"         # default (cheap + good)
# OPENROUTER_MODEL = "google/gemini-flash-1.5"   # alternative
```

### Change search region

```python
SERPER_COUNTRY  = "gb"    # gb = UK, us = USA, au = Australia, etc.
SERPER_LANGUAGE = "en"    # en = English
```

---

## Troubleshooting

### "Python is not recognized"

Python wasn't added to PATH during install. Either:
- Reinstall Python and tick **"Add Python to PATH"**
- Or find where Python was installed and use the full path, e.g. `C:\Users\YourName\AppData\Local\Programs\Python\Python312\python.exe main.py`

### "Serper API key is not set" or "OpenRouter API key is not set"

You haven't replaced the placeholder keys in `config.py`. Open it and paste your real keys.

### "Serper API key is invalid"

The key you pasted is wrong. Go back to https://serper.dev, copy it again, and paste it into `config.py`. Make sure there are no extra spaces.

### "OpenRouter API key is invalid"

Same — go to https://openrouter.ai/keys, copy your key again. Make sure it starts with `sk-or-`.

### "Companies House API key is invalid"

Go to https://developer.company-information.service.gov.uk, log in, check your application's API key. Copy it again into `config.py`. Or just leave it as `YOUR_CH_API_KEY` to skip Companies House.

### "Could not connect" / "Check your internet connection"

Your internet is down, or a firewall is blocking the connection. Try opening https://google.com in your browser to check.

### "Unexpected response from OpenRouter"

The AI model might be temporarily unavailable. Wait a minute and try again. If it keeps happening, try a different model in `config.py`.

### Nothing happens / terminal closes immediately

You might be double-clicking the `.py` file instead of running it from a terminal. Follow Step 4 to open a terminal first, then run the command from there.

### "No leads found"

Your search queries didn't return results. Try broader queries in `config.py`, e.g. `"plumbers in London"` instead of a very specific one.

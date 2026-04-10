### Project Goal: Philosophy Newsletter Automation
Build a modular Python application that scrapes 5 news articles and 2 opinion pieces, summarises it with LLMs, pits each article/piece against a relevant political philosopher/historian, and emails the collated newsletter to subscribers.

### 1. Stack & Infrastructure
- Orchestrator: GitHub Actions (Cron: every 72 hours)
- Database: Neon (PostgreSQL). The following tables have already been created. 
-- subscribers (id SERIAL, email TEXT, is_subscribed BOOLEAN, unsub_token UUID DEFAULT gen_unique_uuid NOT NULL UNIQUE)
-- newsletters (id SERIAL, newsletter_date DATE, title TEXT, content TEXT)
- Scraping: TinyFish API (Targets: CNA, AP, CNN, Al Jazeera)
- LLMs (Two-Step Chain): 
-- GPT-4o: Summarise each article 

[Gemini 1.5 Pro / GPT-4o] (Two-step chain: 1. Summarize, 2. Philosophical analysis)
- Email: Resend API

### 2. Implementation Requirements (The "Levers")
- Modular Architecture: Separate files for `db.py`, `scraper.py`, `brain.py`, and `mailer.py`.
- Resilience: Wrap API calls in try/except blocks. If one news source fails, continue with others.
- Data Contract: Scraper must return a list of Pydantic objects or dicts: [title, url, source, text].
- Environmental Variables: Use `os.getenv` for all API keys and DB URLs.

### 3. Deliverables
1. SQL Schema for Neon.
2. Complete Python codebase across the defined modules.
3. `requirements.txt` file.
4. `workflow.yml` for GitHub Actions.

Keep the code lean, avoid heavy frameworks, and prioritize readability.
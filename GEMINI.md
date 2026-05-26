# Philosophy Newsletter Automation

A modular full-stack application that automates the creation and delivery of a philosophical newsletter. It scrapes news articles, summarizes them, provides philosophical analysis using LLMs, and emails subscribers.

## Project Overview

- **Frontend:** Next.js (App Router), TypeScript, React. Provides a simple subscription interface.
- **Backend:** Python 3.12. Handles the newsletter pipeline (Scrape -> Summarize -> Analyze -> DB -> Email).
- **Database:** Neon (PostgreSQL). Stores subscribers and historical newsletters.
- **LLMs:** Multi-step chain using GPT-4o (summarization) and Gemini 1.5 Pro / GPT-4o (philosophical analysis).
- **External APIs:** 
    - **TinyFish:** News scraping (CNA, AP, CNN, Al Jazeera).
    - **Resend:** Email delivery.
- **Automation:** GitHub Actions cron job (runs every 72 hours).

## Project Structure

- `app/`: Next.js frontend and API routes (e.g., `api/subscribe`).
- `backend/`: Core Python pipeline modules.
    - `main.py`: Pipeline entry point and orchestration.
    - `tinyfish.py`: Scraper integration.
    - `output.py`: LLM summarization and analysis logic.
    - `mailer.py`: Resend email integration.
    - `model_utils.py`: Database and LLM helper functions.
- `tests/`: Project test suite.
    - `playwright/`: Visual and E2E tests using Playwright.
    - `playwright-report/`: HTML reports from Playwright (gitignored).
    - `test-results/`: Artifacts from Playwright runs (gitignored).
    - Backend tests: `test_mailer.py`, `test_main.py`, etc. (using `pytest`).
- `.github/workflows/`: GitHub Actions configuration.

## Building and Running

### Frontend (Next.js)

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm run start
```

### Backend (Python)

```bash
# Set up virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the pipeline
# Modes: prod (live), testing (fixture + DB), dryrun (fixture + LLM only)
python -m backend.main --mode dryrun

# Generate a visual preview (creates newsletter_preview.html)
python -m backend.main --mode dryrun --preview
```

*Note: The GitHub Action is configured to run `python -m backend.main --mode prod`. This ensures the execution context is correct from the root directory.*

### Testing

```bash
# Run backend tests
pytest

# Run visual rendering tests
PYTHONPATH=. pytest tests/test_visual_logic.py
```

## Development Conventions

- **Modularity:** Keep logic separated into `db.py`, `scraper.py`, `brain.py` (implemented as `output.py`/`model_utils.py`), and `mailer.py`.
- **Resilience:** All API calls should be wrapped in try/except blocks to ensure the pipeline continues even if one source or API fails.
- **Environment Variables:** All secrets (API keys, DB URLs) must be managed via `os.getenv` or `.env` files. NEVER hardcode secrets.
- **Data Contract:** Scrapers and LLM modules should return predictable Pydantic objects or dictionaries.
- **Type Safety:** Use TypeScript for the frontend and type hints for Python code where possible.

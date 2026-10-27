import json
import os
import time
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, NAMESPACE_URL, uuid5

import requests
from pydantic import AliasChoices, BaseModel, Field, model_validator

from backend.model_utils import get_tinyfish_client


class Article(BaseModel):
    """The validated contract for every article returned by Tinyfish."""

    id: UUID | None = None
    date: datetime | None = Field(
        default=None,
        validation_alias=AliasChoices("date", "published_at", "published_date"),
    )
    news_outlet: str = Field(
        min_length=1,
        validation_alias=AliasChoices("news_outlet", "source"),
    )
    title: str = Field(min_length=1)
    article: str = Field(
        min_length=1,
        validation_alias=AliasChoices("article", "text", "content"),
    )
    url: str = Field(min_length=1)
    extracted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @model_validator(mode="after")
    def set_stable_id(self) -> "Article":
        # Repeated extraction of the same canonical URL must address the same record.
        if self.id is None:
            self.id = uuid5(NAMESPACE_URL, self.url)
        return self


# Retain the original name for callers that imported this model before it was used.
article = Article


def _parse_tinyfish_result(result: Any) -> list[Article]:
    """Accept Tinyfish's JSON result and reject incomplete or unstructured output."""
    if isinstance(result, str):
        text_value = result.strip()
        if text_value.startswith("```"):
            text_value = text_value.split("\n", 1)[1] if "\n" in text_value else ""
            if text_value.rstrip().endswith("```"):
                text_value = text_value.rstrip()[:-3]
        result = json.loads(text_value)

    if isinstance(result, dict):
        for key in ("articles", "news_articles", "data", "result"):
            if isinstance(result.get(key), list):
                result = result[key]
                break
        else:
            result = [result]

    if not isinstance(result, list):
        raise ValueError("Tinyfish result is not a JSON article list.")

    articles = [Article.model_validate(item) for item in result]
    if not articles:
        raise ValueError("Tinyfish returned an empty article list.")
    return articles


def get_tinyfish_news() -> list[Article] | None:
    """Fetch, validate, cache, and durably persist a Tinyfish article batch."""
    # Local JSON is intentionally no longer used: Redis is the shared cache.
    from backend.storage import StorageError, cache_and_persist_articles, get_cached_articles
    from backend.run_cache import current_run

    try:
        cached_articles = get_cached_articles()
        if cached_articles:
            print("Loading validated articles from Redis cache...")
            return cached_articles
    except StorageError as exc:
        print(f"Redis cache is unavailable: {exc}")
        return None

    try:
        tinyfish_api_key = get_tinyfish_client()
        if not tinyfish_api_key or not tinyfish_api_key.strip():
            print("Error: TINYFISH_API_KEY is not set or is empty.")
            return None

        headers = {"X-API-Key": tinyfish_api_key, "Content-Type": "application/json"}
        payload = {
            "url": "https://example.com/task",
            "goal": (
                "Scrape the most pressing 2 articles and 1 opinion piece from the last week "
                "from CNA, Al Jazeera, CNN and AP. Return exactly 3 non-overlapping pieces. "
                "Return ONLY a JSON array. Every item must have these keys: title, url, source, "
                "date (an ISO-8601 date-time or null), and text (the complete, unsummarised article text)."
            ),
        }

        response = requests.post(
            "https://agent.tinyfish.ai/v1/automation/run-async",
            json=payload,
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
        response_json = response.json()
        run_id, error = response_json.get("run_id"), response_json.get("error")
        if error or not run_id:
            print(f"There was an error in getting a response: {error or 'no run_id returned'}")
            return None

        if run_cache := current_run():
            run_cache.write_json("tinyfish-submission.json", {"run_id": run_id})

        print("Waiting for Tinyfish results...")
        status_url = f"https://agent.tinyfish.ai/v1/runs/{run_id}"
        deadline = time.monotonic() + 15 * 60
        while time.monotonic() < deadline:
            status_response = requests.get(status_url, headers=headers, timeout=30)
            status_response.raise_for_status()
            status_check = status_response.json()
            status = status_check.get("status")
            if status == "COMPLETED":
                raw_result = status_check.get("result")
                if run_cache := current_run():
                    run_cache.write_json("tinyfish-result.json", raw_result)
                articles = _parse_tinyfish_result(raw_result)
                if run_cache := current_run():
                    run_cache.write_json(
                        "validated-articles.json",
                        [article.model_dump(mode="json") for article in articles],
                    )
                # Cache-first order is deliberate and applies before any LLM call.
                cache_and_persist_articles(articles)
                print("Validated articles cached in Redis and persisted to Neon.")
                return articles
            if status == "FAILED":
                error_message = (status_check.get("error") or {}).get("message", "Unknown error")
                print(f"Tinyfish failed to obtain news articles: {error_message}")
                return None

            print("Tinyfish task not finished.")
            time.sleep(10)

        print("Tinyfish task timed out after 15 minutes.")
        return None
    except (requests.RequestException, ValueError, StorageError) as exc:
        print(f"Tinyfish request failed: {exc}")
        return None


def load_fixture_articles(path=None):
    path = path or os.getenv("FIXTURE_PATH", "stuff.json")
    try:
        with open(path, "r") as file:
            return json.load(file)
    except Exception as exc:
        print(f"Unable to load fixture articles from {path}: {exc}")
        return None


if __name__ == "__main__":
    get_tinyfish_news()

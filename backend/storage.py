"""Redis cache and PostgreSQL persistence for scraped and generated content.

Redis is deliberately written first to match the pipeline's cache-first contract.
PostgreSQL remains the durable record.
"""

import json
import os
from datetime import datetime, timezone
from typing import Any, Sequence
from uuid import UUID, uuid4

import redis
from pydantic import BaseModel, Field
from sqlalchemy import text

from backend.model_utils import get_neon_client


class StorageError(RuntimeError):
    """Raised when the required cache or durable store cannot be updated."""


class Commentary(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)
    model: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


def _redis_client() -> redis.Redis:
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        raise StorageError("REDIS_URL must be configured for the production cache.")

    try:
        client = redis.Redis.from_url(
            redis_url,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
        )
        client.ping()
        return client
    except redis.RedisError as exc:
        raise StorageError(f"Unable to connect to Redis: {exc}") from exc


def _ttl(name: str, default: int) -> int:
    value = os.getenv(name, str(default))
    try:
        return max(int(value), 1)
    except ValueError:
        return default


def _article_key(article_id: UUID) -> str:
    return f"newsletter:article:{article_id}"


def _commentary_key(commentary_id: UUID) -> str:
    return f"newsletter:commentary:{commentary_id}"


def get_cached_articles() -> list[Any] | None:
    """Return the most recent validated article batch, if its Redis TTL is active."""
    client = _redis_client()
    batch = client.get("newsletter:articles:current")
    if not batch:
        return None

    try:
        article_ids = json.loads(batch)
        payloads = client.mget([_article_key(UUID(article_id)) for article_id in article_ids])
        if not payloads or any(payload is None for payload in payloads):
            return None

        # Import lazily: tinyfish calls this module after defining Article.
        from backend.tinyfish import Article

        return [Article.model_validate_json(payload) for payload in payloads]
    except (ValueError, TypeError) as exc:
        raise StorageError(f"Redis article cache contains invalid data: {exc}") from exc


def cache_and_persist_articles(articles: Sequence[Any]) -> None:
    """Write validated articles to Redis first, then upsert them into PostgreSQL."""
    if not articles:
        raise StorageError("Refusing to persist an empty article batch.")

    client = _redis_client()
    ttl = _ttl("ARTICLE_CACHE_TTL_SECONDS", 24 * 60 * 60)
    try:
        pipeline = client.pipeline(transaction=True)
        for article in articles:
            pipeline.set(_article_key(article.id), article.model_dump_json(), ex=ttl)
        pipeline.set(
            "newsletter:articles:current",
            json.dumps([str(article.id) for article in articles]),
            ex=ttl,
        )
        pipeline.execute()
    except redis.RedisError as exc:
        raise StorageError(f"Unable to cache extracted articles in Redis: {exc}") from exc

    engine = get_neon_client()
    if engine is None:
        raise StorageError("Unable to create the Neon database engine.")

    query = text(
        """
        INSERT INTO articles
            (date, news_outlet, title, article)
        VALUES
            (:date, :news_outlet, :title, :article)
        RETURNING id;
        """
    )
    try:
        with engine.begin() as connection:
            for article in articles:
                connection.execute(
                    query,
                    {
                        "date": article.date,
                        "news_outlet": article.news_outlet,
                        "title": article.title,
                        "article": article.article,
                    },
                )
    except Exception as exc:
        raise StorageError(f"Unable to persist extracted articles in Neon: {exc}") from exc
    finally:
        engine.dispose()


def cache_and_persist_commentary(commentary: Commentary) -> int:
    """Write the completed Gemini newsletter to Redis first, then Neon."""
    client = _redis_client()
    ttl = _ttl("COMMENTARY_CACHE_TTL_SECONDS", 7 * 24 * 60 * 60)
    try:
        client.set(_commentary_key(commentary.id), commentary.model_dump_json(), ex=ttl)
    except redis.RedisError as exc:
        raise StorageError(f"Unable to cache LLM commentary in Redis: {exc}") from exc

    engine = get_neon_client()
    if engine is None:
        raise StorageError("Unable to create the Neon database engine.")

    query = text(
        """
        INSERT INTO newsletters
            (newsletterdate, title, content)
        VALUES
            (:newsletterdate, :title, :content)
        RETURNING id;
        """
    )
    try:
        with engine.begin() as connection:
            result = connection.execute(
                query,
                {
                    "newsletterdate": commentary.generated_at.date(),
                    "title": commentary.title,
                    "content": commentary.content,
                },
            )
            return result.scalar_one()
    except Exception as exc:
        raise StorageError(f"Unable to persist LLM commentary in Neon: {exc}") from exc
    finally:
        engine.dispose()

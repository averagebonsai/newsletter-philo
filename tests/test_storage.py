from unittest.mock import MagicMock, Mock

from backend.storage import cache_and_persist_articles
from backend.tinyfish import Article


def test_articles_are_cached_before_the_neon_upsert(mocker):
    redis_client = Mock()
    redis_pipeline = Mock()
    redis_client.pipeline.return_value = redis_pipeline
    engine = MagicMock()
    connection = engine.begin.return_value.__enter__.return_value
    mocker.patch("backend.storage._redis_client", return_value=redis_client)
    mocker.patch("backend.storage.get_neon_client", return_value=engine)

    article = Article(
        title="Example",
        url="https://example.com/article",
        source="AP",
        text="Full article text.",
    )
    cache_and_persist_articles([article])

    redis_pipeline.execute.assert_called_once()
    connection.execute.assert_called_once()
    engine.dispose.assert_called_once()

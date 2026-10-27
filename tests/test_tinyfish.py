from backend.tinyfish import _parse_tinyfish_result


def test_parse_tinyfish_result_validates_and_normalises_agent_keys():
    articles = _parse_tinyfish_result(
        '[{"title":"A title","url":"https://example.com/article",'
        '"source":"CNA","date":"2026-10-01T00:00:00Z",'
        '"text":"The complete article."}]'
    )

    assert len(articles) == 1
    assert articles[0].news_outlet == "CNA"
    assert articles[0].article == "The complete article."
    assert articles[0].id is not None


def test_parse_tinyfish_result_rejects_unstructured_response():
    try:
        _parse_tinyfish_result("This is not a JSON article list")
    except ValueError:
        pass
    else:
        raise AssertionError("Unstructured Tinyfish output must not be cached or persisted")

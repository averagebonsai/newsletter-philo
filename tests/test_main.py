from datetime import date

import backend.main as main


def _patch_pipeline_internals(mocker):
    mocker.patch("backend.main.summariser", return_value="summary")
    mocker.patch("backend.main.philosopher", return_value="NEWSLETTER TITLE: Theme\n\nFinal body")
    mocker.patch("backend.main.parse_newsletter", return_value=("Theme", "Final body"))


def test_run_pipeline_prod_calls_all_side_effects(mocker):
    tinyfish_mock = mocker.patch("backend.main.get_tinyfish_news", return_value="articles")
    fixture_mock = mocker.patch("backend.main.load_fixture_articles", return_value={"news_articles": []})
    _patch_pipeline_internals(mocker)
    to_database_mock = mocker.patch("backend.main.to_database", return_value=99)
    send_emails_mock = mocker.patch("backend.main.send_emails", return_value={"sent": 2, "failed": []})

    result = main.run_pipeline("prod")

    expected_title = f"{date.today().isoformat()} - Theme"
    tinyfish_mock.assert_called_once()
    fixture_mock.assert_not_called()
    to_database_mock.assert_called_once_with(expected_title, "Final body")
    send_emails_mock.assert_called_once_with(expected_title, "Final body")
    assert result == {
        "status": "ok",
        "step": "completed",
        "mode": "prod",
        "title": expected_title,
        "newsletter_id": 99,
        "email": {"sent": 2, "failed": []},
    }


def test_run_pipeline_testing_skips_email(mocker):
    tinyfish_mock = mocker.patch("backend.main.get_tinyfish_news", return_value="articles")
    fixture_mock = mocker.patch(
        "backend.main.load_fixture_articles", return_value={"news_articles": [{"id": 1}]}
    )
    _patch_pipeline_internals(mocker)
    to_database_mock = mocker.patch("backend.main.to_database", return_value=42)
    send_emails_mock = mocker.patch("backend.main.send_emails")

    result = main.run_pipeline("testing")

    expected_title = f"{date.today().isoformat()} - Theme"
    tinyfish_mock.assert_not_called()
    fixture_mock.assert_called_once()
    to_database_mock.assert_called_once_with(expected_title, "Final body")
    send_emails_mock.assert_not_called()
    assert result["status"] == "ok"
    assert result["mode"] == "testing"
    assert result["newsletter_id"] == 42
    assert result["email"] == {"skipped": True, "reason": "mode=testing"}


def test_run_pipeline_dryrun_skips_db_and_email(mocker):
    tinyfish_mock = mocker.patch("backend.main.get_tinyfish_news", return_value="articles")
    fixture_mock = mocker.patch(
        "backend.main.load_fixture_articles", return_value={"news_articles": [{"id": 1}]}
    )
    _patch_pipeline_internals(mocker)
    to_database_mock = mocker.patch("backend.main.to_database")
    send_emails_mock = mocker.patch("backend.main.send_emails")

    result = main.run_pipeline("dryrun")

    tinyfish_mock.assert_not_called()
    fixture_mock.assert_called_once()
    to_database_mock.assert_not_called()
    send_emails_mock.assert_not_called()
    assert result["status"] == "ok"
    assert result["mode"] == "dryrun"
    assert result["newsletter_id"] is None
    assert result["email"] == {"skipped": True, "reason": "mode=dryrun"}


def test_run_pipeline_fails_fast_on_missing_scrape(mocker):
    mocker.patch("backend.main.get_tinyfish_news", return_value=None)

    result = main.run_pipeline("prod")

    assert result["status"] == "failed"
    assert result["step"] == "scrape"
    assert result["mode"] == "prod"


def test_run_pipeline_fails_fast_on_missing_fixture(mocker):
    mocker.patch("backend.main.load_fixture_articles", return_value=None)

    result = main.run_pipeline("dryrun")

    assert result["status"] == "failed"
    assert result["step"] == "scrape"
    assert result["mode"] == "dryrun"

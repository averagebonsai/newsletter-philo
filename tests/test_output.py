from datetime import date

import backend.output as output


def test_summariser_success(mocker):
    fake_client = mocker.Mock()
    fake_response = mocker.Mock(text="summary text")
    fake_client.models.generate_content.return_value = fake_response
    mocker.patch("backend.output.get_gemini_client", return_value=fake_client)

    result = output.summariser("raw articles")

    assert result == "summary text"
    fake_client.models.generate_content.assert_called_once()


def test_philosopher_success(mocker):
    fake_client = mocker.Mock()
    fake_response = mocker.Mock(text="NEWSLETTER TITLE: A title\n\nBody")
    fake_client.models.generate_content.return_value = fake_response
    mocker.patch("backend.output.get_gemini_client", return_value=fake_client)

    result = output.philosopher("summary")

    assert "NEWSLETTER TITLE:" in result
    fake_client.models.generate_content.assert_called_once()


def test_parse_newsletter_happy_path():
    raw = "NEWSLETTER TITLE: Global Power in Transition\n\nArticle one.\n\nArticle two."
    title, body = output.parse_newsletter(raw)
    assert title == "Global Power in Transition"
    assert body.startswith("Article one.")


def test_parse_newsletter_case_and_whitespace():
    raw = "  newsletter title:   Sharp Turns in Democracy \n\nFirst paragraph."
    title, body = output.parse_newsletter(raw)
    assert title == "Sharp Turns in Democracy"
    assert body == "First paragraph."


def test_parse_newsletter_missing_marker():
    raw = "No marker here."
    title, body = output.parse_newsletter(raw)
    assert title == "Newsletter"
    assert body == raw


def test_to_database_inserts_and_commits(mocker):
    fake_result = mocker.Mock()
    fake_result.scalar_one.return_value = 123
    fake_connection = mocker.Mock()
    fake_connection.execute.return_value = fake_result

    fake_engine = mocker.MagicMock()
    mocker.patch("backend.output.get_neon_client", return_value=fake_engine)
    engine = output.get_neon_client()
    engine.connect.return_value.__enter__.return_value = fake_connection
    engine.connect.return_value.__exit__.return_value = None

    newsletter_id = output.to_database("2026-05-08 - Title", "Body")

    assert newsletter_id == 123
    fake_connection.execute.assert_called_once()
    args, _ = fake_connection.execute.call_args
    params = args[1]
    assert params["title"] == "2026-05-08 - Title"
    assert params["content"] == "Body"
    assert params["newsletterdate"] == date.today()
    fake_connection.commit.assert_called_once()


def test_get_latest_newsletter(mocker):
    fake_connection = mocker.Mock()
    fake_connection.execute.return_value.fetchone.return_value = ("Latest Title", "Latest Content")
    fake_engine = mocker.MagicMock()
    fake_engine.connect.return_value.__enter__.return_value = fake_connection
    mocker.patch("backend.output.get_neon_client", return_value=fake_engine)

    title, content = output.get_latest_newsletter()

    assert title == "Latest Title"
    assert content == "Latest Content"

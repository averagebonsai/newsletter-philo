import mailer


def test_get_subscribers(mocker):
    fake_connection = mocker.Mock()
    fake_connection.execute.return_value = [("a@example.com", "tok1"), ("b@example.com", "tok2")]
    fake_engine = mocker.MagicMock()
    fake_engine.connect.return_value.__enter__.return_value = fake_connection
    fake_engine.connect.return_value.__exit__.return_value = None
    mocker.patch("mailer.get_neon_client", return_value=fake_engine)

    subscribers = mailer.get_subscribers()

    assert subscribers == [("a@example.com", "tok1"), ("b@example.com", "tok2")]


def test_format_html_contains_content_and_unsub():
    html = mailer.format_html("Title", "Para one.\n\nPara two.", "token-123")
    assert "<h1>Title</h1>" in html
    assert "<p>Para one.</p>" in html
    assert "<p>Para two.</p>" in html
    assert "https://example.com/unsubscribe?token=token-123" in html


def test_send_emails_success_and_partial_failure(mocker):
    mocker.patch(
        "mailer.get_subscribers",
        return_value=[("ok@example.com", "tok1"), ("bad@example.com", "tok2")],
    )
    fake_client = mocker.Mock()
    fake_client.Emails.send.side_effect = [None, Exception("invalid recipient")]
    mocker.patch("mailer.get_resend_client", return_value=fake_client)

    result = mailer.send_emails("2026-05-08 - Title", "Body text")

    assert result["sent"] == 1
    assert len(result["failed"]) == 1
    assert result["failed"][0]["email"] == "bad@example.com"
    assert fake_client.Emails.send.call_count == 2

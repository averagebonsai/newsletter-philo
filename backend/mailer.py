import os

from backend.model_utils import get_neon_client, get_resend_client
from sqlalchemy import text

def get_subscribers():
    engine = get_neon_client()
    query = "SELECT email, unsub_token FROM subscribers WHERE is_subscribed;"
    with engine.connect() as connection:
        result = connection.execute(text(query))
        subscribers = [(row[0], row[1]) for row in result]
    return subscribers

def get_mailing_list():
    return [email for email, _ in get_subscribers()]

def format_html(title, content, unsub_token):
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    body_html = "".join(f"<p>{paragraph}</p>" for paragraph in paragraphs)
    base_url = os.getenv("UNSUBSCRIBE_BASE_URL", "https://example.com").rstrip("/")
    unsubscribe_url = f"{base_url}/unsubscribe?token={unsub_token}"
    return (
        "<html><body style='font-family:Arial,sans-serif;line-height:1.6;'>"
        f"<h1>{title}</h1>"
        f"{body_html}"
        f"<hr><p style='font-size:12px;color:#555;'>"
        f"<a href='{unsubscribe_url}'>Unsubscribe</a>"
        "</p></body></html>"
    )

def send_emails(title, content):
    client = get_resend_client()
    from_email = os.getenv("FROM_EMAIL", "onboarding@resend.dev")
    send_result = {"sent": 0, "failed": []}

    for email, unsub_token in get_subscribers():
        try:
            client.Emails.send(
                {
                    "from": from_email,
                    "to": [email],
                    "subject": title,
                    "html": format_html(title, content, str(unsub_token)),
                }
            )
            send_result["sent"] += 1
        except Exception as e:
            send_result["failed"].append({"email": email, "error": str(e)})

    return send_result

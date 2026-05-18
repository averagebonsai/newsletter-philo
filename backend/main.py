import argparse
import os
from datetime import date

from backend.tinyfish import get_tinyfish_news, load_fixture_articles
from backend.output import (
    summariser,
    philosopher,
    parse_newsletter,
    to_database,
    generate_preview,
    get_latest_newsletter,
)
from backend.mailer import send_emails, get_first_subscriber, format_html, get_resend_client


def run_pipeline(mode, preview=False):
    run_result = {"status": "failed", "step": None, "title": None, "mode": mode}

    if mode == "email":
        print("[email] Fetching latest newsletter and first subscriber...")
        title, content = get_latest_newsletter()
        if not title or not content:
            run_result["step"] = "database"
            run_result["error"] = "No newsletters found in the database."
            return run_result

        email, unsub_token = get_first_subscriber()
        if not email:
            run_result["step"] = "database"
            run_result["error"] = "No subscribers found in the database."
            return run_result

        print(f"[email] Sending '{title}' to {email}...")
        try:
            client = get_resend_client()
            from_email = os.getenv("FROM_EMAIL", "onboarding@resend.dev")
            base_url = os.getenv("UNSUBSCRIBE_BASE_URL", "https://example.com").rstrip("/")
            unsubscribe_url = f"{base_url}/unsubscribe?token={unsub_token}"
            client.Emails.send(
                {
                    "from": from_email,
                    "to": [email],
                    "subject": title,
                    "html": format_html(title, content, str(unsub_token)),
                    "headers": {
                        "List-Unsubscribe": f"<{unsubscribe_url}>"
                    }
                }
            )
            return {
                "status": "ok",
                "step": "completed",
                "mode": mode,
                "title": title,
                "recipient": email,
            }
        except Exception as e:
            run_result["step"] = "email"
            run_result["error"] = str(e)
            return run_result

    if mode == "prod":
        articles = get_tinyfish_news()
    else:
        articles = load_fixture_articles()
    if not articles:
        run_result["step"] = "scrape"
        run_result["error"] = (
            "No articles returned from TinyFish."
            if mode == "prod"
            else "No articles loaded from fixture."
        )
        return run_result

    summary = summariser(articles)
    if not summary:
        run_result["step"] = "summarise"
        run_result["error"] = "Unable to generate article summaries."
        return run_result

    final_text = philosopher(summary)
    if not final_text:
        run_result["step"] = "philosopher"
        run_result["error"] = "Unable to generate philosopher output."
        return run_result

    llm_title, body = parse_newsletter(final_text)
    if not body.strip():
        run_result["step"] = "parse"
        run_result["error"] = "Newsletter body is empty after parsing."
        return run_result

    full_title = f"{date.today().isoformat()} - {llm_title}"

    if preview:
        preview_path = generate_preview(full_title, body)
        print(f"Preview generated at: {preview_path}")

    newsletter_id = None
    if mode in ("prod", "testing"):
        try:
            newsletter_id = to_database(full_title, body)
        except Exception as e:
            run_result["step"] = "database"
            run_result["title"] = full_title
            run_result["error"] = str(e)
            return run_result
    else:
        print(f"[{mode}] Skipping database write.")

    if mode == "prod":
        try:
            email_result = send_emails(full_title, body)
        except Exception as e:
            run_result["step"] = "email"
            run_result["title"] = full_title
            run_result["newsletter_id"] = newsletter_id
            run_result["error"] = str(e)
            return run_result
    else:
        print(f"[{mode}] Skipping email send.")
        email_result = {"skipped": True, "reason": f"mode={mode}"}

    return {
        "status": "ok",
        "step": "completed",
        "mode": mode,
        "title": full_title,
        "newsletter_id": newsletter_id,
        "email": email_result,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the newsletter pipeline.")
    parser.add_argument(
        "--mode",
        choices=["prod", "testing", "dryrun", "email"],
        required=True,
        help=(
            "prod: live TinyFish + LLMs + Neon + Resend. "
            "testing: fixture + LLMs + Neon, no email. "
            "dryrun: fixture + LLMs only, no DB, no email. "
            "email: fetch latest newsletter + first subscriber and send email."
        ),
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Generate an HTML preview of the newsletter.",
    )
    args = parser.parse_args()
    print(run_pipeline(args.mode, args.preview))

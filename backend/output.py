from datetime import date
import json
import re
import os

from pydantic import BaseModel
from sqlalchemy import text

from backend.model_utils import get_neon_client, get_gemini_client

chat_prompt = (
    "There are 2 news articles and 1 opinion piece below. In one response, produce a newsletter that "
    "summarises and philosophically critiques every piece. Begin each piece with its title wrapped in "
    "<b> tags (for example, <b>Article Title</b>; for an opinion article include its publisher). Write a "
    "100-150 word factual summary that fully presents the argument and counterarguments without adding your "
    "own opinion. Immediately follow it with an approximately 200-word critical assessment from one relevant "
    "political philosopher or historian; use a different perspective for each piece. Ground the assessment in "
    "that thinker's ideas, identifying a hidden assumption, risk, opportunity, historical parallel, or useful "
    "qualification. Avoid generic agreement or disagreement. End each piece with <hr />. "
    "Begin your entire response with one line in the exact "
    "form NEWSLETTER TITLE: <a concise 5-10 word title that captures the overarching theme of this issue>. "
    "Then leave one blank line and continue with the articles as instructed. Do not put any other text before this line."
)

gemini_model = "gemini-2.5-flash"

def summariser(articles):
    client = get_gemini_client()
    if isinstance(articles, (dict, list)):
        articles_text = json.dumps(
            articles,
            ensure_ascii=True,
            default=lambda value: value.model_dump(mode="json")
            if isinstance(value, BaseModel)
            else str(value),
        )
    else:
        articles_text = str(articles)
    try:
        response = client.models.generate_content(
            model=gemini_model,
            contents=f"{chat_prompt}\n\n{articles_text}",
        )
        return response.text
    except Exception as e:
        print(f"Unable to generate newsletter: {e}")
        return None

def parse_newsletter(text_value):
    if not text_value:
        return "Newsletter", ""

    lines = text_value.splitlines()
    for idx, line in enumerate(lines):
        match = re.match(r"^\s*NEWSLETTER TITLE:\s*(.+?)\s*$", line, flags=re.IGNORECASE)
        if match:
            parsed_title = match.group(1).strip()
            body_lines = lines[idx + 1 :]
            while body_lines and not body_lines[0].strip():
                body_lines = body_lines[1:]
            return parsed_title or "Newsletter", "\n".join(body_lines).strip()

    print("Warning: Missing NEWSLETTER TITLE marker in Gemini output.")
    return "Newsletter", text_value

def to_database(title, content):
    engine = get_neon_client()
    query = """
        INSERT INTO newsletters (newsletterdate, title, content)
        VALUES (:newsletterdate, :title, :content)
        RETURNING id;
    """
    with engine.connect() as connection:
        result = connection.execute(
            text(query),
            {
                "newsletterdate": date.today(),
                "title": title,
                "content": content,
            },
        )
        newsletter_id = result.scalar_one()
        connection.commit()
    return newsletter_id

def get_latest_newsletter():
    engine = get_neon_client()
    query = "SELECT title, content FROM newsletters ORDER BY newsletterdate DESC, id DESC LIMIT 1;"
    with engine.connect() as connection:
        result = connection.execute(text(query))
        row = result.fetchone()
        if row:
            return row[0], row[1]
    return None, None

def generate_preview(title, content):
    """Generates an HTML preview of the newsletter that matches the website's styling."""
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Newsletter Preview: {title}</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                background-color: #fff;
                color: #000;
                margin: 0;
                padding: 0;
                line-height: 1.8;
            }}
            article {{
                padding: 4rem 2rem;
                max-width: 800px;
                margin: 0 auto;
            }}
            header {{
                margin-bottom: 3rem;
                border-bottom: 1px solid #2c2c2c;
                padding-bottom: 2rem;
            }}
            .date {{
                font-size: 0.9rem;
                text-transform: uppercase;
                opacity: 0.6;
            }}
            h1 {{
                font-size: 3rem;
                margin: 1rem 0;
                font-weight: normal;
                line-height: 1.2;
            }}
            .content {{
                font-size: 1.1rem;
                white-space: pre-wrap;
            }}
        </style>
    </head>
    <body>
        <article>
            <header>
                <span class="date">{date_str}</span>
                <h1>{title}</h1>
            </header>
            <div class="content">{content_html}</div>
        </article>
    </body>
    </html>
    """
    
    content_html = content.replace('\\n', '<br />')
    # If the text has actual newline characters as well
    content_html = content_html.replace('\n', '<br />')
    
    date_str = date.today().strftime('%B %d, %Y')
    full_html = html_template.format(
        title=title,
        date_str=date_str,
        content_html=content_html
    )
    
    with open("newsletter_preview.html", "w") as f:
        f.write(full_html)
    
    return os.path.abspath("newsletter_preview.html")

if __name__ == "__main__":
    print("Run `python -m backend.main` to execute the full pipeline.")


    
    


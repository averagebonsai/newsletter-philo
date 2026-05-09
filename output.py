from datetime import date
import json
import re

from sqlalchemy import text

from model_utils import get_neon_client, get_openai_client, get_gemini_client

chat_model = "gpt-5-nano"
chat_prompt = "There should be 5 news articles and 2 opinion pieces. Summarise each article into roughly 2 paragraphs or 200 words. Ensure that arguments are fully fleshed out along with any counterarguments. Do not add in your own opinions. Do not address me, simply give the summary."
gemini_model = "gemini-2.5-flash"
gemini_prompt = (
    "There are summaries of 5 news articles and 2 opinion pieces here. For each piece, place it in "
    "conversation with a relevant political philosopher and historian. Ideally, this should be a response in "
    "support of or against one of the viewpoints raised in the article. Introducing a third, unconsidered "
    "perspective is also good. Do not edit the article summary, but add another paragraph at the end of the "
    "summary detailing what this philosopher or historian might say. This paragraph should be around 150-200 "
    "words. Briefly raise 1 contention with this viewpoint too. Remove all formatting (bolding, horizontal "
    "lines). Begin each article with the article's title. Begin your entire response with one line in the exact "
    "form NEWSLETTER TITLE: <a concise 5-10 word title that captures the overarching theme of this issue>. "
    "Then leave one blank line and continue with the articles as instructed. Do not put any other text before "
    "this line."
)

def summariser(articles):
    client = get_openai_client()
    if isinstance(articles, (dict, list)):
        articles_text = json.dumps(articles, ensure_ascii=True)
    else:
        articles_text = str(articles)
    try:
        response = client.responses.create(
            model=chat_model,
            input = [{
                "role": "user",
                "content": chat_prompt + "\n\n" + articles_text
                }]
        )
        return response.output_text
    except Exception as e:
        print(f"Unable to get summary: {e}")
        return None

def philosopher(response_text):
    client = get_gemini_client()
    try:
        response = client.models.generate_content(
            model=gemini_model,
            contents=f"{gemini_prompt}\n\n{response_text}",
        )
        return response.text
    except Exception as e:
        print(f"Unable to get philosophy commentary: {e}")
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

    print("Warning: Missing NEWSLETTER TITLE marker in philosopher output.")
    return "Newsletter", text_value

def to_database(title, content):
    engine = get_neon_client()
    query = """
        INSERT INTO newsletters (newsletter_date, title, content)
        VALUES (:newsletter_date, :title, :content)
        RETURNING id;
    """
    with engine.connect() as connection:
        result = connection.execute(
            text(query),
            {
                "newsletter_date": date.today(),
                "title": title,
                "content": content,
            },
        )
        newsletter_id = result.scalar_one()
        connection.commit()
    return newsletter_id

if __name__ == "__main__":
    print("Run `python main.py` to execute the full pipeline.")


    
    


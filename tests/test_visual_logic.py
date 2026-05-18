import os
import pytest
from backend.output import generate_preview

def test_generate_preview_creates_file():
    title = "Test Title"
    content = "Line 1\nLine 2 with <b>bold</b>"
    
    # Ensure file doesn't exist
    if os.path.exists("newsletter_preview.html"):
        os.remove("newsletter_preview.html")
        
    path = generate_preview(title, content)
    
    assert os.path.exists(path)
    assert path.endswith("newsletter_preview.html")
    
    with open(path, "r") as f:
        html = f.read()
        assert "<title>Newsletter Preview: Test Title</title>" in html
        assert "<h1>Test Title</h1>" in html
        assert "Line 1<br />Line 2 with <b>bold</b>" in html
        
    # Cleanup
    os.remove(path)

def test_generate_preview_markdown_bolding():
    title = "Markdown Test"
    content = "**Bold Title**\nNormal text.\n**Another Bold**"
    path = generate_preview(title, content)
    
    with open(path, "r") as f:
        html = f.read()
        assert "<b>Bold Title</b>" in html
        assert "<b>Another Bold</b>" in html
        assert "**" not in html
        
    os.remove(path)

def test_generate_preview_styling_exists():
    path = generate_preview("Styles", "Content")
    with open(path, "r") as f:
        html = f.read()
        assert "max-width: 800px;" in html
        assert "white-space: pre-wrap;" in html
        assert "line-height: 1.8;" in html
    os.remove(path)

import pytest


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("RESEND_API_KEY", "test_key")
    monkeypatch.setenv("FROM_EMAIL", "onboarding@resend.dev")
    monkeypatch.setenv("UNSUBSCRIBE_BASE_URL", "https://example.com")
    monkeypatch.setenv("OPENAI_API_KEY", "test_openai")
    monkeypatch.setenv("GEMINI_API_KEY", "test_gemini")
    monkeypatch.setenv("NEON_DATABASE_URL", "postgresql://user:pass@localhost/db")

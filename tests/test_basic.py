import sys
import os
import pytest

# Fix import path so app can be found when running pytest from root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"URL Shortener" in response.data  # check page content

def test_shorten_and_redirect(client):
    # Shorten a URL
    response = client.post("/shorten", json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.get_json()
    assert "short_url" in data
    short_url = data["short_url"]
    short_code = short_url.split("/")[-1]

    # Try redirection
    response = client.get(f"/{short_code}", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] == "https://example.com"

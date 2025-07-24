# tests/test_basic.py
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}

def test_shorten_and_redirect(client):
    res = client.post("/api/shorten", json={"url": "https://example.com"})
    assert res.status_code == 200
    data = res.get_json()
    short_code = data["short_code"]

    redirect_res = client.get(f"/{short_code}", follow_redirects=False)
    assert redirect_res.status_code == 302
    assert redirect_res.headers["Location"] == "https://example.com"

def test_stats(client):
    res = client.post("/api/shorten", json={"url": "https://example.org"})
    short_code = res.get_json()["short_code"]

    client.get(f"/{short_code}")
    client.get(f"/{short_code}")
    
    stats_res = client.get(f"/api/stats/{short_code}")
    assert stats_res.status_code == 200
    stats = stats_res.get_json()
    assert stats["url"] == "https://example.org"
    assert stats["clicks"] == 2

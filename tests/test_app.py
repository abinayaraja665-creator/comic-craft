import os

os.environ["AI_MOCK_MODE"] = "true"

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "ComicCraft" in response.text


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["mock_mode"] is True


def test_json_generation():
    payload = {
        "story_prompt": "A brave fox discovers a hidden library.",
        "character_name": "Milo",
        "setting": "enchanted forest",
        "tone": "funny",
        "art_style": "comic book",
    }
    response = client.post("/api/generate-comic", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["panels"]) == 5
    assert data["pdf_url"].endswith(".pdf")


def test_invalid_payload():
    response = client.post("/api/generate-comic", json={"story_prompt": "x"})
    assert response.status_code == 422

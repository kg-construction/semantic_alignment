import json

import pytest

from src.app import create_app


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch):
    from src.infrastructure import ollama_client
    from src.application import analyze_service

    def fake_generate(self, prompt: str):
        return "The sentence represented by RDF."

    class FakeBleurtEvaluator:
        def __init__(self, config, device=None):
            self.config = config
            self.device = device

        def compute_score(self, reference: str, candidate: str) -> float:
            return 0.91

    monkeypatch.setattr(ollama_client.OllamaClient, "generate_text", fake_generate)
    monkeypatch.setattr(analyze_service, "BLEURTEvaluator", FakeBleurtEvaluator)
    monkeypatch.setenv("OLLAMA_MODEL", "llama3:8b")
    monkeypatch.setenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")

    app = create_app()
    app.config.update({"TESTING": True})

    with app.test_client() as test_client:
        yield test_client


def test_analyze_request_flow(client):
    payload = {
        "text": "The original sentence.",
        "rdf": "@prefix ex: <http://example.org/> .",
    }
    resp = client.post("/analyze", data=json.dumps(payload), content_type="application/json")

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["text"] == "The original sentence."
    assert data["rdf"].startswith("@prefix")
    assert data["generated_text"] == "The sentence represented by RDF."
    assert data["bleurt"] == 0.91

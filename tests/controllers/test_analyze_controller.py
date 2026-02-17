import json

from flask import Flask

from src.controllers.analyze_controller import create_analyze_blueprint
from src.domain.models import AnalyzeResponse


class StubService:
    def __init__(self):
        self.called_with = None

    def analyze(self, request):
        self.called_with = request
        return AnalyzeResponse(text=request.text, rdf=request.rdf, generated_text="generated sentence", bleurt=0.87)


def make_client():
    service = StubService()
    app = Flask(__name__)
    app.register_blueprint(create_analyze_blueprint(service))
    app.config.update({"TESTING": True})
    return app.test_client(), service


def test_health_ok():
    client, _ = make_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_analyze_happy_path():
    client, service = make_client()
    payload = {"text": "original text", "rdf": "@prefix ex: <http://example.org/> ."}
    resp = client.post("/analyze", data=json.dumps(payload), content_type="application/json")

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["text"] == "original text"
    assert data["rdf"].startswith("@prefix")
    assert data["generated_text"] == "generated sentence"
    assert data["bleurt"] == 0.87
    assert service.called_with.text == "original text"


def test_analyze_missing_text_returns_400():
    client, _ = make_client()
    payload = {"rdf": "@prefix ex: <http://example.org/> ."}
    resp = client.post("/analyze", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 400
    assert "text" in resp.get_json()["error"]


def test_analyze_missing_rdf_returns_400():
    client, _ = make_client()
    payload = {"text": "original text"}
    resp = client.post("/analyze", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 400
    assert "rdf" in resp.get_json()["error"]

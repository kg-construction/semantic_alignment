import requests

from src.config.diplomat_config import DiplomatConfig
from src.infrastructure.ollama_client import OllamaClient


class StubResponse:
    def __init__(self, status_code: int, body: dict):
        self.status_code = status_code
        self._body = body
        self.text = str(body)

    def json(self):
        return self._body

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError("failed", response=self)


def make_client() -> OllamaClient:
    return OllamaClient(
        DiplomatConfig(
            ollama_timeout_seconds=600,
            ollama_max_retries=3,
            ollama_retry_sleep_seconds=0,
            ollama_num_predict=160,
        )
    )


def test_generate_text_uses_configured_timeout(monkeypatch):
    captured = {}

    def fake_post(url, json, timeout):
        captured["timeout"] = timeout
        captured["options"] = json["options"]
        return StubResponse(200, {"response": "generated text"})

    monkeypatch.setattr(requests, "post", fake_post)

    assert make_client().generate_text("prompt") == "generated text"
    assert captured["timeout"] == 600
    assert captured["options"] == {"num_predict": 160, "temperature": 0}


def test_generate_text_retries_transient_gateway_error(monkeypatch):
    responses = [
        StubResponse(502, {"error": "temporary"}),
        StubResponse(200, {"response": "generated text"}),
    ]
    calls = []

    def fake_post(url, json, timeout):
        calls.append(timeout)
        return responses.pop(0)

    monkeypatch.setattr(requests, "post", fake_post)

    assert make_client().generate_text("prompt") == "generated text"
    assert calls == [600, 600]


def test_generate_text_retries_ollama_internal_error(monkeypatch):
    responses = [
        StubResponse(500, {"error": "llama runner failed"}),
        StubResponse(200, {"response": "generated text"}),
    ]

    def fake_post(url, json, timeout):
        return responses.pop(0)

    monkeypatch.setattr(requests, "post", fake_post)

    assert make_client().generate_text("prompt") == "generated text"

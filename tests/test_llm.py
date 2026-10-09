
from fastapi.testclient import TestClient

from app.main import app
from app.services.llm.orchestrator import LLMOrchestrator


client = TestClient(app)


def test_llm_interpret_returns_deterministic_fallback_when_provider_fails(
    monkeypatch,
) -> None:
    def simulate_provider_failure(self, prompt: str):
        raise RuntimeError("Simulated Gemini outage")

    monkeypatch.setattr(
        LLMOrchestrator,
        "generate",
        simulate_provider_failure,
    )

    response = client.post(
        "/api/v1/llm/interpret",
        json={
            "request": "Investigate the cholera signal in Edo State",
            "forecast_horizon_days": 14,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["provider"] == "popu_deterministic"
    assert body["model"] == "deterministic_investigation_engine"
    assert body["fallback_used"] is True
    assert "no AI-generated interpretation was produced" in (
        body["interpretation"]
    )
    assert body["human_review_required"] is True
    assert any(
        "AI interpretation was unavailable" in item
        for item in body["uncertainty"]
    )
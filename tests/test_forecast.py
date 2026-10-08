from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_cholera_edo_forecast() -> None:
    response = client.get(
        "/api/v1/analysis/forecast",
        params={
            "disease": "cholera",
            "geography": "Edo State",
            "horizon_days": 7,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["disease"] == "cholera"
    assert body["geography"] == "Edo State"

    assert body["forecast_horizon_days"] == 7

    assert len(body["predicted_values"]) == 7
    assert len(body["confidence_interval"]) == 7

    assert body["data_status"] == "SYNTHETIC DATA"

    assert body["model"] == "baseline_trend_forecast"
    assert body["model_version"] == "0.1.0"

    assert 0 <= body["risk_score"] <= 100

    assert body["human_review_required"] is True

    assert "synthetic" in body["uncertainty"][0].lower()


def test_forecast_unknown_scenario_returns_404() -> None:
    response = client.get(
        "/api/v1/analysis/forecast",
        params={
            "disease": "malaria",
            "geography": "Edo State",
            "horizon_days": 7,
        },
    )

    assert response.status_code == 404


def test_forecast_horizon_cannot_exceed_30_days() -> None:
    response = client.get(
        "/api/v1/analysis/forecast",
        params={
            "disease": "cholera",
            "geography": "Edo State",
            "horizon_days": 31,
        },
    )

    assert response.status_code == 422
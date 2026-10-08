from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_cholera_edo_investigation():
    response = client.get(
        "/api/v1/analysis/investigation",
        params={
            "disease": "cholera",
            "geography": "Edo State",
            "forecast_horizon_days": 14,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["disease"] == "cholera"
    assert data["geography"] == "Edo State"

    assert data["anomaly"] is not None
    assert data["evidence"] is not None
    assert data["forecast"] is not None
    assert data["risk"] is not None

    assert len(data["forecast"]["predicted_values"]) == 14

    assert data["overall_signal"] in [
        "LOW",
        "MODERATE",
        "ELEVATED",
        "ANOMALY",
    ]

    assert len(data["key_findings"]) >= 1

    assert data["data_status"] == "SYNTHETIC DATA"

    assert "SYNTHETIC DEMONSTRATION DATA" in data["notice"]

    assert data["human_review_required"] is True


def test_unknown_investigation_scenario_returns_404():
    response = client.get(
        "/api/v1/analysis/investigation",
        params={
            "disease": "unknown_disease",
            "geography": "Edo State",
        },
    )

    assert response.status_code == 404


def test_investigation_forecast_horizon_limit():
    response = client.get(
        "/api/v1/analysis/investigation",
        params={
            "disease": "cholera",
            "geography": "Edo State",
            "forecast_horizon_days": 31,
        },
    )

    assert response.status_code == 422
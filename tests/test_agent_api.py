from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_agent_investigation_endpoint():
    response = client.post(
        "/api/v1/agent/investigate",
        json={
            "request": "Investigate the cholera signal in Edo State.",
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

    assert data["data_status"] == "SYNTHETIC DATA"
    assert data["human_review_required"] is True


def test_agent_unknown_request():
    response = client.post(
        "/api/v1/agent/investigate",
        json={
            "request": "Show me the weather forecast.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["intent"] == "UNKNOWN"
    assert data["disease"] is None
    assert data["geography"] is None


def test_agent_missing_disease():
    response = client.post(
        "/api/v1/agent/investigate",
        json={
            "request": "Investigate the signal in Edo State.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["intent"] == "INVESTIGATE"
    assert data["disease"] is None
    assert data["geography"] == "Edo State"


def test_agent_missing_geography():
    response = client.post(
        "/api/v1/agent/investigate",
        json={
            "request": "Investigate the cholera signal.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["intent"] == "INVESTIGATE"
    assert data["disease"] == "cholera"
    assert data["geography"] is None


def test_agent_unknown_scenario():
    response = client.post(
        "/api/v1/agent/investigate",
        json={
            "request": "Investigate cholera in Lagos State.",
            "forecast_horizon_days": 14,
        },
    )

    assert response.status_code == 404


def test_agent_rejects_invalid_horizon():
    response = client.post(
        "/api/v1/agent/investigate",
        json={
            "request": "Investigate the cholera signal in Edo State.",
            "forecast_horizon_days": 31,
        },
    )

    assert response.status_code == 422


def test_agent_rejects_empty_request():
    response = client.post(
        "/api/v1/agent/investigate",
        json={
            "request": "",
        },
    )

    assert response.status_code == 422
def test_agent_lassa_investigation_endpoint():
    response = client.post(
        "/api/v1/agent/investigate",
        json={
            "request": "Investigate the Lassa fever signal in Edo State.",
            "forecast_horizon_days": 14,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["disease"] == "lassa_fever"
    assert data["geography"] == "Edo State"

    assert data["anomaly"] is not None
    assert data["evidence"] is not None
    assert data["forecast"] is not None
    assert data["risk"] is not None
    assert data["integrated_risk"] is not None

    assert len(data["forecast"]["predicted_values"]) == 14

    assert data["data_status"] == "SYNTHETIC DATA"
    assert data["human_review_required"] is True
def test_agent_investigation_report_endpoint():
    response = client.post(
        "/api/v1/agent/investigate/report",
        json={
            "request": "Investigate the Lassa fever signal in Edo State.",
            "forecast_horizon_days": 14,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["disease"] == "lassa_fever"
    assert data["geography"] == "Edo State"

    assert data["summary"]
    assert len(data["key_findings"]) > 0
    assert len(data["investigation_priorities"]) > 0

    assert data["data_status"] == "SYNTHETIC DATA"
    assert "SYNTHETIC DEMONSTRATION DATA" in data["notice"]

    assert data["human_review_required"] is True
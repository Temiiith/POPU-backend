from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_cholera_edo_scenario() -> None:
    response = client.get(
        "/api/v1/data/scenario",
        params={
            "disease": "cholera",
            "geography": "Edo State",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "AVAILABLE"
    assert body["mode"] == "synthetic_demo"
    assert body["data_status"] == "SYNTHETIC DATA"
    assert "SYNTHETIC DEMONSTRATION DATA" in body["notice"]

    scenario = body["scenario"]

    assert scenario["disease"] == "cholera"
    assert scenario["geography"] == "Edo State"
    assert scenario["surveillance"]["total_cases"] == 146
    assert scenario["hospital"]["signal"] == "elevated"
    assert scenario["laboratory"]["signal"] == "elevated"
    assert scenario["environmental"]["signal"] == "elevated"


def test_unsupported_disease_returns_404() -> None:
    response = client.get(
        "/api/v1/data/scenario",
        params={
            "disease": "malaria",
            "geography": "Edo State",
        },
    )

    assert response.status_code == 404

    body = response.json()

    assert body["status"] == "DATA_UNAVAILABLE"
    assert body["scenario"] is None


def test_unsupported_geography_returns_404() -> None:
    response = client.get(
        "/api/v1/data/scenario",
        params={
            "disease": "cholera",
            "geography": "Unknown State",
        },
    )

    assert response.status_code == 404

    body = response.json()

    assert body["status"] == "INVALID_GEOGRAPHY"
    assert body["scenario"] is None


def test_scenario_options() -> None:
    response = client.get(
        "/api/v1/data/scenario-options"
    )

    assert response.status_code == 200

    body = response.json()

    assert "cholera" in body["diseases"]
    assert "dengue" in body["diseases"]
    assert "lassa_fever" in body["diseases"]

    assert "Edo State" in body["geographies"]

    assert body["data_status"] == "SYNTHETIC DATA"
    assert "SYNTHETIC DEMONSTRATION DATA" in body["notice"]
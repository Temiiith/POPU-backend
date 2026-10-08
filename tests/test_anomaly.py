from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_cholera_edo_anomaly() -> None:
    response = client.get(
        "/api/v1/analysis/anomaly",
        params={
            "disease": "cholera",
            "geography": "Edo State",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "ANOMALY"

    assert body["disease"] == "cholera"
    assert body["geography"] == "Edo State"

    assert body["data_status"] == "SYNTHETIC DATA"

    assert body["baseline_value"] == 35
    assert body["observed_value"] == 91

    assert body["absolute_deviation"] == 56
    assert body["percent_deviation"] == 160.0

    assert body["method"] == "baseline_percentage_deviation"

    assert body["human_review_required"] is True

    assert "synthetic" in body["uncertainty"][0].lower()


def test_unknown_scenario_returns_404() -> None:
    response = client.get(
        "/api/v1/analysis/anomaly",
        params={
            "disease": "malaria",
            "geography": "Edo State",
        },
    )

    assert response.status_code == 404
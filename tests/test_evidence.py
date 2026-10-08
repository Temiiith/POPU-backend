from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_cholera_edo_evidence():
    response = client.get(
        "/api/v1/analysis/evidence",
        params={
            "disease": "cholera",
            "geography": "Edo State",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["disease"] == "cholera"
    assert data["geography"] == "Edo State"

    assert data["data_status"] == "SYNTHETIC DATA"

    assert "SYNTHETIC DEMONSTRATION DATA" in data["notice"]

    assert len(data["evidence"]) == 4

    assert data["elevated_signal_count"] >= 1

    assert len(data["geographic_evidence"]) == 4

    assert data["human_review_required"] is True


def test_unknown_evidence_scenario_returns_404():
    response = client.get(
        "/api/v1/analysis/evidence",
        params={
            "disease": "unknown_disease",
            "geography": "Edo State",
        },
    )

    assert response.status_code == 404


def test_evidence_requires_disease_and_geography():
    response = client.get(
        "/api/v1/analysis/evidence",
    )

    assert response.status_code == 422
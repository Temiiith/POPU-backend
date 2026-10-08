from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_cholera_edo_risk():
    response = client.get(
        "/api/v1/analysis/risk",
        params={
            "disease": "cholera",
            "geography": "Edo State",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["disease"] == "cholera"
    assert data["geography"] == "Edo State"

    assert data["risk_level"] in [
        "LOW",
        "MODERATE",
        "ELEVATED",
    ]

    assert 0 <= data["risk_score"] <= 100

    assert data["evidence_signal_count"] == 4

    assert data["elevated_signal_count"] >= 1

    assert len(data["contributing_factors"]) >= 1

    assert data["data_status"] == "SYNTHETIC DATA"

    assert "SYNTHETIC DEMONSTRATION DATA" in data["notice"]

    assert data["human_review_required"] is True


def test_unknown_risk_scenario_returns_404():
    response = client.get(
        "/api/v1/analysis/risk",
        params={
            "disease": "unknown_disease",
            "geography": "Edo State",
        },
    )

    assert response.status_code == 404


def test_risk_requires_disease_and_geography():
    response = client.get(
        "/api/v1/analysis/risk",
    )

    assert response.status_code == 422


def test_integrated_cholera_edo_risk():
    response = client.get(
        "/api/v1/analysis/risk/integrated",
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

    assert data["risk_level"] == "ELEVATED"
    assert data["risk_score"] == 85.0

    assert data["data_status"] == "SYNTHETIC DATA"
    assert "SYNTHETIC DEMONSTRATION DATA" in data["notice"]

    assert data["human_review_required"] is True

    component_names = [
        component["name"]
        for component in data["components"]
    ]

    assert component_names == [
        "Anomaly",
        "Hospital",
        "Laboratory",
        "Environmental",
        "Geographic clustering",
        "Forecast",
    ]

    contributions = [
        component["contribution"]
        for component in data["components"]
    ]

    assert contributions == [
        25.0,
        10.0,
        10.0,
        10.0,
        15.0,
        15.0,
    ]

    assert sum(contributions) == data["risk_score"]

    assert len(data["key_factors"]) == 6

    assert "Surveillance anomaly detected." in data["key_factors"]
    assert "Elevated hospital syndrome signal." in data["key_factors"]
    assert "Elevated laboratory signal." in data["key_factors"]
    assert "Elevated environmental signal." in data["key_factors"]
    assert "3 geographic areas show elevated signals." in data["key_factors"]
    assert "Forecast indicates elevated projected risk." in data["key_factors"]


def test_unknown_integrated_risk_scenario_returns_404():
    response = client.get(
        "/api/v1/analysis/risk/integrated",
        params={
            "disease": "unknown_disease",
            "geography": "Unknown State",
            "forecast_horizon_days": 14,
        },
    )

    assert response.status_code == 404


def test_integrated_risk_requires_disease_and_geography():
    response = client.get(
        "/api/v1/analysis/risk/integrated",
    )

    assert response.status_code == 422


def test_integrated_risk_rejects_invalid_forecast_horizon():
    response = client.get(
        "/api/v1/analysis/risk/integrated",
        params={
            "disease": "cholera",
            "geography": "Edo State",
            "forecast_horizon_days": 0,
        },
    )

    assert response.status_code == 422


def test_integrated_risk_rejects_forecast_horizon_above_30():
    response = client.get(
        "/api/v1/analysis/risk/integrated",
        params={
            "disease": "cholera",
            "geography": "Edo State",
            "forecast_horizon_days": 31,
        },
    )

    assert response.status_code == 422
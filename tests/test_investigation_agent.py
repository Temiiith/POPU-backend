from app.agents.investigation_agent import run_investigation_agent


def test_investigation_agent_cholera_edo():
    result = run_investigation_agent(
        disease="cholera",
        geography="Edo State",
        forecast_horizon_days=14,
    )

    assert result is not None

    assert result.disease == "cholera"
    assert result.geography == "Edo State"

    assert result.anomaly is not None
    assert result.evidence is not None
    assert result.forecast is not None
    assert result.risk is not None

    assert len(result.forecast.predicted_values) == 14

    assert result.human_review_required is True
    assert result.data_status == "SYNTHETIC DATA"


def test_investigation_agent_unknown_scenario():
    result = run_investigation_agent(
        disease="unknown_disease",
        geography="Unknown State",
        forecast_horizon_days=14,
    )

    assert result is None


def test_investigation_agent_rejects_invalid_horizon():
    result = run_investigation_agent(
        disease="cholera",
        geography="Edo State",
        forecast_horizon_days=31,
    )

    assert result is None


def test_investigation_agent_rejects_empty_disease():
    result = run_investigation_agent(
        disease="",
        geography="Edo State",
        forecast_horizon_days=14,
    )

    assert result is None


def test_investigation_agent_rejects_empty_geography():
    result = run_investigation_agent(
        disease="cholera",
        geography="",
        forecast_horizon_days=14,
    )

    assert result is None
def test_investigation_agent_lassa_edo():
    result = run_investigation_agent(
        disease="lassa_fever",
        geography="Edo State",
        forecast_horizon_days=14,
    )

    assert result is not None

    assert result.disease == "lassa_fever"
    assert result.geography == "Edo State"

    assert result.anomaly is not None
    assert result.evidence is not None
    assert result.forecast is not None
    assert result.risk is not None
    assert result.integrated_risk is not None

    assert len(result.forecast.predicted_values) == 14

    assert result.human_review_required is True
    assert result.data_status == "SYNTHETIC DATA"
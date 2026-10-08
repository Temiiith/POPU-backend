from app.services.risk_fusion_service import assess_integrated_risk


def test_integrated_risk_for_cholera_edo():
    result = assess_integrated_risk(
        disease="cholera",
        geography="Edo State",
        forecast_horizon_days=14,
    )

    assert result is not None
    assert result.disease == "cholera"
    assert result.geography == "Edo State"
    assert result.risk_level == "ELEVATED"
    assert result.risk_score > 60
    assert result.human_review_required is True
    assert result.data_status == "SYNTHETIC DATA"
    assert len(result.components) == 6


def test_integrated_risk_contains_expected_components():
    result = assess_integrated_risk(
        disease="cholera",
        geography="Edo State",
    )

    assert result is not None

    component_names = [component.name for component in result.components]

    assert "Anomaly" in component_names
    assert "Hospital" in component_names
    assert "Laboratory" in component_names
    assert "Environmental" in component_names
    assert "Geographic clustering" in component_names
    assert "Forecast" in component_names


def test_integrated_risk_unknown_scenario_returns_none():
    result = assess_integrated_risk(
        disease="unknown_disease",
        geography="Unknown State",
    )

    assert result is None
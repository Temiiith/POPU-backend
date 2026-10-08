from app.agents.intent_agent import parse_investigation_request


def test_parse_cholera_edo_investigation():
    result = parse_investigation_request(
        "Investigate the cholera signal in Edo State."
    )

    assert result.intent == "INVESTIGATE"
    assert result.disease == "cholera"
    assert result.geography == "Edo State"
    assert result.forecast_horizon_days == 7
    assert result.original_request == (
        "Investigate the cholera signal in Edo State."
    )


def test_parse_dengue_lagos_investigation():
    result = parse_investigation_request(
        "Investigate dengue in Lagos State."
    )

    assert result.intent == "INVESTIGATE"
    assert result.disease == "dengue"
    assert result.geography == "Lagos State"


def test_parse_lassa_fever_kano_investigation():
    result = parse_investigation_request(
        "Check the Lassa fever signal in Kano State."
    )

    assert result.intent == "INVESTIGATE"
    assert result.disease == "lassa_fever"
    assert result.geography == "Kano State"


def test_unknown_request():
    result = parse_investigation_request(
        "Show me the weather forecast."
    )

    assert result.intent == "UNKNOWN"
    assert result.disease is None
    assert result.geography is None


def test_empty_request():
    result = parse_investigation_request("")

    assert result.intent == "UNKNOWN"
    assert result.disease is None
    assert result.geography is None


def test_investigation_without_supported_disease():
    result = parse_investigation_request(
        "Investigate the signal in Edo State."
    )

    assert result.intent == "INVESTIGATE"
    assert result.disease is None
    assert result.geography == "Edo State"
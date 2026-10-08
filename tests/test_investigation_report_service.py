from app.services.investigation_report_service import (
    generate_investigation_report,
)
from app.services.investigation_service import investigate


def test_generate_investigation_report():
    result = investigate(
        disease="cholera",
        geography="Edo State",
        forecast_horizon_days=14,
    )

    assert result is not None

    report = generate_investigation_report(result)

    assert report.disease == "cholera"
    assert report.geography == "Edo State"

    assert report.summary
    assert len(report.key_findings) > 0
    assert len(report.investigation_priorities) > 0
    assert len(report.supporting_evidence) > 0

    assert report.data_status == "SYNTHETIC DATA"
    assert "SYNTHETIC DEMONSTRATION DATA" in report.notice

    assert report.human_review_required is True
import re

from app.schemas.agent import AgentIntent


SUPPORTED_DISEASE_ALIASES = {
    "cholera": "cholera",
    "dengue": "dengue",
    "lassa fever": "lassa_fever",
    "lassa": "lassa_fever",
}


def parse_investigation_request(
    request: str,
) -> AgentIntent:
    """
    Parse a natural-language epidemiological investigation request.

    This is a deterministic parser for the MVP.
    It does not use an LLM and does not make epidemiological decisions.
    """

    original_request = request.strip()

    if not original_request:
        return AgentIntent(
            intent="UNKNOWN",
            original_request=original_request,
        )

    normalized = original_request.lower()

    investigation_keywords = [
        "investigate",
        "investigation",
        "check",
        "analyze",
        "analyse",
    ]

    is_explicit_investigation = any(
        keyword in normalized
        for keyword in investigation_keywords
    )

    disease = None

    for disease_alias, canonical_disease in SUPPORTED_DISEASE_ALIASES.items():
        if re.search(
            rf"\b{re.escape(disease_alias)}\b",
            normalized,
        ):
            disease = canonical_disease
            break

    geography = None

    geography_match = re.search(
        r"\b(?:in|for|at)\s+([A-Za-z][A-Za-z\s-]*?(?:State|LGA|Local Government Area))\b",
        original_request,
        re.IGNORECASE,
    )

    if geography_match:
        geography = geography_match.group(1).strip()

        geography_aliases = {
            "edo state": "Edo State",
            "lagos state": "Lagos State",
            "kano state": "Kano State",
            "kaduna state": "Kaduna State",
            "rivers state": "Rivers State",
        }

        geography = geography_aliases.get(
            geography.lower(),
            geography,
        )

    # Natural epidemiological shorthand:
    # "Lassa in Edo"
    # "Cholera in Lagos"
    #
    # Treat a disease + geography combination as an investigation
    # request even when the user does not explicitly say "investigate".
    shorthand_investigation = (
        disease is not None
        and geography is not None
        and re.search(
            r"\b(?:in|for|at)\s+[A-Za-z]",
            original_request,
            re.IGNORECASE,
        )
        is not None
    )

    if not is_explicit_investigation and not shorthand_investigation:
        return AgentIntent(
            intent="UNKNOWN",
            disease=disease,
            geography=geography,
            original_request=original_request,
        )

    return AgentIntent(
        intent="INVESTIGATE",
        disease=disease,
        geography=geography,
        original_request=original_request,
    )
from typing import Final


SYNTHETIC_DATA_NOTICE: Final[str] = (
    "SYNTHETIC DEMONSTRATION DATA - NOT FOR OFFICIAL CLINICAL ACTION"
)


SYNTHETIC_SCENARIOS: Final[dict[str, dict[str, dict]]] = {
    "cholera": {
        "Edo State": {
            "disease": "cholera",
            "geography": "Edo State",
            "data_status": "SYNTHETIC DATA",
            "notice": SYNTHETIC_DATA_NOTICE,
            "scenario_type": "demonstration_signal",
            "surveillance": {
                "reporting_period": "14 days",
                "total_cases": 146,
                "suspected_cases": 118,
                "confirmed_cases": 28,
                "weekly_baseline_cases": 35,
                "recent_week_cases": 91,
                "case_change_percent": 160.0,
                "daily_cases": [
                    8,
                    9,
                    10,
                    11,
                    9,
                    12,
                    13,
                    15,
                    18,
                    17,
                    21,
                    23,
                    27,
                    31,
                ],
            },
            "hospital": {
                "reporting_facilities": 8,
                "gastrointestinal_syndrome_count": 74,
                "dehydration_cases": 31,
                "hospitalization_count": 18,
                "signal": "elevated",
            },
            "laboratory": {
                "samples_tested": 42,
                "positive_samples": 14,
                "positivity_rate_percent": 33.3,
                "signal": "elevated",
            },
            "environmental": {
                "rainfall_trend": "increasing",
                "flooding_reports": 7,
                "water_quality_signal": "elevated",
                "signal": "elevated",
            },
            "geographic_signals": [
                {
                    "lga": "Oredo",
                    "cases": 34,
                    "baseline_cases": 8,
                    "signal": "elevated",
                },
                {
                    "lga": "Ikpoba-Okha",
                    "cases": 27,
                    "baseline_cases": 7,
                    "signal": "elevated",
                },
                {
                    "lga": "Egor",
                    "cases": 22,
                    "baseline_cases": 6,
                    "signal": "elevated",
                },
                {
                    "lga": "Uhunmwode",
                    "cases": 8,
                    "baseline_cases": 7,
                    "signal": "stable",
                },
            ],
            "uncertainty": [
                "All values are synthetic demonstration data.",
                "The scenario does not represent confirmed real-world conditions in Edo State.",
                "Environmental and hospital signals are illustrative.",
                "No public-health action should be taken from this scenario.",
            ],
        },
        "Nigeria": {
            "disease": "cholera",
            "geography": "Nigeria",
            "data_status": "SYNTHETIC DATA",
            "notice": SYNTHETIC_DATA_NOTICE,
            "scenario_type": "national_demonstration",
            "surveillance": {
                "reporting_period": "14 days",
                "total_cases": 540,
                "suspected_cases": 430,
                "confirmed_cases": 110,
                "weekly_baseline_cases": 140,
                "recent_week_cases": 310,
                "case_change_percent": 121.4,
                "daily_cases": [
                    29,
                    31,
                    34,
                    36,
                    32,
                    38,
                    40,
                    43,
                    46,
                    48,
                    52,
                    55,
                    60,
                    64,
                ],
            },
            "hospital": {
                "reporting_facilities": 42,
                "gastrointestinal_syndrome_count": 251,
                "dehydration_cases": 97,
                "hospitalization_count": 63,
                "signal": "elevated",
            },
            "laboratory": {
                "samples_tested": 120,
                "positive_samples": 37,
                "positivity_rate_percent": 30.8,
                "signal": "elevated",
            },
            "environmental": {
                "rainfall_trend": "increasing",
                "flooding_reports": 31,
                "water_quality_signal": "elevated",
                "signal": "elevated",
            },
            "geographic_signals": [
                {
                    "lga": "Edo State",
                    "cases": 146,
                    "baseline_cases": 35,
                    "signal": "elevated",
                },
                {
                    "lga": "Kano State",
                    "cases": 91,
                    "baseline_cases": 48,
                    "signal": "elevated",
                },
                {
                    "lga": "Borno State",
                    "cases": 64,
                    "baseline_cases": 41,
                    "signal": "elevated",
                },
            ],
            "uncertainty": [
                "All values are synthetic demonstration data.",
                "National geographic values are illustrative.",
                "The scenario does not represent official Nigerian surveillance data.",
            ],
        },
    },
    "dengue": {
        "Edo State": {
            "disease": "dengue",
            "geography": "Edo State",
            "data_status": "SYNTHETIC DATA",
            "notice": SYNTHETIC_DATA_NOTICE,
            "scenario_type": "demonstration_signal",
            "surveillance": {
                "reporting_period": "14 days",
                "total_cases": 74,
                "suspected_cases": 58,
                "confirmed_cases": 16,
                "weekly_baseline_cases": 31,
                "recent_week_cases": 43,
                "case_change_percent": 38.7,
                "daily_cases": [
                    4,
                    5,
                    4,
                    5,
                    6,
                    5,
                    5,
                    6,
                    7,
                    6,
                    7,
                    8,
                    9,
                    10,
                ],
            },
            "hospital": {
                "reporting_facilities": 7,
                "gastrointestinal_syndrome_count": 0,
                "dehydration_cases": 0,
                "hospitalization_count": 9,
                "signal": "moderate",
            },
            "laboratory": {
                "samples_tested": 29,
                "positive_samples": 8,
                "positivity_rate_percent": 27.6,
                "signal": "moderate",
            },
            "environmental": {
                "rainfall_trend": "stable",
                "flooding_reports": 2,
                "water_quality_signal": "unknown",
                "signal": "moderate",
            },
            "geographic_signals": [
                {
                    "lga": "Oredo",
                    "cases": 18,
                    "baseline_cases": 7,
                    "signal": "elevated",
                },
                {
                    "lga": "Egor",
                    "cases": 12,
                    "baseline_cases": 6,
                    "signal": "elevated",
                },
            ],
                       "uncertainty": [
                "All values are synthetic demonstration data.",
                "Laboratory values are illustrative and not linked to real specimens.",
            ],
        },
        "Lagos State": {
            "disease": "dengue",
            "geography": "Lagos State",
            "data_status": "SYNTHETIC DATA",
            "notice": SYNTHETIC_DATA_NOTICE,
            "scenario_type": "demonstration_signal",
            "surveillance": {
                "reporting_period": "14 days",
                "total_cases": 96,
                "suspected_cases": 72,
                "confirmed_cases": 24,
                "weekly_baseline_cases": 34,
                "recent_week_cases": 57,
                "case_change_percent": 67.6,
                "daily_cases": [
                    5,
                    6,
                    5,
                    7,
                    6,
                    8,
                    7,
                    9,
                    10,
                    8,
                    11,
                    12,
                    14,
                    16,
                ],
            },
            "hospital": {
                "reporting_facilities": 10,
                "gastrointestinal_syndrome_count": 0,
                "dehydration_cases": 0,
                "hospitalization_count": 13,
                "signal": "elevated",
            },
            "laboratory": {
                "samples_tested": 36,
                "positive_samples": 11,
                "positivity_rate_percent": 30.6,
                "signal": "elevated",
            },
            "environmental": {
                "rainfall_trend": "increasing",
                "flooding_reports": 5,
                "water_quality_signal": "unknown",
                "signal": "moderate",
            },
            "geographic_signals": [
                {
                    "lga": "Ikeja",
                    "cases": 21,
                    "baseline_cases": 7,
                    "signal": "elevated",
                },
                {
                    "lga": "Lagos Mainland",
                    "cases": 17,
                    "baseline_cases": 6,
                    "signal": "elevated",
                },
                {
                    "lga": "Alimosho",
                    "cases": 14,
                    "baseline_cases": 8,
                    "signal": "moderate",
                },
            ],
            "uncertainty": [
                "All values are synthetic demonstration data.",
                "The scenario does not represent confirmed real-world dengue activity.",
                "Laboratory values are illustrative and not linked to real specimens.",
                "No public-health action should be taken from this scenario.",
            ],
        }
    },
    "lassa_fever": {
        "Edo State": {
            "disease": "lassa_fever",
            "geography": "Edo State",
            "data_status": "SYNTHETIC DATA",
            "notice": SYNTHETIC_DATA_NOTICE,
            "scenario_type": "demonstration_signal",
            "surveillance": {
                "reporting_period": "14 days",
                "total_cases": 21,
                "suspected_cases": 16,
                "confirmed_cases": 5,
                "weekly_baseline_cases": 12,
                "recent_week_cases": 14,
                "case_change_percent": 16.7,
                "daily_cases": [
                    1,
                    1,
                    2,
                    1,
                    2,
                    1,
                    2,
                    1,
                    2,
                    2,
                    1,
                    2,
                    1,
                    2,
                ],
            },
            "hospital": {
                "reporting_facilities": 6,
                "gastrointestinal_syndrome_count": 0,
                "dehydration_cases": 0,
                "hospitalization_count": 8,
                "signal": "moderate",
            },
            "laboratory": {
                "samples_tested": 18,
                "positive_samples": 5,
                "positivity_rate_percent": 27.8,
                "signal": "moderate",
            },
            "environmental": {
                "rainfall_trend": "stable",
                "flooding_reports": 1,
                "water_quality_signal": "unknown",
                "signal": "stable",
            },
            "geographic_signals": [
                {
                    "lga": "Oredo",
                    "cases": 6,
                    "baseline_cases": 3,
                    "signal": "moderate",
                },
                {
                    "lga": "Egor",
                    "cases": 4,
                    "baseline_cases": 3,
                    "signal": "stable",
                },
            ],
            "uncertainty": [
                "All values are synthetic demonstration data.",
                "The scenario does not represent confirmed real-world Lassa fever activity.",
            ],
        }
    },
}


SUPPORTED_DISEASES: Final[tuple[str, ...]] = tuple(SYNTHETIC_SCENARIOS.keys())

SUPPORTED_GEOGRAPHIES: Final[tuple[str, ...]] = tuple(
    sorted(
        {
            geography
            for disease_scenarios in SYNTHETIC_SCENARIOS.values()
            for geography in disease_scenarios
        }
    )
)
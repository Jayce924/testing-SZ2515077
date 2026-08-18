from __future__ import annotations

import pytest

from flight_risk import FlightConditions, calculate_risk_score, classify_risk


def test_low_risk_conditions() -> None:
    conditions = FlightConditions(15, 5, 0, 50, 0.1)
    assert calculate_risk_score(conditions) == 2
    assert classify_risk(2) == "low"


def test_moderate_risk_conditions() -> None:
    conditions = FlightConditions(6, 16, 10, 30, 0.4)
    assert calculate_risk_score(conditions) == 54
    assert classify_risk(54) == "moderate"


def test_score_is_capped_at_100() -> None:
    conditions = FlightConditions(0.5, 30, 30, 10, 1.0)
    assert calculate_risk_score(conditions) == 100
    assert classify_risk(100) == "high"


@pytest.mark.parametrize(
    ("score", "expected"),
    [(0, "low"), (29, "low"), (30, "moderate"), (59, "moderate"), (60, "high"), (100, "high")],
)
def test_risk_classification_boundaries(score: int, expected: str) -> None:
    assert classify_risk(score) == expected


@pytest.mark.parametrize(
    "conditions",
    [
        FlightConditions(-1, 5, 0, 50, 0.1),
        FlightConditions(10, -1, 0, 50, 0.1),
        FlightConditions(10, 5, -1, 50, 0.1),
        FlightConditions(10, 5, 0, -1, 0.1),
        FlightConditions(10, 5, 0, 50, 1.1),
    ],
)
def test_invalid_conditions_are_rejected(conditions: FlightConditions) -> None:
    with pytest.raises(ValueError):
        calculate_risk_score(conditions)


@pytest.mark.parametrize("score", [-1, 101])
def test_invalid_score_is_rejected(score: int) -> None:
    with pytest.raises(ValueError):
        classify_risk(score)

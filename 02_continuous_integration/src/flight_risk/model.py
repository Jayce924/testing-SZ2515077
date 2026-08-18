"""Pure, deterministic business rules suitable for automated CI testing."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FlightConditions:
    visibility_km: float
    wind_speed_ms: float
    precipitation_mm: float
    turnaround_minutes: int
    airport_congestion: float

    def validate(self) -> None:
        if self.visibility_km < 0:
            raise ValueError("visibility_km must be non-negative")
        if self.wind_speed_ms < 0:
            raise ValueError("wind_speed_ms must be non-negative")
        if self.precipitation_mm < 0:
            raise ValueError("precipitation_mm must be non-negative")
        if self.turnaround_minutes < 0:
            raise ValueError("turnaround_minutes must be non-negative")
        if not 0 <= self.airport_congestion <= 1:
            raise ValueError("airport_congestion must be between 0 and 1")


def calculate_risk_score(conditions: FlightConditions) -> int:
    """Return a bounded risk score from 0 to 100."""

    conditions.validate()
    score = 0

    if conditions.visibility_km < 1:
        score += 30
    elif conditions.visibility_km < 5:
        score += 18
    elif conditions.visibility_km < 10:
        score += 8

    if conditions.wind_speed_ms >= 25:
        score += 30
    elif conditions.wind_speed_ms >= 15:
        score += 18
    elif conditions.wind_speed_ms >= 8:
        score += 6

    if conditions.precipitation_mm >= 20:
        score += 20
    elif conditions.precipitation_mm >= 8:
        score += 12
    elif conditions.precipitation_mm > 0:
        score += 4

    if conditions.turnaround_minutes < 20:
        score += 20
    elif conditions.turnaround_minutes < 35:
        score += 10

    score += round(conditions.airport_congestion * 15)
    return min(score, 100)


def classify_risk(score: int) -> str:
    """Map a validated score to a stable reporting category."""

    if not 0 <= score <= 100:
        raise ValueError("score must be between 0 and 100")
    if score < 30:
        return "low"
    if score < 60:
        return "moderate"
    return "high"

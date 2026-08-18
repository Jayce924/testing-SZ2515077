from __future__ import annotations

import pytest

from analyzer import analyze_baseline, analyze_optimized, iter_flight_log


@pytest.mark.parametrize("record_count", [1, 20, 1000])
def test_optimized_result_matches_baseline(record_count: int) -> None:
    baseline = analyze_baseline(iter_flight_log(record_count))
    optimized = analyze_optimized(iter_flight_log(record_count))
    assert optimized == baseline


def test_expected_summary_for_small_dataset() -> None:
    result = analyze_optimized(iter_flight_log(20))
    assert result["records"] == 20
    assert result["days_observed"] == 14
    assert result["cancelled"] == 1
    assert 0 <= result["average_delay_minutes"] <= 90


def test_generator_is_deterministic() -> None:
    assert list(iter_flight_log(25)) == list(iter_flight_log(25))

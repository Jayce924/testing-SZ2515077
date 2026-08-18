"""Baseline and optimized implementations of an aviation log analyzer."""

from __future__ import annotations

from collections import Counter
from datetime import date, datetime, timedelta
from typing import Iterable, Iterator


ROUTES = (
    "NKG-PEK",
    "NKG-SHA",
    "NKG-CAN",
    "NKG-CTU",
    "NKG-SZX",
    "NKG-XMN",
    "NKG-KMG",
    "NKG-CKG",
    "NKG-TAO",
    "NKG-XIY",
    "NKG-HGH",
    "NKG-WUH",
    "NKG-CSX",
    "NKG-TSN",
    "NKG-DLC",
    "NKG-SHE",
    "NKG-FOC",
    "NKG-CGO",
    "NKG-KHN",
    "NKG-URC",
)


def iter_flight_log(record_count: int) -> Iterator[str]:
    """Yield deterministic pipe-separated records without keeping them in memory."""

    start = date(2026, 8, 1)
    for index in range(record_count):
        flight_date = start + timedelta(days=index % 14)
        flight_no = f"MU{2000 + index % 7000:04d}"
        route = ROUTES[(index * 7) % len(ROUTES)]
        delay_minutes = (index * 17) % 91
        if index % 97 == 0:
            status = "CANCELLED"
        elif delay_minutes >= 15:
            status = "DELAYED"
        else:
            status = "ON_TIME"
        note = f"scheduled-operation-record-{index:06d}"
        yield "|".join(
            (
                flight_date.isoformat(),
                flight_no,
                route,
                str(delay_minutes),
                status,
                note,
            )
        )


def _build_summary(
    total: int,
    total_delay: int,
    status_counts: Counter[str],
    route_counts: dict[str, int],
    observed_days: set[object],
) -> dict[str, object]:
    busiest_route = min(route_counts.items(), key=lambda item: (-item[1], item[0]))[0]
    return {
        "records": total,
        "days_observed": len(observed_days),
        "delayed": status_counts["DELAYED"],
        "cancelled": status_counts["CANCELLED"],
        "average_delay_minutes": round(total_delay / total, 2) if total else 0.0,
        "busiest_route": busiest_route,
        "busiest_route_flights": route_counts[busiest_route],
    }


def analyze_baseline(lines: Iterable[str]) -> dict[str, object]:
    """Readable first version with intentional CPU and memory inefficiencies."""

    parsed_records: list[dict[str, object]] = []
    for line in lines:
        day_text, flight_no, route, delay_text, status, note = line.split("|")
        parsed_records.append(
            {
                "day": datetime.strptime(day_text, "%Y-%m-%d").date(),
                "flight_no": flight_no,
                "route": route,
                "delay": int(delay_text),
                "status": status,
                "note": note,
            }
        )

    route_names = [record["route"] for record in parsed_records]
    route_counts = {route: route_names.count(route) for route in set(route_names)}
    status_counts = Counter(str(record["status"]) for record in parsed_records)
    observed_days = {record["day"] for record in parsed_records}
    total_delay = sum(int(record["delay"]) for record in parsed_records)
    return _build_summary(
        len(parsed_records), total_delay, status_counts, route_counts, observed_days
    )


def analyze_optimized(lines: Iterable[str]) -> dict[str, object]:
    """Streaming version that keeps only small aggregate structures."""

    total = 0
    total_delay = 0
    status_counts: Counter[str] = Counter()
    route_counts: Counter[str] = Counter()
    observed_days: set[str] = set()

    for line in lines:
        day_text, _flight_no, route, delay_text, status, _note = line.split("|")
        total += 1
        total_delay += int(delay_text)
        status_counts[status] += 1
        route_counts[route] += 1
        observed_days.add(day_text)

    return _build_summary(
        total, total_delay, status_counts, dict(route_counts), observed_days
    )

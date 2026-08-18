"""Small client and contract checks for the Open-Meteo Forecast API."""

from __future__ import annotations

from typing import Any

import requests


FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_current_weather(
    latitude: float,
    longitude: float,
    *,
    timezone: str = "Asia/Shanghai",
    timeout: float = 10.0,
) -> requests.Response:
    """Call the public forecast endpoint for a compact current-weather payload."""

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": timezone,
    }
    return requests.get(FORECAST_URL, params=params, timeout=timeout)


def assert_forecast_contract(payload: dict[str, Any]) -> None:
    """Validate stable schema and ranges without asserting live values exactly."""

    required_top_level = {
        "latitude",
        "longitude",
        "timezone",
        "current_units",
        "current",
    }
    missing = required_top_level - payload.keys()
    if missing:
        raise AssertionError(f"missing top-level fields: {sorted(missing)}")

    current = payload["current"]
    for field in ("temperature_2m", "relative_humidity_2m", "wind_speed_10m"):
        if field not in current:
            raise AssertionError(f"missing current field: {field}")

    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    wind_speed = current["wind_speed_10m"]

    if not isinstance(temperature, (int, float)) or not -90 <= temperature <= 60:
        raise AssertionError(f"unreasonable temperature: {temperature!r}")
    if not isinstance(humidity, (int, float)) or not 0 <= humidity <= 100:
        raise AssertionError(f"unreasonable humidity: {humidity!r}")
    if not isinstance(wind_speed, (int, float)) or not 0 <= wind_speed <= 500:
        raise AssertionError(f"unreasonable wind speed: {wind_speed!r}")

from __future__ import annotations

import json
from pathlib import Path

import pytest
import requests

from weather_api import FORECAST_URL, assert_forecast_contract, fetch_current_weather


DATA_FILE = Path(__file__).parents[1] / "data" / "airports.json"
AIRPORTS = json.loads(DATA_FILE.read_text(encoding="utf-8"))


@pytest.mark.live_api
@pytest.mark.parametrize("airport", AIRPORTS, ids=[item["name"] for item in AIRPORTS])
def test_airport_forecast_contract(airport: dict[str, object]) -> None:
    response = fetch_current_weather(airport["latitude"], airport["longitude"])

    assert response.status_code == 200
    payload = response.json()
    assert payload["timezone"] == "Asia/Shanghai"
    assert_forecast_contract(payload)


@pytest.mark.live_api
def test_response_declares_units() -> None:
    response = fetch_current_weather(31.742, 118.862)

    assert response.status_code == 200
    units = response.json()["current_units"]
    assert units["temperature_2m"] == "°C"
    assert units["relative_humidity_2m"] == "%"
    assert units["wind_speed_10m"] in {"km/h", "m/s", "mph", "kn"}


@pytest.mark.live_api
@pytest.mark.parametrize("bad_latitude", [-91, 91, 1000])
def test_invalid_latitude_is_rejected(bad_latitude: int) -> None:
    response = requests.get(
        FORECAST_URL,
        params={"latitude": bad_latitude, "longitude": 118.862, "current": "temperature_2m"},
        timeout=10,
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["error"] is True
    assert "latitude" in payload["reason"].lower()


@pytest.mark.live_api
def test_missing_longitude_is_rejected() -> None:
    response = requests.get(
        FORECAST_URL,
        params={"latitude": 31.742, "current": "temperature_2m"},
        timeout=10,
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["error"] is True
    assert "longitude" in payload["reason"].lower()

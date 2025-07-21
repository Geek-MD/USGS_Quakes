"""Sensor for USGS Quakes integration."""

from __future__ import annotations

from typing import Any
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import UnitOfTime
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN

SENSOR_NAME = "USGS Quakes Latest"
SENSOR_UNIQUE_ID = "usgs_quakes_latest"

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the USGS Quakes Latest sensor entity."""
    data = hass.data[DOMAIN].get(entry.entry_id, {})
    events = data.get("events", [])
    device_info = DeviceInfo(
        identifiers={(DOMAIN, "usgs_quakes")},
        name="USGS Quakes",
        manufacturer="USGS",
        entry_type="service",
        configuration_url="https://earthquake.usgs.gov/",
    )
    async_add_entities([UsgsQuakesLatestSensor(events, device_info)], True)

class UsgsQuakesLatestSensor(SensorEntity):
    """Sensor to store the latest USGS quake events."""

    _attr_has_entity_name = True
    _attr_name = SENSOR_NAME
    _attr_unique_id = SENSOR_UNIQUE_ID
    _attr_icon = "mdi:pulse"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_native_unit_of_measurement = UnitOfTime.SECONDS
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, events: list[dict[str, Any]], device_info: DeviceInfo) -> None:
        self._events = events or []
        self._attr_device_info = device_info
        self._attr_native_value = self._events[-1]["time"] if self._events else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {
            "events": self._events[-10:] if self._events else []
        }

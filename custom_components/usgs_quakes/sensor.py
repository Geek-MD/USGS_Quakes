"""Sensor for USGS Quakes integration."""

from __future__ import annotations

from typing import Any
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN

SENSOR_NAME = "USGS Quakes Latest"
SENSOR_UNIQUE_ID = "usgs_quakes_latest"

# Usa la misma convención f-string que geo_location.py
SIGNAL_EVENTS_UPDATED = f"{DOMAIN}_events_updated_{{}}"

class UsgsQuakesLatestSensor(SensorEntity):
    """Sensor to store the latest USGS quake events."""

    _attr_has_entity_name = True
    _attr_name = SENSOR_NAME
    _attr_unique_id = SENSOR_UNIQUE_ID
    _attr_icon = "mdi:pulse"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, hass, entry_id: str, device_info: DeviceInfo) -> None:
        self.hass = hass
        self._entry_id = entry_id
        self._attr_device_info = device_info
        self._events: list[dict[str, Any]] = []
        self._unsub_dispatcher = None
        self._attr_native_value = None

    async def async_added_to_hass(self):
        # Escucha actualizaciones del feed usando el mismo signal
        self._unsub_dispatcher = async_dispatcher_connect(
            self.hass,
            SIGNAL_EVENTS_UPDATED.format(self._entry_id),
            self._async_update_events,
        )
        await self._async_update_events()

    async def async_will_remove_from_hass(self):
        if self._unsub_dispatcher:
            self._unsub_dispatcher()
            self._unsub_dispatcher = None

    @callback
    async def _async_update_events(self):
        """Update sensor state from the shared event list."""
        events = self.hass.data[DOMAIN][self._entry_id].get("events", [])
        self._events = events[-10:] if events else []
        self._attr_native_value = self._events[-1]["time"] if self._events else None
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {
            "events": self._events
        }


async def async_setup_entry(hass, entry, async_add_entities):
    device_info = DeviceInfo(
        identifiers={(DOMAIN, "usgs_quakes")},
        name="USGS Quakes Feed",
        manufacturer="USGS",
        entry_type="service",
        configuration_url="https://earthquake.usgs.gov/",
    )
    async_add_entities([UsgsQuakesLatestSensor(hass, entry.entry_id, device_info)], True)

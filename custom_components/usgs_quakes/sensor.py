"""Sensor for USGS Quakes integration."""

from __future__ import annotations

from typing import Any
from datetime import datetime

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

import logging

_LOGGER = logging.getLogger(__name__)

SENSOR_NAME = "USGS Quakes Latest"
SENSOR_UNIQUE_ID = "usgs_quakes_latest"

SIGNAL_EVENTS_UPDATED = f"{DOMAIN}_events_updated_{{}}"


class UsgsQuakesLatestSensor(SensorEntity):
    """Sensor to store the latest USGS quake events."""

    _attr_has_entity_name = True
    _attr_name = SENSOR_NAME
    _attr_unique_id = SENSOR_UNIQUE_ID
    _attr_icon = "mdi:pulse"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, hass: HomeAssistant, entry_id: str, device_info: DeviceInfo) -> None:
        self.hass = hass
        self._entry_id = entry_id
        self._attr_device_info = device_info
        self._events: list[dict[str, Any]] = []
        self._unsub_dispatcher: Any = None
        self._attr_native_value: str | None = None

    async def async_added_to_hass(self) -> None:
        # Escucha actualizaciones del feed usando el mismo signal
        self._unsub_dispatcher = async_dispatcher_connect(
            self.hass,
            SIGNAL_EVENTS_UPDATED.format(self._entry_id),
            self._async_update_events,
        )
        await self._async_update_events()

    async def async_will_remove_from_hass(self) -> None:
        if self._unsub_dispatcher:
            self._unsub_dispatcher()
            self._unsub_dispatcher = None

    @callback
    async def _async_update_events(self) -> None:
        """Update sensor state from the shared event list."""
        events = self.hass.data[DOMAIN][self._entry_id].get("events", [])

        def parse_time(e: dict[str, Any]) -> datetime:
            try:
                # Admite fechas con o sin Z al final
                t = str(e["time"])
                if t.endswith("Z"):
                    t = t.replace("Z", "+00:00")
                return datetime.fromisoformat(t)
            except Exception:
                return datetime.min

        # Ordena del más nuevo al más antiguo según fecha/hora real
        self._events = sorted(events, key=parse_time, reverse=True) if events else []
        if self._events:
            self._attr_native_value = self._events[0]["time"]
        else:
            self._attr_native_value = None

        _LOGGER.debug(
            "USGS Quakes Sensor actualizado. Eventos almacenados: %d. Último evento: %s",
            len(self._events),
            self._attr_native_value,
        )
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {
            "events": self._events
        }


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    device_info = DeviceInfo(
        identifiers={(DOMAIN, "usgs_quakes")},
        name="USGS Quakes Feed",
        manufacturer="USGS",
        entry_type="service",
        configuration_url="https://earthquake.usgs.gov/",
    )
    async_add_entities([UsgsQuakesLatestSensor(hass, entry.entry_id, device_info)], True)

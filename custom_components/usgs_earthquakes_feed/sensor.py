"""Sensor for USGS Quakes integration."""

from __future__ import annotations

from typing import Any
from datetime import datetime, timezone

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.dt import as_local

from .const import DOMAIN
from .helpers import parse_event_time

import logging

_LOGGER = logging.getLogger(__name__)

SENSOR_NAME = "USGS Quakes Latest"
SENSOR_UNIQUE_ID = "usgs_earthquakes_feed_latest"

SIGNAL_EVENTS_UPDATED = f"{DOMAIN}_events_updated_{{}}"


class UsgsQuakesLatestSensor(SensorEntity):
    """Sensor to store the latest USGS quake events."""

    _attr_has_entity_name = True
    _attr_name = SENSOR_NAME
    _attr_unique_id = SENSOR_UNIQUE_ID
    _attr_suggested_object_id = SENSOR_UNIQUE_ID
    _attr_icon = "mdi:pulse"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    
    def __init__(self, hass: HomeAssistant, entry_id: str, device_info: DeviceInfo) -> None:
        self.hass = hass
        self._entry_id = entry_id
        self._attr_device_info = device_info
        self._seen_ids: set[str] = set()
        self._latest_events: list[dict[str, Any]] = []
        self._unsub_dispatcher: Any = None
        self._attr_native_value: datetime | None = None

    async def async_added_to_hass(self) -> None:
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

    async def _async_update_events(self) -> None:
        """Update sensor state from the shared event list."""
        new_events = self.hass.data[DOMAIN][self._entry_id].get("events", [])

        # Determinar qué eventos son nuevos (no vistos antes)
        filtered_events = [e for e in new_events if e["id"] not in self._seen_ids]

        # Registrar los nuevos IDs como vistos
        self._seen_ids.update(e["id"] for e in filtered_events)

        # latest_events: solo los eventos nuevos de este ciclo, del más reciente al más antiguo
        self._latest_events = sorted(filtered_events, key=parse_event_time, reverse=True)

        # Publicar latest_events en hass.data para que el servicio format_events pueda leerlos
        entry_data = self.hass.data[DOMAIN].setdefault(self._entry_id, {})
        entry_data["latest_events"] = self._latest_events

        # Actualizar el estado del sensor solo cuando lleguen eventos nuevos
        if self._latest_events:
            try:
                time_val = self._latest_events[0]["time"]
                if isinstance(time_val, datetime):
                    dt = time_val if time_val.tzinfo else time_val.replace(tzinfo=timezone.utc)
                else:
                    dt = datetime.fromisoformat(str(time_val).replace("Z", "+00:00"))
                self._attr_native_value = as_local(dt)
            except (ValueError, AttributeError):
                _LOGGER.debug("Could not parse native value from event time: %s", self._latest_events[0].get("time"))

        _LOGGER.debug(
            "USGS Quakes Sensor actualizado. Nuevos eventos: %d.",
            len(filtered_events),
        )
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {
            "latest_events": self._latest_events,
        }


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    device_info = DeviceInfo(
        identifiers={(DOMAIN, "usgs_earthquakes_feed")},
        name="USGS Quakes Feed",
        manufacturer="USGS",
        entry_type="service",
        configuration_url="https://earthquake.usgs.gov/",
    )
    async_add_entities([UsgsQuakesLatestSensor(hass, entry.entry_id, device_info)], True)

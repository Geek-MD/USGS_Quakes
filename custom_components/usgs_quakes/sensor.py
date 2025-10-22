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
from homeassistant.util.dt import as_local

from .const import DOMAIN

import logging

_LOGGER = logging.getLogger(__name__)

SENSOR_NAME = "USGS Quakes Latest"
SENSOR_UNIQUE_ID = "usgs_quakes_latest"

SIGNAL_EVENTS_UPDATED = f"{DOMAIN}_events_updated_{{}}"

MAX_EVENTS = 50  # Máximo de eventos a almacenar


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
        self._events: list[dict[str, Any]] = []
        self._unsub_dispatcher: Any = None
        self._attr_native_value: str | None = None

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

    @callback
    async def _async_update_events(self) -> None:
        """Update sensor state from the shared event list."""
        new_events = self.hass.data[DOMAIN][self._entry_id].get("events", [])

        # Crear conjunto con las ids ya almacenadas
        existing_ids = {e["id"] for e in self._events}

        # Determinar si es primera ejecución (sin eventos guardados)
        if not self._events:
            filtered_events = new_events
        else:
            filtered_events = [e for e in new_events if e["id"] not in existing_ids]

        def parse_time(e: dict[str, Any]) -> datetime:
            t = str(e["time"])
            if t.endswith("Z"):
                t = t.replace("Z", "+00:00")
            try:
                return datetime.fromisoformat(t)
            except Exception:
                return datetime.min

        # Agregar nuevos eventos y reordenar
        self._events.extend(filtered_events)
        self._events = sorted(self._events, key=parse_time, reverse=True)[:MAX_EVENTS]

        # Actualizar valor del sensor (fecha del más reciente)
        if self._events:
            try:
                dt = datetime.fromisoformat(self._events[0]["time"].replace("Z", "+00:00"))
                self._attr_native_value = as_local(dt)
            except Exception:
                self._attr_native_value = None
        else:
            self._attr_native_value = None

        _LOGGER.debug(
            "USGS Quakes Sensor actualizado. Nuevos eventos: %d. Total almacenados: %d.",
            len(filtered_events),
            len(self._events),
        )
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        formatted_lines = []

        for e in self._events:
            # Fecha y hora local
            dt_str = e.get("time", "")
            try:
                dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
                dt_str = as_local(dt).strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                pass

            # Coordenadas
            coords = e.get("coordinates", [None, None])
            lat = coords[0]
            lon = coords[1]
            maps_url = f"https://www.google.com/maps?q={lat},{lon}" if lat is not None and lon is not None else "N/A"

            # Formato
            text = (
                f"{e.get('title', 'N/A')}\n"
                f"Lugar: {e.get('place', 'N/A')}\n"
                f"Magnitud: {e.get('magnitude', 'N/A')} Mw\n"
                f"Fecha/Hora: {dt_str}\n"
                f"Localización: {maps_url}"
            )
            formatted_lines.append(text)

        return {
            "events": self._events,
            "formatted_events": "\n\n".join(formatted_lines),
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

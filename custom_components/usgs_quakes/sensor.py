"""Sensor to track the latest USGS earthquake events."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the USGS Quakes latest events sensor."""
    feed_manager = hass.data[DOMAIN][entry.entry_id]["feed_manager"]
    sensor = UsgsQuakesLatestSensor(feed_manager, entry.entry_id)
    async_add_entities([sensor])


class UsgsQuakesLatestSensor(SensorEntity, RestoreEntity):
    """Sensor that stores the latest USGS earthquakes."""

    _attr_has_entity_name = True
    _attr_name = "Latest Earthquakes"
    _attr_icon = "mdi:earth"
    _attr_attribution = "Data provided by the USGS Earthquake Hazards Program"
    _attr_native_unit_of_measurement = None

    def __init__(self, feed_manager, entry_id: str) -> None:
        """Initialize the sensor."""
        self._entry_id = entry_id
        self._feed_manager = feed_manager
        self._attr_unique_id = f"{entry_id}_latest"
        self._last_event_ids: set[str] = set()

    async def async_added_to_hass(self) -> None:
        """Handle when entity is added to hass."""
        await super().async_added_to_hass()
        self._feed_manager.register_listener(self._update_from_feed)

    async def async_will_remove_from_hass(self) -> None:
        """Handle when entity will be removed."""
        self._feed_manager.unregister_listener(self._update_from_feed)

    def _update_from_feed(self) -> None:
        """Process the feed update from the manager."""
        new_events = []
        seen_ids = set()
        entries = self._feed_manager.last_entries

        for entry in entries:
            event_id = entry.external_id
            seen_ids.add(event_id)

            # Solo agregar si es un nuevo evento
            if event_id not in self._last_event_ids:
                new_events.append({
                    "title": entry.title,
                    "magnitude": entry.magnitude,
                    "latitude": entry.latitude,
                    "longitude": entry.longitude,
                    "distance": entry.distance,
                    "time": entry.publication_date.isoformat(),
                    "id": event_id,
                })

        if new_events:
            # Mantener máximo 10 eventos
            combined = new_events + [
                e for e in getattr(self, "events", []) if e["id"] not in {e["id"] for e in new_events}
            ]
            self.events = combined[:10]
            self._last_event_ids = seen_ids
            if self.events:
                latest = max(self.events, key=lambda x: x["time"])
                self._attr_native_value = latest["time"]
            else:
                self._attr_native_value = None

            self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return attributes with recent events."""
        return {
            ATTR_ATTRIBUTION: self._attr_attribution,
            "events": getattr(self, "events", []),
        }

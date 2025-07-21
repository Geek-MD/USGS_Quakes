"""Sensor: USGS Quakes latest events."""
from __future__ import annotations

from datetime import datetime
import logging

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the USGS Quakes latest sensor."""
    data = hass.data[DOMAIN].get(entry.entry_id, {})
    feed_manager = data.get("feed_manager")

    if not feed_manager:
        _LOGGER.error("Feed manager not found for USGS Quakes sensor (entry_id: %s)", entry.entry_id)
        return

    async_add_entities([UsgsQuakesLatestSensor(feed_manager)], True)

class UsgsQuakesLatestSensor(SensorEntity):
    """Sensor that stores the latest USGS earthquake events."""

    _attr_has_entity_name = True
    _attr_name = "USGS Quakes Latest"
    _attr_unique_id = "usgs_quakes_latest"
    _attr_icon = "mdi:pulse"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(self, feed_manager):
        self._feed_manager = feed_manager
        self._latest_event_time = None
        self._events = []

    async def async_update(self):
        # Get current feed entries from the feed_manager
        entries = list(self._feed_manager.feed_entries.values())
        if not entries:
            return

        # Sort by time, filter by configured min_magnitude if present
        entries.sort(key=lambda e: e.time or datetime.min, reverse=True)

        # Only latest 10 events
        self._events = []
        seen_ids = set()
        for entry in entries:
            # Avoid duplicates by external_id
            if entry.external_id in seen_ids:
                continue
            seen_ids.add(entry.external_id)
            self._events.append({
                "external_id": entry.external_id,
                "title": entry.title,
                "magnitude": entry.magnitude,
                "place": entry.place,
                "time": entry.time.isoformat() if entry.time else None,
                "updated": entry.updated.isoformat() if entry.updated else None,
                "coordinates": entry.coordinates,
            })
            if len(self._events) == 10:
                break

        if self._events:
            self._latest_event_time = self._events[0]["time"]
            self._attr_native_value = self._latest_event_time
        else:
            self._attr_native_value = None

    @property
    def extra_state_attributes(self):
        return {
            "events": self._events,
            "attribution": "USGS Earthquake Hazards Program",
        }

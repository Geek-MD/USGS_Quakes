from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, CONF_MINIMUM_MAGNITUDE

_LOGGER = logging.getLogger(__name__)

ATTR_EVENTS = "events"
ATTR_LAST_UPDATE = "last_update"
ATTRIBUTION = "Data provided by the USGS Earthquake Hazards Program"


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up manually is not supported."""
    return


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """Set up the latest earthquake sensor."""
    if DOMAIN not in hass.data or entry.entry_id not in hass.data[DOMAIN]:
        return

    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    min_magnitude = entry.options.get(CONF_MINIMUM_MAGNITUDE, 0.0)

    sensor = LatestEarthquakeSensor(coordinator, entry.entry_id, min_magnitude)
    async_add_entities([sensor], True)


class LatestEarthquakeSensor(SensorEntity, CoordinatorEntity):
    """Sensor that stores the latest USGS earthquake events."""

    _attr_icon = "mdi:earth"
    _attr_has_entity_name = True
    _attr_translation_key = "latest_quake"
    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator, entry_id: str, min_magnitude: float) -> None:
        super().__init__(coordinator)
        self._attr_name = "Latest Earthquakes"
        self._attr_unique_id = f"{entry_id}_latest"
        self._entry_id = entry_id
        self._min_magnitude = min_magnitude
        self._events_seen = set()
        self._latest = None

    @property
    def state(self) -> str | None:
        return self._latest.isoformat() if self._latest else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {
            ATTR_EVENTS: self._get_recent_events(),
            ATTR_LAST_UPDATE: datetime.utcnow().isoformat(),
            ATTR_ATTRIBUTION: self._attr_attribution,
        }

    def _get_recent_events(self) -> list[dict[str, Any]]:
        new_events = []
        seen = self._events_seen.copy()

        for event in self.coordinator.feed_manager.feed.entries:
            if event.external_id in seen:
                continue

            if event.magnitude is not None and event.magnitude < self._min_magnitude:
                continue

            seen.add(event.external_id)

            new_events.append({
                "title": event.title,
                "magnitude": event.magnitude,
                "time": event.time.isoformat() if event.time else None,
                "latitude": event.coordinates[0],
                "longitude": event.coordinates[1],
                "depth": event.coordinates[2],
                "external_id": event.external_id,
                "link": event.link,
            })

        # Update internal record
        if new_events:
            self._events_seen.update(e["external_id"] for e in new_events)
            self._latest = max(
                [datetime.fromisoformat(e["time"]) for e in new_events if e["time"]],
                default=self._latest,
            )

        return new_events[-10:]  # Keep last 10

    async def async_update(self) -> None:
        """Trigger manual update if needed."""
        await self.coordinator.async_request_refresh()

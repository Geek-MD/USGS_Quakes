"""Support for USGS Quakes geolocation integration."""

from __future__ import annotations

from datetime import timedelta
from typing import Any, Callable

import logging

from aio_geojson_usgs_earthquakes import UsgsEarthquakeHazardsProgramFeedManager
from aio_geojson_usgs_earthquakes.feed_entry import UsgsEarthquakeHazardsProgramFeedEntry

from homeassistant.components.geo_location import GeolocationEvent
from homeassistant.const import ATTR_TIME, EVENT_HOMEASSISTANT_START, UnitOfLength
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect, async_dispatcher_send
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)

SIGNAL_DELETE_ENTITY = "usgs_quakes_delete_{}"
SIGNAL_UPDATE_ENTITY = "usgs_quakes_update_{}"
SIGNAL_EVENTS_UPDATED = f"{DOMAIN}_events_updated_{{}}"

SOURCE = "usgs_quakes"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: Any,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up USGS Quakes platform."""
    data = config_entry.data
    entry_id = config_entry.entry_id
    options = config_entry.options

    coordinates = (
        data.get("latitude"),
        data.get("longitude"),
    )

    feed_type = options.get("feed_type", data.get("feed_type"))
    radius = options.get("radius", data.get("radius"))
    minimum_magnitude = options.get("minimum_magnitude", data.get("minimum_magnitude"))

    manager = UsgsQuakesFeedEntityManager(
        hass,
        async_add_entities,
        coordinates,
        feed_type,
        radius,
        minimum_magnitude,
        entry_id,
    )

    hass.data.setdefault(DOMAIN, {})[entry_id] = {}
    hass.data[DOMAIN][entry_id]["manager"] = manager
    await manager.async_init()

    async def start_feed_manager(event: Any = None) -> None:
        _LOGGER.debug("USGS Quakes: Inicio de actualización tras EVENT_HOMEASSISTANT_START")
        await manager.async_update()

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, start_feed_manager)


class UsgsQuakesFeedEntityManager:
    """Manages entities from USGS feed."""

    def __init__(
        self,
        hass: HomeAssistant,
        async_add_entities: AddEntitiesCallback,
        coordinates: tuple[float, float],
        feed_type: str,
        radius: float,
        minimum_magnitude: float,
        entry_id: str,
    ) -> None:
        self._hass = hass
        self._async_add_entities = async_add_entities
        self._entry_id = entry_id
        session = async_get_clientsession(hass)

        self._feed_manager = UsgsEarthquakeHazardsProgramFeedManager(
            session,
            self._generate_entity,
            self._update_entity,
            self._remove_entity,
            coordinates,
            feed_type,
            filter_radius=radius,
            filter_minimum_magnitude=minimum_magnitude,
        )
        self._latest_events: list[dict[str, Any]] = []

    async def async_init(self) -> None:
        async def update(event_time: Any) -> None:
            _LOGGER.debug("USGS Quakes: Ejecutando actualización periódica del feed")
            await self.async_update()

        async_track_time_interval(
            self._hass, update, SCAN_INTERVAL, cancel_on_shutdown=True
        )
        _LOGGER.debug("Feed entity manager initialized")
        await self.async_update()  # Ensure first fetch on init

    async def async_update(self) -> None:
        _LOGGER.debug("USGS Quakes: Ejecutando async_update (manager)")
        await self._feed_manager.update()
        _LOGGER.debug("Feed entity manager updated. Entradas del feed: %d", len(self._feed_manager.feed_entries))

        # Build a list of all current events
        latest_events = []
        for entry in self._feed_manager.feed_entries.values():
            latest_events.append({
                "id": entry.external_id,
                "title": entry.title,
                "place": entry.place,
                "magnitude": entry.magnitude,
                "time": entry.time,
                "updated": entry.updated,
                "coordinates": entry.coordinates,
                "distance": entry.distance_to_home,
            })

        # Sort events by time (most recent first)
        latest_events.sort(key=lambda e: e["time"], reverse=True)
        self._latest_events = latest_events

        # Share with other platforms (sensor)
        if self._entry_id in self._hass.data.get(DOMAIN, {}):
            self._hass.data[DOMAIN][self._entry_id]["events"] = self._latest_events
        else:
            _LOGGER.warning(
                "Entry ID %s not found in hass.data[DOMAIN]. Entity will not update events.",
                self._entry_id,
            )
            return

        # Dispatch update for sensor
        async_dispatcher_send(self._hass, SIGNAL_EVENTS_UPDATED.format(self._entry_id))

    def get_entry(self, external_id: str) -> UsgsEarthquakeHazardsProgramFeedEntry | None:
        return self._feed_manager.feed_entries.get(external_id)

    async def _generate_entity(self, external_id: str) -> None:
        entity = UsgsQuakesEvent(self, external_id)
        self._async_add_entities([entity], True)

    async def _update_entity(self, external_id: str) -> None:
        async_dispatcher_send(self._hass, SIGNAL_UPDATE_ENTITY.format(external_id))

    async def _remove_entity(self, external_id: str) -> None:
        async_dispatcher_send(self._hass, SIGNAL_DELETE_ENTITY.format(external_id))


class UsgsQuakesEvent(GeolocationEvent):
    """Represents a USGS earthquake event."""

    _attr_source = SOURCE
    _attr_should_poll = False
    _attr_unit_of_measurement = UnitOfLength.KILOMETERS
    _attr_icon = "mdi:pulse"

    def __init__(self, manager: UsgsQuakesFeedEntityManager, external_id: str) -> None:
        self._manager = manager
        self._external_id = external_id
        self._remove_signal_delete: Callable[[], None]
        self._remove_signal_update: Callable[[], None]
        self._place = None
        self._magnitude = None
        self._time = None
        self._updated = None
        self._status = None
        self._type = None
        self._alert = None

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, "usgs_quakes")},
            name="USGS Quakes Feed",
            manufacturer="USGS",
            entry_type="service",
            configuration_url="https://earthquake.usgs.gov/",
        )

    async def async_added_to_hass(self) -> None:
        self._remove_signal_delete = async_dispatcher_connect(
            self.hass, SIGNAL_DELETE_ENTITY.format(self._external_id), self._delete_callback
        )
        self._remove_signal_update = async_dispatcher_connect(
            self.hass, SIGNAL_UPDATE_ENTITY.format(self._external_id), self._update_callback
        )

    @callback
    def _delete_callback(self) -> None:
        self._remove_signal_delete()
        self._remove_signal_update()
        self.hass.async_create_task(self.async_remove(force_remove=True))

    @callback
    def _update_callback(self) -> None:
        self.async_schedule_update_ha_state(True)

    async def async_update(self) -> None:
        feed_entry = self._manager.get_entry(self._external_id)
        if feed_entry:
            self._update_from_feed(feed_entry)

    def _update_from_feed(self, entry: UsgsEarthquakeHazardsProgramFeedEntry) -> None:
        self._attr_name = entry.title
        self._attr_distance = entry.distance_to_home
        self._attr_latitude = entry.coordinates[0]
        self._attr_longitude = entry.coordinates[1]
        self._attr_attribution = entry.attribution
        self._time = entry.time
        self._place = entry.place
        self._magnitude = entry.magnitude
        self._updated = entry.updated
        self._status = entry.status
        self._type = entry.type
        self._alert = entry.alert

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {
            key: value
            for key, value in (
                ("external_id", self._external_id),
                ("place", self._place),
                ("magnitude", self._magnitude),
                (ATTR_TIME, self._time),
                ("updated", self._updated),
                ("status", self._status),
                ("type", self._type),
                ("alert", self._alert),
            )
            if value is not None
        }

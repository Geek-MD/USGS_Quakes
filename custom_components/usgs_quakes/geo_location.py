from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import datetime, timedelta
from typing import Any

from aio_geojson_usgs_earthquakes import UsgsEarthquakeHazardsProgramFeedManager
from aio_geojson_usgs_earthquakes.feed_entry import UsgsEarthquakeHazardsProgramFeedEntry

from homeassistant.components.geo_location import GeolocationEvent
from homeassistant.const import ATTR_TIME, EVENT_HOMEASSISTANT_START, UnitOfLength
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.dispatcher import async_dispatcher_connect, async_dispatcher_send
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.typing import ConfigType

from .const import (
    DOMAIN,
    CONF_FEED_TYPE,
    CONF_MINIMUM_MAGNITUDE,
    VALID_FEED_TYPES,
    DEFAULT_MINIMUM_MAGNITUDE,
    DEFAULT_RADIUS_IN_KM,
)

_LOGGER = logging.getLogger(__name__)

ATTR_ALERT = "alert"
ATTR_EXTERNAL_ID = "external_id"
ATTR_MAGNITUDE = "magnitude"
ATTR_PLACE = "place"
ATTR_STATUS = "status"
ATTR_TYPE = "type"
ATTR_UPDATED = "updated"

SCAN_INTERVAL = timedelta(minutes=5)

SIGNAL_DELETE_ENTITY = "usgs_quakes_delete_{}"
SIGNAL_UPDATE_ENTITY = "usgs_quakes_update_{}"

SOURCE = DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigType, async_add_entities: AddEntitiesCallback) -> None:
    config = entry.data

    coordinates = (config["latitude"], config["longitude"])
    radius = config["radius"]
    magnitude = config["minimum_magnitude"]
    feed_type = config["feed_type"]

    manager = UsgsEarthquakesFeedEntityManager(
        hass, async_add_entities, SCAN_INTERVAL, coordinates, feed_type, radius, magnitude
    )
    await manager.async_init()

    async def start_feed_manager(event=None):
        await manager.async_update()

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, start_feed_manager)


class UsgsEarthquakesFeedEntityManager:
    def __init__(
        self,
        hass: HomeAssistant,
        async_add_entities: AddEntitiesCallback,
        scan_interval: timedelta,
        coordinates: tuple[float, float],
        feed_type: str,
        radius_in_km: float,
        minimum_magnitude: float,
    ) -> None:
        self._hass = hass
        websession = aiohttp_client.async_get_clientsession(hass)
        self._feed_manager = UsgsEarthquakeHazardsProgramFeedManager(
            websession,
            self._generate_entity,
            self._update_entity,
            self._remove_entity,
            coordinates,
            feed_type,
            filter_radius=radius_in_km,
            filter_minimum_magnitude=minimum_magnitude,
        )
        self._async_add_entities = async_add_entities
        self._scan_interval = scan_interval

    async def async_init(self) -> None:
        async def update(event_time: datetime) -> None:
            await self.async_update()

        async_track_time_interval(
            self._hass, update, self._scan_interval, cancel_on_shutdown=True
        )
        _LOGGER.debug("Feed entity manager initialized")

    async def async_update(self) -> None:
        await self._feed_manager.update()
        _LOGGER.debug("Feed entity manager updated")

    def get_entry(self, external_id: str) -> UsgsEarthquakeHazardsProgramFeedEntry | None:
        return self._feed_manager.feed_entries.get(external_id)

    async def _generate_entity(self, external_id: str) -> None:
        new_entity = UsgsEarthquakesEvent(self, external_id)
        self._async_add_entities([new_entity], True)

    async def _update_entity(self, external_id: str) -> None:
        async_dispatcher_send(self._hass, SIGNAL_UPDATE_ENTITY.format(external_id))

    async def _remove_entity(self, external_id: str) -> None:
        async_dispatcher_send(self._hass, SIGNAL_DELETE_ENTITY.format(external_id))


class UsgsEarthquakesEvent(GeolocationEvent):
    _attr_icon = "mdi:pulse"
    _attr_should_poll = False
    _attr_source = SOURCE
    _attr_unit_of_measurement = UnitOfLength.KILOMETERS

    def __init__(self, feed_manager: UsgsEarthquakesFeedEntityManager, external_id: str) -> None:
        self._feed_manager = feed_manager
        self._external_id = external_id
        self._place = None
        self._magnitude = None
        self._time = None
        self._updated = None
        self._status = None
        self._type = None
        self._alert = None
        self._remove_signal_delete: Callable[[], None]
        self._remove_signal_update: Callable[[], None]

    async def async_added_to_hass(self) -> None:
        self._remove_signal_delete = async_dispatcher_connect(
            self.hass,
            SIGNAL_DELETE_ENTITY.format(self._external_id),
            self._delete_callback,
        )
        self._remove_signal_update = async_dispatcher_connect(
            self.hass,
            SIGNAL_UPDATE_ENTITY.format(self._external_id),
            self._update_callback,
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
        _LOGGER.debug("Updating %s", self._external_id)
        feed_entry = self._feed_manager.get_entry(self._external_id)
        if feed_entry:
            self._update_from_feed(feed_entry)

    def _update_from_feed(self, feed_entry: UsgsEarthquakeHazardsProgramFeedEntry) -> None:
        self._attr_name = feed_entry.title
        self._attr_distance = feed_entry.distance_to_home
        self._attr_latitude = feed_entry.coordinates[0]
        self._attr_longitude = feed_entry.coordinates[1]
        self._attr_attribution = feed_entry.attribution
        self._place = feed_entry.place
        self._magnitude = feed_entry.magnitude
        self._time = feed_entry.time
        self._updated = feed_entry.updated
        self._status = feed_entry.status
        self._type = feed_entry.type
        self._alert = feed_entry.alert

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {
            key: value
            for key, value in (
                (ATTR_EXTERNAL_ID, self._external_id),
                (ATTR_PLACE, self._place),
                (ATTR_MAGNITUDE, self._magnitude),
                (ATTR_TIME, self._time),
                (ATTR_UPDATED, self._updated),
                (ATTR_STATUS, self._status),
                (ATTR_TYPE, self._type),
                (ATTR_ALERT, self._alert),
            )
            if value or isinstance(value, bool)
        }

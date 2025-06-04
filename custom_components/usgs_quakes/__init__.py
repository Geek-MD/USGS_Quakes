from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .sensor import USGSDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # Inicializar feed y coordinator
    from aio_geojson_usgs_earthquakes import USGSEarthquakeFeed

    latitude = entry.data["latitude"]
    longitude = entry.data["longitude"]
    radius = entry.data["radius"]
    min_mag = entry.data.get("minimum_magnitude", 0.0)
    feed_type = entry.data.get("feed_type", "past_day_all")

    feed = USGSEarthquakeFeed(
        home_coordinates=(latitude, longitude),
        filter_radius=radius,
        filter_minimum_magnitude=min_mag,
        feed_type=feed_type
    )

    coordinator = USGSDataUpdateCoordinator(hass, feed)
    await coordinator.async_refresh()

    # Guardar en hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
    }

    # Reenviar a plataformas
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "geo_location")
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = all(await asyncio.gather(
        hass.config_entries.async_forward_entry_unload(entry, "sensor"),
        hass.config_entries.async_forward_entry_unload(entry, "geo_location")
    ))

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

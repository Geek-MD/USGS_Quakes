"""USGS Quakes integration."""
from __future__ import annotations

import logging
from typing import Any

from aio_geojson_usgs_earthquakes import (
    UsgsEarthquakeHazardsProgramFeed,
    UsgsEarthquakeHazardsProgramFeedManager,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.storage import STORAGE_DIR, Store

from .const import (
    DOMAIN,
    PLATFORMS,
    STORAGE_VERSION,
    STORAGE_KEY,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the USGS Quakes integration (legacy config)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up USGS Quakes from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Load previous events from storage
    store = Store(hass, STORAGE_VERSION, f"{STORAGE_KEY}_{entry.entry_id}.json")
    stored = await store.async_load()
    if stored is None:
        stored = {"event_ids": []}

    hass.data[DOMAIN][entry.entry_id] = {
        "store": store,
        "event_ids": stored.get("event_ids", []),
    }

    # Forward config to the platform(s)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Reload config entry if options are updated
    entry.async_on_unload(entry.add_update_listener(_update_listener))

    return True


async def _update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    _LOGGER.debug("Reloading config entry %s due to options update", entry.entry_id)
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok and DOMAIN in hass.data:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok


async def async_get_options_flow(config_entry: ConfigEntry):
    """Return the options flow handler."""
    from .options_flow import OptionsFlowHandler
    return OptionsFlowHandler(config_entry)

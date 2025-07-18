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
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry
from homeassistant.helpers.typing import ConfigType

from .const import (
    DOMAIN,
    PLATFORMS,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the USGS Quakes integration (legacy config)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up USGS Quakes from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Forward config to the platform(s)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register listener to reload if options are updated
    entry.async_on_unload(entry.add_update_listener(_update_listener))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok and DOMAIN in hass.data:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok


async def _update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update by reloading the entry."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_get_options_flow(config_entry: ConfigEntry):
    from .options_flow import OptionsFlowHandler
    return OptionsFlowHandler(config_entry)

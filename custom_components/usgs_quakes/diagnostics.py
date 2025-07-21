"""Diagnostics support for USGS Quakes integration."""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict:
    """Return diagnostics for a config entry."""
    data = hass.data.get(DOMAIN, {}).get(entry.entry_id, {}).copy()
    # Solo exponer los eventos y la config relevante (sin exponer info sensible)
    diagnostics = {
        "config": entry.data,
        "options": entry.options,
        "events": data.get("events", []),
    }
    return diagnostics

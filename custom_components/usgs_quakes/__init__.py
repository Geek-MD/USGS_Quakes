from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN
from .coordinator import UsgsEarthquakeFeedCoordinator

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True  # No YAML support

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator = UsgsEarthquakeFeedCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "geo_location")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "geo_location")
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

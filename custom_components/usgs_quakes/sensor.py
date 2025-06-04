from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    # Placeholder until we re-implement the actual USGS data logic
    async_add_entities([
        DummyUSGSSensor(entry.data)
    ])


class DummyUSGSSensor(SensorEntity):
    def __init__(self, config):
        self._attr_name = "USGS Quakes Dummy Sensor"
        self._attr_unique_id = "usgs_quakes_dummy"
        self._config = config

    @property
    def native_value(self):
        return f"Lat: {self._config.get('latitude')}, Lon: {self._config.get('longitude')}"

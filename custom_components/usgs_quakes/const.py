DOMAIN = "usgs_quakes"

CONF_RADIUS = "radius"
CONF_MINIMUM_MAGNITUDE = "minimum_magnitude"
CONF_FEED_TYPE = "feed_type"
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"

DEFAULT_RADIUS = 50.0
DEFAULT_MINIMUM_MAGNITUDE = 0.0

# Plataformas activadas por la integración
PLATFORMS = ["geo_location", "sensor"]

# Claves de almacenamiento
STORAGE_KEY = "usgs_quakes_events"
STORAGE_VERSION = 1

# Tipos de feed válidos
VALID_FEED_TYPES = [
    "past_hour_all_earthquakes",
    "past_hour_significant_earthquakes",
    "past_day_all_earthquakes",
    "past_day_significant_earthquakes",
    "past_day_4.5_earthquakes",
    "past_day_2.5_earthquakes",
    "past_day_1.0_earthquakes",
    "past_week_all_earthquakes",
    "past_week_significant_earthquakes",
    "past_week_4.5_earthquakes",
    "past_week_2.5_earthquakes",
    "past_week_1.0_earthquakes",
    "past_month_all_earthquakes",
    "past_month_significant_earthquakes",
    "past_month_4.5_earthquakes",
    "past_month_2.5_earthquakes",
    "past_month_1.0_earthquakes",
    "summary_significant_month",
    "summary_significant_week",
    "summary_significant_day",
]

# Mapeo entre ID y nombre amigable
FEED_TYPE_FRIENDLY_NAMES = {
    "past_hour_all_earthquakes": "Past Hour - All Earthquakes",
    "past_hour_significant_earthquakes": "Past Hour - Significant",
    "past_day_all_earthquakes": "Past Day - All Earthquakes",
    "past_day_significant_earthquakes": "Past Day - Significant",
    "past_day_4.5_earthquakes": "Past Day - M4.5+",
    "past_day_2.5_earthquakes": "Past Day - M2.5+",
    "past_day_1.0_earthquakes": "Past Day - M1.0+",
    "past_week_all_earthquakes": "Past Week - All Earthquakes",
    "past_week_significant_earthquakes": "Past Week - Significant",
    "past_week_4.5_earthquakes": "Past Week - M4.5+",
    "past_week_2.5_earthquakes": "Past Week - M2.5+",
    "past_week_1.0_earthquakes": "Past Week - M1.0+",
    "past_month_all_earthquakes": "Past Month - All Earthquakes",
    "past_month_significant_earthquakes": "Past Month - Significant",
    "past_month_4.5_earthquakes": "Past Month - M4.5+",
    "past_month_2.5_earthquakes": "Past Month - M2.5+",
    "past_month_1.0_earthquakes": "Past Month - M1.0+",
    "summary_significant_month": "Summary - Month",
    "summary_significant_week": "Summary - Week",
    "summary_significant_day": "Summary - Day",
}

# Reverso para buscar ID desde nombre amigable
FRIENDLY_NAME_TO_FEED_TYPE = {
    v: k for k, v in FEED_TYPE_FRIENDLY_NAMES.items()
}

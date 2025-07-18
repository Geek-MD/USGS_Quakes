DOMAIN = "usgs_quakes"

CONF_RADIUS = "radius"
CONF_MINIMUM_MAGNITUDE = "minimum_magnitude"
CONF_FEED_TYPE = "feed_type"
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"

DEFAULT_RADIUS = 50.0
DEFAULT_MINIMUM_MAGNITUDE = 0.0

PLATFORMS = ["geo_location"]

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

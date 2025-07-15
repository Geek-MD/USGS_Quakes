DOMAIN = "usgs_quakes"

CONF_RADIUS = "radius"
CONF_MINIMUM_MAGNITUDE = "minimum_magnitude"
CONF_FEED_TYPE = "feed_type"

DEFAULT_RADIUS = 50.0
DEFAULT_MINIMUM_MAGNITUDE = 0.0
DEFAULT_FEED_TYPE = "past_day_all_earthquakes"

FEED_TYPES = {
    "past_hour_all_earthquakes": "Past Hour - All Earthquakes",
    "past_day_all_earthquakes": "Past Day - All Earthquakes",
    "past_day_significant_earthquakes": "Past Day - Significant Earthquakes",
    "past_day_1.0_earthquakes": "Past Day - Magnitude 1.0+",
    "past_day_2.5_earthquakes": "Past Day - Magnitude 2.5+",
    "past_day_4.5_earthquakes": "Past Day - Magnitude 4.5+",
    "past_week_all_earthquakes": "Past Week - All Earthquakes",
    "past_week_significant_earthquakes": "Past Week - Significant Earthquakes",
    "past_week_1.0_earthquakes": "Past Week - Magnitude 1.0+",
    "past_week_2.5_earthquakes": "Past Week - Magnitude 2.5+",
    "past_week_4.5_earthquakes": "Past Week - Magnitude 4.5+",
    "past_month_all_earthquakes": "Past Month - All Earthquakes",
    "past_month_significant_earthquakes": "Past Month - Significant Earthquakes",
    "past_month_1.0_earthquakes": "Past Month - Magnitude 1.0+",
    "past_month_2.5_earthquakes": "Past Month - Magnitude 2.5+",
    "past_month_4.5_earthquakes": "Past Month - Magnitude 4.5+",
}

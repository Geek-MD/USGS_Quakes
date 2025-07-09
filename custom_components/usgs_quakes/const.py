DOMAIN = "usgs_quakes"

DEFAULT_MINIMUM_MAGNITUDE = 0.0
DEFAULT_RADIUS_IN_KM = 50.0

CONF_FEED_TYPE = "feed_type"
CONF_MINIMUM_MAGNITUDE = "minimum_magnitude"

VALID_FEED_TYPES = [
    "past_hour_significant_earthquakes",
    "past_hour_m45_earthquakes",
    "past_hour_m25_earthquakes",
    "past_hour_m10_earthquakes",
    "past_hour_all_earthquakes",
    "past_day_significant_earthquakes",
    "past_day_m45_earthquakes",
    "past_day_m25_earthquakes",
    "past_day_m10_earthquakes",
    "past_day_all_earthquakes",
    "past_week_significant_earthquakes",
    "past_week_m45_earthquakes",
    "past_week_m25_earthquakes",
    "past_week_m10_earthquakes",
    "past_week_all_earthquakes",
    "past_month_significant_earthquakes",
    "past_month_m45_earthquakes",
    "past_month_m25_earthquakes",
    "past_month_m10_earthquakes",
    "past_month_all_earthquakes",
]

FEED_TYPE_FRIENDLY_NAMES = {
    "past_hour_significant_earthquakes": "Past Hour – Significant",
    "past_hour_m45_earthquakes": "Past Hour – Magnitude ≥ 4.5",
    "past_hour_m25_earthquakes": "Past Hour – Magnitude ≥ 2.5",
    "past_hour_m10_earthquakes": "Past Hour – Magnitude ≥ 1.0",
    "past_hour_all_earthquakes": "Past Hour – All",
    "past_day_significant_earthquakes": "Past Day – Significant",
    "past_day_m45_earthquakes": "Past Day – Magnitude ≥ 4.5",
    "past_day_m25_earthquakes": "Past Day – Magnitude ≥ 2.5",
    "past_day_m10_earthquakes": "Past Day – Magnitude ≥ 1.0",
    "past_day_all_earthquakes": "Past Day – All",
    "past_week_significant_earthquakes": "Past Week – Significant",
    "past_week_m45_earthquakes": "Past Week – Magnitude ≥ 4.5",
    "past_week_m25_earthquakes": "Past Week – Magnitude ≥ 2.5",
    "past_week_m10_earthquakes": "Past Week – Magnitude ≥ 1.0",
    "past_week_all_earthquakes": "Past Week – All",
    "past_month_significant_earthquakes": "Past Month – Significant",
    "past_month_m45_earthquakes": "Past Month – Magnitude ≥ 4.5",
    "past_month_m25_earthquakes": "Past Month – Magnitude ≥ 2.5",
    "past_month_m10_earthquakes": "Past Month – Magnitude ≥ 1.0",
    "past_month_all_earthquakes": "Past Month – All",
}

# Inverse mapping for form selector
FRIENDLY_NAME_TO_FEED_TYPE = {v: k for k, v in FEED_TYPE_FRIENDLY_NAMES.items()}

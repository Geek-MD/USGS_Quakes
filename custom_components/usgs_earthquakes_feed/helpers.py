"""Helper utilities for USGS Quakes integration."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from homeassistant.util.dt import as_local

_LOGGER = logging.getLogger(__name__)


def parse_event_time(time_val: Any) -> datetime:
    """Parse an event time value that may be a datetime object or an ISO string."""
    if isinstance(time_val, datetime):
        return time_val
    t_str = str(time_val) if time_val is not None else ""
    if t_str.endswith("Z"):
        t_str = t_str.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(t_str)
    except ValueError:
        _LOGGER.debug("Could not parse event time: %s", time_val)
        return datetime.min


def format_event(e: dict[str, Any]) -> str:
    """Return a human-readable string for a single earthquake event."""
    t = e.get("time")
    try:
        if isinstance(t, datetime):
            dt = t if t.tzinfo else t.replace(tzinfo=timezone.utc)
        else:
            dt = datetime.fromisoformat(str(t).replace("Z", "+00:00"))
        dt_str = as_local(dt).strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, AttributeError):
        _LOGGER.debug("Could not format event time: %s", t)
        dt_str = str(t)

    coords = e.get("coordinates") or [None, None]
    lat = coords[0] if len(coords) > 0 else None
    lon = coords[1] if len(coords) > 1 else None
    maps_url = (
        f"https://www.google.com/maps?q={lat},{lon}"
        if lat is not None and lon is not None
        else "N/A"
    )

    return (
        f"{e.get('title', 'N/A')}\n"
        f"Lugar: {e.get('place', 'N/A')}\n"
        f"Magnitud: {e.get('magnitude', 'N/A')} Mw\n"
        f"Fecha/Hora: {dt_str}\n"
        f"Localización: {maps_url}"
    )

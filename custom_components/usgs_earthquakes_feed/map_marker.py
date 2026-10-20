"""Local magnitude images for the built-in Home Assistant map."""

from decimal import Decimal, InvalidOperation
from functools import lru_cache
import re

from aiohttp import web

from homeassistant.components.http import HomeAssistantView

MARKER_URL = "/api/usgs_earthquakes_feed/marker/v1/{magnitude}.svg"
_MAGNITUDE = re.compile(r"-?\d{1,2}(?:\.\d{1,6})?", re.ASCII)


def magnitude_label(value: object) -> str | None:
    """Return a safe numeric label, preserving USGS decimal precision."""
    text = str(value)
    if not _MAGNITUDE.fullmatch(text):
        return None
    try:
        number = Decimal(text)
    except InvalidOperation:
        return None
    if not Decimal("-10") <= number <= Decimal("20"):
        return None
    label = format(number.normalize(), "f")
    if "." not in label:
        label += ".0"
    return label


def marker_url(value: object) -> str | None:
    """Use the magnitude in the URL so revisions invalidate browser caches."""
    label = magnitude_label(value)
    return MARKER_URL.format(magnitude=label) if label is not None else None


@lru_cache(maxsize=256)
def render_marker(label: str) -> bytes:
    """Render validated labels only; no external resources or file writes."""
    # Scale longer labels to fit inside the round entity picture.
    font_size = min(44, 140 / len(label))
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" '
        'viewBox="0 0 128 128">'
        '<circle cx="64" cy="64" r="62" fill="#164e63" '
        'stroke="#ffffff" stroke-width="4"/>'
        '<text x="64" y="66" text-anchor="middle" '
        'dominant-baseline="middle" font-family="Arial, sans-serif" '
        f'font-size="{font_size:g}" font-weight="700" fill="#ffffff">'
        f'{label}</text></svg>'
    ).encode("utf-8")


class UsgsMagnitudeMarkerView(HomeAssistantView):
    """Serve only magnitude images, without exposing entity or location data."""

    url = MARKER_URL
    name = "api:usgs_earthquakes_feed:marker"
    # Browser image requests do not carry the frontend bearer token.
    requires_auth = False

    async def get(self, request: web.Request, magnitude: str) -> web.Response:
        """Return an SVG for a validated magnitude."""
        label = magnitude_label(magnitude)
        if label is None:
            raise web.HTTPNotFound
        return web.Response(
            body=render_marker(label),
            content_type="image/svg+xml",
            headers={
                "Cache-Control": "public, max-age=31536000, immutable",
                "X-Content-Type-Options": "nosniff",
            },
        )

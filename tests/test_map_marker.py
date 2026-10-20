"""Exercise image responses without requiring a full Home Assistant install."""

import ast
import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "custom_components/usgs_earthquakes_feed"
http_stub = ModuleType("homeassistant.components.http")
http_stub.HomeAssistantView = type("HomeAssistantView", (), {})
spec = importlib.util.spec_from_file_location("map_marker", COMPONENT / "map_marker.py")
marker = importlib.util.module_from_spec(spec)
with patch.dict(sys.modules, {"homeassistant.components.http": http_stub}):
    spec.loader.exec_module(marker)


class MarkerTests(unittest.TestCase):
    def test_numeric_labels(self):
        for value, expected in [(4.3, "4.3"), (0, "0.0"), (-1.2, "-1.2"),
                                (4.35, "4.35"), ("4.300", "4.3")]:
            with self.subTest(value=value):
                self.assertEqual(marker.magnitude_label(value), expected)

    def test_invalid_labels(self):
        for value in [None, True, float("nan"), float("inf"), "<script>",
                      "../4.3", "1e3", "9" * 10000, -11, 21]:
            with self.subTest(value=str(value)[:30]):
                self.assertIsNone(marker.marker_url(value))

    def test_svg_and_bounded_cache(self):
        marker.render_marker.cache_clear()
        svg = marker.render_marker("4.3")
        root = ET.fromstring(svg)
        self.assertEqual(root.find("{http://www.w3.org/2000/svg}text").text, "4.3")
        self.assertEqual(marker.render_marker("4.3"), svg)
        self.assertEqual(marker.render_marker.cache_info().hits, 1)
        for index in range(300):
            marker.render_marker(marker.magnitude_label(index / 100))
        self.assertLessEqual(marker.render_marker.cache_info().currsize, 256)

    def test_feed_revision_updates_picture_and_preserves_data(self):
        # Execute the real update method with a small feed fixture.
        tree = ast.parse((COMPONENT / "geo_location.py").read_text())
        entity_class = next(n for n in tree.body if isinstance(n, ast.ClassDef)
                            and n.name == "UsgsQuakesEvent")
        method = next(n for n in entity_class.body if isinstance(n, ast.FunctionDef)
                      and n.name == "_update_from_feed")
        namespace = {"marker_url": marker.marker_url,
                     "UsgsEarthquakeHazardsProgramFeedEntry": object}
        exec(compile(ast.Module(body=[method], type_ignores=[]), "geo_location.py", "exec"), namespace)
        entity = SimpleNamespace()
        feed = SimpleNamespace(title="USGS Quakes M 4.3", distance_to_home=127.1,
                               coordinates=(-32.759, -71.7298), attribution="USGS",
                               time=None, place="Valparaíso", magnitude=4.3,
                               updated=None, status="reviewed", type="earthquake", alert=None)
        update = namespace["_update_from_feed"]
        update(entity, feed)
        first_url = entity._attr_entity_picture
        self.assertTrue(first_url.endswith("/4.3.svg"))
        self.assertEqual(entity._attr_distance, 127.1)
        self.assertEqual(entity._attr_latitude, -32.759)
        feed.magnitude = 4.5
        update(entity, feed)
        self.assertNotEqual(entity._attr_entity_picture, first_url)
        feed.magnitude = None
        update(entity, feed)
        self.assertIsNone(entity._attr_entity_picture)


class MarkerHTTPTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        view = marker.UsgsMagnitudeMarkerView()

        async def handle(request):
            return await view.get(request, request.match_info["magnitude"])

        app = web.Application()
        app.router.add_get(view.url, handle)
        self.client = TestClient(TestServer(app))
        await self.client.start_server()

    async def asyncTearDown(self):
        await self.client.close()

    async def test_image_without_authentication(self):
        response = await self.client.get(marker.marker_url(4.3))
        self.assertEqual(response.status, 200)
        self.assertEqual(response.content_type, "image/svg+xml")
        self.assertIn("immutable", response.headers["Cache-Control"])
        self.assertIn(">4.3</text>", await response.text())
        self.assertFalse(marker.UsgsMagnitudeMarkerView.requires_auth)

    async def test_invalid_request(self):
        response = await self.client.get(marker.MARKER_URL.format(magnitude="nan"))
        self.assertEqual(response.status, 404)


if __name__ == "__main__":
    unittest.main()

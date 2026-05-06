"""Baseline smoke tests for the TapsAff app.

These tests are intentionally shallow: their job is to confirm that URL
routing, view dispatch, template rendering, and the JSON API contract all
still work after each Django version bump. They are NOT a substitute for
proper unit tests - they're a regression net for the upgrade.

External dependencies (weather.com, icon generation) are mocked. The cache
backend is DummyCache via settings_test.py so cache state never leaks
between tests.
"""
from unittest import mock

from django.test import TestCase
from django.urls import resolve

from www.models import Settings


# Shape mirrors www.taps.forecast._build_packet().
SAMPLE_FORECAST = {
    "temp_f": 50.0,
    "temp_c": 10.0,
    "code": 1000,
    "taps": {"status": "OAN", "message": ""},
    "aff": False,
    "message": "",
    "description": {"english": "Sunny", "scots": "Braw"},
    "datetime": "2026-05-06 12:00:00",
    "location": "Glasgow",
    "daytime": True,
    "place_error": None,
    "forecast": [],
}


def _make_settings():
    """Create the singleton Settings row that views/forecast both rely on."""
    return Settings.objects.create(
        location="Glasgow",
        cache_seconds=300,
        threshold=70.0,
        google_id="fake",
        delta=5.0,
    )


class URLRoutingTests(TestCase):
    """URL patterns must resolve to the named views."""

    def test_index_root(self):
        self.assertEqual(resolve("/").view_name, "www:index")

    def test_index_with_location(self):
        self.assertEqual(resolve("/Glasgow/").view_name, "www:index")

    def test_api_with_location(self):
        self.assertEqual(resolve("/api/Glasgow/").view_name, "www:api")

    def test_map_clothing(self):
        self.assertEqual(resolve("/map/clothing").view_name, "www:clothing")

    def test_map_weather(self):
        self.assertEqual(resolve("/map/weather").view_name, "www:weather")

    def test_admin(self):
        self.assertEqual(resolve("/admin/login/").app_name, "admin")


class IndexViewTests(TestCase):

    def setUp(self):
        _make_settings()

    @mock.patch("www.views.forecast.query")
    def test_get_default_location(self, mock_query):
        mock_query.return_value = SAMPLE_FORECAST
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        mock_query.assert_called_once()

    @mock.patch("www.views.forecast.query")
    def test_get_with_location(self, mock_query):
        mock_query.return_value = SAMPLE_FORECAST
        response = self.client.get("/Glasgow/")
        self.assertEqual(response.status_code, 200)
        mock_query.assert_called_once()
        args, _ = mock_query.call_args
        self.assertEqual(args[0], "Glasgow")


class ApiViewTests(TestCase):

    def setUp(self):
        _make_settings()

    @mock.patch("www.views.forecast.query")
    def test_returns_json(self, mock_query):
        mock_query.return_value = SAMPLE_FORECAST
        response = self.client.get("/api/Glasgow/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        body = response.json()
        self.assertEqual(body["location"], "Glasgow")
        self.assertEqual(body["code"], 1000)


class MapViewTests(TestCase):
    """The map view renders an SVG template and is gated by a cache."""

    @mock.patch("www.views.icons")
    def test_clothing_map_renders_svg(self, mock_icons):
        mock_icons.get_clothing.return_value = []
        mock_icons.C_WIDTH = 800
        mock_icons.C_HEIGHT = 600
        response = self.client.get("/map/clothing")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/svg+xml")
        mock_icons.get_clothing.assert_called_once()

    @mock.patch("www.views.icons")
    def test_weather_map_renders_svg(self, mock_icons):
        mock_icons.get_weather.return_value = []
        mock_icons.C_WIDTH = 800
        mock_icons.C_HEIGHT = 600
        response = self.client.get("/map/weather")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/svg+xml")
        mock_icons.get_weather.assert_called_once()

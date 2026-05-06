"""Tests for the TapsAff app.

Two layers:

* Smoke tests (URLRoutingTests, IndexViewTests, ApiViewTests, MapViewTests)
  exist as the upgrade regression net - shallow checks that URL routing,
  view dispatch, template rendering, and the JSON API contract still work.
  External dependencies (forecast.query, icons module) are mocked.

* Unit tests (ForecastHelperTests) cover the pure-ish business logic in
  www.taps.forecast directly: the taps-aff threshold rules, the description
  lookup, and the is_taps_aff convenience wrapper.

Cache is DummyCache via tapsaff.settings_test so cache state never leaks
between tests.
"""
from unittest import mock

from django.test import TestCase
from django.urls import resolve

from www.models import Settings, Weather
from www.taps.forecast import _get_description, _test_taps_aff, is_taps_aff
from www.taps.status import AFF, OAN


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


def _make_settings(**overrides):
    """Create or update the singleton Settings row with sensible test values."""
    defaults = {
        "location": "Glasgow",
        "cache_seconds": 300,
        "threshold": 70.0,
        "google_id": "fake",
        "delta": 5.0,
    }
    defaults.update(overrides)
    settings, _ = Settings.objects.update_or_create(pk=1, defaults=defaults)
    return settings


def _make_weather(code=1000, description="Sunny", scots="Braw", terrible=False, delta=0.0):
    return Weather.objects.create(
        code=code,
        description=description,
        scots=scots,
        terrible=terrible,
        delta=delta,
    )


# --------------------------------------------------------------------------
# Smoke tests
# --------------------------------------------------------------------------

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


# --------------------------------------------------------------------------
# Unit tests for forecast helpers
# --------------------------------------------------------------------------

class ForecastHelperTests(TestCase):
    """Direct tests of the taps-aff threshold rules and description lookup.

    Fixtures: Settings has threshold=70, delta=5; Weather code 1000 is
    benign (not terrible) with delta=0, code 9999 is terrible.
    """

    def setUp(self):
        _make_settings(threshold=70.0, delta=5.0)
        _make_weather(code=1000, terrible=False, delta=0.0,
                      description="Sunny", scots="Braw")
        _make_weather(code=9999, terrible=True, delta=0.0,
                      description="Hellfire", scots="Roastin")

    # -- _test_taps_aff branches --

    def test_well_above_threshold_is_aff(self):
        # 80 >= 70 -> AFF, no bawhair message
        result = _test_taps_aff(code=1000, temp_f=80.0, daytime=True)
        self.assertEqual(result["status"], AFF)
        self.assertEqual(result["message"], "")

    def test_well_below_threshold_is_oan(self):
        # 60 < 70 and 60+5=65 still < 70 -> OAN, no message
        result = _test_taps_aff(code=1000, temp_f=60.0, daytime=True)
        self.assertEqual(result["status"], OAN)
        self.assertEqual(result["message"], "")

    def test_close_to_threshold_gets_bawhair_message(self):
        # 68 < 70 (so not AFF), but 68+5=73 > 70 -> OAN with bawhair
        result = _test_taps_aff(code=1000, temp_f=68.0, daytime=True)
        self.assertEqual(result["status"], OAN)
        self.assertIn("bawhair", result["message"])

    def test_terrible_weather_stays_oan_even_when_hot(self):
        # Code 9999 is flagged terrible - never AFF regardless of temp
        result = _test_taps_aff(code=9999, temp_f=100.0, daytime=True)
        self.assertEqual(result["status"], OAN)

    def test_nighttime_stays_oan_even_when_hot(self):
        # daytime=False short-circuits to OAN regardless of temp
        result = _test_taps_aff(code=1000, temp_f=100.0, daytime=False)
        self.assertEqual(result["status"], OAN)

    def test_weather_specific_delta_raises_threshold(self):
        # Override Weather.delta - threshold becomes 70 + 5 = 75
        Weather.objects.filter(code=1000).update(delta=5.0)
        # 73 >= 70 but < 75, also 73+5=78 > 75 -> OAN with bawhair
        result = _test_taps_aff(code=1000, temp_f=73.0, daytime=True)
        self.assertEqual(result["status"], OAN)
        self.assertIn("bawhair", result["message"])

    # -- _get_description --

    def test_get_description_returns_english_and_scots(self):
        desc = _get_description(1000)
        self.assertEqual(desc, {"english": "Sunny", "scots": "Braw"})

    # -- is_taps_aff --

    def test_is_taps_aff_true_when_aff(self):
        self.assertTrue(is_taps_aff(code=1000, temp_f=80.0, daytime=True))

    def test_is_taps_aff_false_when_oan(self):
        self.assertFalse(is_taps_aff(code=1000, temp_f=60.0, daytime=True))

    def test_is_taps_aff_false_at_night(self):
        self.assertFalse(is_taps_aff(code=1000, temp_f=80.0, daytime=False))


# --------------------------------------------------------------------------
# Resilience tests
# --------------------------------------------------------------------------

class QueryResilienceTests(TestCase):
    """forecast.query() must always return a packet, never raise, even when
    the underlying weather API is unavailable."""

    def setUp(self):
        _make_settings()

    @mock.patch("www.taps.forecast._grab_forecast_data")
    def test_default_location_failure_returns_packet_with_error(self, mock_grab):
        # Simulate API down: every call raises TapsLocationError
        from www.taps.forecast import TapsLocationError, query
        mock_grab.side_effect = TapsLocationError
        packet = query()
        self.assertIsNotNone(packet)
        self.assertTrue(packet["place_error"])

    @mock.patch("www.taps.forecast._grab_forecast_data")
    def test_user_location_unknown_falls_through_to_default(self, mock_grab):
        # First call (user location) fails, second call (default) succeeds
        from www.taps.forecast import TapsLocationError
        mock_grab.side_effect = [TapsLocationError, {
            "location": {"name": "Glasgow"},
            "current": {
                "condition": {"code": 1000},
                "feelslike_f": 50.0,
                "is_day": 1,
            },
            "forecast": {"forecastday": []},
        }]
        _make_weather(code=1000, terrible=False, delta=0.0,
                      description="Sunny", scots="Braw")
        from www.taps.forecast import query
        packet = query(location_request="Atlantis")
        self.assertEqual(packet["location"], "Glasgow")
        self.assertIn("Atlantis", packet["place_error"])

from django.urls import path, re_path

from . import views

app_name = "www"

# The location patterns use a custom character class (word chars, hyphens,
# spaces, plus signs, single quotes) so they stay as re_path. Everything
# else is a literal route and uses path().
_LOCATION = r"[\w\-\ \+ \']+"

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    re_path(rf"^api/(?P<location>{_LOCATION})/$", views.Api.as_view(), name="api"),
    re_path(rf"^(?P<location>{_LOCATION})/$", views.Index.as_view(), name="index"),
    path("map/clothing", views.Map.as_view(), {"show": "clothing"}, name="clothing"),
    path("map/weather", views.Map.as_view(), {"show": "weather"}, name="weather"),
]

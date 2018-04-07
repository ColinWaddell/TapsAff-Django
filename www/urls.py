from django.conf.urls import url

from . import views

app_name = 'www'
urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^api/(?P<location>[\w\-\ \+ \']+)/$', views.Api.as_view(), name='api'),
    url(r'^(?P<location>[\w\-\ \+ \']+)/$', views.Index.as_view(), name='index'),
    url(r'^map/clothing$', views.Map.as_view(), {'show': 'clothing'}, name='clothing'),
    url(r'^map/weather$', views.Map.as_view(), {'show': 'weather'}, name='weather'),
]
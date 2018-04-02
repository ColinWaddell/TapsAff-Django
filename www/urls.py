from django.conf.urls import url

from . import views

app_name = 'www'
urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^(?P<location>[\w\-\ \+ \']+)/$', views.Index.as_view(), name='index'),
]
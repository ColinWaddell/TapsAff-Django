from www.tapmap.codetoicon import GetWeatherIcon
from django import template

register = template.Library()


@register.filter(name='weather_icon')
def weather_icon(code):
  return GetWeatherIcon(int(code), True)
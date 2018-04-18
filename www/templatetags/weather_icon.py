from django import template

register = template.Library()


@register.filter(name='weather_icon')
def weather_icon(code):
  from www.tapmap.codetoicon import GetWeatherIcon
  return GetWeatherIcon(int(code), True)
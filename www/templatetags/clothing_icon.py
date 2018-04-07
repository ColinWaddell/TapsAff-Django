from www.tapmap.codetoicon import GetClothingIcon
from django import template

register = template.Library()


@register.filter(name='clothing_icon')
def clothing_icon(code, temp_f):
  return GetClothingIcon(int(code), temp_f)
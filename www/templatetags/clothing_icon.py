from django import template

register = template.Library()


@register.filter(name='clothing_icon')
def clothing_icon(code, temp_f):
  from www.tapmap.codetoicon import GetClothingIcon
  return GetClothingIcon(int(code), temp_f)
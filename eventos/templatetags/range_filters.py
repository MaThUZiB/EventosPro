from django import template

register = template.Library()

@register.filter
def times(value):
    """Devuelve un rango de 1 a value inclusive"""
    return range(1, value + 1)

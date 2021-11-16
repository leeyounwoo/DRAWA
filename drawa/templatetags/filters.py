from django import template

register = template.Library()

@register.filter
def dictionary(h, key):
    return h[key]
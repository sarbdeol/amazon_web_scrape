# custom_tags.py

from django import template

register = template.Library()

@register.filter
def get_attribute(instance, attribute_name):
    return getattr(instance, attribute_name, False)
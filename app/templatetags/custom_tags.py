# custom_tags.py
from django import template

register = template.Library()

@register.filter
def get_dict_value(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

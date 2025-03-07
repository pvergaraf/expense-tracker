from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using bracket notation"""
    try:
        # Convert key to string since JSON only has string keys
        str_key = str(key)
        return dictionary.get(str_key)
    except (AttributeError, KeyError, TypeError):
        return None 
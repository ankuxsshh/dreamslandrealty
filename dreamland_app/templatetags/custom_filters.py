from django import template

register = template.Library()

@register.filter
def length_is(value, length):
    """
    Custom template filter to check if the length of a given value is equal to a specified number.
    Usage:
        {{ some_list|length_is:3 }}
    """
    try:
        return len(value) == int(length)
    except (TypeError, ValueError):
        return False

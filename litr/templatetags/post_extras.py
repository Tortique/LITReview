from django import template

register = template.Library()


@register.filter
def model_type(value):
    return type(value).__name__


@register.filter()
def rating_range(default=5):
    return range(1, default + 1, 1)

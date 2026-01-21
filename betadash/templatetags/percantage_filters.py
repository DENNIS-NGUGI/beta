from django import template

register = template.Library()

@register.filter
def percentage(value1, value2):
    try:
        value1 = float(value1)
        value2 = float(value2)
        if value2 == 0:
            return 0
        return round((value1 / value2) * 100, 2)
    except (ValueError, TypeError):
        return 0

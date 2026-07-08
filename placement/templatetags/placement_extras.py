from django import template

register = template.Library()


@register.filter
def get_display(obj, field_name):
    """
    Returns the human-friendly display value of `field_name` on `obj`.
    Used by the generic list template to render each model's fields
    dynamically without needing one hard-coded template per entity.
    """
    display_method = getattr(obj, f"get_{field_name}_display", None)
    if callable(display_method):
        return display_method()
    value = getattr(obj, field_name, "")
    if value is None:
        return ""
    return value

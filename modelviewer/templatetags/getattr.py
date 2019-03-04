from django import template

register = template.Library()


@register.filter
def getattr(obj, args):
    """ Try to get an attribute from an object.
    """
    try:
        return obj.__getattribute__(args)
    except AttributeError:
        return "Unknown attribute"

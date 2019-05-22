from django.template import Library

from .. import utils as fahrenheit_utils

register = Library()


@register.filter
def is_blocked(content_object, request):
    return fahrenheit_utils.object_is_blocked(
        request=request,
        content_object=content_object
    )


@register.simple_tag(takes_context=True)
def is_blocked(context, content_object):
    return fahrenheit_utils.object_is_blocked(
        request=context['request'],
        content_object=content_object
    )

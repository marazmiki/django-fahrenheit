import pytest
from django.http import HttpRequest
from django.template import RequestContext, Template

from django_fahrenheit.models import Claimer
from django_fahrenheit.utils import block_object

FILTER_TEMPLATE = (
    '{% if object|is_blocked:request %}blocked'
    '{% else %}not blocked'
    '{% endif %}'
)

TAG_TEMPLATE = (
    '{% is_blocked object as it_is_blocked %}'
    '{% if it_is_blocked %}blocked'
    '{% else %}not blocked'
    '{% endif %}'
)


@pytest.fixture
def blocked_object():
    obj = Claimer.objects.create(name='RosKomNadzor')
    block_object(obj, countries='RU')
    return obj


@pytest.fixture
def non_blocked_object():
    return Claimer.objects.create(name='Telegram')


@pytest.mark.parametrize(
    argnames='template_string',
    argvalues=[FILTER_TEMPLATE, TAG_TEMPLATE]
)
@pytest.mark.parametrize(
    argnames='obj_name, expected_string',
    argvalues=[
        ('blocked_object', 'blocked'),
        ('non_blocked_object', 'not blocked'),
    ]
)
def test_is_blocked_templatetag(
        request,
        obj_name, expected_string, template_string
):
    http_request = HttpRequest()
    http_request.META['HTTP_CF_IPCOUNTRY'] = 'RU'

    return Template(
        '{% load fahrenheit_tags %}' + template_string
    ).render(RequestContext(http_request, {
        'object': request.getfixturevalue(obj_name)
    })) == expected_string

import pytest
from django.contrib.gis.geoip2 import GeoIP2Exception
from django.http import HttpRequest

from django_fahrenheit import settings, utils
from django_fahrenheit.exceptions import CountryNotFound
from django_fahrenheit.models import Claimer
from django_fahrenheit.utils import (block_object, block_url, extract_ip,
                                     get_country, object_is_blocked,
                                     url_is_blocked)


@pytest.mark.parametrize(
    argnames='remote_addr, forwarded_for, expected_value',
    argvalues=[
        ('1.2.3.4', '', '1.2.3.4'),
        ('1.2.3.4', '4.3.2.1', '4.3.2.1'),
        ('1.2.3.4', '4.3.2.1,44.33.22.11', '4.3.2.1'),
        ('1.2.3.4', ' 4.3.2.1 , 44.33.22.11', '4.3.2.1'),
    ],
    ids=[
        'there is no X-Forwarded-For headers',
        'there is a X-Forwarded-For header with the only value',
        'there is a X-Forwarded-For header with a chain of addresses',
        'deleting leading and trailing spaces',
    ]
)
def test_extract_ip(remote_addr, forwarded_for, expected_value):
    request = HttpRequest()
    request.META['REMOTE_ADDR'] = remote_addr
    if forwarded_for:
        request.META['HTTP_X_FORWARDED_FOR'] = forwarded_for
    assert extract_ip(request) == expected_value


@pytest.mark.parametrize(
    argnames='current_country, blocked_countries, expected',
    argvalues=[
        ('RU', None, False),
        ('RU', ['US'], False),
        ('CH', ['RU', 'US'], False),
        ('RU', ['RU'], True),
        ('RU', ['RU', 'US'], True),
        ('', [], False),
    ],
    ids=[
        'not blocked if there is no entry for the object',
        'not blocked if there is an another country entry for the object',
        'not blocked if there are other country entries for the object',
        'blocked if there is an entry for the same country',
        'blocked if there are some entries including the request\'s country',
        'not blocked if could not detect a country',
    ]
)
def test_object_is_blocked(current_country, blocked_countries, expected):
    content_object = Claimer.objects.create(name='Roskomnadzor')

    if blocked_countries:
        block_object(content_object, countries=blocked_countries)

    request = HttpRequest()
    request.META['HTTP_CF_IPCOUNTRY'] = current_country

    assert object_is_blocked(request, content_object) is expected


@pytest.mark.parametrize(
    argnames='current_country, blocked_countries, expected',
    argvalues=[
        ('RU', None, False),
        ('RU', ['US'], False),
        ('CH', ['RU', 'US'], False),
        ('RU', ['RU'], True),
        ('RU', ['RU', 'US'], True),
    ],
)
def test_url_is_blocked(current_country, blocked_countries, expected,
                        monkeypatch
                        ):
    url = '/forbidden/in/ru/'

    if blocked_countries:
        block_url(url, countries=blocked_countries)

    request = HttpRequest()
    request.META['HTTP_CF_IPCOUNTRY'] = current_country

    assert url_is_blocked(request, url) is expected


def test_url_is_blocked_no_cloudflare():
    url = '/forbidden/in/ru/'
    block_url(url, countries=['US', 'RU'])
    request = HttpRequest()
    assert not url_is_blocked(request, url)


@pytest.mark.parametrize(
    argnames='country_code, exc, mock_geoip',
    argvalues=[
        ('US', None, True),
        (None, GeoIP2Exception, True,),
        (None, TypeError, True),
        (None, KeyError, True,),
        (None, True, False),
        (None, True, True),
    ])
def test_get_country_maxmind(monkeypatch, country_code, exc, mock_geoip):
    class GeoIPMock:
        def country(self, ip):
            if exc:
                raise exc()
            else:
                return {'country_code': country_code}

    monkeypatch.setattr(settings, 'USE_MAXMIND_GEOIP2', True)
    monkeypatch.setattr(utils, 'geoip', GeoIPMock() if mock_geoip else None)

    request = HttpRequest()
    request.META['REMOTE_ADDR'] = '8.8.8.8'

    if exc:
        with pytest.raises(CountryNotFound):
            get_country(request)
    else:
        assert get_country(request) == country_code

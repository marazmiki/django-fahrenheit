import logging
from django.contrib.gis.geoip2 import GeoIP2, GeoIP2Exception
from django.db.models import Q

from .exceptions import CountryNotFound
from .models import Object, URL
from . import settings

log = logging.getLogger(__name__)
geoip = None


if settings.USE_MAXMIND_GEOIP2:
    try:
        geoip = GeoIP2()
    except GeoIP2Exception as ex:
        log.warning(
            'It seems, it was improperly configured: Fahrenheit intended to '
            'use MaxMind\'s geoip2 as you specified USE_MAXMIND_GEOIP2 = True '
            'but geoip failed to initialize: %s', ex
        )


def extract_ip(request):
    return (
        request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() or
        request.META.get('REMOTE_ADDR')
    )


def get_country(request):
    ip = extract_ip(request)
    if settings.USE_CLOUDFLARE_GEOLOCATION:
        cf_country = request.META.get('HTTP_CF_IPCOUNTRY')
        if cf_country:
            return cf_country
    if settings.USE_MAXMIND_GEOIP2:
        if geoip:
            try:
                return geoip.country(ip)['country_code']
            except (GeoIP2Exception, TypeError, KeyError) as ex:
                log.warning('Failed to geolocate ip %s: %s', ip, ex)
        else:
            log.warning('geoip2 not configured!')
    raise CountryNotFound()


def url_is_blocked(request, url):
    blocking = URL.objects.filter(pattern=url)
    if not blocking.exists():
        return False
    try:
        country = get_country(request)
    except CountryNotFound:
        return False
    return blocking.filter(
        Q(country_code__icontains=country) |
        Q(country_code=None),
    ).exists()


def object_is_blocked(request, content_object):
    country = get_country(request)
    claims = Object.objects.filter(Q(country_code__icontains=country) |
                                   Q(country_code=None),
                                   content_object=content_object)
    return claims.exists()


def block_object(
        content_object, title=None, reason=None, countries=None,
        claimer=None
):
    return Object.objects.create(
        content_object=content_object,
        title=title,
        reason=reason,
        country_code=countries,
        claimer=claimer
    )


def block_url(url, title=None, reason=None, countries=None, claimer=None):
    return URL.objects.create(
        pattern=url,
        title=title,
        reason=reason,
        country_code=countries,
        claimer=claimer
    )

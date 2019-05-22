from django.conf import settings


def enable_added_by():
    return all((
        'django.contrib.auth' in settings.INSTALLED_APPS,
        USE_ADDED_BY_FIELD,
    ))


_conf = getattr(settings, 'FAHRENHEIT', {})


USE_MAXMIND_GEOIP2 = _conf.get('USE_MAXMIND_GEOIP2', False)
USE_CLOUDFLARE_GEOLOCATION = _conf.get('USE_CLOUDFLARE_GEOLOCATION', True)
USE_ADDED_BY_FIELD = _conf.get('USE_ADDED_BY_FIELD', True)

from django import apps
from django.utils.translation import ugettext_lazy as _


class FahrenheitAppConfig(apps.AppConfig):
    name = 'django_fahrenheit'
    verbose_name = _('Fahrenheit 451')

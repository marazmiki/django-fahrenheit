import pytest

from django_fahrenheit import settings as fahrenheit_settings


@pytest.mark.parametrize(
    argnames='auth_installed, use_added_by, expected_value',
    argvalues=[
        (True, True, True),
        (True, False, False),
        (False, True, False),
        (False, False, False)
    ],
)
def test_enable_added_by(
        settings,
        auth_installed, use_added_by, expected_value
):
    if 'django.contrib.auth' in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS.remove('django.contrib.auth')
    if auth_installed:
        settings.INSTALLED_APPS.append('django.contrib.auth')
    fahrenheit_settings.USE_ADDED_BY_FIELD = use_added_by

    assert fahrenheit_settings.enable_added_by() is expected_value

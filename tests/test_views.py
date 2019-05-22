import pytest
from django.http import HttpRequest
from django.template import TemplateDoesNotExist

from django_fahrenheit import views
from django_fahrenheit.views import unavailable_for_legal_reasons


def test_view_default_set():
    request = HttpRequest()
    resp = unavailable_for_legal_reasons(request)
    assert resp.status_code == 451
    assert b'dude' not in resp.content


def test_custom_template_name():
    resp = unavailable_for_legal_reasons(
        HttpRequest(),
        template_name='451_custom.html'
    )
    assert resp.status_code == 451
    assert b'dude' in resp.content


def test_custom_template_name_that_does_not_exist():
    with pytest.raises(TemplateDoesNotExist):
        unavailable_for_legal_reasons(
            HttpRequest(),
            template_name='451-not-exists.html'
        )


def test_builtin_template_name_that_does_not_exist(monkeypatch):
    template_name = '451-not-exists.html'
    monkeypatch.setattr(views, 'ERROR_451_TEMPLATE_NAME', template_name)
    unavailable_for_legal_reasons(HttpRequest(), template_name)

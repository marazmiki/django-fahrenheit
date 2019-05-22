import pytest

from django_fahrenheit import models as m


@pytest.mark.parametrize(
    argnames='model_class, kw, expected_string',
    argvalues=[
        (m.Object, {'title': 'An object'}, 'An object'),
        (m.URL, {'pattern': '/telegram/'}, '/telegram/'),
        (m.Claimer, {'name': 'RosKomNadzor'}, 'RosKomNadzor'),
        (m.Document, {'name': 'RKN is informing'}, 'RKN is informing'),
    ]
)
def test_model_str_magic_method(model_class, kw, expected_string):
    assert expected_string == str(model_class(**kw))

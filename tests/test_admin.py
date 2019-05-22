import pytest

URL_TEMPLATE = '/admin/django_fahrenheit/{}/'
MODELS = (
    'claimer',
    'url',
    'object',
)


@pytest.mark.parametrize('url', MODELS)
def test_admin_list_create(url, admin_client):
    resp = admin_client.get(URL_TEMPLATE.format(url))
    assert resp.status_code == 200


@pytest.mark.parametrize('url', MODELS)
def test_set_a_current_user_into_initial_data_when_add_an_entry(
        url, admin_client, admin_user
):
    resp = admin_client.get(URL_TEMPLATE.format(f'{url}/add'))
    assert resp.context['adminform'].form.initial['added_by'] == admin_user

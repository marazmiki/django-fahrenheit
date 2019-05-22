import pytest

from django_fahrenheit.utils import block_url


@pytest.mark.parametrize('url', [
    '/',
    '/forbidden/in/ru/',
    '/page/'
])
def test_page_available_for_all(client, url):
    resp = client.get(url, HTTP_CF_IPCOUNTRY='ru')
    assert resp.status_code == 200


@pytest.mark.parametrize('current_country, banned', [
    ('RU', True),
    ('US', False),
])
def test_visiting_a_blocked_url(client, current_country, banned):
    url = '/forbidden/in/ru/'
    block_url(url, ['RU'])

    resp = client.get(url, HTTP_CF_IPCOUNTRY=current_country)
    assert resp.status_code == 451

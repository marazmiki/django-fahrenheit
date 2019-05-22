import pytest


@pytest.fixture(autouse=True)
def autouse_db(db):
    "Ensure the database connection is available in all the tests"
    pass

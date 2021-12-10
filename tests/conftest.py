import os
import pytest
from avaandmed import Avaandmed
from tests.data_mock import DataJsonMock
from tests.request_mock import RequestMock

API_TOKEN = os.getenv('AVAANDMED_TEST_KEY', 'none')
KEY_ID = os.getenv('AVAANDMED_TEST_KEY_ID', 'none')
BASE_HOSTNAME = 'avaandmedtest.eesti.ee'


@pytest.fixture
def api_token():
    return API_TOKEN


@pytest.fixture
def key_id():
    return KEY_ID


@pytest.fixture()
def avaandmed_client():
    return Avaandmed(API_TOKEN, KEY_ID, BASE_HOSTNAME)


@pytest.fixture
def datasets(avaandmed_client: Avaandmed):
    return avaandmed_client.datasets


@pytest.fixture
def users_datasets(avaandmed_client: Avaandmed):
    return avaandmed_client.users.me.dataset


@pytest.fixture(scope='class')
def request_mock():
    return RequestMock()


@pytest.fixture(scope='class')
def data_mock():
    return DataJsonMock()

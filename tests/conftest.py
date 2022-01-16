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


@pytest.fixture
def my_org_id():
    return 'cf923536-2dbb-4e2e-8167-218e52316283'


@pytest.fixture()
def avaandmed_client():
    return Avaandmed(API_TOKEN, KEY_ID, BASE_HOSTNAME)


@pytest.fixture
def datasets(avaandmed_client: Avaandmed):
    return avaandmed_client.datasets


@pytest.fixture
def users_datasets(avaandmed_client: Avaandmed):
    return avaandmed_client.users.me.dataset


@pytest.fixture()
def organization_datasets(avaandmed_client: Avaandmed, my_org_id: str):
    return avaandmed_client.organizations(my_org_id).my_orgranization.dataset


@pytest.fixture(scope='class')
def request_mock():
    return RequestMock()


@pytest.fixture(scope='class')
def data_mock():
    return DataJsonMock()

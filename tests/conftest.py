import os
import pytest
from avaandmed import Avaandmed

API_TOKEN = os.getenv('AVAANDMED_KEY', 'none')
KEY_ID = os.getenv('AVAANDMED_KEY_ID', 'none')


@pytest.fixture
def api_token():
    return API_TOKEN


@pytest.fixture
def key_id():
    return KEY_ID


@pytest.fixture
def avaandmed_client():
    return Avaandmed(API_TOKEN, KEY_ID)

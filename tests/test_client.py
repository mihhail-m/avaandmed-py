import json
from avaandmed.entities.organizations import Organizations
from avaandmed.entities.datasets import Datasets
from avaandmed import Avaandmed
from avaandmed.http.http_client import HttpMethod

API_TOKEN = "token"
KEY_ID = "id"

client = Avaandmed(API_TOKEN, KEY_ID)


def test_client_init():
    assert isinstance(client, Avaandmed)
    assert client.api_token == "token"
    assert client.key_id == "id"


def test_datasets_entity():
    datasets = client.datasets
    assert isinstance(datasets, Datasets)


def test_organizations_entity():
    organizations = client.organizations
    assert isinstance(organizations, Organizations)


def test_http_methods_enum():
    assert HttpMethod.GET.value == 'get'
    assert HttpMethod.POST.value == 'post'
    assert HttpMethod.DELETE.value == 'delete'
    assert HttpMethod.UPDATE.value == 'update'


def test_json_to_model():
    datasets_json_path = "C:\\Users\\mihha\\Desktop\\Projects\\bcs\\avaandmed-python\\tests\\data\\dataset.json"
    dataset = Datasets.parse_file(datasets_json_path)
    # print(dataset.name)
    assert dataset.name == 'dataset1'
    assert isinstance(dataset, Datasets)

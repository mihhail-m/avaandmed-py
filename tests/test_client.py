import os
from avaandmed.entities.organizations import Organizations
from avaandmed.entities.datasets import Datasets, Dataset
from avaandmed import Avaandmed
from avaandmed.http.http_client import HttpClient, HttpMethod

API_TOKEN = os.getenv('AVAANDMED_KEY', 'none')
KEY_ID = os.getenv('AVAANDMED_KEY_ID', 'none')

client = Avaandmed(API_TOKEN, KEY_ID)
DATASET_ID = '8d681e55-4118-41f5-b319-1d2bdd36408c'
DATASET_SLUG = 'soidukite-staatused-eestis'


def test_client_init():
    assert API_TOKEN != 'none'
    assert KEY_ID != 'none'
    assert isinstance(client, Avaandmed)


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
    dataset = Dataset.parse_file(datasets_json_path)
    # print(dataset.name)
    assert dataset.name == 'dataset1'
    assert isinstance(dataset, Dataset)


def test_dataset_retrieve_by_id():
    dataset = client.datasets.retrieve_by_id(DATASET_ID)
    assert DATASET_ID == dataset.id


def test_dataset_retrieve_by_slug():
    dataset = client.datasets.retrieve_by_slug(DATASET_SLUG)
    # print(dataset)
    assert DATASET_SLUG == dataset.slug

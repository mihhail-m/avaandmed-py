import pytest

from avaandmed import Avaandmed
from avaandmed.api_resources.datasets import Datasets
from avaandmed.api_resources.datasets.dataset import Dataset
from avaandmed.exceptions import AvaandmedApiExcepiton

DATASET_ID = '8d681e55-4118-41f5-b319-1d2bdd36408c'
DATASET_SLUG = 'soidukite-staatused-eestis'


@pytest.fixture
def datasets(avaandmed_client: Avaandmed):
    return avaandmed_client.datasets


def test_json_to_model():
    datasets_json_path = "C:\\Users\\mihha\\Desktop\\Projects\\bcs\\avaandmed-python\\tests\\data\\dataset.json"
    dataset = Dataset.parse_file(datasets_json_path)
    assert dataset.name == 'dataset1'
    assert isinstance(dataset, Dataset)


@pytest.mark.skip(reason='dynamic dataset ID')
def test_retrieve_by_id(datasets: Datasets):
    dataset = datasets.retrieve_by_id(DATASET_ID)
    assert isinstance(dataset, Dataset)
    assert DATASET_ID == dataset.id


def test_negative_retrieve_by_id(datasets: Datasets):
    with pytest.raises(AvaandmedApiExcepiton):
        datasets.retrieve_by_id('sdfsdfsd')


def test_retrieve_by_slug(datasets: Datasets):
    dataset = datasets.retrieve_by_slug(DATASET_SLUG)
    assert isinstance(dataset, Dataset)
    assert DATASET_SLUG == dataset.slug


def test_negative_retrieve_by_slug(datasets: Datasets):
    with pytest.raises(AvaandmedApiExcepiton):
        datasets.retrieve_by_slug('sdfsdf')

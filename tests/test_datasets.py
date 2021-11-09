import pytest
import responses
from pathlib import Path

from avaandmed import Avaandmed
from avaandmed.api_resources.datasets import Datasets
from avaandmed.api_resources.datasets.dataset import Dataset
from avaandmed.exceptions import AvaandmedApiExcepiton, AvaandmedException
from .utils import load_json, format_mock_url

DATA_DIR = Path.cwd() / 'data'
DATASET_ID = '8d681e55-4118-41f5-b319-1d2bdd36408c'
DATASET_SLUG = 'soidukite-staatused-eestis'
MOCK_GET_DATASET_ID_URL = 'https://avaandmed.eesti.ee/api/datasets'
MOCK_GET_DATASET_SLUG_URL = 'https://avaandmed.eesti.ee/api/datasets/slug'
MOCK_TOKEN_URL = 'https://avaandmed.eesti.ee/api/auth/key-login'
MOCK_DATASET_FILE = DATA_DIR / 'dataset.json'
MOCK_ERROR_FILE = DATA_DIR / 'error.json'
MOCK_TOKEN_FILE = DATA_DIR / 'token.json'
MOCK_DATASET_LIST_FILE = DATA_DIR / 'dataset_list.json'
WRONG_SLUG = 'sdfsdf'
WRONG_ID = 'sdfsdfsd'


@pytest.fixture
def datasets(avaandmed_client: Avaandmed):
    return avaandmed_client.datasets


def mock_post_auth():
    responses.add(
        responses.POST,
        MOCK_TOKEN_URL,
        json=load_json(MOCK_TOKEN_FILE),
        status=201
    )


def test_json_to_model():
    dataset = Dataset.parse_obj(load_json(MOCK_DATASET_FILE)['data'])
    assert dataset.name == 'Sõidukite staatused Eestis'
    assert isinstance(dataset, Dataset)


# @pytest.mark.skip(reason='dynamic dataset ID')
@responses.activate
def test_retrieve_by_id(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.GET,
        format_mock_url(MOCK_GET_DATASET_ID_URL, DATASET_ID),
        json=load_json(MOCK_DATASET_FILE),
        status=200
    )

    dataset = datasets.retrieve_by_id(DATASET_ID)
    assert isinstance(dataset, Dataset)
    assert DATASET_ID == dataset.id


@responses.activate
def test_negative_retrieve_by_id(datasets: Datasets):
    with pytest.raises(AvaandmedApiExcepiton):
        mock_post_auth()
        responses.add(
            responses.GET,
            format_mock_url(MOCK_GET_DATASET_ID_URL, WRONG_ID),
            json=load_json(MOCK_ERROR_FILE),
            status=404
        )

        datasets.retrieve_by_id(WRONG_ID)


@responses.activate
def test_retrieve_by_slug(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.GET,
        format_mock_url(MOCK_GET_DATASET_SLUG_URL, DATASET_SLUG),
        json=load_json(MOCK_DATASET_FILE),
        status=200
    )

    dataset = datasets.retrieve_by_slug(DATASET_SLUG)
    assert isinstance(dataset, Dataset)
    assert DATASET_SLUG == dataset.slug


@responses.activate
def test_negative_retrieve_by_slug(datasets: Datasets):
    with pytest.raises(AvaandmedApiExcepiton):
        mock_post_auth()
        responses.add(
            responses.GET,
            format_mock_url(MOCK_GET_DATASET_SLUG_URL, WRONG_SLUG),
            json=load_json(MOCK_ERROR_FILE),
            status=404
        )

        datasets.retrieve_by_slug(WRONG_SLUG)


@responses.activate
def test_get_dataset_list(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.GET,
        MOCK_GET_DATASET_ID_URL + '?limit=5',
        json=load_json(MOCK_DATASET_LIST_FILE),
        status=200
    )
    limit = 5
    dataset_list = datasets.get_dataset_list(limit=limit)
    assert dataset_list is not None
    assert len(dataset_list) == limit


def test_negative_dataset_list_limit_zero(datasets: Datasets):
    with pytest.raises(AvaandmedException):
        datasets.get_dataset_list(limit=0)


def test_negative_dataset_list_negative_limit(datasets: Datasets):
    with pytest.raises(AvaandmedException):
        datasets.get_dataset_list(limit=-1)

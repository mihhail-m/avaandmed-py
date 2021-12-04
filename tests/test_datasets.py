# type: ignore
import pytest
import responses
from pathlib import Path
from typing import List

from avaandmed import Avaandmed
from avaandmed.api_resources.common import (
    Access,
    Category,
    Citation,
    Conformity,
    CoordinateReferenceSystem,
    File,
    Keyword,
    Licence,
    Notification,
    Region,
    ResourceType,
    TopicCategory,
    UpdateIntervalUnit
)
from avaandmed.api_resources.datasets import Datasets
from avaandmed.api_resources.datasets.dataset import Dataset
from avaandmed.api_resources.organizations.organization import Organization
from avaandmed.api_resources.users.user import User
from avaandmed.exceptions import AvaandmedApiExcepiton, AvaandmedException
from .utils import load_json

DATA_DIR = Path('data')
DATASET_ID = '8d681e55-4118-41f5-b319-1d2bdd36408c'
DATASET_SLUG = 'soidukite-staatused-eestis'
WRONG_SLUG = 'sdfsdf'
WRONG_ID = 'sdfsdfsd'
BASE_URL = 'https://avaandmedtest.eesti.ee/api/datasets'
MOCK_TOKEN_URL = 'https://avaandmedtest.eesti.ee/api/auth/key-login'
MOCK_DATASET_FILE = DATA_DIR / 'dataset.json'
MOCK_ERROR_FILE = DATA_DIR / 'error.json'
MOCK_TOKEN_FILE = DATA_DIR / 'token.json'
MOCK_DATASET_LIST_FILE = DATA_DIR / 'dataset_list.json'


def join_base_url_values(path_values: List[str]):
    """
    Joins values in list and base url into valid path.
    Ex.: baseurl/value/value
    """
    return f"{BASE_URL}/{'/'.join(path_values)}"


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


def mock_negative_post_auth(status: int, msg: str):
    responses.add(
        responses.POST,
        MOCK_TOKEN_URL,
        json={
            "statusCode": status,
            "message": msg,
        },
        status=status
    )


def stub_get_dataset_by(url_values: List[str], filename: Path):
    mock_post_auth()
    responses.add(
        responses.GET,
        join_base_url_values(url_values),
        json=load_json(filename),
        status=200
    )


def test_json_to_model():
    dataset = Dataset.parse_obj(load_json(MOCK_DATASET_FILE)['data'])
    assert dataset.name == 'Sõidukite staatused Eestis'
    assert isinstance(dataset, Dataset)


@responses.activate
def test_negative_post_auth(datasets: Datasets):
    with pytest.raises(AvaandmedApiExcepiton):
        mock_negative_post_auth(401, "Unauthorized")
        stub_get_dataset_by([DATASET_ID], MOCK_DATASET_FILE)
        dataset = datasets.retrieve_by_id(DATASET_ID)


@responses.activate
def test_retrieve_by_id(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.GET,
        join_base_url_values([DATASET_ID]),
        json=load_json(MOCK_DATASET_FILE),
        status=200
    )

    dataset = datasets.retrieve_by_id(DATASET_ID)
    assert isinstance(dataset, Dataset)
    assert DATASET_ID == dataset.id
    assert dataset.user is not None


@responses.activate
def test_negative_retrieve_by_id(datasets: Datasets):
    with pytest.raises(AvaandmedApiExcepiton):
        mock_post_auth()
        responses.add(
            responses.GET,
            join_base_url_values([WRONG_ID]),
            json=load_json(MOCK_ERROR_FILE),
            status=404
        )

        datasets.retrieve_by_id(WRONG_ID)


@responses.activate
def test_retrieve_by_slug(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.GET,
        join_base_url_values(['slug', DATASET_SLUG]),
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
            join_base_url_values(['slug', WRONG_SLUG]),
            json=load_json(MOCK_ERROR_FILE),
            status=404
        )

        datasets.retrieve_by_slug(WRONG_SLUG)


@responses.activate
def test_get_dataset_list(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.GET,
        BASE_URL + '?limit=5',
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


@responses.activate
def test_get_datasets_total(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.GET,
        BASE_URL + '/total',
        json={'data': 123},
        status=200
    )

    total = datasets.get_total()
    assert total is not None
    assert isinstance(total, int)


@responses.activate
def test_get_mimetypes(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.GET,
        BASE_URL + '/mimetypes/distinct',
        json={
            'data': [
                'application/pdf',
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'text/xml'
            ]
        },
        status=200
    )

    mimetypes = datasets.get_distinct_mimetypes()
    assert mimetypes is not None


@responses.activate
def test_user_is_deserialized(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.GET,
        join_base_url_values([DATASET_ID]),
        json=load_json(MOCK_DATASET_FILE),
        status=200
    )

    dataset = datasets.retrieve_by_id(DATASET_ID)
    user_dict = dataset.user.dict()  # type: ignore
    for v in user_dict.values():
        assert v is not None
    assert isinstance(dataset.user, User)


@responses.activate
def test_organization_is_deserialized(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.GET,
        join_base_url_values([DATASET_ID]),
        json=load_json(MOCK_DATASET_FILE),
        status=200
    )

    dataset = datasets.retrieve_by_id(DATASET_ID)
    organization_dict = dataset.organization.dict()
    assert isinstance(dataset.organization, Organization)
    for v in organization_dict.values():
        assert v is not None


@responses.activate
def test_files_are_deserialized(datasets: Datasets):
    stub_get_dataset_by([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.retrieve_by_id(DATASET_ID)
    files = dataset.files
    assert isinstance(files[0], File)


@responses.activate
def test_keywords_are_deserialized(datasets: Datasets):
    stub_get_dataset_by([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.retrieve_by_id(DATASET_ID)
    keywords = dataset.keywords
    assert isinstance(keywords[0], Keyword)


@responses.activate
def test_categories_are_deserialized(datasets: Datasets):
    stub_get_dataset_by([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.retrieve_by_id(DATASET_ID)
    categories = dataset.categories
    assert isinstance(categories[0], Category)


@responses.activate
def test_regions_are_deserialized(datasets: Datasets):
    stub_get_dataset_by([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.retrieve_by_id(DATASET_ID)
    regions = dataset.regions
    assert isinstance(regions[0], Region)


@responses.activate
def test_coords_are_deserialized(datasets: Datasets):
    stub_get_dataset_by([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.retrieve_by_id(DATASET_ID)
    coords = dataset.coordinate_reference_systems
    assert isinstance(coords[0], CoordinateReferenceSystem)


@responses.activate
def test_citations_are_deserialized(datasets: Datasets):
    stub_get_dataset_by([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.retrieve_by_id(DATASET_ID)
    citations = dataset.citations
    assert isinstance(citations[0], Citation)


@responses.activate
def test_conformities_are_deserialized(datasets: Datasets):
    stub_get_dataset_by([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.retrieve_by_id(DATASET_ID)
    conformities = dataset.conformities
    assert isinstance(conformities[0], Conformity)


@responses.activate
def test_license_is_deserialized(datasets: Datasets):
    stub_get_dataset_by([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.retrieve_by_id(DATASET_ID)
    licence = dataset.licence
    assert isinstance(licence, Licence)


@responses.activate
def test_interval_is_deserialized(datasets: Datasets):
    stub_get_dataset_by([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.retrieve_by_id(DATASET_ID)
    interval = dataset.update_interval_unit
    assert isinstance(interval, UpdateIntervalUnit)


@responses.activate
def test_access_is_deserialized(datasets: Datasets):
    stub_get_dataset_by([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.retrieve_by_id(DATASET_ID)
    access = dataset.access
    assert isinstance(access, Access)


@responses.activate
def test_res_type_is_deserialized(datasets: Datasets):
    stub_get_dataset_by([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.retrieve_by_id(DATASET_ID)
    res_type = dataset.resource_type
    assert isinstance(res_type, ResourceType)


@responses.activate
def test_topics_are_deserialized(datasets: Datasets):
    stub_get_dataset_by([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.retrieve_by_id(DATASET_ID)
    topics = dataset.topic_categories

    for topic in topics:
        assert isinstance(topic, TopicCategory)


@responses.activate
def test_notifications_are_deserialized(datasets: Datasets):
    stub_get_dataset_by([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.retrieve_by_id(DATASET_ID)
    notifs = dataset.organization.notifications

    for n in notifs:
        assert isinstance(n, Notification)

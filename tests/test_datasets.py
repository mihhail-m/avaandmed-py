# type: ignore
import pytest
import responses
from pathlib import Path
from typing import List

from avaandmed import Avaandmed
from avaandmed.api_resources.entities import (
    Access,
    Category,
    Citation,
    Conformity,
    CoordinateReferenceSystem,
    File,
    FileColumn,
    Keyword,
    Licence,
    Notification,
    Region,
    ResourceType,
    SearchResult,
    TopicCategory,
    UpdateIntervalUnit
)
from avaandmed.api_resources.datasets import Datasets
from avaandmed.api_resources.datasets.dataset import Dataset
from avaandmed.api_resources.organizations.organization import Organization
from avaandmed.api_resources.users.user import User
from avaandmed.api_resources.organizations.my_organization import MyOrganization
from avaandmed.exceptions import AvaandmedApiExcepiton, AvaandmedException
from .utils import load_json

DATA_DIR = Path('data')
DATASET_ID = '8d681e55-4118-41f5-b319-1d2bdd36408c'
DATASET_ID_2 = '4446e091-adfc-4e1a-9e13-733d2b95f6e4'
PROTO_DATASET_ID = 'c114a8a9-40ed-46c9-824f-dda1d92776de'
DATASET_SLUG = 'soidukite-staatused-eestis'
FILE_ID = 'b88c9edc-cf81-47a5-aaf0-40d2af2c73a1'
WRONG_SLUG = 'sdfsdf'
WRONG_ID = 'sdfsdfsd'
BASE_URL = 'https://avaandmedtest.eesti.ee/api/datasets'
MOCK_TOKEN_URL = 'https://avaandmedtest.eesti.ee/api/auth/key-login'

# Mock data/files
MOCK_DATASET_FILE = DATA_DIR / 'dataset.json'
MOCK_DATSET_FILE_2 = DATA_DIR / 'dataset2.json'
MOCK_ERROR_FILE = DATA_DIR / 'error.json'
MOCK_TOKEN_FILE = DATA_DIR / 'token.json'
MOCK_DATASET_LIST_FILE = DATA_DIR / 'dataset_list.json'
MOCK_PREVIEW_FILE = DATA_DIR / 'preview.json'
MOCK_COLUMNS_FILE = DATA_DIR / 'file_columns.json'
MOCK_SEARCH_RESULTS = DATA_DIR / 'search.json'


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


def stub_get(url_values: List[str], filename: Path):
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
        stub_get([DATASET_ID], MOCK_DATASET_FILE)
        dataset = datasets.get_by_id(DATASET_ID)


@responses.activate
def test_get_by_id(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.GET,
        join_base_url_values([DATASET_ID]),
        json=load_json(MOCK_DATASET_FILE),
        status=200
    )

    dataset = datasets.get_by_id(DATASET_ID)
    assert isinstance(dataset, Dataset)
    assert DATASET_ID == dataset.id
    assert dataset.user is not None


@responses.activate
def test_negative_get_by_id(datasets: Datasets):
    with pytest.raises(AvaandmedApiExcepiton):
        mock_post_auth()
        responses.add(
            responses.GET,
            join_base_url_values([WRONG_ID]),
            json=load_json(MOCK_ERROR_FILE),
            status=404
        )

        datasets.get_by_id(WRONG_ID)


@responses.activate
def test_get_by_slug(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.GET,
        join_base_url_values(['slug', DATASET_SLUG]),
        json=load_json(MOCK_DATASET_FILE),
        status=200
    )

    dataset = datasets.get_by_slug(DATASET_SLUG)
    assert isinstance(dataset, Dataset)
    assert DATASET_SLUG == dataset.slug


@responses.activate
def test_negative_get_by_slug(datasets: Datasets):
    with pytest.raises(AvaandmedApiExcepiton):
        mock_post_auth()
        responses.add(
            responses.GET,
            join_base_url_values(['slug', WRONG_SLUG]),
            json=load_json(MOCK_ERROR_FILE),
            status=404
        )

        datasets.get_by_slug(WRONG_SLUG)


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

    dataset = datasets.get_by_id(DATASET_ID)
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

    dataset = datasets.get_by_id(DATASET_ID)
    organization_dict = dataset.organization.dict()
    assert isinstance(dataset.organization, Organization)
    for v in organization_dict.values():
        assert v is not None


@responses.activate
def test_files_are_deserialized(datasets: Datasets):
    stub_get([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.get_by_id(DATASET_ID)
    files = dataset.files
    assert isinstance(files[0], File)


@responses.activate
def test_keywords_are_deserialized(datasets: Datasets):
    stub_get([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.get_by_id(DATASET_ID)
    keywords = dataset.keywords
    assert isinstance(keywords[0], Keyword)


@responses.activate
def test_categories_are_deserialized(datasets: Datasets):
    stub_get([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.get_by_id(DATASET_ID)
    categories = dataset.categories
    assert isinstance(categories[0], Category)


@responses.activate
def test_regions_are_deserialized(datasets: Datasets):
    stub_get([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.get_by_id(DATASET_ID)
    regions = dataset.regions
    assert isinstance(regions[0], Region)


@responses.activate
def test_coords_are_deserialized(datasets: Datasets):
    stub_get([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.get_by_id(DATASET_ID)
    coords = dataset.coordinate_reference_systems
    assert isinstance(coords[0], CoordinateReferenceSystem)


@responses.activate
def test_citations_are_deserialized(datasets: Datasets):
    stub_get([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.get_by_id(DATASET_ID)
    citations = dataset.citations
    assert isinstance(citations[0], Citation)


@responses.activate
def test_conformities_are_deserialized(datasets: Datasets):
    stub_get([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.get_by_id(DATASET_ID)
    conformities = dataset.conformities
    assert isinstance(conformities[0], Conformity)


@responses.activate
def test_license_is_deserialized(datasets: Datasets):
    stub_get([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.get_by_id(DATASET_ID)
    licence = dataset.licence
    assert isinstance(licence, Licence)


@responses.activate
def test_interval_is_deserialized(datasets: Datasets):
    stub_get([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.get_by_id(DATASET_ID)
    interval = dataset.update_interval_unit
    assert isinstance(interval, UpdateIntervalUnit)


@responses.activate
def test_access_is_deserialized(datasets: Datasets):
    stub_get([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.get_by_id(DATASET_ID)
    access = dataset.access
    assert isinstance(access, Access)


@responses.activate
def test_res_type_is_deserialized(datasets: Datasets):
    stub_get([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.get_by_id(DATASET_ID)
    res_type = dataset.resource_type
    assert isinstance(res_type, ResourceType)


@responses.activate
def test_topics_are_deserialized(datasets: Datasets):
    stub_get([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.get_by_id(DATASET_ID)
    topics = dataset.topic_categories

    for topic in topics:
        assert isinstance(topic, TopicCategory)


@responses.activate
def test_notifications_are_deserialized(datasets: Datasets):
    stub_get([DATASET_ID], MOCK_DATASET_FILE)

    dataset = datasets.get_by_id(DATASET_ID)
    notifs = dataset.organization.notifications

    for n in notifs:
        assert isinstance(n, Notification)


@responses.activate
def test_get_file_preview(datasets: Datasets):
    mock_post_auth()
    stub_get([DATASET_ID, 'files', FILE_ID, 'preview'], MOCK_PREVIEW_FILE)
    preview = datasets.get_file_rows_preview(DATASET_ID, FILE_ID)

    assert preview is not None


@responses.activate
def test_get_dataset2(datasets: Datasets):
    mock_post_auth()
    stub_get([DATASET_ID_2], MOCK_DATSET_FILE_2)
    dataset = datasets.get_by_id(DATASET_ID_2)

    assert dataset.parent_datasets is not None


@responses.activate
def test_file_columns(datasets: Datasets):
    mock_post_auth()
    stub_get([DATASET_ID, 'files', FILE_ID, 'columns'], MOCK_COLUMNS_FILE)
    file_columns = datasets.get_file_columns(DATASET_ID, FILE_ID)

    assert isinstance(file_columns[0], FileColumn)


@responses.activate
def test_get_dataset_rating_by_slug(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.GET,
        join_base_url_values(['rating', DATASET_SLUG]),
        json={
            "data": "5.00"
        },
        status=200
    )

    rating = datasets.get_dataset_rating_by_slug(DATASET_SLUG)

    assert isinstance(rating, str)
    assert rating == '5.00'


@responses.activate
def test_file_privacy_violation(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.POST,
        join_base_url_values(['privacy-violations']),
        status=201
    )

    violation = datasets.file_privacy_violations(PROTO_DATASET_ID,
                                                 "This is long privacy violation message for testing.")

    assert violation == 'Submitted'


@responses.activate
def test_negative_file_privacy_violation(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.POST,
        join_base_url_values(['privacy-violations']),
        status=201
    )

    with pytest.raises(AvaandmedException):
        datasets.apply_for_access(
            PROTO_DATASET_ID, "")

    # > 1000 characters
    with pytest.raises(AvaandmedException):
        datasets.apply_for_access(PROTO_DATASET_ID, """D0roypVrlJRk8ocBSRtQGXesa4PaZOHDsLH4HDKbUgqkB
        nMVLgvyXTwoa3BOxGSPnFIfVjJoEEzp75JAe3a65auWTavf3vecdurrjjV9LKGyo48ThzONFa6u0DX7IUoRiIEUkfCAb
        iqzXfsVa543qD6R3BKTtyDabYdmZfEiahMiQ6GyCt90WeS1CpEmb2pJHHLZ6lQu
        x8tclXlcXqBXATDGTWzgWc8E23Dk5TnJdT4ZcEDZLAFhieiYvebe98Sq2pK0rkc
        Ik56MVctve2d1FOmtbypO9iRvgBSOjl1aweuIcpKK8HVnVLVsc3ssGTSYQuyZya
        zHxfA4xsi9kla09GezkIGllpJUJBblkqAv0hDVNSbAAlmx0TFDhOl6ue2LsoBLP
        LiIyEdkeFe17VQp2xvKbbguY4DMXjpyQUl6OgcfS5tpyOoXN1aXjBAVTx3sAfYe
        qo44Y3cM0wHkZIWeixTJ0VS035xs4GQd1CA5tw2Ym5H2sxwR1Q2wNca0XjdA9x7
        n38TCavreODCq3tVXveNZNl77hGTr1HNp8zdDsGlKsICy3qhBPelFSTSC855NrA
        ZnnT6OW1HT4QokYKraib5J4FkQ3m6533TJSVKyAb3TisQOi4TsyrSIuhqWtYHhs
        lSUtZxDd7jLdXCVstmBGDlBXdB8kJQEvYf3tSOvWpvyq3r2YdtytIdfDrXQU9Jj
        haT3oMpRE8UcecvBBbqxaIZCHBEepZ2ZMXmdZUY4R1vvEyZGn2r388jULxFdl4U
        XSKIRUh0ch4UNOJDCqBASGEOalB39ezgsKoBlwjRSSuT61Dhjtk4AXBVJk6ogdL
        EUTpw2Hx7y6OWHIwOj6JNqmOBDiYwDZHCbUaN7MHqAsHuAXE889MdtzmgilbXVk
        o44RNWMUEwJIDhXnRfSQxqrKioJj3Iv66c8lzEKUdNucCAFDFj71ut7aLxyy3Xf
        eHhVkPP9z3MjI9ug5f9Q0W8qvLCkSYw4x""")


@responses.activate
def test_apply_for_permissions(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.POST,
        join_base_url_values(['access-permissions']),
        status=201
    )

    access = datasets.apply_for_access(PROTO_DATASET_ID,
                                       "This is long access permissions message for testing.")

    assert access == 'Submitted'


@responses.activate
def test_negative_apply_for_permissions(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.POST,
        join_base_url_values(['access-permissions']),
        status=201
    )

    with pytest.raises(AvaandmedException):
        datasets.apply_for_access(
            PROTO_DATASET_ID, "")

    # > 1000 characters
    with pytest.raises(AvaandmedException):
        datasets.apply_for_access(PROTO_DATASET_ID, """D0roypVrlJRk8ocBSRtQGXesa4PaZOHDsLH4HDKbUgqkB
        nMVLgvyXTwoa3BOxGSPnFIfVjJoEEzp75JAe3a65auWTavf3vecdurrjjV9LKGyo48ThzONFa6u0DX7IUoRiIEUkfCAb
        iqzXfsVa543qD6R3BKTtyDabYdmZfEiahMiQ6GyCt90WeS1CpEmb2pJHHLZ6lQu
        x8tclXlcXqBXATDGTWzgWc8E23Dk5TnJdT4ZcEDZLAFhieiYvebe98Sq2pK0rkc
        Ik56MVctve2d1FOmtbypO9iRvgBSOjl1aweuIcpKK8HVnVLVsc3ssGTSYQuyZya
        zHxfA4xsi9kla09GezkIGllpJUJBblkqAv0hDVNSbAAlmx0TFDhOl6ue2LsoBLP
        LiIyEdkeFe17VQp2xvKbbguY4DMXjpyQUl6OgcfS5tpyOoXN1aXjBAVTx3sAfYe
        qo44Y3cM0wHkZIWeixTJ0VS035xs4GQd1CA5tw2Ym5H2sxwR1Q2wNca0XjdA9x7
        n38TCavreODCq3tVXveNZNl77hGTr1HNp8zdDsGlKsICy3qhBPelFSTSC855NrA
        ZnnT6OW1HT4QokYKraib5J4FkQ3m6533TJSVKyAb3TisQOi4TsyrSIuhqWtYHhs
        lSUtZxDd7jLdXCVstmBGDlBXdB8kJQEvYf3tSOvWpvyq3r2YdtytIdfDrXQU9Jj
        haT3oMpRE8UcecvBBbqxaIZCHBEepZ2ZMXmdZUY4R1vvEyZGn2r388jULxFdl4U
        XSKIRUh0ch4UNOJDCqBASGEOalB39ezgsKoBlwjRSSuT61Dhjtk4AXBVJk6ogdL
        EUTpw2Hx7y6OWHIwOj6JNqmOBDiYwDZHCbUaN7MHqAsHuAXE889MdtzmgilbXVk
        o44RNWMUEwJIDhXnRfSQxqrKioJj3Iv66c8lzEKUdNucCAFDFj71ut7aLxyy3Xf
        eHhVkPP9z3MjI9ug5f9Q0W8qvLCkSYw4x""")


@responses.activate
def test_rate_dataset(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.POST,
        join_base_url_values(['rating']),
        status=201
    )

    rating = datasets.rate_dataset(
        'c114a8a9-40ed-46c9-824f-dda1d92776de', 1, 1)

    assert rating == 'Submitted'


@responses.activate
def test_negative_rate_dataset(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.POST,
        join_base_url_values(['rating']),
        status=201
    )

    with pytest.raises(AvaandmedException):
        rating = datasets.rate_dataset(
            'c114a8a9-40ed-46c9-824f-dda1d92776de', -1, 11)

    with pytest.raises(AvaandmedException):
        rating = datasets.rate_dataset(
            'c114a8a9-40ed-46c9-824f-dda1d92776de', 0, -1)

    with pytest.raises(AvaandmedException):
        rating = datasets.rate_dataset(
            'c114a8a9-40ed-46c9-824f-dda1d92776de', 11, -1)


@responses.activate
def test_download_file(datasets: Datasets):
    mock_post_auth()
    responses.add(
        responses.POST,
        join_base_url_values([DATASET_ID, 'files', FILE_ID, 'download']),
        body=b"Some sort of text.",
    )
    outfile = 'outfile.txt'

    result = datasets.download_file(
        DATASET_ID,
        FILE_ID,
        outfile
    )

    from pathlib import Path
    f = Path(outfile)

    assert f.exists()
    assert result == 0


@responses.activate
def test_search(datasets: Datasets):
    keyword_id = 41
    region_id = 2
    year = 2020
    search_url = f"search?keywordIds={keyword_id}&regionIds={region_id}&year={year}"

    stub_get([search_url], MOCK_SEARCH_RESULTS)
    result = datasets.search(keyword_id, region_id, year)

    assert isinstance(result[0], SearchResult)

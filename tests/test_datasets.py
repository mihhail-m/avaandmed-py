# type: ignore
import pytest
import responses
from typing import List

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
from tests.data_mock import DataJsonMock
from .request_mock import RequestMock

DATASET_ID = '8d681e55-4118-41f5-b319-1d2bdd36408c'
DATASET_ID_2 = '4446e091-adfc-4e1a-9e13-733d2b95f6e4'
PROTO_DATASET_ID = 'c114a8a9-40ed-46c9-824f-dda1d92776de'
DATASET_SLUG = 'soidukite-staatused-eestis'
FILE_ID = 'b88c9edc-cf81-47a5-aaf0-40d2af2c73a1'
WRONG_SLUG = 'sdfsdf'
WRONG_ID = 'sdfsdfsd'


class TestDatasets:

    @pytest.fixture(autouse=True)
    def _request_mock(self, request_mock: RequestMock):
        self.request_mock = request_mock
        self.request_mock.endpoint = '/datasets'

    @pytest.fixture(autouse=True)
    def _datasets(self, datasets: Datasets):
        self.datasets = datasets

    @pytest.fixture(autouse=True)
    def _data_mock(self, data_mock: DataJsonMock):
        """
        Fixture to define all mock data for the current test file.
        """
        self.mock_dataset = data_mock.MOCK_DATASET_FILE
        self.mock_dataset_2 = data_mock.MOCK_DATSET_FILE_2
        self.mock_error = data_mock.MOCK_ERROR_FILE
        self.mock_dataset_list = data_mock.MOCK_DATASET_LIST_FILE
        self.mock_preview_file = data_mock.MOCK_PREVIEW_FILE
        self.mock_columns_file = data_mock.MOCK_COLUMNS_FILE
        self.mock_search_results = data_mock.MOCK_SEARCH_RESULTS

    def test_json_to_model(self):
        dataset = Dataset.parse_obj(self.mock_dataset['data'])
        assert dataset.name == 'Sõidukite staatused Eestis'
        assert isinstance(dataset, Dataset)

    @responses.activate
    def test_negative_post_auth(self):
        with pytest.raises(AvaandmedApiExcepiton):
            self.request_mock.mock_negative_post_auth(401, "Unauthorized")
            self.request_mock.stub_for(f"/{DATASET_ID}")
            dataset = self.datasets.get_by_id(DATASET_ID)

    @responses.activate
    def test_get_by_id(self):
        self.request_mock.stub_for(
            url=f"/{DATASET_ID}", json=self.mock_dataset)
        dataset = self.datasets.get_by_id(DATASET_ID)
        assert isinstance(dataset, Dataset)
        assert DATASET_ID == dataset.id
        assert dataset.user is not None

    @responses.activate
    def test_negative_get_by_id(self):
        with pytest.raises(AvaandmedApiExcepiton):
            self.request_mock.stub_for(
                url=f"/{WRONG_ID}", status=404, json=self.mock_error)
            self.datasets.get_by_id(WRONG_ID)

    @responses.activate
    def test_get_by_slug(self):
        self.request_mock.stub_for(
            url=f"/slug/{DATASET_SLUG}", json=self.mock_dataset)
        dataset = self.datasets.get_by_slug(DATASET_SLUG)
        assert isinstance(dataset, Dataset)
        assert DATASET_SLUG == dataset.slug

    @responses.activate
    def test_negative_get_by_slug(self):
        with pytest.raises(AvaandmedApiExcepiton):
            self.request_mock.stub_for(
                url=f"/slug/{WRONG_SLUG}", status=404, json=self.mock_error)
            self.datasets.get_by_slug(WRONG_SLUG)

    @responses.activate
    def test_get_dataset_list(self):
        limit = 5
        self.request_mock.stub_for(
            url=f"?limit={limit}", json=self.mock_dataset_list)
        dataset_list = self.datasets.get_dataset_list(limit=limit)
        assert dataset_list is not None
        assert len(dataset_list) == limit

    def test_negative_dataset_list_limit_zero(self):
        with pytest.raises(AvaandmedException):
            self.datasets.get_dataset_list(limit=0)

    def test_negative_dataset_list_negative_limit(self):
        with pytest.raises(AvaandmedException):
            self.datasets.get_dataset_list(limit=-1)

    @responses.activate
    def test_get_datasets_total(self):
        n = 123
        self.request_mock.stub_for(url='/total', json={'data': n})

        total = self.datasets.get_total()
        assert total is not None
        assert isinstance(total, int)
        assert total == n

    @responses.activate
    def test_get_mimetypes(self):
        json = {
            'data': [
                'application/pdf',
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'text/xml'
            ]
        }
        self.request_mock.stub_for(url='/mimetypes/distinct', json=json)
        mimetypes = self.datasets.get_distinct_mimetypes()
        assert mimetypes is not None

    @responses.activate
    def test_user_is_deserialized(self):
        self.request_mock.stub_for(
            url=f"/{DATASET_ID}", json=self.mock_dataset)
        dataset = self.datasets.get_by_id(DATASET_ID)
        user_dict = dataset.user.dict()  # type: ignore
        for v in user_dict.values():
            assert v is not None
        assert isinstance(dataset.user, User)

    @responses.activate
    def test_organization_is_deserialized(self):
        self.request_mock.stub_for(
            url=f"/{DATASET_ID}", json=self.mock_dataset)
        dataset = self.datasets.get_by_id(DATASET_ID)
        organization_dict = dataset.organization.dict()
        assert isinstance(dataset.organization, Organization)

    @responses.activate
    def test_files_are_deserialized(self):
        self.request_mock.stub_for(
            url=f"/{DATASET_ID}", json=self.mock_dataset)
        dataset = self.datasets.get_by_id(DATASET_ID)
        files = dataset.files
        assert isinstance(files[0], File)

    @responses.activate
    def test_keywords_are_deserialized(self):
        self.request_mock.stub_for(
            url=f"/{DATASET_ID}", json=self.mock_dataset)
        dataset = self.datasets.get_by_id(DATASET_ID)
        keywords = dataset.keywords
        assert isinstance(keywords[0], Keyword)

    @responses.activate
    def test_categories_are_deserialized(self):
        self.request_mock.stub_for(
            url=f"/{DATASET_ID}", json=self.mock_dataset)
        dataset = self.datasets.get_by_id(DATASET_ID)
        categories = dataset.categories
        assert isinstance(categories[0], Category)

    @responses.activate
    def test_regions_are_deserialized(self):
        self.request_mock.stub_for(
            url=f"/{DATASET_ID}", json=self.mock_dataset)
        dataset = self.datasets.get_by_id(DATASET_ID)
        regions = dataset.regions
        assert isinstance(regions[0], Region)

    @responses.activate
    def test_coords_are_deserialized(self):
        self.request_mock.stub_for(
            url=f"/{DATASET_ID}", json=self.mock_dataset)
        dataset = self.datasets.get_by_id(DATASET_ID)
        coords = dataset.coordinate_reference_systems
        assert isinstance(coords[0], CoordinateReferenceSystem)

    @responses.activate
    def test_citations_are_deserialized(self):
        self.request_mock.stub_for(
            url=f"/{DATASET_ID}", json=self.mock_dataset)
        dataset = self.datasets.get_by_id(DATASET_ID)
        citations = dataset.citations
        assert isinstance(citations[0], Citation)

    @responses.activate
    def test_conformities_are_deserialized(self):
        self.request_mock.stub_for(
            url=f"/{DATASET_ID}", json=self.mock_dataset)
        dataset = self.datasets.get_by_id(DATASET_ID)
        conformities = dataset.conformities
        assert isinstance(conformities[0], Conformity)

    @responses.activate
    def test_license_is_deserialized(self):
        self.request_mock.stub_for(
            url=f"/{DATASET_ID}", json=self.mock_dataset)
        dataset = self.datasets.get_by_id(DATASET_ID)
        licence = dataset.licence
        assert isinstance(licence, Licence)

    @responses.activate
    def test_interval_is_deserialized(self):
        self.request_mock.stub_for(
            url=f"/{DATASET_ID}", json=self.mock_dataset)
        dataset = self.datasets.get_by_id(DATASET_ID)
        interval = dataset.update_interval_unit
        assert isinstance(interval, UpdateIntervalUnit)

    @responses.activate
    def test_access_is_deserialized(self):
        self.request_mock.stub_for(
            url=f"/{DATASET_ID}", json=self.mock_dataset)
        dataset = self.datasets.get_by_id(DATASET_ID)
        access = dataset.access
        assert isinstance(access, Access)

    @responses.activate
    def test_res_type_is_deserialized(self):
        self.request_mock.stub_for(
            url=f"/{DATASET_ID}", json=self.mock_dataset)
        dataset = self.datasets.get_by_id(DATASET_ID)
        res_type = dataset.resource_type
        assert isinstance(res_type, ResourceType)

    @responses.activate
    def test_topics_are_deserialized(self):
        self.request_mock.stub_for(
            url=f"/{DATASET_ID}", json=self.mock_dataset)
        dataset = self.datasets.get_by_id(DATASET_ID)
        topics = dataset.topic_categories

        for topic in topics:
            assert isinstance(topic, TopicCategory)

    @responses.activate
    def test_notifications_are_deserialized(self):
        self.request_mock.stub_for(
            url=f"/{DATASET_ID}", json=self.mock_dataset)
        dataset = self.datasets.get_by_id(DATASET_ID)
        notifs = dataset.organization.notifications

        for n in notifs:
            assert isinstance(n, Notification)

    @responses.activate
    def test_get_file_preview(self):
        url = f"/{DATASET_ID}/files/{FILE_ID}/preview"
        self.request_mock.stub_for(url=url, json=self.mock_preview_file)
        preview = self.datasets.get_file_rows_preview(DATASET_ID, FILE_ID)

        assert preview is not None

    @responses.activate
    def test_get_dataset2(self):
        self.request_mock.stub_for(
            url=f"/{DATASET_ID_2}", json=self.mock_dataset_2)
        dataset = self.datasets.get_by_id(DATASET_ID_2)

        assert dataset.parent_datasets is not None

    @responses.activate
    def test_file_columns(self):
        url = f"/{DATASET_ID}/files/{FILE_ID}/columns"
        self.request_mock.stub_for(url=url, json=self.mock_columns_file)
        file_columns = self.datasets.get_file_columns(DATASET_ID, FILE_ID)

        assert isinstance(file_columns[0], FileColumn)

    @responses.activate
    def test_get_dataset_rating_by_slug(self):
        self.request_mock.stub_for(url=f"/rating/{DATASET_SLUG}", json={
            "data": "5.00"
        })
        rating = self.datasets.get_dataset_rating_by_slug(DATASET_SLUG)

        assert isinstance(rating, str)
        assert rating == '5.00'

    @responses.activate
    def test_file_privacy_violation(self):
        self.request_mock.stub_for(
            method=responses.POST, url='/privacy-violations', status=201)
        violation = self.datasets.file_privacy_violations(PROTO_DATASET_ID,
                                                          "This is long privacy violation message for testing.")

        assert violation == 'Submitted'

    @responses.activate
    def test_negative_file_privacy_violation(self):
        self.request_mock.stub_for(
            method=responses.POST, url='/privacy-violations', status=201)
        with pytest.raises(AvaandmedException):
            self.datasets.apply_for_access(
                PROTO_DATASET_ID, "")

        # > 1000 characters
        with pytest.raises(AvaandmedException):
            self.datasets.apply_for_access(PROTO_DATASET_ID, """D0roypVrlJRk8ocBSRtQGXesa4PaZOHDsLH4HDKbUgqkB
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
    def test_apply_for_permissions(self):
        self.request_mock.stub_for(
            method=responses.POST, url='/access-permissions', status=201)
        access = self.datasets.apply_for_access(PROTO_DATASET_ID,
                                                "This is long access permissions message for testing.")

        assert access == 'Submitted'

    @responses.activate
    def test_negative_apply_for_permissions(self):
        self.request_mock.stub_for(
            method=responses.GET, url='/access-permissions', status=201)

        with pytest.raises(AvaandmedException):
            self.datasets.apply_for_access(
                PROTO_DATASET_ID, "")

        # > 1000 characters
        with pytest.raises(AvaandmedException):
            self.datasets.apply_for_access(PROTO_DATASET_ID, """D0roypVrlJRk8ocBSRtQGXesa4PaZOHDsLH4HDKbUgqkB
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
    def test_rate_dataset(self):
        self.request_mock.stub_for(
            method=responses.POST, url='/rating', status=201)
        rating = self.datasets.rate_dataset(
            'c114a8a9-40ed-46c9-824f-dda1d92776de', 1, 1)

        assert rating == 'Submitted'

    @responses.activate
    def test_negative_rate_dataset(self):
        self.request_mock.stub_for(
            method=responses.POST, url='/rating', status=201)

        with pytest.raises(AvaandmedException):
            rating = self.datasets.rate_dataset(
                'c114a8a9-40ed-46c9-824f-dda1d92776de', -1, 11)

        with pytest.raises(AvaandmedException):
            rating = self.datasets.rate_dataset(
                'c114a8a9-40ed-46c9-824f-dda1d92776de', 0, -1)

        with pytest.raises(AvaandmedException):
            rating = self.datasets.rate_dataset(
                'c114a8a9-40ed-46c9-824f-dda1d92776de', 11, -1)

    @responses.activate
    def test_download_file(self):
        url = f"/{DATASET_ID}/files/{FILE_ID}/download"
        self.request_mock.stub_for(
            method=responses.POST, url=url, body=b"Some sort of text", status=201)
        outfile = 'outfile.txt'

        result = self.datasets.download_file(
            DATASET_ID,
            FILE_ID,
            outfile
        )

        from pathlib import Path
        f = Path(outfile)

        assert f.exists()
        assert result == 0

    @responses.activate
    def test_search(self):
        keyword_id = 41
        region_id = 2
        year = 2020
        search_url = f"/search?keywordIds={keyword_id}&regionIds={region_id}&year={year}"

        self.request_mock.stub_for(
            url=search_url, json=self.mock_search_results)
        result = self.datasets.search(keyword_id, region_id, year)

        assert isinstance(result[0], SearchResult)

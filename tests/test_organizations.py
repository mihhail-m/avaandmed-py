import pytest
import responses

from typing import List
from avaandmed.api_resources.organizations.my_organization import MyOrganization, OrganizationDataset
from avaandmed.api_resources.datasets.dataset import Dataset
from avaandmed.api_resources.entities import AccessPermission, DatasetMetadata, DatasetRating, File, Identifier, Index, Polynomial, PrivacyViolation, ProcessingStatus, UpdateIntervalUnit
from avaandmed.api_resources.organizations.organization import Organization
from avaandmed.exceptions import AvaandmedApiExcepiton
from avaandmed.utils import build_endpoint
from .request_mock import RequestMock
from .data_mock import DataJsonMock

DATASET_ID = '4446e091-adfc-4e1a-9e13-733d2b95f6e4'
DATASET_SLUG = 'eesti-rahvastikutiheduse-1-km-x-1-km-ruutkaart'
FILE_ID = 'b88c9edc-cf81-47a5-aaf0-40d2af2c73a1'
VIOLTION_ID = '278876a6-24d2-4301-aafd-c14f4470c430'
PERM_ID = 'af1a7ed9-31c9-45a5-a8b3-e59345538444'
MY_ORG_ID = 'cf923536-2dbb-4e2e-8167-218e52316283'


class TestOrganizations:

    @pytest.fixture(autouse=True)
    def _request_mock(self, request_mock: RequestMock, my_org_id: str):
        self.request_mock = request_mock
        self.request_mock.endpoint = f"/organizations/my-organizations/{my_org_id}"
        self.my_org_dataset_base = "/datasets"
        self.my_orgs_endpoint = "/organizations/my-organizations"

    @pytest.fixture(autouse=True)
    def _my_org_datasets(self, organization_datasets: OrganizationDataset):
        self.datasets = organization_datasets

    @pytest.fixture(autouse=True)
    def _my_org(self, my_org: MyOrganization):
        self.my_org = my_org

    @pytest.fixture(autouse=True)
    def _data_mock(self, data_mock: DataJsonMock):
        self.mock_dataset = data_mock.MOCK_DATSET_FILE_2
        self.mock_error = data_mock.MOCK_ERROR_FILE
        self.mock_dataset_list = data_mock.MOCK_DATASET_LIST_FILE
        self.mock_file_preview = data_mock.MOCK_PREVIEW_FILE
        self.mock_privacy_violations = data_mock.MOCK_PRIVACY_VIOLATIONS
        self.mock_access_perms = data_mock.MOCK_ACCESS_PERMISSIONS
        self.mock_files_list = data_mock.MOCK_FILES_LIST
        self.mock_file_index = data_mock.MOCK_FILE_INDEX

    def build_mock_endpoint(self, resources: List[str] = []):
        return build_endpoint(self.my_org_dataset_base, resources)

    @responses.activate
    def test_get_by_id(self):
        self.request_mock.stub_for(
            url=self.build_mock_endpoint([DATASET_ID]),
            json=self.mock_dataset
        )
        my_org_ds = self.datasets.get_by_id(DATASET_ID)
        assert isinstance(my_org_ds, Dataset)

    @responses.activate
    def test_negative_get_by_id(self):
        self.request_mock.stub_for(
            url=self.build_mock_endpoint(['sdfsdf']),
            json=self.mock_error, status=404
        )

        with pytest.raises(AvaandmedApiExcepiton):
            my_ds = self.datasets.get_by_id('sdfsdf')

    @responses.activate
    def test_get_by_slug(self):
        self.request_mock.stub_for(
            url=self.build_mock_endpoint(['slug', DATASET_SLUG]),
            json=self.mock_dataset)
        dataset = self.datasets.get_by_slug(DATASET_SLUG)

        assert isinstance(dataset, Dataset)

    @responses.activate
    def test_get_dataset_list(self):
        self.request_mock.stub_for(
            url=f"{self.my_org_dataset_base}",
            json=self.mock_dataset_list)
        dataset_list = self.datasets.get_dataset_list()

        assert isinstance(dataset_list[0], Dataset)

    @responses.activate
    def test_get_file_preview(self):
        url = self.build_mock_endpoint(
            [DATASET_ID, 'files', FILE_ID, 'preview'])
        self.request_mock.stub_for(url=url, json=self.mock_file_preview)
        preview = self.datasets.get_file_rows_preview(DATASET_ID, FILE_ID)

        assert preview is not None

    @responses.activate
    def test_get_all_privacy_violations(self):
        url = self.build_mock_endpoint(['privacy-violations'])
        self.request_mock.stub_for(url=url, json=self.mock_privacy_violations)
        privacy_violations = self.datasets.get_all_privacy_violations()

        assert privacy_violations is not None
        assert isinstance(privacy_violations[0], PrivacyViolation)

    @responses.activate
    def test_get_privacy_violation_by_id(self):
        url = self.build_mock_endpoint(['privacy-violations', VIOLTION_ID])
        json = {
            "data": {
                "id": "c1e5e65e-3b1b-477e-966f-e402d1838c3a",
                "userId": "fa9d654b-48ed-49f2-871d-b70c535d90bc",
                "description": "This is long privacy violation message for testing.",
                "datasetId": "c114a8a9-40ed-46c9-824f-dda1d92776de",
                "status": "pending",
                "createdAt": "2021-12-06T10:59:54.447Z",
                "dataset": {
                    "id": "c114a8a9-40ed-46c9-824f-dda1d92776de",
                    "nameEt": "__proto__",
                    "nameEn": "__proto__",
                    "slug": "__proto__",
                    "organizationId": None,
                    "userId": "527a38c1-ea81-43ec-beb8-c616b5195fd1",
                    "name": "__proto__"
                },
                "user": {
                    "id": "fa9d654b-48ed-49f2-871d-b70c535d90bc",
                    "firstName": "Mihhail",
                    "lastName": "Matisinets",
                    "name": "Mihhail Matisinets"
                }
            }
        }
        self.request_mock.stub_for(url=url, json=json)
        violation = self.datasets.get_privacy_violation(VIOLTION_ID)

        assert isinstance(violation, PrivacyViolation)
        assert violation.user.first_name == 'Mihhail'

    @responses.activate
    def test_consider_privacy_violation(self):
        url = self.build_mock_endpoint(
            ['privacy-violations', VIOLTION_ID, 'consider'])
        self.request_mock.stub_for(url=url, method=responses.PUT, body='')
        result = self.datasets.consider_privacy_violation(VIOLTION_ID)

        assert result is True

    @responses.activate
    def test_disregard_privacy_violation(self):
        url = self.build_mock_endpoint(
            ['privacy-violations', VIOLTION_ID, 'disregard'])
        self.request_mock.stub_for(url, method=responses.PUT, body='')
        result = self.datasets.disregard_privacy_violtion(VIOLTION_ID)

        assert result is True

    @responses.activate
    def test_get_all_permissions(self):
        url = self.build_mock_endpoint(['access-permissions'])
        self.request_mock.stub_for(url, json=self.mock_access_perms)
        perms = self.datasets.get_all_access_permissions()

        assert isinstance(perms[0], AccessPermission)

    @responses.activate
    def test_get_access_permission(self):
        url = self.build_mock_endpoint(['access-permissions', PERM_ID])
        json = {
            "data": {
                "id": "af1a7ed9-31c9-45a5-a8b3-e59345538444",
                "userId": "fa9d654b-48ed-49f2-871d-b70c535d90bc",
                "datasetId": "818fe24e-4db3-4737-bcfc-84e7e2f550af",
                "status": "pending",
                "description": "Long description to apply for permissions access for testing.",
                "createdAt": "2021-12-16T10:17:20.949Z",
                "dataset": {
                    "id": "818fe24e-4db3-4737-bcfc-84e7e2f550af",
                    "nameEt": "avaandmed-py-test",
                    "nameEn": "avaandmed-py-test",
                    "slug": "avaandmed-py-test",
                    "organizationId": None,
                    "userId": "fa9d654b-48ed-49f2-871d-b70c535d90bc",
                    "name": "avaandmed-py-test"
                },
                "user": {
                    "id": "fa9d654b-48ed-49f2-871d-b70c535d90bc",
                    "firstName": "Mihhail",
                    "lastName": "Matisinets",
                    "name": "Mihhail Matisinets"
                }
            }
        }
        self.request_mock.stub_for(url=url, json=json)
        perm = self.datasets.get_access_permission(PERM_ID)

        assert isinstance(perm, AccessPermission)
        assert perm.id == PERM_ID

    @responses.activate
    def test_approve_permission(self):
        url = self.build_mock_endpoint(
            ['access-permissions', PERM_ID, 'approve'])
        self.request_mock.stub_for(url, method=responses.PUT, body='')
        result = self.datasets.approve_access_permission(PERM_ID)

        assert result is True

    @responses.activate
    def test_decline_permission(self):
        url = self.build_mock_endpoint(
            ['access-permissions', PERM_ID, 'decline'])
        self.request_mock.stub_for(url, method=responses.PUT, body='')
        result = self.datasets.decline_access_permission(PERM_ID)

        assert result is True

    @responses.activate
    def test_get_latest_pending(self):
        url = self.build_mock_endpoint(['latest', 'pending'])
        self.request_mock.stub_for(url=url, json=self.mock_dataset)
        dataset = self.datasets.get_latest_pending()

        assert isinstance(dataset, Dataset)
        assert dataset.status == ProcessingStatus.PENDING

    @responses.activate
    def test_delete_dataset(self):
        url = self.build_mock_endpoint([DATASET_ID])
        self.request_mock.stub_for(url=url, method=responses.DELETE, json={
            "data": "Dataset deleted"
        })
        result = self.datasets.delete(DATASET_ID)

        assert result is True

    @responses.activate
    def test_update_dataset(self):
        url = self.build_mock_endpoint([DATASET_ID])
        params = {
            "maintainerPhone": "+37255213451",
            "maintainerEmail": "new_email@gmail.com"
        }
        self.request_mock.stub_for(url=url, method=responses.PUT)
        result = self.datasets.update(DATASET_ID, params)

        assert result is True

    @responses.activate
    def test_discard_dataset(self):
        url = self.build_mock_endpoint([DATASET_ID, 'discard'])
        self.request_mock.stub_for(url=url, method=responses.PUT)
        result = self.datasets.discard(DATASET_ID)

        assert result is True

    @responses.activate
    def test_publish_dataset(self):
        url = self.build_mock_endpoint([DATASET_ID, 'publish'])
        self.request_mock.stub_for(url=url, method=responses.PUT)
        result = self.datasets.publish(DATASET_ID)

        assert result is True

    @responses.activate
    def test_get_files(self):
        url = self.build_mock_endpoint([DATASET_ID, 'files'])
        self.request_mock.stub_for(url, json=self.mock_files_list)
        result = self.datasets.get_all_files(DATASET_ID)

        assert isinstance(result[0], File)

    @responses.activate
    def test_get_file_index(self):
        url = self.build_mock_endpoint(
            [DATASET_ID, 'files', FILE_ID, 'indices'])
        self.request_mock.stub_for(url, json=self.mock_file_index)
        result = self.datasets.get_file_index(DATASET_ID, FILE_ID)

        assert isinstance(result, Index)
        assert isinstance(result.polynomial[0], Polynomial)
        assert isinstance(result.identifier[0], Identifier)

    @responses.activate
    def test_get_file_rows(self):
        url = self.build_mock_endpoint([DATASET_ID, 'files', FILE_ID])
        self.request_mock.stub_for(url, json=self.mock_file_preview)
        result = self.datasets.get_file_rows_with_errors(DATASET_ID, FILE_ID)

        assert result is not None

    @responses.activate
    def test_delete_file(self):
        url = self.build_mock_endpoint([DATASET_ID, 'files', FILE_ID])
        self.request_mock.stub_for(url=url, method=responses.DELETE, json={
            "data": "deleted"
        })
        result = self.datasets.delete_file(DATASET_ID, FILE_ID)

        assert result is True

    @responses.activate
    def test_get_user_dataset_rating(self):
        url = self.build_mock_endpoint([DATASET_SLUG, 'ratings'])
        json = {
            "data": [
                {
                    "id": 76,
                    "datasetId": "a25f9e33-cc44-43a5-988d-15af80de5c0b",
                    "qualityRating": 9,
                    "metadataRating": 10,
                    "description": "kirjeldus",
                    "createdAt": "2021-12-27T10:26:49.318Z",
                    "updatedAt": "2021-12-27T10:26:49.318Z",
                    "user": {
                        "id": "fa9d654b-48ed-49f2-871d-b70c535d90bc",
                        "firstName": "Mihhail",
                        "lastName": "Matisinets",
                        "slug": "mihhail-matisinets",
                        "email": "mihhail.matisinets@gmail.com",
                        "name": "Mihhail Matisinets"
                    }
                }
            ],
            "metadata": {
                "total": 1
            }
        }

        self.request_mock.stub_for(url=url, json=json)
        result = self.datasets.get_rating(DATASET_SLUG)

        assert isinstance(result[0], DatasetRating)

    @responses.activate
    def test_create_file_indices(self):
        url = self.build_mock_endpoint(
            [DATASET_ID, 'files', FILE_ID, 'indices'])
        json = {
            "identifier": [
                {
                    "column": "aasta",
                    "identifier": "id-1"
                },
                {
                    "column": "Movie",
                    "identifier": "movie-1"
                }
            ],
            "polynomial": [
                {
                    "column": "aasta"
                }
            ]
        }
        response_json = {
            "data": "Indices created"
        }

        self.request_mock.stub_for(
            url=url, method=responses.POST, json=response_json, status=201)
        result = self.datasets.create_file_indices(
            DATASET_ID,
            FILE_ID,
            json
        )

        assert result is not None
        assert result is True

    @responses.activate
    def test_get_list_orgs(self):
        my_org = self.my_org
        json_mock = {
            "data": [
                {
                    "id": "cf923536-2dbb-4e2e-8167-218e52316283",
                    "regCode": "11383889",
                    "name": "TARA Test AS",
                    "slug": "organization-slug-22",
                    "contact": "User user",
                    "contactEmail": "test@test.se",
                    "description": "Andmetöötlus, veebihosting jms tegevused",
                    "isPublicBody": None,
                    "notifications": [
                        "DATASET_COMMENTED",
                        "DATASET_RATED",
                        "DATASET_ACCESS_REQUEST",
                        "DATA_WISH_NEW",
                        "DATASET_PRIVACY_VIOLATION"
                    ],
                    "orgUser": {
                        "id": "c8ece9d8-a5aa-45dd-951c-11a0b86a572a",
                        "organizationId": "cf923536-2dbb-4e2e-8167-218e52316283",
                        "userId": "fa9d654b-48ed-49f2-871d-b70c535d90bc",
                        "userJobTitle": "tudeng",
                        "userRole": "manager",
                        "userDomain": "local",
                        "userRoleValidFrom": "2021-11-10T14:34:02.000Z",
                        "userRoleValidTo": "2026-11-10T14:34:02.000Z"
                    },
                    "domain": "local"
                },
                {
                    "id": "cf923536-2dbb-4e2e-8167-218e52316283",
                    "regCode": "11383889",
                    "name": "TARA Test AS",
                    "slug": "organization-slug-22",
                    "contact": "User user",
                    "contactEmail": "test@test.se",
                    "description": "Andmetöötlus, veebihosting jms tegevused",
                    "isPublicBody": None,
                    "notifications": [
                        "DATASET_COMMENTED",
                        "DATASET_RATED",
                        "DATASET_ACCESS_REQUEST",
                        "DATA_WISH_NEW",
                        "DATASET_PRIVACY_VIOLATION"
                    ],
                    "orgUser": {
                        "id": "c8ece9d8-a5aa-45dd-951c-11a0b86a572a",
                        "organizationId": "cf923536-2dbb-4e2e-8167-218e52316283",
                        "userId": "fa9d654b-48ed-49f2-871d-b70c535d90bc",
                        "userJobTitle": "tudeng",
                        "userRole": "manager",
                        "userDomain": "local",
                        "userRoleValidFrom": "2021-11-10T14:34:02.000Z",
                        "userRoleValidTo": "2026-11-10T14:34:02.000Z"
                    },
                    "domain": "local"
                }
            ]
        }
        self.request_mock.endpoint = self.my_orgs_endpoint
        self.request_mock.stub_for(url='', json=json_mock)
        list_orgs = my_org.get_list_my_orgs()

        assert list_orgs is not None
        assert len(list_orgs) == 2
        assert isinstance(list_orgs[0], Organization)

    @responses.activate
    def test_get_org_by_id(self):
        my_org = self.my_org
        json_mock = {
            "data": {
                "id": "cf923536-2dbb-4e2e-8167-218e52316283",
                "regCode": "11383889",
                "name": "TARA Test AS",
                "slug": "organization-slug-22",
                "contact": "User user",
                "contactEmail": "test@test.se",
                "description": "Andmetöötlus, veebihosting jms tegevused",
                "isPublicBody": None,
                "notifications": [
                    "DATASET_COMMENTED",
                    "DATASET_RATED",
                    "DATASET_ACCESS_REQUEST",
                    "DATA_WISH_NEW",
                    "DATASET_PRIVACY_VIOLATION"
                ],
                "image": None
            }
        }
        self.request_mock.endpoint = f"{self.my_orgs_endpoint}/{MY_ORG_ID}"
        self.request_mock.stub_for(url='', json=json_mock)
        org = my_org.get_my_org_by_id(MY_ORG_ID)

        assert org is not None
        assert isinstance(org, Organization)

    @responses.activate
    def test_create_dataset_metadata(self):
        metadata = DatasetMetadata(
            nameEt="name8",
            nameEn="name8",
            descriptionEt="desc",
            descriptionEn="desc",
            maintainer="mihhail",
            maintainerEmail="mihhail@gmail.com",
            maintainerPhone="+37255555555",
            keywordIds=[20],
            categoryIds=[1],
            regionIds=[1],
            dataFrom="2022-02-13T22:00:00.000Z",
            availableTo="2022-02-28T21:59:59.999Z",
            updateIntervalUnit=UpdateIntervalUnit.DAY,
            updateIntervalFrequency=1)

        self.request_mock.stub_for(
            '/datasets', responses.POST, status=201, json=self.mock_dataset)
        result = self.datasets.create_dataset_metadata(metadata)

        assert result is not None
        assert isinstance(result, Dataset)

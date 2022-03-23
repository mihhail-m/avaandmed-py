import pytest
import responses
from avaandmed.api_resources.datasets.dataset import Dataset
from avaandmed.api_resources.entities import AccessPermission, DatasetMetadata, DatasetRating, File, Identifier, Index, Polynomial, PrivacyViolation, ProcessingStatus, UpdateIntervalUnit
from avaandmed.api_resources.users.me import UserDataset
from avaandmed.exceptions import AvaandmedApiExcepiton
from tests.data_mock import DataJsonMock
from .request_mock import RequestMock

DATASET_ID_2 = '4446e091-adfc-4e1a-9e13-733d2b95f6e4'
DATASET_SLUG = 'eesti-rahvastikutiheduse-1-km-x-1-km-ruutkaart'
FILE_ID = 'b88c9edc-cf81-47a5-aaf0-40d2af2c73a1'
VIOLTION_ID = '278876a6-24d2-4301-aafd-c14f4470c430'
PERM_ID = 'af1a7ed9-31c9-45a5-a8b3-e59345538444'


class TestUsersDatasets:

    @pytest.fixture(autouse=True)
    def _request_mock(self, request_mock: RequestMock):
        self.request_mock = request_mock
        self.request_mock.endpoint = '/users/me/datasets'

    @pytest.fixture(autouse=True)
    def _users_datasets(self, users_datasets: UserDataset):
        self.datasets = users_datasets

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
        self.mock_file_path = data_mock.MOCK_FILE_PATH

    @responses.activate
    def test_get_by_id(self):
        self.request_mock.stub_for(
            url=f"/{DATASET_ID_2}", json=self.mock_dataset)
        my_ds = self.datasets.get_by_id(DATASET_ID_2)

        assert isinstance(my_ds, Dataset)

    @responses.activate
    def test_negative_get_by_id(self):
        self.request_mock.stub_for(
            url=f"/sdfsdf", json=self.mock_error, status=404
        )

        with pytest.raises(AvaandmedApiExcepiton):
            my_ds = self.datasets.get_by_id('sdfsdf')

    @responses.activate
    def test_get_by_slug(self):
        self.request_mock.stub_for(
            url=f"/slug/{DATASET_SLUG}", json=self.mock_dataset)
        dataset = self.datasets.get_by_slug(DATASET_SLUG)

        assert isinstance(dataset, Dataset)

    @responses.activate
    def test_get_dataset_list(self):
        self.request_mock.stub_for(
            url='', json=self.mock_dataset_list)
        dataset_list = self.datasets.get_dataset_list()

        assert isinstance(dataset_list[0], Dataset)

    @responses.activate
    def test_get_file_preview(self):
        url = f"/{DATASET_ID_2}/files/{FILE_ID}/preview"
        self.request_mock.stub_for(url=url, json=self.mock_file_preview)
        preview = self.datasets.get_file_rows_preview(DATASET_ID_2, FILE_ID)

        assert preview is not None

    @responses.activate
    def test_get_all_privacy_violations(self):
        url = "/privacy-violations"
        self.request_mock.stub_for(url=url, json=self.mock_privacy_violations)
        privacy_violations = self.datasets.get_all_privacy_violations()

        assert privacy_violations is not None
        assert isinstance(privacy_violations[0], PrivacyViolation)

    @responses.activate
    def test_get_privacy_violation_by_id(self):
        url = f"/privacy-violations/{VIOLTION_ID}"
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
        url = f"/privacy-violations/{VIOLTION_ID}/consider"
        self.request_mock.stub_for(url=url, method=responses.PUT, body='')
        result = self.datasets.consider_privacy_violation(VIOLTION_ID)

        assert result is True

    @responses.activate
    def test_disregard_privacy_violation(self):
        url = f"/privacy-violations/{VIOLTION_ID}/disregard"
        self.request_mock.stub_for(url, method=responses.PUT, body='')
        result = self.datasets.disregard_privacy_violtion(VIOLTION_ID)

        assert result is True

    @responses.activate
    def test_get_all_permissions(self):
        url = f"/access-permissions"
        self.request_mock.stub_for(url, json=self.mock_access_perms)
        perms = self.datasets.get_all_access_permissions()

        assert isinstance(perms[0], AccessPermission)

    @responses.activate
    def test_get_access_permission(self):
        url = f"/access-permissions/{PERM_ID}"
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
        url = f"/access-permissions/{PERM_ID}/approve"
        self.request_mock.stub_for(url, method=responses.PUT, body='')
        result = self.datasets.approve_access_permission(PERM_ID)

        assert result is True

    @responses.activate
    def test_decline_permission(self):
        url = f"/access-permissions/{PERM_ID}/decline"
        self.request_mock.stub_for(url, method=responses.PUT, body='')
        result = self.datasets.decline_access_permission(PERM_ID)

        assert result is True

    @responses.activate
    def test_get_latest_pending(self):
        url = "/latest/pending"
        self.request_mock.stub_for(url=url, json=self.mock_dataset)
        dataset = self.datasets.get_latest_pending()

        assert isinstance(dataset, Dataset)
        assert dataset.status == ProcessingStatus.PENDING

    @responses.activate
    def test_delete_dataset(self):
        url = f"/{DATASET_ID_2}"
        self.request_mock.stub_for(url=url, method=responses.DELETE, json={
            "data": "Dataset deleted"
        })
        result = self.datasets.delete(DATASET_ID_2)

        assert result is True

    @responses.activate
    def test_update_dataset(self):
        url = f"/{DATASET_ID_2}"
        params = {
            "maintainerPhone": "+37255213451",
            "maintainerEmail": "new_email@gmail.com"
        }
        self.request_mock.stub_for(url=url, method=responses.PUT)
        result = self.datasets.update(DATASET_ID_2, params)

        assert result is True

    @responses.activate
    def test_discard_dataset(self):
        url = f"/{DATASET_ID_2}/discard"
        self.request_mock.stub_for(url=url, method=responses.PUT)
        result = self.datasets.discard(DATASET_ID_2)

        assert result is True

    @responses.activate
    def test_publish_dataset(self):
        url = f"/{DATASET_ID_2}/publish"
        self.request_mock.stub_for(url=url, method=responses.PUT)
        result = self.datasets.publish(DATASET_ID_2)

        assert result is True

    @responses.activate
    def test_get_files(self):
        url = f"/{DATASET_ID_2}/files"
        self.request_mock.stub_for(url, json=self.mock_files_list)
        result = self.datasets.get_all_files(DATASET_ID_2)

        assert isinstance(result[0], File)

    @responses.activate
    def test_get_file_index(self):
        url = f"/{DATASET_ID_2}/files/{FILE_ID}/indices"
        self.request_mock.stub_for(url, json=self.mock_file_index)
        result = self.datasets.get_file_index(DATASET_ID_2, FILE_ID)

        assert isinstance(result, Index)
        assert isinstance(result.polynomial[0], Polynomial)
        assert isinstance(result.identifier[0], Identifier)

    @responses.activate
    def test_get_file_rows(self):
        url = f"/{DATASET_ID_2}/files/{FILE_ID}"
        self.request_mock.stub_for(url, json=self.mock_file_preview)
        result = self.datasets.get_file_rows_with_errors(DATASET_ID_2, FILE_ID)

        assert result is not None

    @responses.activate
    def test_delete_file(self):
        url = f"/{DATASET_ID_2}/files/{FILE_ID}"
        self.request_mock.stub_for(url=url, method=responses.DELETE, json={
            "data": "deleted"
        })
        result = self.datasets.delete_file(DATASET_ID_2, FILE_ID)

        assert result is True

    @responses.activate
    def test_get_user_dataset_rating(self):
        url = f"/{DATASET_SLUG}/ratings"
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
        url = f"/{DATASET_ID_2}/files/{FILE_ID}/indices"
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
            DATASET_ID_2,
            FILE_ID,
            json
        )

        assert result is not None
        assert result is True

    @responses.activate
    def test_create_dataset_metadata(self):
        metadata = DatasetMetadata(
            nameEt="name2",
            nameEn="name2",
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
            '', responses.POST, status=201, json=self.mock_dataset)
        result = self.datasets.create_dataset_metadata(metadata)

        assert result is not None
        assert isinstance(result, Dataset)

    @responses.activate
    def test_upload_file(self):
        file_path = self.mock_file_path
        url = f"/{DATASET_ID_2}/upload"
        json_res = {
            "data": [
                {
                    "name": "highestGrossers.csv",
                    "mimetype": "text/csv",
                    "size": 2707,
                    "datasetId": "a25f9e33-cc44-43a5-988d-15af80de5c0b",
                    "metadata": {},
                    "processingStatus": "pending",
                    "id": "5372cf83-8c59-4d4f-bf16-98581a09c733",
                    "storageFilename": "5372cf83-8c59-4d4f-bf16-98581a09c733-PopularCreativeTypes-(1).csv"
                }
            ]
        }
        self.request_mock.stub_for(
            url=url, method=responses.POST, status=201, json=json_res)
        result = self.datasets.upload_file(
            DATASET_ID_2, 'highestGrossers.csv', 'text/csv', file_path)

        assert isinstance(result, File)
        assert result.name == 'highestGrossers.csv'
        assert result.mimetype == 'text/csv'

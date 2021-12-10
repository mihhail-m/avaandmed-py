import pytest
import responses

from avaandmed.api_resources.datasets import Datasets
from avaandmed.api_resources.datasets.dataset import Dataset
from avaandmed.api_resources.users.me import UserDataset
from avaandmed.exceptions import AvaandmedApiExcepiton
from tests.data_mock import DataJsonMock
from .request_mock import RequestMock

DATASET_ID_2 = '4446e091-adfc-4e1a-9e13-733d2b95f6e4'


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

    @responses.activate
    def test_get_my_dataset_by_id(self):
        self.request_mock.stub_for(
            url=f"/{DATASET_ID_2}", json=self.mock_dataset)
        my_ds = self.datasets.get_by_id(DATASET_ID_2)

        assert isinstance(my_ds, Dataset)

    @responses.activate
    def test_negative_get_my_dataset_by_id(self):
        self.request_mock.stub_for(
            url=f"/sdfsdf", json=self.mock_error, status=404
        )

        with pytest.raises(AvaandmedApiExcepiton):
            my_ds = self.datasets.get_by_id('sdfsdf')

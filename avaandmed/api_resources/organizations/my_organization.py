from avaandmed.api_resources.datasets.dataset_repository import DatasetRepository
from avaandmed.http.http_client import HttpClient


class MyOrganization:
    """
    Controller class to handled Organizations endpoints. 
    """

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client
        self._ENDPOINT = '/organizations/my-organizations'
        self._dataset = None

    @property
    def dataset(self):
        if self._dataset is None:
            self._dataset = OrganizationDataset(
                self._ENDPOINT, self._http_client)
        return self._dataset


class OrganizationDataset:
    def __init__(self, base_end_point: str, http_client: HttpClient) -> None:
        self._ENDPOINT = f"{base_end_point}/datasets"
        self._dataset_repository = DatasetRepository(http_client)

    def get_by_id(self, id: str):
        url = f"{self._ENDPOINT}/{id}"
        return self._dataset_repository._get_dataset(url)

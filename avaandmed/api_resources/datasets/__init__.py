from typing import Optional
from .dataset import Dataset
from avaandmed.http.http_client import HttpClient, HttpMethod


class Datasets:
    """
    Collection class responsible for actions with Datasets.
    """
    _http_client: HttpClient
    _DATASET_ENDPOINT = '/datasets'

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def retrieve_by_id(self, id: Optional[str]) -> Dataset:
        url = f"{self._DATASET_ENDPOINT}/{id}"
        dataset_json = self._http_client.request(HttpMethod.GET, url=url)
        return Dataset.parse_obj(dataset_json)

    def retrieve_by_slug(self, slug: Optional[str]) -> Dataset:
        url = f"{self._DATASET_ENDPOINT}/slug/{slug}"
        dataset_json = self._http_client.request(HttpMethod.GET, url=url)
        return Dataset.parse_obj(dataset_json)

    def update(self):
        pass

    def delete(self):
        pass

    def create(self):
        pass

    def list(self):
        pass

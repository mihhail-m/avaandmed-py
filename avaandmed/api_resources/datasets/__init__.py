from typing import List

from avaandmed.exceptions import AvaandmedException
from avaandmed.http.http_client import HttpClient, HttpMethod
from .dataset import Dataset
from pydantic import parse_obj_as


class Datasets:
    """
    Collection class responsible for actions with Datasets.
    """
    _http_client: HttpClient
    _DATASET_ENDPOINT = '/datasets'

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def retrieve_by_id(self, id: str) -> Dataset:
        """
        Returns Dataset instance with specified id.
        """
        url = f"{self._DATASET_ENDPOINT}/{id}"
        dataset_json = self._http_client.request(HttpMethod.GET, url=url)
        return Dataset.parse_obj(dataset_json)

    def retrieve_by_slug(self, slug: str) -> Dataset:
        """
        Returns Dataset instance with specified slug.
        """
        url = f"{self._DATASET_ENDPOINT}/slug/{slug}"
        dataset_json = self._http_client.request(HttpMethod.GET, url=url)
        return Dataset.parse_obj(dataset_json)

    def get_dataset_list(self, limit: int = 20) -> List[Dataset]:
        """
        Retrieves list of datasets from /datasets endpoint.
        By default returns 20 instances, but limit can be adjusted.
        """
        if limit <= 0:
            raise AvaandmedException('Limit cannot 0 or less.')

        url = f"{self._DATASET_ENDPOINT}?limit={limit}"
        datasets_json = self._http_client.request(HttpMethod.GET, url=url)
        dataset_list = parse_obj_as(List[Dataset], datasets_json)
        return dataset_list

    def get_total(self) -> int:
        """
        Returns total amount of datasets present at the moment.
        """
        url = f"{self._DATASET_ENDPOINT}/total"
        total = self._http_client.request(HttpMethod.GET, url=url)
        return total

    def get_distinct_mimetypes(self) -> List[str]:
        """
        Returns distinct mimetypes used by API.
        """
        url = f"{self._DATASET_ENDPOINT}/mimetypes/distinct"
        mimetypes = self._http_client.request(HttpMethod.GET, url=url)
        return mimetypes

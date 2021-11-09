from typing import Optional, List

from avaandmed.exceptions import AvaandmedException
from .dataset import Dataset, DatasetList
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

    def get_dataset_list(self, limit: int = 20) -> List[Dataset]:
        """
        Retrieves list of datasets from /datasets endpoint.
        By default returns 20 instances, but limit can be adjusted.
        """
        if limit <= 0:
            raise AvaandmedException('Limit cannot 0 or less.')

        url = f"{self._DATASET_ENDPOINT}?limit={limit}"
        datasets_json = self._http_client.request(HttpMethod.GET, url=url)
        dataset_list: DatasetList = DatasetList.parse_obj(datasets_json)
        return dataset_list.__root__

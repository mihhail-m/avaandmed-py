from typing import List
from pydantic import parse_obj_as
from avaandmed.http.http_client import HttpClient, HttpMethod
from avaandmed.api_resources.datasets.dataset import Dataset
from avaandmed.api_resources.entities import FileColumn, Preview, SearchResult


class DatasetRepository:

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def _get_dataset(self, url: str) -> Dataset:
        dataset_json = self._http_client.request(HttpMethod.GET, url=url)
        return Dataset.parse_obj(dataset_json)

    def _get_dataset_list(self, url: str) -> List[Dataset]:
        datasets_json = self._http_client.request(HttpMethod.GET, url=url)
        dataset_list = parse_obj_as(List[Dataset], datasets_json)
        return dataset_list

    def _get_total(self, url: str) -> int:
        total = self._http_client.request(HttpMethod.GET, url=url)
        return total

    def _get_distinct_mimetypes(self, url: str) -> List[str]:
        mimetypes = self._http_client.request(HttpMethod.GET, url=url)
        return mimetypes

    def _get_file_rows_preview(self, url: str) -> Preview:
        preview = self._http_client.request(HttpMethod.GET, url=url)
        return preview

    def _paginate_file_by_id(self, url: str) -> Preview:
        file = self._http_client.request(HttpMethod.GET, url=url)
        return file

    def _get_file_columns(self, url: str) -> List[FileColumn]:
        columns = self._http_client.request(HttpMethod.GET, url=url)
        return parse_obj_as(List[FileColumn], columns)

    def _download_file(self, url: str, out_file: str) -> int:
        return self._http_client.download(url, out_file)

    def _file_privacy_violations(self, url: str, data: dict) -> str:
        body = {
            "datasetId": data['datasetId'],
            "description": data['description']
        }
        self._http_client.request(HttpMethod.POST, url, body)
        return 'Submitted'

    def _apply_for_access(self, url: str, data: dict):
        body = {
            "datasetId": data['datasetId'],
            "description": data['description']
        }
        self._http_client.request(HttpMethod.POST, url, body)
        return 'Submitted'

    def _rate_dataset(self, url: str, data: dict) -> str:
        body = {
            "datasetId": data['datasetId'],
            "qualityRating": data['qualityRating'],
            "metadataRating": data['metadataRating']
        }
        self._http_client.request(HttpMethod.POST, url, body)
        return 'Submitted'

    def _get_dataset_rating_by_slug(self, url: str) -> str:
        return self._http_client.request(HttpMethod.GET, url=url)

    def _search(self, url: str) -> List[SearchResult]:
        results = self._http_client.request(HttpMethod.GET, url)
        return parse_obj_as(List[SearchResult], results)

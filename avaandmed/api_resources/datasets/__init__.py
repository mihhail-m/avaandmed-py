from typing import Any, List, Dict
from avaandmed.api_resources.common import FileColumn, SearchResult

from avaandmed.exceptions import AvaandmedException
from avaandmed.http.http_client import HttpClient, HttpMethod
from .dataset import Dataset
from pydantic import parse_obj_as

Preview = List[Dict[str, Any]]


class Datasets:
    """
    Collection class responsible for actions with Datasets.
    """
    _http_client: HttpClient
    _ENDPOINT = '/datasets'

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def get_by_id(self, id: str) -> Dataset:
        """
        Returns Dataset instance with specified id.
        """
        url = f"{self._ENDPOINT}/{id}"
        dataset_json = self._http_client.request(HttpMethod.GET, url=url)
        return Dataset.parse_obj(dataset_json)

    def get_by_slug(self, slug: str) -> Dataset:
        """
        Returns Dataset instance with specified slug.
        """
        url = f"{self._ENDPOINT}/slug/{slug}"
        dataset_json = self._http_client.request(HttpMethod.GET, url=url)
        return Dataset.parse_obj(dataset_json)

    def get_dataset_list(self, limit: int = 20) -> List[Dataset]:
        """
        Retrieves list of datasets from /datasets endpoint.
        By default returns 20 instances, but limit can be adjusted.
        """
        if limit <= 0:
            raise AvaandmedException('Limit cannot 0 or less.')

        url = f"{self._ENDPOINT}?limit={limit}"
        datasets_json = self._http_client.request(HttpMethod.GET, url=url)
        dataset_list = parse_obj_as(List[Dataset], datasets_json)
        return dataset_list

    def get_total(self) -> int:
        """
        Returns total amount of datasets present at the moment.
        """
        url = f"{self._ENDPOINT}/total"
        total = self._http_client.request(HttpMethod.GET, url=url)
        return total

    def get_distinct_mimetypes(self) -> List[str]:
        """
        Returns distinct mimetypes used by API.
        """
        url = f"{self._ENDPOINT}/mimetypes/distinct"
        mimetypes = self._http_client.request(HttpMethod.GET, url=url)
        return mimetypes

    def get_file_rows_preview(self, id: str, fileId: str) -> Preview:
        """
        Preview the file rows in the way, how end user will see them.
        Returns object according to the provided data in the dataset's file.
        """
        url = f"{self._ENDPOINT}/{id}/files/{fileId}/preview"
        preview = self._http_client.request(HttpMethod.GET, url=url)
        return preview

    def paginate_file_by_id(self, id: str, fileId: str) -> Preview:
        """
        Paginate through successfully processed file content.
        """
        url = f"{self._ENDPOINT}/{id}/files/{fileId}"
        file = self._http_client.request(HttpMethod.GET, url=url)
        return file

    def get_file_columns(self, id: str, fileId: str) -> List[FileColumn]:
        """
        Returns columns from the dataset file.
        """
        url = f"{self._ENDPOINT}/{id}/files/{fileId}/columns"
        columns = self._http_client.request(HttpMethod.GET, url=url)
        return parse_obj_as(List[FileColumn], columns)

    def download_file(self, id: str, fileId: str, out_file: str) -> int:
        """
        Downloads processed file of a dataset.
        By default file will be downloaded into current user's working directory.
        """
        if len(out_file) == 0:
            raise AvaandmedException('File name cannot be empty')

        url = f"{self._ENDPOINT}/{id}/files/{fileId}/download"
        return self._http_client.download(url, out_file)

    def file_privacy_violations(self, id: str, description: str) -> str:
        """
        Submits privacy violations form for the dataset.
        Returns 'Submitted' status if succesful.
        """
        if len(description) < 20 or len(description) > 1000:
            raise AvaandmedException(
                'Description must be at least 20 characters long, but no longer than 1000.'
            )
        url = f"{self._ENDPOINT}/privacy-violations"
        data = {
            "datasetId": id,
            "description": description
        }
        self._http_client.request(HttpMethod.POST, url, data)
        return 'Submitted'

    def apply_for_access(self, id: str, description: str):
        """
        Submits request to get additional permissions for dataset.
        Returns 'Submitted' status if succesful.
        """
        if len(description) < 20 or len(description) > 1000:
            raise AvaandmedException(
                'Description must be at least 20 characters long, but no longer than 1000.'
            )
        url = f"{self._ENDPOINT}/access-permissions"
        data = {
            "datasetId": id,
            "description": description
        }
        self._http_client.request(HttpMethod.POST, url, data)
        return 'Submitted'

    def rate_dataset(self, id: str, quality_rating: int, meta_data_rating: int) -> str:
        """
        Submits rating for the dataset.
        Returns 'Submitted' status if succesful.
        """
        if ((quality_rating < 0 or quality_rating > 10) or
                (meta_data_rating < 0 or meta_data_rating > 10)):
            raise AvaandmedException('Rating must be from 0 to 10.')

        url = f"{self._ENDPOINT}/rating"
        data = {
            "datasetId": id,
            "qualityRating": quality_rating,
            "metadataRating": meta_data_rating
        }
        self._http_client.request(HttpMethod.POST, url, data)
        return 'Submitted'

    def get_dataset_rating_by_slug(self, slug: str) -> str:
        """
        Retrieves rating of the dataset by given slug.
        """
        url = f"{self._ENDPOINT}/rating/{slug}"
        return self._http_client.request(HttpMethod.GET, url=url)

    def search(self, keywordId: int, regionId: int, year: int) -> List[SearchResult]:
        """
        Search datasets based on keyword ID, region ID and year.
        Quite limited search capabilities.
        """
        url = f"{self._ENDPOINT}/search?keywordIds={keywordId}&regionIds={regionId}&year={year}"
        results = self._http_client.request(HttpMethod.GET, url)
        return parse_obj_as(List[SearchResult], results)

from typing import Any
from avaandmed.http.http_client import HttpClient, HttpMethod
from .api_resource import ApiResource
from typing import List, Optional


class Dataset(ApiResource):
    """
    Class for representing Dataset model.
    """
    id: Optional[str]
    status: Optional[str]
    slug: Optional[str]
    name: Optional[str]
    url: Optional[str]
    organization: Optional[Any]  # TODO
    organization_id: Optional[str]
    user: Optional[Any]  # TODO
    user_id: Optional[str]
    files: Optional[List[Any]]  # TODO
    keywords: Optional[List[Any]]  # TODO
    categories: Optional[List[Any]]  # TODO
    regions: Optional[List[Any]]  # TODO
    coord_ref_system: Optional[List[Any]]  # TODO
    is_actual: Optional[bool]
    created_at: Optional[str]
    updated_at: Optional[str]
    deleted_at: Optional[str]
    name_et: Optional[str]
    name_en: Optional[str]
    description_et: Optional[str]
    description_en: Optional[str]
    maintainer: Optional[str]
    maintainer_email: Optional[str]
    maintainer_phone: Optional[str]
    citations: Optional[List[Any]]  # TODO
    conformities: Optional[List[Any]]  # TODO
    south_lat: Optional[str]
    north_lat: Optional[str]
    west_lon: Optional[str]
    east_long: Optional[str]
    language: Optional[str]
    license: Optional[Any]  # TODO
    license_id: Optional[int]
    data_from: Optional[str]
    data_to: Optional[str]
    update_interval_unit: Optional[str]  # TODO
    update_interval_frequency: Optional[int]
    access: Optional[str]  # TODO
    available_to: Optional[str]
    landing_page: Optional[str]
    qualified_attribution: Optional[str]
    was_generated_by: Optional[str]
    spatial_resolution: Optional[str]
    geoportal_identifier: Optional[str]
    geoportal_keywords: Optional[str]
    lineage: Optional[str]
    pixel_size: Optional[str]
    resource_type: Optional[str]  # TODO
    topic_categories: Optional[List[str]]  # TODO


class Datasets:
    """
    Collection class responsible for actions with Datasets.
    """
    _http_client: HttpClient

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def retrieve_by_id(self, id: Optional[str]) -> Dataset:
        url = f"/datasets/{id}"
        dataset_json = self._http_client.request(HttpMethod.GET, url=url)
        return Dataset.parse_obj(dataset_json)

    def retrieve_by_slug(self, slug: Optional[str]) -> Dataset:
        url = f"/datasets/slug/{slug}"
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

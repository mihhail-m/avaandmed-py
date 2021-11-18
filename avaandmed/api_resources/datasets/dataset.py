from typing import List, Optional, Any
from avaandmed.api_resources import ApiResource
from avaandmed.api_resources.users.user import User


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
    user: Optional[User]
    user_id: Optional[str]
    files: Optional[List[Any]]  # TODO
    keywords: Optional[List[Any]]  # TODO
    categories: Optional[List[Any]]  # TODO
    regions: Optional[List[Any]]  # TODO
    coordinate_reference_systems: Optional[List[Any]]  # TODO
    is_actual: Optional[bool]
    created_at: Optional[str]
    updated_at: Optional[str]
    name_et: Optional[str]
    name_en: Optional[str]
    description_et: Optional[str]
    description_en: Optional[str]
    maintainer: Optional[str]
    maintainer_email: Optional[str]
    maintainer_phone: Optional[str]
    citations: Optional[List[Any]]  # TODO
    conformities: Optional[List[Any]]  # TODO
    south_latitude: Optional[str]
    north_latitude: Optional[str]
    west_longitude: Optional[str]
    east_longitude: Optional[str]
    language: Optional[str]
    licence: Optional[Any]  # TODO Fix type
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
    spatial_representation_type: Optional[str]
    spatial_data_service_type: Optional[str]
    geoportal_identifier: Optional[str]
    geoportal_keywords: Optional[str]
    lineage: Optional[str]
    pixel_size: Optional[str]
    resource_type: Optional[str]  # TODO
    topic_categories: Optional[List[str]]  # TODO
    maturity: Optional[str]
    temporal_resolution: Optional[str]
    version_notes: Optional[str]
    parent_datasets: Optional[List['Dataset']]
    child_datasets: Optional[List['Dataset']]
    map_regions: Optional[List[str]]
    is_content_allowed: Optional[bool]


Dataset.update_forward_refs()

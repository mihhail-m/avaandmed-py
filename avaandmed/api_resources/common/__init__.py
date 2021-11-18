from typing import Any, Dict, List, Optional
from enum import Enum
from avaandmed.api_resources import ApiResource

# "id": 3068,
# "name": "rahvastik",
# "language": "et",
# "keywordId": 3068,
# "keywordEmsCategory": {
#     "id": 4614,
#     "emsCategoryId": 14,
#     "keywordId": 3068
# }


class KeywordEmsCategory(ApiResource):
    id: int
    ems_category_id: int
    keyword_id: int


class Keyword(ApiResource):
    """
    Handles keywords serialization in Dataset model.
    """
    id: int
    name: str
    language: str
    keyword_ems_category: KeywordEmsCategory


class Citation(ApiResource):
    """
    Handles citations serialization in Dataset model.
    """
    url: str
    name: str


class Conformity(ApiResource):
    """
    Handles conformities serialization in Dataset model.
    """
    release_date: str
    specification: str


class Licence(ApiResource):
    """
    Handles licences serialization.
    """
    id: str
    name: str
    description: str
    code: Optional[str]
    identifier: Optional[str]


class CoordinateReferenceSystem(ApiResource):
    """
    Handles coordinateReferenceSystems serialization in Dataset model.
    """
    id: int
    uri: str


class Category(ApiResource):
    """
    Handles categories serialization.
    """
    id: int
    name: str
    description: Optional[str]
    ems_ids: Optional[List[int]]


class Region(ApiResource):
    """
    Handles regions serialization.
    """
    id: int
    name: str
    coordinates: Optional[str]


class ProcessingStatus(Enum):
    NONE = 'none'
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'


class File(ApiResource):
    """
    Handles files field serialization in Dataset model.
    """
    id: str
    name: str
    mimetype: str
    size: str
    dataset_id: str
    metadata: Dict[str, Any]
    processing_status: ProcessingStatus
    storage_filename: str

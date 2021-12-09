from typing import Optional, List
from avaandmed.api_resources.entities import Notification
from avaandmed.api_resources import ApiResource


class Organization(ApiResource):
    """
    Represents Organization enitity.
    """
    id: Optional[str]
    reg_code: Optional[str]
    name: Optional[str]
    slug: Optional[str]
    contact: Optional[str]
    contact_email: Optional[str]
    description: Optional[str]
    is_public_body: Optional[bool]
    notifications: Optional[List[Notification]]

from .api_resource import ApiResource
from typing import Optional


class Datasets(ApiResource):
    """
    Class for representing Datasets entity.
    """
    id: Optional[str] = None
    name: Optional[str] = None
    slug: Optional[str] = None

    @classmethod
    def retrieve(self):
        pass

    @classmethod
    def update(self):
        pass

    @classmethod
    def delete(self):
        pass

    @classmethod
    def create(self):
        pass

    @classmethod
    def list(self):
        pass

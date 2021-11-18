from avaandmed.http.http_client import HttpClient
from .user import User


class Users:
    """
    Collection class responsible for itercations with user's datasets.
    """
    _http_client: HttpClient
    _USER_DATASET_ENDPOINT = '/users/me/datasets'

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

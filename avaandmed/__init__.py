from avaandmed.http.http_client import HttpClient


class Avaandmed:
    """A client for accessing Avaadnmed API"""

    def __init__(self, api_token: str, key_id: str, base_hostname: str = 'avaandmed.eesti.ee') -> None:
        self._api_token = api_token
        self._key_id = key_id
        self._http_client = HttpClient(base_hostname, api_token, key_id)
        self._datasets = None
        self._organizations = None
        self._users = None

    @property
    def api_token(self) -> str:
        return self._api_token

    @property
    def key_id(self) -> str:
        return self._key_id

    @property
    def datasets(self):
        if self._datasets is None:
            from avaandmed.api_resources.datasets import Datasets
            self._datasets = Datasets(http_client=self._http_client)
        return self._datasets

    @property
    def organizations(self):
        if self._organizations is None:
            from avaandmed.api_resources.organizations import Organizations
            self._organizations = Organizations(http_client=self._http_client)
        return self._organizations

    @property
    def users(self):
        if self._users is None:
            from avaandmed.api_resources.users import Users
            self._users = Users(http_client=self._http_client)
        return self._users

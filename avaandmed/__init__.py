from avaandmed.http.http_client import HttpClient


class Avaandmed:
    """A client for accessing Avaadnmed API"""

    def __init__(self, api_token: str, key_id: str) -> None:
        self._api_token = api_token
        self._key_id = key_id
        self._datasets = None
        self._organizations = None
        self._http_client = HttpClient(api_token, key_id)

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
            self._organizations = Organizations()
        return self._organizations

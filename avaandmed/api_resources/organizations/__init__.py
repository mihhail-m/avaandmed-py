from avaandmed.http.http_client import HttpClient


class Organizations:
    """
    Controller class to handled Organizations endpoints. 
    """
    _http_client: HttpClient
    _ENDPOINT = '/organizations/my-organizations'

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

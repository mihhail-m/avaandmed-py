from avaandmed.http.http_client import HttpClient


class Organizations:
    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client
        self._my_organization = None

    @property
    def my_orgranization(self):
        if self._my_organization is None:
            from avaandmed.api_resources.organizations.my_organization import MyOrganization
            self._my_organization = MyOrganization(self._http_client)
        return self._my_organization

import responses
import logging

from tests.data_mock import DataJsonMock

BASE_URL = 'https://avaandmedtest.eesti.ee/api'
MOCK_TOKEN_URL = 'https://avaandmedtest.eesti.ee/api/auth/key-login'


class RequestMock:

    def __init__(self, endpoint: str = '') -> None:
        self.endpoint = endpoint
        self.data_mock = DataJsonMock()
        self.token_file = self.data_mock.MOCK_TOKEN_FILE

    def mock_post_auth(self):
        responses.add(
            responses.POST,
            MOCK_TOKEN_URL,
            json=self.token_file,
            status=201
        )

    def mock_negative_post_auth(self, status: int, msg: str):
        responses.add(
            responses.POST,
            MOCK_TOKEN_URL,
            json={
                "statusCode": status,
                "message": msg,
            },
            status=status
        )

    def stub_for(self, url: str, method: str = responses.GET,
                 status: int = 200, json=None, body=None, auth: bool = True):
        """
        Stub request for given method and url. 
        Defaults to GET request with authetication, status 200 and empty body.
        Given url is appended to {BASE_URL}{endpoint}{url} value.
        So, you just need to provide endpoint as url param.
        """
        if auth:
            self.mock_post_auth()

        if len(self.endpoint) == 0:
            logging.warning('endpoint value is an empty string.')

        url = f"{BASE_URL}{self.endpoint}{url}"

        responses.add(
            method=method,
            url=url,
            json=json,
            body=body,
            status=status
        )

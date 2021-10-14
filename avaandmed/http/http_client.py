import requests
from base64 import b64encode
from enum import Enum

from avaandmed.exceptions import AvaandmedApiExcepiton


class HttpMethod(Enum):
    GET = 'get'
    POST = 'post'
    DELETE = 'delete'
    UPDATE = 'update'


class AllowedLang(Enum):
    EN = 'en'
    ET = 'en'


class HttpClient:
    """
    Class that is responsible for basic HTTP logic for the client.
    """
    __headers = {
        'content-Type': 'application/json'
    }
    __SCHEME = 'https'
    __HOSTNAME = 'avaandmed.eesti.ee'
    __BASE_ENDPOINT = 'api'
    __BASE_URL = f"{__SCHEME}://{__HOSTNAME}/{__BASE_ENDPOINT}"

    def __init__(self, api_key: str = None, key_id: str = None) -> None:
        self.__api_key = api_key
        self.__key_id = key_id

    def __get_token(self) -> str:
        """
        Makes a requst to /auth/key-login endpoint and retrieves an access token
        to authorize future requests.
        """
        def encode_key():
            key = f"{self.__key_id}:{self.__api_key}".encode('ascii')
            return b64encode(key).decode('ascii')

        x_api_key = encode_key()
        self.__headers['X-API-KEY'] = x_api_key
        auth_url = f"{self.__BASE_URL}/auth/key-login"
        r = requests.post(auth_url, headers=self.__headers)

        if r.status_code != 201:
            msg = r.json()['message']
            raise AvaandmedApiExcepiton(
                status=r.status_code, uri=r.url, msg=msg)

        return r.json()['data']['accessToken']

    def request(self, method: HttpMethod, url: str, data={}, lang: AllowedLang = AllowedLang.EN):
        """
        Generic request method to make request to the API.
        """
        url = f"{self.__BASE_URL}{url}?lang={lang.value}"
        access_token = self.__get_token()
        self.__headers['Authorization'] = f"Bearer {access_token}"
        res = requests.request(method=method.name,
                               url=url,
                               json=data,
                               headers=self.__headers)

        return res.json()['data']

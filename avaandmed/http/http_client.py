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

        try:
            res = requests.post(auth_url, headers=self.__headers)
            res.raise_for_status()

        except requests.exceptions.HTTPError:
            raise AvaandmedApiExcepiton(
                status=res.status_code,
                uri=res.url,
                msg=res.json()['message']
            )

        except requests.exceptions.RequestException as ex:
            raise SystemExit(ex)

        return res.json()['data']['accessToken']

    def request(self, method: HttpMethod, url: str, data={}):
        """
        Generic request method to make request to the API.
        """
        url = f"{self.__BASE_URL}{url}"
        access_token = self.__get_token()
        self.__headers['Authorization'] = f"Bearer {access_token}"

        try:
            res = requests.request(
                method=method.name,
                url=url,
                json=data,
                headers=self.__headers
            )
            res.raise_for_status()

        except requests.exceptions.HTTPError as err:
            raise AvaandmedApiExcepiton(
                status=res.status_code,
                uri=url,
                msg=res.json()['message'],
            )

        except requests.exceptions.RequestException as ex:
            raise SystemExit(ex)

        return res.json()['data']

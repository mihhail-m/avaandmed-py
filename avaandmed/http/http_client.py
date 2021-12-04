from requests import Session, exceptions
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

    def __init__(self, hostname: str, api_key: str = None, key_id: str = None) -> None:
        self.__HEADERS = {
            'Content-Type': 'application/json'
        }
        self.__SCHEME = 'https'
        self.__BASE_ENDPOINT = 'api'
        self.__session = Session()
        self.__api_key = api_key
        self.__key_id = key_id
        self.__HOSTNAME = hostname
        self.__BASE_URL = f"{self.__SCHEME}://{self.__HOSTNAME}/{self.__BASE_ENDPOINT}"
        self.__session.headers.update(self.__HEADERS)

    def __get_token(self) -> str:
        """
        Makes a requst to /auth/key-login endpoint and retrieves an access token
        to authorize future requests.
        """
        session = self.__session

        def encode_key():
            key = f"{self.__key_id}:{self.__api_key}".encode('ascii')
            return b64encode(key).decode('ascii')

        x_api_key = encode_key()
        session.headers.update({'X-API-KEY': x_api_key})
        auth_url = f"{self.__BASE_URL}/auth/key-login"

        try:
            res = session.post(url=auth_url)
            res.raise_for_status()

        except exceptions.HTTPError:
            raise AvaandmedApiExcepiton(
                status=res.status_code,
                uri=res.url,
                msg=res.json()['message']
            )

        except exceptions.RequestException as ex:
            raise SystemExit(ex)

        return res.json()['data']['accessToken']

    def request(self, method: HttpMethod, url: str, data={}):
        """
        Generic request method to make request to the API.
        """
        session = self.__session
        url = f"{self.__BASE_URL}{url}"

        with session as s:
            try:
                access_token = self.__get_token()
                s.headers.update({'Authorization': f"Bearer {access_token}"})
                res = s.request(
                    method=method.name,
                    url=url,
                    json=data
                )
                res.raise_for_status()

            except exceptions.HTTPError:
                raise AvaandmedApiExcepiton(
                    status=res.status_code,
                    uri=url,
                    msg=res.json()['message'],
                )

            except exceptions.RequestException as ex:
                raise SystemExit(ex)

            return res.json()['data']

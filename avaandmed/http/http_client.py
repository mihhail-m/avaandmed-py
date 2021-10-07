import requests
from typing import Dict
from enum import Enum

from avaandmed.entities.api_resource import ApiResource


class HttpMethod(Enum):
    GET = 'get'
    POST = 'post'
    DELETE = 'delete'
    UPDATE = 'update'


class HttpClient:
    __headers: Dict = {
        'content-Type': 'application/json'
    }

    def __init__(self) -> None:
        pass

    def get_token(self) -> str:
        pass

    def request(self, method: HttpMethod, url: str, data: ApiResource):
        params = '' if data is None else data.json()
        res = requests.request(method=method.name,
                               url=url,
                               json=params,
                               headers=self.__headers)
        return res.json()

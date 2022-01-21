import pytest
import responses
from .request_mock import RequestMock
from avaandmed import Avaandmed
from avaandmed.api_resources.entities import (
    Category,
    CoordinateReferenceSystem,
    EmsCategory,
    KeywordInfo,
    Language,
    Licence,
    Region)


def test_client_init(api_token, key_id, avaandmed_client):
    assert api_token != 'none'
    assert key_id != 'none'
    assert isinstance(avaandmed_client, Avaandmed)


class TestAvaandmedClient:

    @pytest.fixture(autouse=True)
    def _request_mock(self, request_mock: RequestMock):
        self.request_mock = request_mock

    @pytest.fixture(autouse=True)
    def _client(self, avaandmed_client: Avaandmed):
        self.client = avaandmed_client

    @responses.activate
    def test_get_categories(self):
        response = {
            "data": [
                {
                    "id": 13,
                    "name": "Elanikkond ja ühiskond",
                    "description": "CATEGORY_POPULATION_INFO",
                    "emsIds": [
                        8,
                        14,
                        11
                    ]
                },
                {
                    "id": 14,
                    "name": "Energeetika",
                    "description": "CATEGORY_ENERGY_INFO",
                    "emsIds": [
                        30
                    ]
                }]
        }
        self.request_mock.stub_for(url='/categories', json=response)
        categories = self.client.get_categories()

        assert categories is not None
        assert isinstance(categories[0], Category)

    @responses.activate
    def test_get_euro_categories(self):
        response = {
            "data": [
                {
                    "id": 13,
                    "name": "Elanikkond ja ühiskond",
                    "description": "CATEGORY_POPULATION_INFO",
                    "emsIds": [
                        8,
                        14,
                        11
                    ]
                },
                {
                    "id": 14,
                    "name": "Energeetika",
                    "description": "CATEGORY_ENERGY_INFO",
                    "emsIds": [
                        30
                    ]
                }]
        }
        self.request_mock.stub_for(url='/euro-categories', json=response)
        categories = self.client.get_euro_categories()

        assert categories is not None
        assert isinstance(categories[0], Category)

    @responses.activate
    def test_get_ems_categories(self):
        response = {
            "data": [
                {
                    "id": 1,
                    "name": "ÜLDMÕISTED"
                },
                {
                    "id": 2,
                    "name": "FILOSOOFIA. EETIKA. SEMIOOTIKA"
                },
                {
                    "id": 3,
                    "name": "RELIGIOON. EOLOOGIA. ESOTEERIKA"
                }]
        }
        self.request_mock.stub_for(url='/ems-categories', json=response)
        categories = self.client.get_ems_categories()

        assert categories is not None
        assert isinstance(categories[0], EmsCategory)

    @responses.activate
    def test_get_regions(self):
        response = {
            "data": [
                {
                    "id": 17,
                    "name": "Muu"
                },
                {
                    "id": 1,
                    "name": "Harju maakond"
                },
                {
                    "id": 2,
                    "name": "Tartu maakond"
                }]
        }
        self.request_mock.stub_for(url='/regions', json=response)
        categories = self.client.get_regions()

        assert categories is not None
        assert isinstance(categories[0], Region)

    @responses.activate
    def test_get_coordinate_ref_system(self):
        response = {
            "data": [
                {
                    "id": 1,
                    "uri": "http://www.opengis.net/def/crs/EPSG/0/2000"
                },
                {
                    "id": 2,
                    "uri": "http://www.opengis.net/def/crs/EPSG/0/20004"
                }]
        }
        self.request_mock.stub_for(
            url='/coordinateReferenceSystems', json=response)
        coords = self.client.get_coordinate_ref_system()

        assert coords is not None
        assert isinstance(coords[0], CoordinateReferenceSystem)

    @responses.activate
    def test_get_languages(self):
        response = {
            "data": [
                {
                    "code": "aa",
                    "name": "afari keel"
                },
                {
                    "code": "ab",
                    "name": "abhaasi keel"
                }]
        }
        self.request_mock.stub_for(url='/languages', json=response)
        categories = self.client.get_languages()

        assert categories is not None
        assert isinstance(categories[0], Language)

    @responses.activate
    def test_get_keyword(self):
        response = {
            "data": [
                {
                    "id": 12777,
                    "name": "au",
                    "emsId": "EMS021459"
                },
                {
                    "id": 36558,
                    "name": "Oš",
                    "emsId": "EMS133635"
                }]
        }
        self.request_mock.stub_for(url='/keywords', json=response)
        keywords = self.client.get_keywords()

        assert keywords is not None
        assert len(keywords) == 2
        assert isinstance(keywords[0], KeywordInfo)

    @responses.activate
    def test_get_licenses(self):
        response = {
            "data": [
                {
                    "id": 1,
                    "name": "Creative Commons CC0 1.0 Üldine",
                    "description": "õigus vabalt edasi arendada, muuta, muudesse töödesse inkorporeerida, taaskasutada ja jagada mistahes eesmärgil",
                    "code": "CC0 1.0",
                    "identifier": "CC0-1.0"
                },
                {
                    "id": 19,
                    "name": "Creative Commons Autorile viitamine–Mitteäriline eesmärk 3.0 Jurisdiktsiooniga sidumata",
                    "description": "viidates Autorile, õigus toota ja reprodutseerida kohandatud materjali üksnes mitteärilisel eesmärgil",
                    "code": "CC BY-NC 3.0",
                    "identifier": "CC-BY-NC-3.0"
                }]
        }
        self.request_mock.stub_for(url='/licences', json=response)
        licenses = self.client.get_licenses()

        assert licenses is not None
        assert isinstance(licenses[0], Licence)

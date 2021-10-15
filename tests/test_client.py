from avaandmed import Avaandmed


def test_client_init(api_token, key_id, avaandmed_client):
    assert api_token != 'none'
    assert key_id != 'none'
    assert isinstance(avaandmed_client, Avaandmed)

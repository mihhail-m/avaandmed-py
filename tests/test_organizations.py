from avaandmed import Avaandmed
from avaandmed.api_resources.organizations import Organizations


def test_organizations_entity(avaandmed_client: Avaandmed):
    organizations = avaandmed_client.organizations
    assert isinstance(organizations, Organizations)

from pydantic import BaseModel


class ApiResource(BaseModel):
    """
    An abstract class for all the entities used in the module.
    Here is defined common properties that are used among all entities.
    """

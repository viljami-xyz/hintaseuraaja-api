""" Models for hintaopas.fi
    """

from typing import Union, List

from pydantic import BaseModel


class ListItem(BaseModel):
    """Model for a single item in a list of Favorites"""

    name: str
    subtitle: str
    price: Union[float, None]


class IdIn(BaseModel):
    """Input requirement for id"""

    id_number: int


class FavoritesOut(BaseModel):
    """Output requirement for favorites"""

    status: str
    data: List[ListItem]

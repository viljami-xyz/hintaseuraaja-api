""" Models for hintaopas.fi
    """

from typing import Union

from pydantic import BaseModel


class ListItem(BaseModel):
    """Model for a single item in a list of Favorites"""

    name: str
    subtitle: str
    price: Union[float, None]

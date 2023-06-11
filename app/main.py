""" Run API """

from fastapi import FastAPI
from hintascraper.services.hintaopas import favorites
from hintascraper.models.hintaopas import FavoritesOut

app = FastAPI()


@app.get("/")
def read_root():
    """Hello World"""
    return {"Hello": "World123"}


@app.get("/favorites/{list_id}", response_model=FavoritesOut)
def read_list(list_id: int):
    """Get favorites list items"""
    favorites_list = favorites(list_id)
    return favorites_list

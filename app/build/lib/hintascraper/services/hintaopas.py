""" Module for getting the data from favorites list with bs4"""

import re

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

from hintascraper.models.hintaopas import ListItem


def list_items(row: str) -> ListItem:
    """Extracts data from a row of html"""
    name_div = row.find("div", class_=re.compile(r"Name-sc*"))
    subtitle_div = row.find("div", class_=re.compile(r"Subtitle-sc*"))
    price_div = row.find("span", class_=re.compile(r"PriceLabel-sc*"))
    try:
        name = name_div.text.strip()
        subtitle = subtitle_div.text.strip()
        if price_div:
            price = float(price_div.text.replace("€", "").strip().replace(",", "."))
        else:
            price = None
        return ListItem(
            name=name,
            subtitle=subtitle,
            price=price,
        ).dict()
    except ValueError as error:
        print(error, "No correct values found")


def favorites(list_id: int) -> dict:
    """Scrapes Hintaopas given favorites list id and return json"""

    result = {"status": "ok", "data": []}
    url = f"https://hintaopas.fi/list/--l{list_id}"
    errors = 0

    try:
        response = requests.get(url)
    except RequestException:
        result["status"] = "error: network request failed"
        return result

    soup = BeautifulSoup(response.text, "html.parser")

    div_element = soup.find("div", class_=re.compile(r"List-sc*"))
    if not div_element:
        result["status"] = "error: no favorites list found"
        return result

    # for prd_list in div_element:
    rows = soup.find_all("div", class_=re.compile(r"ListItem-sc*"))
    for row in rows:
        items = list_items(row)
        if items:
            result["data"].append(items)
        else:
            errors += 1
            result["status"] = f"ok, with {errors} rows not processed"

    if not result["data"]:
        result["status"] = "error: no data found"

    return result

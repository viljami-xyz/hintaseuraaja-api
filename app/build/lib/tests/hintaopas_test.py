""" Unit tests for hintaopas.py"""
import pytest
import requests
from bs4 import BeautifulSoup

from hintascraper.services.hintaopas import favorites, list_items
from hintascraper.models.hintaopas import ListItem


def test_list_items():
    """Test list_items function"""
    row = """<div class="ListItem-sc-1gj7xq6-0 jZqKUQ">
    <div class="Name-sc-1gj7xq6-1 gqRQb">Samsung Galaxy S20 5G 128GB</div>
    <div class="Subtitle-sc-1gj7xq6-2 fWqQb">Älypuhelin, 128 Gt, 6.2", 12 Mpx, Android 10, 5G, musta</div>
    <span class="PriceLabel-sc-1gj7xq6-3 gQqQb">599,00 €</div>
    </div>"""
    result = list_items(BeautifulSoup(row, "html.parser"))
    assert (
        result
        == ListItem(
            name="Samsung Galaxy S20 5G 128GB",
            subtitle='Älypuhelin, 128 Gt, 6.2", 12 Mpx, Android 10, 5G, musta',
            price=599.00,
        ).dict()
    )


def test_favorites(mock_requests_get):
    """
    Test favorites function
    """
    result = favorites(99041)
    assert result["status"] == "ok"
    assert len(result["data"]) == 2
    assert result["data"][0]["name"] == "Samsung Galaxy S20 5G 128GB"
    assert (
        result["data"][0]["subtitle"]
        == 'Älypuhelin, 128 Gt, 6.2", 12 Mpx, Android 10, 5G, musta'
    )
    assert result["data"][0]["price"] == 599.00
    assert result["data"][1]["price"] is None


@pytest.fixture
def mock_requests_get(mocker):
    """Mock requests.get to return a simple test HTML file"""

    def mocked_get(url):
        # Simulate the response based on your test case
        if url == f"https://hintaopas.fi/list/--l{99041}":
            mock_response = """
                <html>
                    <div class="List-sc-1gj7xq6-1 hZqQb">
                        <div class="ListItem-sc-1gj7xq6-0 jZqKUQ">
                            <div class="Name-sc-1gj7xq6-1 gqRQb">Samsung Galaxy S20 5G 128GB</div>
                            <div class="Subtitle-sc-1gj7xq6-2 fWqQb">Älypuhelin, 128 Gt, 6.2", 12 Mpx, Android 10, 5G, musta</div>
                            <span class="PriceLabel-sc-1gj7xq6-3 gQqQb">599,00 €</div>
                        </div>
                        <div class="ListItem-sc-1gj7xq6-0 jZqKUQ">
                            <div class="Name-sc-1gj7xq6-1 gqRQb">Samsung Galaxy S21 5G 128GB</div>
                            <div class="Subtitle-sc-1gj7xq6-2 fWqQb">Älypuhelin, 256 Gt, 6.2", 12 Mpx, Android 10, 5G, musta</div>
                        </div>
                    </div>
                </html>
            """
            return mocker.Mock(status_code=200, text=mock_response)
        else:
            return mocker.Mock(status_code=404)

    mocker.patch.object(requests, "get", side_effect=mocked_get)

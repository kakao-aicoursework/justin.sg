import requests
from bs4 import BeautifulSoup


class Search():
    def query(self, url: str):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
        }

        res = requests.get(url, headers=headers)

        soup = BeautifulSoup(res.content, "html.parser")
        return soup.select_one(".area_document").get_text()

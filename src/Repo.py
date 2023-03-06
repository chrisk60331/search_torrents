"""Define a web based repository and its methods."""
from typing import List

from requests_html import HTMLSession

from src.Torrent import Torrent
from src.constants import QUERY_STRING_DELIMITER, QUERY_STRING_SEPERATOR

ALL = "all"


class Repo:
    def __init__(self, session: HTMLSession):
        self.item = None
        self.session = session
        self.category_number = None
        self.search_term = None


class PirateBayRepo(Repo):
    CATEGORIES = {
        "porn": "501,502,505",
        "movies": "201,202,207",
        "shows": "205,208",
    }
    CATEGORIES[ALL] = ",".join(set(",".join(CATEGORIES.values()).split(",")))
    BASE_URI = "https://thepiratebay.org/search.php"
    CSS_PATH = " ".join(
        [
            "html",
            "body#browse",
            "main",
            "div.browse",
            "section.col-center",
            "ol#torrents.view-single",
            "li#st.list-entry",
        ]
    )

    def __init__(self, session: HTMLSession):
        super().__init__(session)
        self.item = None
        self.session = session
        self.category_number = None
        self.search_term = None
        self.uri = None

    def get_tor_attr(self, expr):
        return [goo.text for goo in self.item.cssselect(expr)][0]

    def get_magnet_link(self):
        items = [
            goo.find("a").attrib.get("href")
            for goo in self.item.cssselect("*")
            if goo.attrib.get("class") == "item-icons"
        ]

        if not items:
            raise Exception("No items")

        return items[0]

    def get_search_uri(self):
        return (
            self.BASE_URI
            + QUERY_STRING_SEPERATOR
            + QUERY_STRING_DELIMITER.join(
                [f"q={self.search_term}", f"cat={self.category_number}"]
            )
        )

    def search(self, search_terms: List[str], category_name: str = ALL):
        self.search_term = "+".join(search_terms)
        self.category_number = self.CATEGORIES.get(category_name)

        self.uri = self.get_search_uri()
        response = self.session.get(self.uri)
        response.html.render()

        for element in response.html.element:
            for item in element.cssselect(self.CSS_PATH):
                self.item = item
                yield Torrent(
                    self.get_tor_attr("span.list-item.item-name.item-title a"),
                    self.get_magnet_link(),
                    self.get_tor_attr("span.list-item.item-size"),
                    int(self.get_tor_attr("span.list-item.item-seed")),
                    int(self.get_tor_attr("span.list-item.item-leech")),
                )

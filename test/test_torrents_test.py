from src.Repo import PirateBayRepo
from requests_html import HTMLSession


def test_main():
    mock_session = HTMLSession()
    expected = ["foo"]

    for actual in PirateBayRepo(mock_session).search(expected):
        assert expected[0] in actual.title.lower()

import argparse
import logging
import os

from requests_html import HTMLSession

from src.Repo import PirateBayRepo, ALL
from src.constants import LOG_LEVEL, DEFAULT_LOG_LEVEL, RESULT_LIMIT


def main(
    session: HTMLSession,
    search_terms: str,
    category_name: str,
):
    for num, result in enumerate(
        PirateBayRepo(session).search(search_terms.split(" "), category_name)
    ):
        if num < RESULT_LIMIT:
            yield result.link


if __name__ == "__main__":
    log_level_str = os.environ.get(LOG_LEVEL, DEFAULT_LOG_LEVEL)
    logging.basicConfig(level=log_level_str)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--search-term", action="store", default="", required=False
    )
    parser.add_argument(
        "-c", "--search-category", action="store", default=ALL, required=False
    )
    args = parser.parse_args()
    print(
        list(
            main(
                HTMLSession(),
                search_terms=args.search_term,
                category_name=args.search_category,
            )
        )[0]
    )

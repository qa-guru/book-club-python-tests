from urllib.parse import parse_qs, urlparse

import pytest
import requests
from jsonschema import validate

from schemas.clubs_schema import clubs_response
from tests.clubs_common import CLUBS_LIST_URL, assert_clubs_list_https, walk_all_pages


class TestClubPaginationPageLinks:
    """Ссылки next/previous на заданной странице."""

    def test_second_page_next_and_previous_urls(self):
        params = {"page": 2}
        response = requests.get(CLUBS_LIST_URL, params=params)

        assert response.status_code == 200

        body = response.json()
        validate(body, schema=clubs_response)

        assert body["next"] == "https://book-club.qa.guru/api/v1/clubs/?page=3"
        assert body["previous"] == "https://book-club.qa.guru/api/v1/clubs/"


class TestClubPaginationTotals:
    """Согласованность count, количества записей и уникальности id."""

    def test_total_items_equals_count_and_ids_are_unique(self):
        count, ids = walk_all_pages(CLUBS_LIST_URL)

        assert len(ids) == count
        assert len(ids) == len(set(ids))


class TestClubPaginationBoundaries:
    """Первая, явная page=1 и последняя страница."""

    def test_first_page_previous_is_null_and_next_has_expected_shape(self):
        body = requests.get(CLUBS_LIST_URL).json()
        validate(body, schema=clubs_response)

        assert body["previous"] is None
        if body["count"] > len(body["results"]):
            assert body["next"] is not None
            assert_clubs_list_https(body["next"])
            parsed = urlparse(body["next"])
            qs = parse_qs(parsed.query)
            assert qs.get("page") == ["2"]

    def test_explicit_page_one_matches_default_list(self):
        default_body = requests.get(CLUBS_LIST_URL).json()
        page_one = requests.get(CLUBS_LIST_URL, params={"page": 1}).json()

        validate(default_body, clubs_response)
        validate(page_one, schema=clubs_response)

        assert default_body["count"] == page_one["count"]
        assert [c["id"] for c in default_body["results"]] == [c["id"] for c in page_one["results"]]

    def test_last_page_next_is_null(self):
        first = requests.get(CLUBS_LIST_URL).json()
        validate(first, schema=clubs_response)

        if first["next"] is None:
            pytest.skip("Одна страница — нет цепочки next для проверки последней.")

        url = CLUBS_LIST_URL
        params = None
        last_body = first
        while True:
            response = requests.get(url, params=params)
            assert response.status_code == 200
            body = response.json()
            validate(body, schema=clubs_response)
            if body["next"] is None:
                last_body = body
                break
            url = body["next"]
            params = None

        assert last_body["next"] is None
        assert last_body["previous"] is not None

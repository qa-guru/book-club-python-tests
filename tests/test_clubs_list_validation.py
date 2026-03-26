import pytest
import requests
from jsonschema import validate

from schemas.clubs_schema import clubs_response
from schemas.error_schema import detail_error
from tests.clubs_common import CLUBS_LIST_URL


class TestClubListPageParameter:
    """Некорректные и выходящие за пределы значения page."""

    @pytest.mark.parametrize("page", ["abc", 0, -1])
    def test_invalid_page_returns_404_with_detail(self, page):
        response = requests.get(CLUBS_LIST_URL, params={"page": page})

        assert response.status_code == 404
        body = response.json()
        validate(body, schema=detail_error)
        assert body["detail"] == "Invalid page."

    def test_page_beyond_last_returns_404(self):
        first = requests.get(CLUBS_LIST_URL).json()
        validate(first, schema=clubs_response)
        huge = 9_999_999
        response = requests.get(CLUBS_LIST_URL, params={"page": huge})

        assert response.status_code == 404
        body = response.json()
        validate(body, schema=detail_error)
        assert body["detail"] == "Invalid page."


class TestClubListQueryParameters:
    """Неизвестные параметры, дублирующийся page и длинный search."""

    def test_unknown_query_parameter_is_ignored(self):
        baseline = requests.get(CLUBS_LIST_URL).json()
        with_extra = requests.get(CLUBS_LIST_URL, params={"foo": "bar"}).json()

        assert baseline["count"] == with_extra["count"]
        assert [c["id"] for c in baseline["results"]] == [c["id"] for c in with_extra["results"]]

    def test_duplicate_page_query_uses_last_value(self):
        response = requests.get(CLUBS_LIST_URL, params=[("page", 1), ("page", 2)])
        assert response.status_code == 200
        combined = response.json()
        validate(combined, schema=clubs_response)

        page_two = requests.get(CLUBS_LIST_URL, params={"page": 2}).json()
        assert [c["id"] for c in combined["results"]] == [c["id"] for c in page_two["results"]]

    def test_long_search_string_still_returns_json_200(self):
        response = requests.get(CLUBS_LIST_URL, params={"search": "x" * 1500})

        assert response.status_code == 200
        body = response.json()
        validate(body, schema=clubs_response)
        assert body["count"] == 0
        assert body["results"] == []

import requests
from jsonschema import validate

from schemas.clubs_schema import clubs_response
from tests.clubs_common import CLUBS_LIST_URL, NO_MATCH_SEARCH


class TestClubSearchByTitle:
    """Поиск клубов по названию книги (основной happy-path)."""

    def test_search_returns_matching_club(self):
        params = {"search": "Сети"}
        response = requests.get(CLUBS_LIST_URL, params=params)

        assert response.status_code == 200

        body = response.json()
        validate(body, schema=clubs_response)

        club = body["results"][0]
        assert club["bookTitle"] == "Сети"
        assert club["bookAuthors"] == "Таненбаум"
        assert isinstance(club["publicationYear"], int)


class TestClubSearchEmptyResults:
    """Поведение поиска при отсутствии совпадений и повторяемость ответа."""

    def test_unknown_title_returns_empty_list(self):
        response = requests.get(CLUBS_LIST_URL, params={"search": NO_MATCH_SEARCH})

        assert response.status_code == 200
        body = response.json()
        validate(body, schema=clubs_response)

        assert body["count"] == 0
        assert body["results"] == []
        assert body["next"] is None
        assert body["previous"] is None

    def test_empty_results_stable_between_requests(self):
        params = {"search": NO_MATCH_SEARCH}
        first = requests.get(CLUBS_LIST_URL, params=params).json()
        second = requests.get(CLUBS_LIST_URL, params=params).json()

        assert first["count"] == second["count"] == 0
        assert first["results"] == second["results"] == []


class TestClubSearchParameter:
    """Граничные значения параметра search."""

    def test_empty_search_string_matches_no_filter(self):
        baseline = requests.get(CLUBS_LIST_URL).json()
        empty_search = requests.get(CLUBS_LIST_URL, params={"search": ""}).json()

        assert empty_search["count"] == baseline["count"]
        assert [c["id"] for c in empty_search["results"]] == [c["id"] for c in baseline["results"]]


class TestClubSearchStringNormalization:
    """Кодировка, регистр и пробелы в строке поиска."""

    def test_percent_encoded_matches_plain_utf8(self):
        plain = requests.get(CLUBS_LIST_URL, params={"search": "Сети"})
        encoded = requests.get(CLUBS_LIST_URL + "?search=%D0%A1%D0%B5%D1%82%D0%B8")

        assert plain.status_code == encoded.status_code == 200
        assert plain.json()["count"] == encoded.json()["count"]
        assert [c["id"] for c in plain.json()["results"]] == [
            c["id"] for c in encoded.json()["results"]
        ]

    def test_case_insensitive_for_cyrillic_title(self):
        lower = requests.get(CLUBS_LIST_URL, params={"search": "сети"})
        title = requests.get(CLUBS_LIST_URL, params={"search": "Сети"})

        assert lower.json()["count"] == title.json()["count"]
        if title.json()["results"]:
            assert lower.json()["results"][0]["id"] == title.json()["results"][0]["id"]

    def test_whitespace_around_query(self):
        stripped = requests.get(CLUBS_LIST_URL, params={"search": "Сети"})
        padded = requests.get(CLUBS_LIST_URL, params={"search": "  Сети  "})

        assert stripped.json()["count"] == padded.json()["count"]
        if stripped.json()["results"]:
            assert stripped.json()["results"][0]["id"] == padded.json()["results"][0]["id"]

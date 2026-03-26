"""Общие константы и хелперы для тестов списка клубов GET /api/v1/clubs."""

from __future__ import annotations

from urllib.parse import urlparse

import requests
from jsonschema import validate

from schemas.clubs_schema import clubs_response

CLUBS_LIST_URL = "https://book-club.qa.guru/api/v1/clubs"

NO_MATCH_SEARCH = "__no_such_club_xyz_qa_guru__"


def walk_all_pages(url: str, params: dict | None = None) -> tuple[int, list[int]]:
    """Собирает все id из results, переходя по next, и возвращает (count с первой страницы, ids)."""
    session = requests.Session()
    next_url: str | None = url
    next_params = params
    first = True
    count: int | None = None
    ids: list[int] = []

    while next_url:
        response = session.get(next_url, params=next_params if first else None)
        assert response.status_code == 200, response.text
        body = response.json()
        validate(body, schema=clubs_response)

        if count is None:
            count = body["count"]
        ids.extend(item["id"] for item in body["results"])

        next_url = body["next"]
        first = False
        next_params = None

    assert count is not None
    return count, ids


def assert_clubs_list_https(url: str) -> None:
    parsed = urlparse(url)
    assert parsed.scheme == "https"
    assert parsed.netloc == "book-club.qa.guru"

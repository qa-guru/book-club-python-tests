import pytest
import requests
from jsonschema import validate

from schemas.error_schema import detail_error
from tests.clubs_common import CLUBS_LIST_URL


class TestClubListUnsafeMethods:
    """Семантика HTTP: список доступен только через GET."""

    @pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
    def test_unsafe_method_does_not_return_successful_list(self, method):
        session = requests.Session()
        req = getattr(session, method)
        response = req(CLUBS_LIST_URL)

        assert response.status_code not in (200, 201)
        if response.headers.get("content-type", "").startswith("application/json"):
            body = response.json()
            assert "count" not in body and "results" not in body


class TestClubListContentNegotiation:
    """Заголовок Accept и формат ошибок."""

    def test_unacceptable_accept_header_returns_406_json(self):
        response = requests.get(
            CLUBS_LIST_URL,
            headers={"Accept": "application/xml"},
        )

        assert response.status_code == 406
        assert "application/json" in response.headers.get("Content-Type", "")
        body = response.json()
        validate(body, schema=detail_error)
        assert "Accept" in body["detail"]

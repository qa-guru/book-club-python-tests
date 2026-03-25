import requests
from jsonschema import validate

from schemas.clubs_schema import clubs_response


def test_get_clubs():
    response = requests.get('https://book-club.qa.guru/api/v1/clubs')

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 200

    body = response.json()
    validate(body, schema=clubs_response)

    assert body['count'] >= 0
    assert body['next'] == 'https://book-club.qa.guru/api/v1/clubs/?page=2'
    assert body['previous'] is None
    assert len(body['results']) >= 0

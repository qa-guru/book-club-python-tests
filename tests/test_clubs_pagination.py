import requests
from jsonschema import validate

from schemas.clubs_schema import clubs_response


def test_get_clubs_page_2():
    params = {'page': 2}

    response = requests.get('https://book-club.qa.guru/api/v1/clubs', params)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 200

    body = response.json()
    validate(body, schema=clubs_response)

    assert body['next'] == 'https://book-club.qa.guru/api/v1/clubs/?page=3'
    assert body['previous'] == 'https://book-club.qa.guru/api/v1/clubs/'

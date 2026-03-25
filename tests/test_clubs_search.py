import requests
from jsonschema import validate

from schemas.clubs_schema import clubs_response


def test_search_clubs_title():
    params = {'search': 'Сети'}

    response = requests.get('https://book-club.qa.guru/api/v1/clubs', params)

    print("\nHeaders:", response.headers)
    print("\nStatus code:", response.status_code)
    print("\nBody", response.text)

    assert response.status_code == 200

    body = response.json()
    validate(body, schema=clubs_response)

    club = body['results'][0]
    assert club['bookTitle'] == 'Сети'
    assert club['bookAuthors'] == 'Таненбаум'
    assert club['publicationYear'] == 2003
import requests
from jsonschema import validate

from schemas.clubs_schema import clubs_response

def test_clubs_get_club():
    response = requests.get('https://book-club.qa.guru/api/v1/clubs')

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 200

    body = response.json()
    validate(body, schema=clubs_response)

    club = body['results'][3]

    assert club['id'] == 4
    assert club['bookTitle'] == "Тестирование Дот Ком"
    assert club['bookAuthors'] == "Роман Савин"
    assert club['publicationYear'] == 2007
    assert club['description'] == "«Тестирование Дот Ком» -- это первая книга, которую рекомендуют прочитать начинающему тестировщику. Выпущенная в 2007 году, «Тестирование Дот Ком» стала библией в мире русскоязычного тестирования. Цель книги -- подготовить человека с нуля до получения работы в качестве тестировщика в российской или западной интернет-компании. Книга также будет интересна всем, кто хочет узнать больше о кухне стартапов и процессе разработки ПО."
    assert club['telegramChatLink'] == "https://t.me/qa.guru"
    assert club['owner'] == 11
    assert 11 in club['members']

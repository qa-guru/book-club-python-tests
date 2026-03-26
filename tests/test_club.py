import requests
import random
from jsonschema import validate
from schemas.club_schema import success_create_club

API_URL = "https://book-club.qa.guru/api/v1"
USERNAME = "user24"
PASSWORD = "pass24"
USERNAME_ID = 690

def test_success_create_club():
    auth_body = {"username": USERNAME, "password": PASSWORD}
    auth_response = requests.post(API_URL + "/auth/token/", json=auth_body)
    access_token = auth_response.json()["access"]

    book_title = f"Some another book {random.randint(1000, 999999)}"
    book_author = f"Some author"
    club_body = {
      "bookTitle": book_title,
      "bookAuthors": book_author,
      "publicationYear": 2147483647,
      "description": "Some descr",
      "telegramChatLink": "https://t.me/qa.guru"
    }
    club_headers = {"Authorization": "Bearer " + access_token}
    club_response = requests.post(API_URL + "/clubs/", headers=club_headers, json=club_body)

    print("\nStatus code:", club_response.status_code)
    print("Headers:", club_response.headers)
    print("Body:", club_response.text)

    assert club_response.status_code == 201

    club_response_body = club_response.json()
    validate(club_response_body, schema=success_create_club)

    assert club_response_body["bookTitle"] == book_title
    assert club_response_body["bookAuthors"] == book_author
    # todo other fields
    assert club_response_body["owner"] == USERNAME_ID
    assert USERNAME_ID in club_response_body["members"]
    assert len(club_response_body["reviews"]) == 0
    assert club_response_body["modified"] is None

    club_id = club_response_body["id"]
    delete_response = requests.delete(API_URL + f"/clubs/{club_id}/", headers=club_headers)
    assert delete_response.status_code is 204

# todo add negative tests for create club
# todo add tests for create club with user registration
# todo add tests for CRUD
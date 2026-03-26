import requests
from jsonschema import validate

from schemas.auth_schema import success_auth, wrong_credentials_auth, unsupported_media_type

API_URL = "https://book-club.qa.guru/api/v1/auth/token/"
USERNAME = "user24"
PASSWORD = "pass24"
TOKEN_PATH = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBl"

def test_successful_auth():
    request_body = {"username": USERNAME, "password": PASSWORD}

    response = requests.post(API_URL, json=request_body)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 200

    body = response.json()
    validate(body, schema=success_auth)

    access_token = body["access"]
    refresh_token = body["refresh"]
    assert TOKEN_PATH in access_token
    assert TOKEN_PATH in refresh_token
    assert len(access_token.split(".")) == 3
    assert len(refresh_token.split(".")) == 3
    assert access_token != refresh_token

def test_wrong_credentials_auth():
    request_body = {"username": USERNAME, "password": "wrong"}

    response = requests.post(API_URL, json=request_body)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 401

    body = response.json()
    validate(body, schema=wrong_credentials_auth)

    assert body["detail"] == "Invalid username or password."

def test_missing_password_auth():
    request_body = {"username": USERNAME}

    response = requests.post(API_URL, json=request_body)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    # todo fix test
    assert response.status_code == 401

    body = response.json()
    validate(body, schema=wrong_credentials_auth)

    assert body["detail"] == "Invalid username or password."

# todo implement more test - missing username, missing username&password, wrong body type (None, True, 123, "text", [])

def test_wrong_content_type_auth():
    request_body = {"username": USERNAME, "password": PASSWORD}
    headers = {"content-type": "image/png"}

    response = requests.post(API_URL, headers=headers, json=request_body)

    print("\nStatus code:", response.status_code)
    print("Headers:", response.headers)
    print("Body:", response.text)

    assert response.status_code == 415

    body = response.json()
    validate(body, schema=unsupported_media_type)

    assert body["detail"] == "Unsupported media type \"image/png\" in request."


# def test_successful_auth_draft():
#     response = requests.post("https://book-club.qa.guru/api/v1/auth/token/", json={"username": "user24", "password": "pass24"})
#
#     print("\nStatus code:", response.status_code)
#     print("Headers:", response.headers)
#     print("Body:", response.text)
#
#     assert response.status_code == 200
#
#     body = response.json()
#     validate(body, schema=success_auth)
#
#     assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBl" in body["access"]
#     assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBl" in body["refresh"]
#     assert body["access"] != body["refresh"]
success_create_club = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "id": {
      "type": "number"
    },
    "bookTitle": {
      "type": "string"
    },
    "bookAuthors": {
      "type": "string"
    },
    "publicationYear": {
      "type": "number"
    },
    "description": {
      "type": "string"
    },
    "telegramChatLink": {
      "type": "string"
    },
    "owner": {
      "type": "number"
    },
    "members": {
      "type": "array",
      "items": {
        "type": "number"
      }
    },
    "reviews": {
      "type": "array",
      "items": {}
    },
    "created": {
      "type": "string"
    },
    "modified": {}
  },
  "required": [
    "id",
    "bookTitle",
    "bookAuthors",
    "publicationYear",
    "description",
    "telegramChatLink",
    "owner",
    "members",
    "reviews",
    "created",
    "modified"
  ]
}
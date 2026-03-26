"""JSON Schema для тел ошибок DRF-подобного API (поле detail)."""

detail_error = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Error with detail",
    "type": "object",
    "properties": {
        "detail": {"type": "string"},
    },
    "required": ["detail"],
}

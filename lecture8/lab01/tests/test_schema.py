from pathlib import Path

import pytest
import yaml
from jsonschema import ValidationError, validate


def test_response_extra_field_blocked(client):
    spec_path = Path(__file__).resolve().parents[2] / "lab02" / "openapi.yaml"
    schema = yaml.safe_load(spec_path.read_text(encoding="utf-8"))["components"]["schemas"]["Book"]
    created = client.post(
        "/books",
        json={"title": "DDIA", "author": "Kleppmann", "year": 2017, "isbn": "9781449373320"},
    )
    assert created.status_code == 201

    response = client.get(created.headers["Location"])
    assert response.status_code == 200
    book = response.get_json()
    validate(book, schema)

    with pytest.raises(ValidationError) as error:
        validate({**book, "password_hash": "example"}, schema)
    assert error.value.validator == "additionalProperties"

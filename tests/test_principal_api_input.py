import uuid

import pytest
from fastapi.testclient import TestClient

from runtime_evidence import request_id_from_headers
from service import app


@pytest.mark.parametrize("key", ["", "   ", "x" * 129])
def test_invalid_request_key_is_rejected(key):
    response = TestClient(app).post("/v1/api", json={"key": key, "payload": {}})
    assert response.status_code == 422


def test_valid_request_keeps_safe_request_id():
    response = TestClient(app).post(
        "/v1/api",
        headers={"x-request-id": "request-123"},
        json={"key": "test", "payload": {"version": "v1"}},
    )
    assert response.status_code == 200
    assert response.headers["x-request-id"] == "request-123"


@pytest.mark.parametrize("unsafe", ["bad\nheader", "x" * 129, ""])
def test_unsafe_request_id_is_regenerated(unsafe):
    new_id = request_id_from_headers({"x-request-id": unsafe})
    uuid.UUID(new_id)
    assert new_id != unsafe

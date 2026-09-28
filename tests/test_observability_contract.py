from fastapi.testclient import TestClient

from service import app


def test_request_id_is_exposed():
    r = TestClient(app).get(
        "/health/live",
        headers={"x-request-id": "req-test"},
    )
    assert r.status_code == 200
    assert r.headers["x-request-id"] == "req-test"

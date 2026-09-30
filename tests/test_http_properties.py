from fastapi.testclient import TestClient
from hypothesis import given
from hypothesis import strategies as st

from service import app

c = TestClient(app)


def test_contract():
    assert c.get("/health/live").status_code == 200


@given(st.text(min_size=1, max_size=32))
def test_property(v):
    response = c.post("/v1/api", json={"key": v, "payload": {"version": "v1"}})
    if v.strip():
        assert response.status_code == 200
    else:
        assert response.status_code == 422

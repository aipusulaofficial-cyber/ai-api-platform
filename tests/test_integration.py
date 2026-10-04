from fastapi.testclient import TestClient

from service import app


def test_http_contract_and_domain():
    c = TestClient(app)
    assert c.get("/health/live").status_code == 200
    r = c.post("/v1/api", json={"key": "integration", "payload": {"version": "v1"}})
    assert r.status_code == 200, r.text


def test_http_path_enforces_request_admission(monkeypatch):
    import service
    from distributed_rate_limit import SharedWindowLimiter

    monkeypatch.setattr(service, "request_limiter", SharedWindowLimiter(limit=1, window_s=60.0))
    client = TestClient(service.app)
    payload = {"key": "limited", "payload": {"version": "v1"}}
    assert client.post("/v1/api", json=payload).status_code == 200
    assert client.post("/v1/api", json=payload).status_code == 429

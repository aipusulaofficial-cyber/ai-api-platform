from api_platform import *
import pytest


def test_authenticated_versioned_request():
    assert APIService({"k"}).handle(APIRequest("k", "v1", {}))["status"] == "accepted"


def test_auth_and_version_boundaries():
    s = APIService({"k"})
    with pytest.raises(APIError):
        s.handle(APIRequest("bad", "v1", {}))
    with pytest.raises(APIError):
        s.handle(APIRequest("k", "v9", {}))


def test_rate_limit():
    s = APIService({"k"}, 1, 60)
    s.handle(APIRequest("k", "v1", {}), 0)
    with pytest.raises(APIError):
        s.handle(APIRequest("k", "v1", {}), 1)

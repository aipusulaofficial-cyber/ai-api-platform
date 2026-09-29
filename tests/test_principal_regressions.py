import pytest

from api_domain import TokenBucket


@pytest.mark.parametrize("rate", [float("nan"), float("inf"), -1.0])
def test_invalid_refill_rate_rejected(rate):
    with pytest.raises(ValueError):
        TokenBucket(10, rate)


def test_nonfinite_clock_rejected():
    bucket = TokenBucket(10, 1)
    with pytest.raises(ValueError):
        bucket.consume(now=float("nan"))

def test_header_request_id_validation():
    from uuid import UUID

    from runtime_evidence import request_id_from_headers

    assert request_id_from_headers({"x-request-id": "valid-123"}) == "valid-123"
    for value in ("", "unsafe\nvalue", "x" * 129, " space "):
        actual = request_id_from_headers({"x-request-id": value})
        assert actual != value
        UUID(actual)

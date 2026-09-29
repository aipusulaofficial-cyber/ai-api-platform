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

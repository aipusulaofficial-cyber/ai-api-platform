from api_domain import *


def test_version_bucket():
    validate_version("v1")
    b = TokenBucket(2, 1)
    assert b.consume(now=0)
    assert b.consume(now=0)
    assert not b.consume(now=0)

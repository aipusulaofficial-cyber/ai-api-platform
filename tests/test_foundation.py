from runtime_evidence import runtime_evidence
import time

def test_contract():
    e=runtime_evidence(request_id="foundation",stage="api",decision="ALLOW",started=time.perf_counter())
    assert e["stage"] == "api"
    assert e["decision"] == "ALLOW"

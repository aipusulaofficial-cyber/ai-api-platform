"""HTTP admission benchmark evidence for CI.

Exercises the actual FastAPI request path under concurrent load. This is a
repeatable CI acceptance benchmark, not a claim about production hardware.
"""
from __future__ import annotations

import json
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from fastapi.testclient import TestClient

import service
from distributed_rate_limit import SharedWindowLimiter


def run(requests: int = 200, workers: int = 16) -> dict[str, object]:
    if requests < 1 or workers < 1:
        raise ValueError("requests and workers must be positive")
    # Keep admission finite but high enough that the benchmark measures the
    # HTTP path rather than intentionally exercising the 429 contract.
    service.request_limiter = SharedWindowLimiter(limit=requests + 1, window_s=60.0)
    latencies: list[float] = []
    failures: list[int] = []

    def one(i: int) -> float:
        started = time.perf_counter()
        with TestClient(service.app) as client:
            response = client.post(
                "/v1/api",
                json={"key": f"bench-{i}", "payload": {"version": "v1"}},
            )
        elapsed = (time.perf_counter() - started) * 1000
        if response.status_code != 200:
            failures.append(response.status_code)
        return elapsed

    wall_started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(one, i) for i in range(requests)]
        for future in as_completed(futures):
            latencies.append(future.result())
    wall_s = time.perf_counter() - wall_started
    ordered = sorted(latencies)

    def percentile(q: float) -> float:
        idx = min(len(ordered) - 1, max(0, int((len(ordered) - 1) * q)))
        return ordered[idx]

    report = {
        "requests": requests,
        "workers": workers,
        "failures": len(failures),
        "error_rate": len(failures) / requests,
        "throughput_rps": round(requests / wall_s, 2),
        "latency_ms": {
            "p50": round(statistics.median(ordered), 3),
            "p95": round(percentile(0.95), 3),
            "p99": round(percentile(0.99), 3),
        },
        "workload": "FastAPI TestClient -> /v1/api -> production request admission",
        "measurement": "repeatable CI HTTP-path acceptance benchmark; not a production hardware claim",
    }
    if failures:
        raise SystemExit(report)
    return report


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))

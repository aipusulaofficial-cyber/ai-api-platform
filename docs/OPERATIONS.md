# Operational runbook

Golden signals: request rate, error rate, p50/p95/p99 latency, throughput, concurrency/saturation, dependency health, retry_count, circuit state and resources.

1. Confirm readiness and deployment revision.
2. Trace by request_id/correlation_id.
3. Inspect error_type and dependency metrics.
4. Inspect retry_count, limits and circuit state.
5. Verify degraded behavior is explicit and safe.
6. Restore dependencies and run smoke/integration checks.

Inspect version, request/correlation IDs, error_type, dependency health, rate-limit and circuit state. Roll back incompatible API changes.
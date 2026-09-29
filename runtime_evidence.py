"""Schema-backed runtime response evidence."""

from __future__ import annotations

import re
import time
import uuid
from datetime import UTC, datetime
from typing import Any

from opentelemetry import trace


def request_id_from_headers(headers: Any) -> str:
    supplied = headers.get("x-request-id")
    if isinstance(supplied, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}", supplied):
        return supplied
    return str(uuid.uuid4())


def trace_id_from_context() -> str:
    ctx = trace.get_current_span().get_span_context()
    return format(ctx.trace_id, "032x") if ctx.is_valid else str(uuid.uuid4())


def runtime_evidence(
    *,
    request_id: str,
    stage: str,
    decision: str,
    started: float,
    error: str | None = None,
    cost_usd: float = 0.0,
    retry_count: int = 0,
    circuit_state: str = "UNKNOWN",
) -> dict[str, Any]:
    if decision not in {"ALLOW", "DENY", "FAIL"}:
        raise ValueError(f"invalid decision: {decision}")
    return {
        "request_id": request_id,
        "trace_id": trace_id_from_context(),
        "stage": stage,
        "decision": decision,
        "timestamp": datetime.now(UTC).isoformat(),
        "latency_ms": round((time.perf_counter() - started) * 1000, 3),
        "error": error,
        "cost_usd": cost_usd,
        "retry_count": retry_count,
        "circuit_state": circuit_state,
    }

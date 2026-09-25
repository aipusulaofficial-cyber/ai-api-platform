import logging
import time
import uuid

from fastapi import FastAPI, HTTPException, Request as FastAPIRequest
from opentelemetry import trace
from pydantic import BaseModel

from api_domain import validate_version

try:
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

    p = TracerProvider(resource=Resource.create({"service.name": "ai-api-platform"}))
    p.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(p)
except (ImportError, RuntimeError) as exc:
    logging.getLogger(__name__).warning("OpenTelemetry setup unavailable: %s", exc)

app = FastAPI(title="ai-api-platform", version="1.0.0")
tracer = trace.get_tracer("ai-api-platform")


class Request(BaseModel):
    key: str
    payload: dict = {}


@app.middleware("http")
async def observability_headers(request: FastAPIRequest, call_next):
    started = time.perf_counter()
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    correlation_id = request.headers.get("x-correlation-id") or request_id
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    response.headers["x-correlation-id"] = correlation_id
    response.headers["x-latency-ms"] = f"{(time.perf_counter() - started) * 1000:.3f}"
    return response


@app.get("/health/live")
def live():
    return {"status": "ok"}


@app.get("/health/ready")
def ready():
    return {"status": "ready"}


@app.post("/v1/api")
def handle(r: Request):
    with tracer.start_as_current_span("ai-api-platform.domain"):
        try:
            validate_version(r.payload.get("version", "v1"))
            return {
                "status": "accepted",
                "request_id": r.key,
                "version": r.payload.get("version", "v1"),
            }
        except (ValueError, KeyError, RuntimeError) as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

import time, logging
from fastapi import FastAPI, HTTPException, Request as FastAPIRequest
from opentelemetry import trace
from pydantic import BaseModel, Field
from api_domain import validate_version
from runtime_evidence import request_id_from_headers, runtime_evidence
try:
 from opentelemetry.sdk.resources import Resource
 from opentelemetry.sdk.trace import TracerProvider
 from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
 p=TracerProvider(resource=Resource.create({"service.name":"ai-api-platform"})); p.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter())); trace.set_tracer_provider(p)
except (ImportError,RuntimeError) as exc: logging.getLogger(__name__).warning("OpenTelemetry setup unavailable: %s",exc)
app=FastAPI(title="ai-api-platform",version="1.0.0"); tracer=trace.get_tracer("ai-api-platform")
class Request(BaseModel): key:str; payload:dict=Field(default_factory=dict)
@app.middleware("http")
async def observability_headers(request:FastAPIRequest,call_next):
 request_id=request_id_from_headers(request.headers); response=await call_next(request); response.headers["x-request-id"]=request_id; return response
@app.get("/health/live")
def live(): return {"status":"ok"}
@app.get("/health/ready")
def ready(): return {"status":"ready"}
@app.post("/v1/api")
def handle(r:Request,http_request:FastAPIRequest):
 started=time.perf_counter(); request_id=request_id_from_headers(http_request.headers)
 with tracer.start_as_current_span("ai-api-platform.domain"):
  try:
   version=r.payload.get("version","v1"); validate_version(version)
   return {"status":"accepted","request_id":request_id,"version":version,"evidence":runtime_evidence(request_id=request_id,stage="api.validate",decision="ALLOW",started=started)}
  except (ValueError,KeyError,RuntimeError) as e:
   evidence=runtime_evidence(request_id=request_id,stage="api.validate",decision="DENY",started=started,error=str(e)); raise HTTPException(status_code=400,detail={"error":str(e),"evidence":evidence}) from e

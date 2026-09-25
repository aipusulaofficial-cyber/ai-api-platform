from fastapi import FastAPI
from pydantic import BaseModel
from opentelemetry import trace
app=FastAPI(title="ai-api-platform",version="1.0.0");tracer=trace.get_tracer("ai-api-platform")
class Request(BaseModel):key:str;payload:dict={}
@app.get("/health/live")
def live():return {"status":"ok"}
@app.get("/health/ready")
def ready():return {"status":"ready"}
@app.post("/v1/api")
def handle(r:Request):
 with tracer.start_as_current_span("api"):return {"status":"accepted","key":r.key}

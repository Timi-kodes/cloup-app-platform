from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time
import random

app = FastAPI(title="Cloud App Platform")

REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["path", "method", "status"])
LATENCY = Histogram("http_request_latency_seconds", "Request latency", ["path"])

@app.middleware("http")
async def metrics_middleware(request, call_next):
    path = request.url.path
    start = time.time()
    try:
        response = await call_next(request)
        status = str(response.status_code)
        return response
    finally:
        LATENCY.labels(path=path).observe(time.time() - start)
        # status might not exist if exception; keep it safe
        REQUESTS.labels(path=path, method=request.method, status=locals().get("status", "500")).inc()

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/orders")
def orders():
    # Fake “business endpoint”
    return {
        "orders": [
            {"id": 1, "amount": round(random.uniform(5, 200), 2)},
            {"id": 2, "amount": round(random.uniform(5, 200), 2)},
        ]
    }

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

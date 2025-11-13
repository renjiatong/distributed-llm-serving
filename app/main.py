import time
import uuid
import logging
from fastapi import FastAPI, Request, Response
from app.utils.logger import logger
from app.routers.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from app.utils.metrics import REQUEST_COUNT, REQUEST_LATENCY
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.utils.rate_limiter import TokenBucket
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def request_middleware(request: Request, call_next):
    trace_id = uuid.uuid4().hex[:8]
    request.state.trace_id = trace_id

    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000

    logger.info({
        "trace_id": trace_id,
        "method": request.method,
        "path": request.url.path,
        "duration_ms": round(duration, 2),
        "message": "request completed"
    })

    response.headers["X-Trace-ID"] = trace_id
    return response

# 每秒允许最多 5 个请求，桶最大容量 10
rate_limiter = TokenBucket(rate=5, capacity=10)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if not rate_limiter.allow():
        raise HTTPException(status_code=429, detail="Too Many Requests")

    return await call_next(request)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    method = request.method
    path = request.url.path

    REQUEST_COUNT.labels(method=method, path=path).inc()

    with REQUEST_LATENCY.labels(method=method, path=path).time():
        response = await call_next(request)

    return response


@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(chat_router)

@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
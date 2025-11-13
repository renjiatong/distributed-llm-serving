import time
import uuid
import logging
from fastapi import FastAPI, Request
from app.utils.logger import logger
from app.routers.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware


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
async def log_requests(request: Request, call_next):
    trace_id = uuid.uuid4().hex[:8]
    request.state.trace_id = trace_id

    start = time.time()

    response = await call_next(request)

    process_time = (time.time() - start) * 1000
    logger.info(f"[{trace_id}] {request.method} {request.url.path} took {process_time:.2f}ms")

    response.headers["X-Trace-ID"] = trace_id
    response.headers["X-Process-Time-ms"] = f"{process_time:.2f}"

    return response


@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(chat_router)
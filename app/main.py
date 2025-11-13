from fastapi import FastAPI, Request
import time
import uuid
import logging
from app.utils.logger import logger
from app.routers.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # 允许所有域名访问
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start = time.time()

    response = await call_next(request)

    process_time = (time.time() - start) * 1000
    logger.info(f"[{request_id}] {request.method} {request.url.path} took {process_time:.2f}ms")

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-ms"] = f"{process_time:.2f}"

    return response


@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(chat_router)
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.chat import ChatRequest
from app.services.chat_service import stream_reply

router = APIRouter()

@router.get("/chat/stream")
def chat_stream(message: str):
    return StreamingResponse(stream_reply(message), media_type="text/event-stream")

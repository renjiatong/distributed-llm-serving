from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.services.chat_service import stream_reply

router = APIRouter()

# 普通聊天 POST 模式
@router.post("/chat")
def chat(req: dict, request: Request):
    from app.services.chat_service import generate_reply
    trace_id = request.state.trace_id
    reply = generate_reply(req["message"])
    return {"reply": reply, "trace_id": trace_id}


# 流式聊天：必须用 GET（因为 EventSource 只能 GET）
@router.get("/chat/stream")
def chat_stream(message: str, request: Request):
    trace_id = request.state.trace_id
    return StreamingResponse(
        stream_reply(message, trace_id),
        media_type="text/event-stream",
    )

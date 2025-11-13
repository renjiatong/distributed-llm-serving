from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User input message")

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    return ChatResponse(reply=f"You said: {req.message}")

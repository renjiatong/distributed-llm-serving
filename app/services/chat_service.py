from openai import OpenAI
import os

# 本地可替换成 vLLM:
# client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----------------------------
# 1) 普通非流式回复（用于 /chat）
# ----------------------------
def generate_reply(message: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message}]
    )
    return resp.choices[0].message.content


# ----------------------------
# 2) 流式回复（用于 /chat/stream）
# ----------------------------
def stream_reply(message: str, trace_id: str):
    # 先推送 trace_id 给前端
    yield f"data: TRACE:{trace_id}\n\n"

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message}],
        stream=True
    )

    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            yield f"data: {delta.content}\n\n"

    yield "data: [DONE]\n\n"

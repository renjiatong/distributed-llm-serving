from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def stream_reply(message: str, trace_id: str):
    # 先发送 trace id
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

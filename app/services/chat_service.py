from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def stream_reply(user_message: str):
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_message}],
        stream=True
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield f"data: {chunk.choices[0].delta.content}\n\n"

    yield "data: [DONE]\n\n"

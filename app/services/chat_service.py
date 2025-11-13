import os
from openai import OpenAI

# 用 OPENAI_API_KEY 环境变量
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_reply(user_message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_message}]
    )
    return response.choices[0].message.content

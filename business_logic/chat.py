import os
from openai import OpenAI

API_KEY = os.getenv('APIKEY')

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.proxyapi.ru/openai/v1",
)

def chatrequest(request: str):
    chat_request = client.chat.completions.create(
    model="gpt-4o", messages=[{"role": "user", "content": f"{request}"}])
    return chat_request.choices[0].message.content

"""
Модуль для работы с API ProxyApi, интеграции с ChatGpt.
"""

from openai import OpenAI
from config import API_KEY

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.proxyapi.ru/openai/v1",
)

def chatrequest(request: str):
    """
    Функция для получения ответа на вопрос ИИ.
    :param request: str(Запрос пользователя к ИИ)
    :return: str (Ответ gpt-4o на запрос)
    """
    chat_request = client.chat.completions.create(
    model="gpt-4o", messages=[{"role": "user", "content": f"{request}"}])
    return chat_request.choices[0].message.content

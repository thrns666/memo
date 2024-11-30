from fastapi import APIRouter
from starlette.websockets import WebSocket

from src.ai_chat.giga_chat_api import AiChat

chat_router = APIRouter()


@chat_router.websocket('/ws')
async def ws_chat(websocket: WebSocket):
    await websocket.accept()
    chat = AiChat()

    while True:
        data = await websocket.receive_text()
        res = await chat.post_promt(data)
        await websocket.send_text(f'{res}')

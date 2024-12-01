from fastapi import APIRouter
from loguru import logger
from starlette.websockets import WebSocket

from src.ai_chat.giga_chat_api import AiChat

chat_router = APIRouter()


@chat_router.websocket('/ws')
async def ws_chat(websocket: WebSocket):
    try:
        await websocket.accept()
        chat = AiChat()

        while True:
            data = await websocket.receive_text()
            res = await chat.post_promt(data)
            await websocket.send_text(f'{res}')
    except Exception as e:
        logger.error(f'websocket -- {e}')

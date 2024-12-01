from datetime import datetime
from uuid import uuid4

import aiohttp
from aiohttp import BasicAuth
from langchain_community.chat_models import GigaChat
from langchain_core.messages import AIMessage
from loguru import logger
from src.config import settings


class AiChat:
    def __init__(self):
        self.__model_response: AIMessage = None
        self.__chat_instance: GigaChat = None
        self.__token: str = None
        self.__token_expire: float = None

    async def _get_access_token(self):
        base_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': str(uuid4())
        }
        payload = {'scope': 'GIGACHAT_API_PERS'}
        auth = BasicAuth(settings.GIGA_CHAT_CLIENT_ID, settings.GIGA_CHAT_CLIENT_SECRET)

        async with aiohttp.ClientSession() as session:
            async with session.post(base_url, headers=headers, data=payload, auth=auth, ssl=False) as resp:
                response_data = await resp.json()

                logger.info(f'GigaChat token response status: {resp.status} -- {response_data}')

                self.__token = response_data.get('access_token')
                self.__token_expire = response_data.get('expires_at')

    async def post_promt(self, promt: str):
        if not self.__token_expire or self.__token_expire < datetime.now().timestamp():
            await self._get_access_token()

        try:
            self.__chat_instance = GigaChat(credentials=self.__token, scope='GIGACHAT_API_PERS', verify_ssl_certs=False)
            self.__model_response = await self.__chat_instance.ainvoke(promt)

            return self.__model_response.content
        except Exception as ex:
            logger.error(f'Error in post_prompt: {ex}')

            return

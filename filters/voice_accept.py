from aiogram.filters import BaseFilter
from aiogram.types import Message

from data import requestDataBase
BotDB = requestDataBase.BotBD("data/database.db")


class VoiceAccept(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        voice = await BotDB.voice_add(message.from_user.id)
        if voice:
            return True
        else:
            return False
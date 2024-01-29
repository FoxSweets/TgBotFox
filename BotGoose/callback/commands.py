from contextlib import suppress

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest

from keyboards import fabrics, inline

from data import requestDataBase
BotDB = requestDataBase.BotBD("data/database.db")

router = Router()

top_led = [
    "🥇",
    "🥈",
    "🥉",
    "🍀",
    "🍀",
    "🍀",
    "🍀",
    "🍀",
    "🍀",
    "🍀",
]

@router.callback_query()
async def menu_hadler(callback: CallbackQuery):
    user_id = callback.message.chat.id
    if callback.data == "start":
        pass

    if callback.data == "kick":
        pass
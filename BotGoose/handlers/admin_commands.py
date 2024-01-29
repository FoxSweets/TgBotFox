from typing import Any

from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from filters.is_admin import IsAdmin

from keyboards import inline

from data import requestDataBase
BotDB = requestDataBase.BotBD("data/database.db")


router = Router()

@router.message(Command("players"))
async def get_players(message: Message):
    count = 1
    text = ""
    list_user = await BotDB.users_list()
    for user in list_user:
        text += f"{count} | @{user}\n"
        count += 1

    if message.from_user.id in [1069370364, 5747700211]:
        await message.answer(f"PLAYERS LIST:\n{text}", reply_markup=inline.start_games)
    else:
        await message.answer(f"PLAYERS LIST:\n{text}")

@router.message(Command("kick"), IsAdmin([1069370364, 5747700211]))
async def kick_game(message: Message, bot: Bot, **data: Any):
    command: CommandObject = data.get("command")
    arg = command.args

    if arg is None:
        await message.answer(f"Вам необходимо ввести УЗ игрока!")
    else:
        name_user = arg.replace("@", "")

        user_list = await BotDB.users_list()
        if name_user in user_list:
            chat_user_id = await BotDB.get_user_id(name_user)
            await bot.send_message(chat_id=chat_user_id, text=f'Вас исключили из лобби!!')

            await BotDB.kick_user(name_user)
            await message.answer(f"Игрок {arg} исключен!")
        else:
            await message.answer("Такого игрока нету!")
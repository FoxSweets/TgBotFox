from typing import Any

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from filters.is_admin import IsAdmin
from random import randint as rnd

from data.request_word import get_word

from data import requestDataBase
BotDB = requestDataBase.BotBD("data/database.db")


router = Router()

@router.message(Command("list"), IsAdmin(1069370364))
async def list_word(message: Message, bot: Bot):
    random_word, random_word_spy = await get_word("word_list.txt")
    print(random_word, random_word_spy)

@router.message(Command("start_game"), IsAdmin(1069370364))
async def start_game(message: Message, bot: Bot):
    if not await BotDB.bot_game():
        start_list_user = await BotDB.user_list_name(1)
        if len(start_list_user) >= 2:
            list_user = await BotDB.user_list_id(1)
            spy_user = list_user[rnd(0, len(list_user)-1)]

            random_word, random_word_spy = await get_word("word_list.txt")

            for i in list_user:
                if i == spy_user:
                    await BotDB.update_game(i, 2)
                    await BotDB.update_spy(i)
                    await BotDB.update_word(i, random_word_spy)
                    await bot.send_message(chat_id=i, text=f'Игра началась!\nЗагаданное слово: "<b>{random_word_spy}</b>"\nНе говори никому это слово')
                else:
                    await BotDB.update_game(i, 2)
                    await BotDB.update_word(i, random_word)
                    await bot.send_message(chat_id=i, text=f'Игра началась!\nЗагаданное слово: "<b>{random_word}</b>"\nНе говори никому это слово')
            await BotDB.update_game_bot(1, 'R1')

@router.message(Command("kick"), IsAdmin([1069370364, 5747700211]))
async def kick_game(message: Message, bot: Bot, **data: Any):
    command: CommandObject = data.get("command")
    arg = command.args

    if arg is None:
        await message.answer(f"Вам необходимо ввести УЗ игрока!")
    else:
        name_user = arg.replace("@", "")

        user_list = await BotDB.user_list_name(1)
        if name_user in user_list:
            user_id = await BotDB.name_in_id(name_user)
            await bot.send_message(chat_id=user_id, text=f'Вас исключили из лобби!!')

            await BotDB.kick_user(name_user)
            await message.answer(f"Игрок {arg} исключен!")
        else:
            await message.answer("Такого игрока нету!")
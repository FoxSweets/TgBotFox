from typing import Any
from random import randint as rnd
from collections import Counter

from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from filters.is_admin import IsAdmin

from data import requestDataBase
BotDB = requestDataBase.BotBD("data/database.db")


router = Router()

@router.message(Command("start_game"), IsAdmin(1069370364))
async def get_players(bot: Bot):
    if not await BotDB.bot_game():
        start_list_user = await BotDB.users_list()
        if len(start_list_user) >= 2:
            list_user = await BotDB.users_list_id()

            with open("data/word_list.txt", "r", encoding="UTF-8") as word_list:
                lines = word_list.readlines()
                random_num: int = rnd(0, len(lines)-1)
                random_word = lines[random_num].strip().lower()

                random_num_spy: int = rnd(0, len(lines) - 1)
                while random_num == random_num_spy:
                    random_num_spy: int = rnd(0, len(lines) - 1)

                random_word_spy = lines[random_num_spy].strip().lower()

            spy_user = list_user[rnd(0, len(list_user)-1)]

            for i in list_user:
                if i == spy_user:
                    await BotDB.update_game(i, 2)
                    await BotDB.update_spy(i)
                    await BotDB.update_word(i, random_word_spy)
                    await bot.send_message(chat_id=i, text=f'Игра началась!\nЗагаданное слово: "<b>{random_word_spy}</b>"')
                else:
                    await BotDB.update_game(i, 2)
                    await BotDB.update_word(i, random_word)
                    await bot.send_message(chat_id=i, text=f'Игра началась!\nЗагаданное слово: "<b>{random_word}</b>"')
            await BotDB.update_game_bot(1, 'R1')

@router.message(Command("next_round"), IsAdmin(1069370364))
async def get_players(bot: Bot):
    if await BotDB.bot_game():
        list_user = await BotDB.user_games_list()

        with open("data/question.txt", "r", encoding="UTF-8") as question_list:
            lines = question_list.readlines()
            random_num: int = rnd(0, len(lines) - 1)
            random_question = lines[random_num].strip().lower()

        list_voice = await BotDB.list_voice()
        kick_voice = Counter(list_voice)

        max_value, max_keys = max(kick_voice.items(), key=lambda x: x[1], default=(None, 0))

        if max_keys == len(list_user)-1:
            spy_player = await BotDB.list_spy()

            await BotDB.kick_user(max_value)
            user_id = await BotDB.name_in_id(max_value)
            await bot.send_message(chat_id=user_id, text=f'Вас выгнали!!')

            for i in list_user:
                name = await BotDB.id_in_name(i)
                await BotDB.kick_user(name)
                message = f'<b>ПОБЕДИЛ ШПИОН: {spy_player}</b>!!!' if (await BotDB.list_spy()) else '<b>ПОБЕДИЛИ МИРНЫЕ</b>!!!'
                await bot.send_message(chat_id=i, text=message)
            await BotDB.update_game_bot(0, "R1")
        else:
            for i in list_user:
                await BotDB.update_user_voice(i, "None")
                await BotDB.update_voice(i, 0)
                await bot.send_message(chat_id=i, text=f'Вопрос раунда: "<b>{random_question}</b>"')

@router.message(Command("kick_player"))
async def voice_kick(message: Message, bot: Bot, **data: Any):
    if await BotDB.bot_game():
        if not await BotDB.get_user_voice(message.from_user.username):
            member_id = message.from_user.id
            command: CommandObject = data.get("command")
            arg = command.args

            if arg is None:
                await message.answer(f"Вам необходимо ввести УЗ игрока!")
            else:
                name_user = arg.replace("@", "")

                if name_user in await BotDB.user_games_list_name():
                    await BotDB.update_user_voice(member_id, name_user)
                    await BotDB.update_voice(member_id, 1)
                    user_id = await BotDB.name_in_id(name_user)
                    await message.answer(f"Вы проголосовали против: <b>{name_user}</b>")
                    await bot.send_message(chat_id=user_id, text=f'За вас проголосовали!!')
                else:
                    await message.answer("Такого игрока нету!")
        else:
            await message.answer("Вы уже проголосовали!")
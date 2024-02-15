from collections import Counter

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from filters.is_admin import IsAdmin

from filters.voice_accept import VoiceAccept

from data import requestDataBase
BotDB = requestDataBase.BotBD("data/database.db")


router = Router()

@router.message(Command("next_round"), IsAdmin(1069370364))
async def get_players(message: Message, bot: Bot):
    if await BotDB.bot_game():
        list_user = await BotDB.user_list_id(2)

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
                await BotDB.new_round(i)
                await bot.send_message(chat_id=i, text=f'<b>Напишите что вы думаете об предмете/персонаже.\nПомните вы можете быть шпионом.</b>')

@router.message(VoiceAccept())
async def item_request(message: Message, bot: Bot):
    message_user = message.text.lower()
    member_id = message.from_user.id

    await message.answer(
        text="Спасибо за ответ, ожидайте других игроков!!",
    )

    await BotDB.update_user_description(member_id, message_user)

    request_list = await BotDB.request_list()
    if not request_list:
        text = "Ответы:\n\n"
        description_list = await BotDB.description_list()
        for description in description_list:
            text += f"@{description[0]} | {description[1]}\n"

        user_list = await BotDB.user_list_id(2)
        for i in user_list:
            await bot.send_message(chat_id=i, text=text)
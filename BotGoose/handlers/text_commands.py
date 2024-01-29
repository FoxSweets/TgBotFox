from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart

from data import requestDataBase
BotDB = requestDataBase.BotBD("data/database.db")

router = Router()

@router.message()
async def echo(message: Message, bot: Bot):
    user_message = message.text.lower()
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    await BotDB.create_user(user_id, message.from_user.username)
    await BotDB.update_name(user_id, message.from_user.username)

    if user_message == "играть":
        if not await BotDB.bot_game():
            if await BotDB.get_user_game(message.from_user.id):
                await message.answer("Вы уже в лобби!")
            else:
                await BotDB.update_game(message.from_user.id, 1)

                chat_user_id = 1069370364
                await bot.send_message(chat_id=chat_user_id,
                                       text=f'@{message.from_user.username} присоединились к лобби')
                await message.answer("Вы присоединились к лобби!")

    if user_message == "помощь":
        await message.reply(f"Вот тебе помощь")
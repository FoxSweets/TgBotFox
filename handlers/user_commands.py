from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from keyboards import reply, inline

from data import requestDataBase
BotDB = requestDataBase.BotBD("data/database.db")


router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, <b>{message.from_user.first_name}</b>!!", reply_markup=reply.main)
    await BotDB.create_user(message.from_user.id, message.from_user.username)

@router.message(Command("players"))
async def get_players(message: Message):
    count = 1
    text = ""
    list_user = await BotDB.user_list_name(1)
    for user in list_user:
        text += f"{count} | @{user}\n"
        count += 1
    await message.answer(f"LIST OF LOBBY PLAYERS:\n{text}")

@router.message(Command("join"))
async def join_game(message: Message, bot: Bot):
    if not await BotDB.bot_game():
        if await BotDB.get_user_game(message.from_user.id):
            await message.answer("Вы уже в лобби!")
        else:
            await BotDB.update_game(message.from_user.id, 1)

            chat_user_id = 1069370364
            await bot.send_message(chat_id=chat_user_id, text=f'@{message.from_user.username} присоединился к лобби')
            await message.answer("Вы присоединились к лобби!")
    else:
        await message.answer("Нельзя войти из лобби, во время игры!")

@router.message(Command("leave"))
async def leave_game(message: Message, bot: Bot):
    if not await BotDB.bot_game():
        if await BotDB.get_user_game(message.from_user.id):
            await BotDB.update_game(message.from_user.id, 0)

            chat_user_id = 1069370364
            await bot.send_message(chat_id=chat_user_id, text=f'@{message.from_user.username} отключился от лобби')
            await message.answer("Вы отключились от лобби")
        else:
            await message.answer("Вы не в лобби!")
    else:
        await message.answer("Нельзя выйти из лобби, во время игры!")

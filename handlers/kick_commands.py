from aiogram import Router, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.reply import make_user

from data import requestDataBase
BotDB = requestDataBase.BotBD("data/database.db")

router = Router()

class OrderUser(StatesGroup):
    choosing_name = State()

@router.message(Command("kick_player"))
async def voice_kick(message: Message, state: FSMContext):
    if await BotDB.bot_game():
        user_list = await BotDB.user_list_name(2)

        await message.answer(text="Выберите игрока из списка ниже!", reply_markup=make_user(user_list))
        await state.set_state(OrderUser.choosing_name)


@router.message(OrderUser.choosing_name)
async def food_chosen(message: Message, state: FSMContext):
    message_user = message.text
    message_id = message.from_user.id

    user_list_name = await BotDB.user_list_name(2)
    user_list = [user_list for user_list in user_list_name]
    if message_user in user_list:
        await BotDB.update_user_voice(message_id, message_user)
        await message.answer(text="Спасибо за выбор.", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.answer(text="Такого игрока нету!")
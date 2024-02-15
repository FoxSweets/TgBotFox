from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

start_games = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🎮Старт", callback_data="start"),
        ]
    ]
)
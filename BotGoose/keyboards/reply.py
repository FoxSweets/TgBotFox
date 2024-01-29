from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Играть"),
            KeyboardButton(text="Помощь")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите действия!",
    selective=True
)
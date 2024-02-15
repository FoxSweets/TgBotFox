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

def make_user(items: list[str]):
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row],
                               resize_keyboard=True,
                               one_time_keyboard=True,
                               input_field_placeholder="Выберите игрока!",
                               selective=True
                               )
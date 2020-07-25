from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Подобрать обувь'),
        ]
    ],
    resize_keyboard=True
)

menu_brends = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='adidas'),
            KeyboardButton(text='adidas Originals'),
        ],
        [
            KeyboardButton(text='Fred Perry'),
            KeyboardButton(text='Nike'),
        ],
        [
            KeyboardButton(text='Reebok'),
            KeyboardButton(text='Reebok Classic'),
        ],
        [
            KeyboardButton(text='Tommy Hilfiger'),
            KeyboardButton(text='Puma'),
        ],
    ],
    resize_keyboard=True
)

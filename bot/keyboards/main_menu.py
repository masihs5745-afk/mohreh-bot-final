
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛒 ثبت سفارش"),
            KeyboardButton(text="📞 پشتیبانی")
        ],
        [
            KeyboardButton(text="ℹ️ درباره ما"),
            KeyboardButton(text="📋 قوانین")
        ]
    ],
    resize_keyboard=True
)

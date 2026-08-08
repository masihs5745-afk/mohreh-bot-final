
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🛒 ثبت سفارش"),
                KeyboardButton(text="📦 سفارش‌های من"),
            ],
            [
                KeyboardButton(text="📞 پشتیبانی"),
                KeyboardButton(text="ℹ️ اطلاعات"),
            ],
        ],
        resize_keyboard=True,
    )

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


channel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📢 عضویت در کانال",
                url="https://t.me/mohrehmarradobargh"
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ بررسی عضویت",
                callback_data="check_join"
            )
        ]
    ]
)

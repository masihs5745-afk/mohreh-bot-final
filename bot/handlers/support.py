from aiogram import Router, F
from aiogram.types import Message

from bot.config import ADMIN_ID
from bot.database.support import save_support_message


router = Router()


@router.message(F.text == "📞 پشتیبانی")
async def support_start(message: Message):
    await message.answer(
        "📩 پیام خود را ارسال کنید تا برای پشتیبانی ارسال شود."
    )


@router.message()
async def send_to_admin(message: Message):
    if message.from_user.id == ADMIN_ID:
        return

    if not message.text:
        return

    admin_message = await message.bot.send_message(
        ADMIN_ID,
        f"📩 پیام جدید از کاربر:\n\n"
        f"نام: {message.from_user.full_name}\n"
        f"آیدی: {message.from_user.id}\n\n"
        f"{message.text}"
    )

    await save_support_message(
        user_id=message.from_user.id,
        message_id=admin_message.message_id
    )

    await message.answer(
        "✅ پیام شما برای پشتیبانی ارسال شد."
    )

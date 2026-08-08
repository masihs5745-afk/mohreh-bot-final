from aiogram import Router
from aiogram.types import Message

from bot.config import ADMIN_ID
from bot.database.support import get_user_by_message


router = Router()


@router.message()
async def admin_reply(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    if not message.reply_to_message:
        return

    if not message.text:
        return

    user_id = await get_user_by_message(
        message.reply_to_message.message_id
    )

    if user_id:
        await message.bot.send_message(
            user_id,
            f"📩 پاسخ پشتیبانی:\n\n{message.text}"
        )
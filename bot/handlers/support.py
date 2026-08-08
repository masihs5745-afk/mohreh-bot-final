from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.config import ADMIN_ID
from bot.database.support import save_support_message
from bot.utils.states import SupportStates


router = Router()


@router.message(F.text == "📞 پشتیبانی")
async def support_start(
    message: Message,
    state: FSMContext,
):
    await state.set_state(SupportStates.waiting_for_message)

    await message.answer(
        "📩 پیام خود را ارسال کنید تا برای پشتیبانی ارسال شود.\n\n"
        "برای لغو، بنویسید: لغو"
    )


@router.message(SupportStates.waiting_for_message)
async def send_to_admin(
    message: Message,
    state: FSMContext,
):
    if message.from_user.id == ADMIN_ID:
        return

    if message.text == "لغو":
        await state.clear()

        await message.answer(
            "❌ ارسال پیام پشتیبانی لغو شد."
        )
        return

    if not message.text:
        await message.answer(
            "❌ لطفاً یک پیام متنی ارسال کنید."
        )
        return

    admin_message = await message.bot.send_message(
        ADMIN_ID,
        f"📩 پیام جدید از کاربر:\n\n"
        f"👤 نام: {message.from_user.full_name}\n"
        f"🆔 آیدی: {message.from_user.id}\n\n"
        f"💬 پیام:\n{message.text}"
    )

    await save_support_message(
        user_id=message.from_user.id,
        message_id=admin_message.message_id,
    )

    await message.answer(
        "✅ پیام شما برای پشتیبانی ارسال شد."
    )

    await state.clear()

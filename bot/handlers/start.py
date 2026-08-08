
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from bot.config import CHANNEL_ID, CHANNEL_URL
from bot.database.database import add_user
from bot.keyboards.main_menu import main_menu
from bot.keyboards.channel import channel_keyboard
from bot.check_membership import check_membership


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    user = message.from_user

    await add_user(
        user_id=user.id,
        full_name=user.full_name,
        username=user.username or "",
    )

    is_member = await check_membership(
        bot=message.bot,
        user_id=user.id,
        channel=CHANNEL_ID,
    )

    if not is_member:
        await message.answer(
            "👋 سلام!\n\n"
            "برای استفاده از ربات ابتدا باید در کانال ما عضو شوید. 📢\n\n"
            "بعد از عضویت روی «✅ بررسی عضویت» بزنید.",
            reply_markup=channel_keyboard(CHANNEL_URL),
        )
        return

    await message.answer(
        f"سلام {user.full_name} 👋\n\n"
        "به ربات خوش آمدید 🌹\n"
        "از منوی زیر گزینه موردنظر خود را انتخاب کنید:",
        reply_markup=main_menu(),
    )


@router.callback_query(F.data == "check_membership")
async def check_membership_callback(callback: CallbackQuery):
    user = callback.from_user

    is_member = await check_membership(
        bot=callback.bot,
        user_id=user.id,
        channel=CHANNEL_ID,
    )

    if not is_member:
        await callback.answer(
            "❌ هنوز در کانال عضو نشده‌اید.",
            show_alert=True,
        )
        return

    await callback.message.delete()

    await callback.message.answer(
        f"سلام {user.full_name} 👋\n\n"
        "✅ عضویت شما تأیید شد.\n"
        "به ربات خوش آمدید 🌹\n"
        "از منوی زیر گزینه موردنظر خود را انتخاب کنید:",
        reply_markup=main_menu(),
    )

    await callback.answer()

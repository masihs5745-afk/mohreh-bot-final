
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from bot.database.database import add_user
from bot.keyboards.main_menu import main_menu
from bot.keyboards.channel import channel_keyboard


router = Router()

CHANNEL = "@mohrehmarradobargh"


async def check_member(bot, user_id):
    member = await bot.get_chat_member(
        CHANNEL,
        user_id
    )

    return member.status in [
        "member",
        "administrator",
        "creator"
    ]


@router.message(Command("start"))
async def start_handler(message: Message):

    is_member = await check_member(
        message.bot,
        message.from_user.id
    )

    if not is_member:
        await message.answer(
            "برای استفاده از ربات ابتدا عضو کانال شوید 👇",
            reply_markup=channel_keyboard
        )
        return

    await add_user(
        user_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username
    )

    await message.answer(
        "سلام 👋\n"
        "به ربات خوش آمدید.",
        reply_markup=main_menu
    )


@router.callback_query(lambda c: c.data == "check_join")
async def check_join(callback: CallbackQuery):

    is_member = await check_member(
        callback.bot,
        callback.from_user.id
    )

    if is_member:
        await add_user(
            user_id=callback.from_user.id,
            full_name=callback.from_user.full_name,
            username=callback.from_user.username
        )

        await callback.message.answer(
            "✅ عضویت تایید شد.\n"
            "خوش آمدید.",
            reply_markup=main_menu
        )

    else:
        await callback.answer(
            "❌ هنوز عضو کانال نشده‌اید.",
            show_alert=True
        )


from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.database.database import add_user
from bot.keyboards.main_menu import main_menu


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    user = message.from_user

    await add_user(
        user_id=user.id,
        full_name=user.full_name,
        username=user.username or "",
    )

    await message.answer(
        f"سلام {user.full_name} 👋\n\n"
        "به ربات خوش آمدید 🌹\n"
        "از منوی زیر گزینه موردنظر خود را انتخاب کنید:",
        reply_markup=main_menu(),
    )

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from bot.config import ADMIN_ID
from bot.database.database import (
    get_users_count,
    get_orders_count,
    get_all_users,
)


router = Router()


class BroadcastState(StatesGroup):
    message = State()


@router.message(Command("panel"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    users = await get_users_count()
    orders = await get_orders_count()

    await message.answer(
        "👨‍💻 پنل مدیریت\n\n"
        f"👥 تعداد کاربران: {users}\n"
        f"📦 تعداد سفارش‌ها: {orders}\n\n"
        "📢 برای ارسال پیام همگانی:\n"
        "/broadcast"
    )


@router.message(Command("broadcast"))
async def broadcast_start(
    message: Message,
    state: FSMContext,
):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "📢 پیام همگانی خود را ارسال کنید.\n\n"
        "برای لغو بنویسید: لغو"
    )

    await state.set_state(BroadcastState.message)


@router.message(BroadcastState.message)
async def send_broadcast(
    message: Message,
    state: FSMContext,
):
    if message.from_user.id != ADMIN_ID:
        return

    if message.text == "لغو":
        await state.clear()

        await message.answer(
            "❌ ارسال همگانی لغو شد."
        )
        return

    if not message.text:
        await message.answer(
            "❌ لطفاً یک پیام متنی ارسال کنید."
        )
        return

    users = await get_all_users()

    success = 0
    failed = 0

    for user_id in users:
        try:
            await message.bot.send_message(
                user_id,
                message.text,
            )
            success += 1

        except Exception:
            failed += 1

    await state.clear()

    await message.answer(
        "📢 ارسال همگانی انجام شد.\n\n"
        f"✅ موفق: {success}\n"
        f"❌ ناموفق: {failed}"
    )
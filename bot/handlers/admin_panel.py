from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.config import ADMIN_ID
from bot.database.database import get_users_count, get_orders_count, get_all_users


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
        f"👥 کاربران: {users}\n"
        f"📦 سفارش‌ها: {orders}\n\n"
        "برای ارسال همگانی دستور زیر را بزن:\n"
        "/broadcast"
    )


@router.message(Command("broadcast"))
async def broadcast_start(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "📢 متن پیام همگانی را ارسال کن:"
    )

    await state.set_state(BroadcastState.message)


@router.message(BroadcastState.message)
async def send_broadcast(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return

    users = await get_all_users()

    count = 0

    for user_id in users:
        try:
            await message.bot.send_message(
                user_id,
                message.text
            )
            count += 1

        except Exception:
            pass

    await message.answer(
        f"✅ پیام برای {count} کاربر ارسال شد."
    )

    await state.clear()

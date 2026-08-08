from aiogram import Router, F
from aiogram.types import Message

from bot.database.database import get_user_orders


router = Router()


@router.message(F.text == "📦 سفارش‌های من")
async def my_orders_handler(message: Message):
    orders = await get_user_orders(
        message.from_user.id
    )

    if not orders:
        await message.answer(
            "📦 شما هنوز هیچ سفارشی ثبت نکرده‌اید."
        )
        return

    text = "📦 سفارش‌های شما:\n\n"

    for order in orders:
        order_id, name, phone, description = order

        text += (
            f"🔹 سفارش شماره: #{order_id}\n"
            f"👤 نام: {name}\n"
            f"📞 تماس: {phone}\n"
            f"📝 توضیحات: {description}\n"
            f"━━━━━━━━━━━━━━\n"
        )

    await message.answer(text)

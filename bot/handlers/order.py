from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from bot.utils.states import OrderState
from bot.database.database import add_order


router = Router()


async def cancel_order(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "❌ سفارش لغو شد."
    )


@router.message(Text("🛒 ثبت سفارش"))
async def order_start(message: Message, state: FSMContext):
    await message.answer(
        "نام خود را وارد کنید.\n\n"
        "برای لغو سفارش بنویسید: لغو"
    )

    await state.set_state(OrderState.name)


@router.message(OrderState.name)
async def get_name(message: Message, state: FSMContext):

    if message.text == "لغو":
        await cancel_order(message, state)
        return

    await state.update_data(
        name=message.text
    )

    await message.answer(
        "شماره تماس خود را وارد کنید.\n\n"
        "برای لغو سفارش بنویسید: لغو"
    )

    await state.set_state(OrderState.phone)


@router.message(OrderState.phone)
async def get_phone(message: Message, state: FSMContext):

    if message.text == "لغو":
        await cancel_order(message, state)
        return

    await state.update_data(
        phone=message.text
    )

    await message.answer(
        "توضیحات سفارش را وارد کنید.\n\n"
        "برای لغو سفارش بنویسید: لغو"
    )

    await state.set_state(OrderState.description)


@router.message(OrderState.description)
async def get_description(message: Message, state: FSMContext):

    if message.text == "لغو":
        await cancel_order(message, state)
        return

    await state.update_data(
        description=message.text
    )

    data = await state.get_data()

    await message.answer(
        "📋 خلاصه سفارش:\n\n"
        f"👤 نام: {data['name']}\n"
        f"📞 تماس: {data['phone']}\n"
        f"📝 توضیحات: {data['description']}\n\n"
        "برای ثبت نهایی بنویسید: تایید\n"
        "برای لغو بنویسید: لغو"
    )

    await state.set_state(OrderState.confirm)


@router.message(OrderState.confirm)
async def confirm_order(message: Message, state: FSMContext):

    if message.text == "لغو":
        await cancel_order(message, state)
        return

    if message.text != "تایید":
        await message.answer(
            "لطفاً فقط «تایید» یا «لغو» را ارسال کنید."
        )
        return

    data = await state.get_data()

    await add_order(
        user_id=message.from_user.id,
        name=data["name"],
        phone=data["phone"],
        description=data["description"]
    )

    await message.answer(
        "✅ سفارش شما با موفقیت ثبت شد."
    )

    await state.clear()

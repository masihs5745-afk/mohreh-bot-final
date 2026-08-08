
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Text


router = Router()


@router.message(Text("ℹ️ درباره ما"))
async def about_handler(message: Message):
    await message.answer(
        "ℹ️ درباره ما\n\n"
        "این ربات جهت ثبت سفارش و ارتباط با پشتیبانی طراحی شده است."
    )


@router.message(Text("📋 قوانین"))
async def rules_handler(message: Message):
    await message.answer(
        "📋 قوانین:\n\n"
        "1- اطلاعات صحیح وارد کنید.\n"
        "2- قبل از ثبت سفارش توضیحات کامل ارائه دهید.\n"
        "3- برای پشتیبانی از بخش مربوطه استفاده کنید."
    )

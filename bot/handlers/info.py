
from aiogram import Router, F
from aiogram.types import Message


router = Router()


@router.message(F.text == "ℹ️ درباره ما")
async def about_handler(message: Message):
    await message.answer(
        "ℹ️ درباره ما\n\n"
        "این ربات جهت ثبت سفارش و ارتباط با پشتیبانی طراحی شده است."
    )


@router.message(F.text == "📋 قوانین")
async def rules_handler(message: Message):
    await message.answer(
        "📋 قوانین:\n\n"
        "1- اطلاعات صحیح وارد کنید.\n"
        "2- قبل از ثبت سفارش توضیحات کامل ارائه دهید.\n"
        "3- برای پشتیبانی از بخش مربوطه استفاده کنید."
    )

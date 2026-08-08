
import asyncio

from aiogram import Bot, Dispatcher

from bot.config import BOT_TOKEN
from bot.handlers.start import router as start_router
from bot.handlers.order import router as order_router
from bot.handlers.support import router as support_router
from bot.handlers.admin import router as admin_router
from bot.handlers.admin_panel import router as admin_panel_router
from bot.handlers.info import router as info_router
from bot.database.database import create_db


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(order_router)
dp.include_router(support_router)
dp.include_router(admin_router)
dp.include_router(admin_panel_router)
dp.include_router(info_router)


async def main():
    await create_db()

    print("Bot is starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from aiogram import Bot, Dispatcher

from bot.config import BOT_TOKEN

from bot.handlers.start import router as start_router
from bot.handlers.order import router as order_router
from bot.handlers.my_orders import router as my_orders_router
from bot.handlers.support import router as support_router
from bot.handlers.admin import router as admin_router
from bot.handlers.admin_panel import router as admin_panel_router
from bot.handlers.info import router as info_router

from bot.database.database import create_db
from bot.database.support import create_support_table


# =========================
# Render Health Check Server
# =========================

class HealthHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        return


def start_health_server():
    port = int(os.getenv("PORT", "10000"))

    server = HTTPServer(
        ("0.0.0.0", port),
        HealthHandler
    )

    print(f"Health server running on port {port}")

    server.serve_forever()


# =========================
# Bot
# =========================

bot = Bot(
    token=BOT_TOKEN
)

dp = Dispatcher()


# =========================
# Routers
# =========================

dp.include_router(start_router)
dp.include_router(order_router)
dp.include_router(my_orders_router)
dp.include_router(support_router)
dp.include_router(admin_router)
dp.include_router(admin_panel_router)
dp.include_router(info_router)


# =========================
# Main
# =========================

async def main():

    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is not set!"
        )

    # ساخت دیتابیس اصلی
    await create_db()

    # ساخت جدول پشتیبانی
    await create_support_table()

    print("Database initialized.")

    # اجرای HTTP server برای Render
    health_thread = Thread(
        target=start_health_server,
        daemon=True
    )

    health_thread.start()

    print("Bot is starting...")

    try:

        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types()
        )

    finally:

        await bot.session.close()


# =========================
# Run
# =========================

if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("Bot stopped.")
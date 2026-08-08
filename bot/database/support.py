import aiosqlite


DB_NAME = "bot.db"


async def create_support_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS support_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message_id INTEGER NOT NULL
        )
        """)

        await db.commit()


async def save_support_message(
    user_id: int,
    message_id: int
):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT INTO support_messages
            (user_id, message_id)
            VALUES (?, ?)
            """,
            (user_id, message_id)
        )

        await db.commit()


async def get_user_by_message(
    message_id: int
):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT user_id
            FROM support_messages
            WHERE message_id = ?
            """,
            (message_id,)
        )

        result = await cursor.fetchone()

        if result:
            return result[0]

        return None

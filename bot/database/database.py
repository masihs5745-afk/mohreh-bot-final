import aiosqlite


DB_NAME = "bot.db"


async def create_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE,
            full_name TEXT,
            username TEXT
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            name TEXT,
            phone TEXT,
            description TEXT
        )
        """)

        await db.commit()


async def add_user(
    user_id: int,
    full_name: str,
    username: str
):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO users
            (user_id, full_name, username)
            VALUES (?, ?, ?)
            """,
            (user_id, full_name, username)
        )

        await db.commit()


async def add_order(
    user_id: int,
    name: str,
    phone: str,
    description: str
):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT INTO orders
            (user_id, name, phone, description)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, name, phone, description)
        )

        await db.commit()


async def get_users_count():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM users"
        )

        result = await cursor.fetchone()
        return result[0]


async def get_orders_count():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM orders"
        )

        result = await cursor.fetchone()
        return result[0]


async def get_all_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT user_id FROM users"
        )

        users = await cursor.fetchall()

        return [user[0] for user in users]


async def get_user_orders(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT id, name, phone, description
            FROM orders
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        )

        orders = await cursor.fetchall()

        return orders
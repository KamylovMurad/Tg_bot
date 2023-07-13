import asyncpg


class Database:
    def __init__(self, dsn):
        self.dsn = dsn
        self.pool = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(self.dsn)
        if self.pool:
            print("Successfully created pool!")
        else:
            print("Failed to create pool.")

    async def create_user_table(self):
        async with self.pool.acquire() as conn:
            await conn.execute(
                'CREATE TABLE IF NOT EXISTS users('
                'id SERIAL PRIMARY KEY, '
                'user_id INTEGER UNIQUE, '
                'date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'
                )

    async def set_user_id(self, user_id):
        async with self.pool.acquire() as conn:
            await conn.execute(
                f"INSERT INTO users (user_id) "
                f"VALUES ('{user_id}') "
                f"ON CONFLICT DO NOTHING"
            )

    async def get_users_list_to_distribute_for_all(self):
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(f"SELECT user_id FROM users")
            return [row[0] for row in rows]

    async def cout_all(self):
        async with self.pool.acquire() as conn:
            elem = await conn.fetchrow(f"SELECT COUNT(*) FROM users")
            return elem[0]

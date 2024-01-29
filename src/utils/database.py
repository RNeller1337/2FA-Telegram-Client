import aiosqlite


class Database:
    def __init__(self):
        self.name = 'db/settings.db'

    async def create_table(self):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = '''CREATE TABLE IF NOT EXISTS keys (user INT, name TEXT, key TEXT)'''
            await cursor.executescript(query)
            await db.commit()

    async def add_key(self, userid, name, key):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = '''INSERT INTO keys VALUES (?, ?, ?)'''
            await cursor.execute(query, (userid, name, key))
            await db.commit()

    async def get_key(self, userid, name):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = '''SELECT key FROM keys WHERE user = ? AND name = ?'''
            await cursor.execute(query, (userid, name))
            return await cursor.fetchone()

    async def remove_key(self, userid, name):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = '''DELETE FROM keys WHERE user = ? AND name = ?'''
            await cursor.execute(query, (userid, name))
            await db.commit()

    async def get_all(self, userid):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = '''SELECT name, key FROM keys WHERE user = ?'''
            await cursor.execute(query, (userid,))
            return await cursor.fetchall()

import aiosqlite
import asyncio

async def create_db():
	async with aiosqlite.connect("data/database.db") as db:
		cursor = await db.cursor()

		query = """
		CREATE TABLE IF NOT EXISTS "users" (
			"id"	INTEGER,
			"name"	TEXT,
			"game_status"	INTEGER,
			"word"	TEXT,
			"spy"	INTEGER,
			"voice"	INTEGER,
			"voice_spy"	TEXT,
			"request"	INTEGER,
			"description"	TEXT
		);
		CREATE TABLE IF NOT EXISTS "bot" (
				"rooms"	TEXT,
				"game"	INTEGER
			)
		"""

		await cursor.executescript(query)
		await db.commit()
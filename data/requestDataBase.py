import aiosqlite
import asyncio
from typing import Dict

class BotBD:
    def __init__(self, db_file: str) -> None:
        self.db_file = db_file
        self.db = None
        self.cursor = None

        asyncio.run(self.connect())

    async def connect(self):
        self.db = await aiosqlite.connect(self.db_file)
        self.cursor = await self.db.cursor()

    async def create_user(self, member_id: int, member_name: str):
        async with self.db.execute(f"SELECT id FROM users WHERE id = ?", (member_id,)) as cursor:
            if await cursor.fetchone() is None:
                await self.cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)",
                                          (member_id, member_name, 0, "None", 0, 0, "None"))
        await self.db.commit()

    async def update_name(self, member_id: int, member_name: str):
        await self.cursor.execute(f"UPDATE users SET name = ? WHERE id = ?", (member_name, member_id,))
        await self.db.commit()

    async def update_game(self, member_id: int, game_status: int):
        await self.cursor.execute(f"UPDATE users SET game_status = ? WHERE id = ?", (game_status, member_id,))
        await self.db.commit()

    async def update_spy(self, member_id: int):
        await self.cursor.execute(f"UPDATE users SET spy = ? WHERE id = ?", (1, member_id,))
        await self.db.commit()

    async def update_word(self, member_id: int, word_game: str):
        await self.cursor.execute(f"UPDATE users SET word = ? WHERE id = ?", (word_game, member_id,))
        await self.db.commit()

    async def update_user_voice(self, member_id: int, user_voice: str):
        await self.cursor.execute(f"UPDATE users SET voice_spy = ? WHERE id = ?", (user_voice, member_id,))
        await self.cursor.execute(f"UPDATE users SET voice = ? WHERE id = ?", (1, member_id,))
        await self.db.commit()

    async def kick_user(self, member_name: str):
        await self.cursor.execute(f"UPDATE users SET game_status = ? WHERE name = ?", (0, member_name,))
        await self.cursor.execute(f"UPDATE users SET word = ? WHERE name = ?", ("None", member_name,))
        await self.cursor.execute(f"UPDATE users SET spy = ? WHERE name = ?", (0, member_name,))
        await self.cursor.execute(f"UPDATE users SET voice = ? WHERE name = ?", (0, member_name,))
        await self.cursor.execute(f"UPDATE users SET voice_spy = ? WHERE name = ?", ("None", member_name,))
        await self.cursor.execute(f"UPDATE users SET request = ? WHERE name = ?", (0, member_name,))
        await self.cursor.execute(f"UPDATE users SET description = ? WHERE name = ?", ("None", member_name,))
        await self.db.commit()

    async def new_round(self, member_id: int):
        await self.cursor.execute(f"UPDATE users SET voice = ? WHERE id = ?", (0, member_id,))
        await self.cursor.execute(f"UPDATE users SET voice_spy = ? WHERE id = ?", ("None", member_id,))
        await self.cursor.execute(f"UPDATE users SET request = ? WHERE id = ?", (1, member_id,))
        await self.cursor.execute(f"UPDATE users SET description = ? WHERE id = ?", ("None", member_id,))
        await self.db.commit()

    async def update_user_description(self, member_id: int, description: str):
        await self.cursor.execute(f"UPDATE users SET request = ? WHERE id = ?", (0, member_id,))
        await self.cursor.execute(f"UPDATE users SET description = ? WHERE id = ?", (description, member_id,))
        await self.db.commit()

    async def voice_add(self, member_id: int) -> bool:
        async with self.db.execute(f"SELECT request FROM users WHERE id = ?", (member_id,)) as cursor:
            user_id = await cursor.fetchone()
        return bool(user_id[0])

    async def name_in_id(self, member_name: str) -> int:
        async with self.db.execute(f"SELECT id FROM users WHERE name = ?", (member_name,)) as cursor:
            user_id = await cursor.fetchone()
        return user_id[0]

    async def id_in_name(self, member_id: int) -> str:
        async with self.db.execute("SELECT name FROM users WHERE id = ?", (member_id,)) as cursor:
            user_name = await cursor.fetchone()
        return user_name[0]

    async def get_user_game(self, member_id: int) -> bool:
        async with self.db.execute("SELECT game_status FROM users WHERE id = ?", (member_id,)) as cursor:
            user_game = await cursor.fetchone()
        return bool(user_game[0])

    async def user_list_id(self, status: int) -> list[int]:
        async with self.db.execute("SELECT id FROM users WHERE game_status = ?", (status,)) as cursor:
            rows = await cursor.fetchall()
            list_user = [row[0] for row in rows]
        return list_user

    async def user_list_name(self, status: int) -> list[str]:
        async with self.db.execute("SELECT name FROM users WHERE game_status = ?", (status,)) as cursor:
            rows = await cursor.fetchall()
            list_user = [row[0] for row in rows]
        return list_user

    async def list_voice(self) -> list[str]:
        async with self.db.execute("SELECT voice_spy FROM users WHERE game_status = 2") as cursor:
            rows = await cursor.fetchall()
            list_user = [row[0] for row in rows]
        return list_user

    async def request_list(self) -> list[int]:
        async with self.db.execute("SELECT request FROM users WHERE request = ? AND game_status = ?", (1, 2,)) as cursor:
            rows = await cursor.fetchall()
            list_user = [row[0] for row in rows]
        return list_user

    async def description_list(self) -> Dict[str, str]:
        async with self.db.execute("SELECT name, description FROM users WHERE game_status = ?", (2,)) as cursor:
            rows = await cursor.fetchall()
        return rows

    async def list_spy(self) -> bool | str:
        async with self.db.execute("SELECT name FROM users WHERE spy = 1") as cursor:
            list_spy = await cursor.fetchone()
            if list_spy is None:
                return False
            else:
                return list_spy[0]

    async def bot_game(self) -> bool:
        async with self.db.execute("SELECT game FROM bot WHERE rooms = ?", ('R1',)) as cursor:
            game_bot = await cursor.fetchone()
        return bool(game_bot[0])

    async def update_game_bot(self, game_bot: int, rooms: str):
        await self.cursor.execute(f"UPDATE bot SET game = ? WHERE rooms = ?", (game_bot, rooms,))
        await self.db.commit()

    async def close_database(self):
        await self.cursor.close()
        await self.db.close()
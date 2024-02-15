import asyncio
import logging
from config_reader import config

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import user_commands, text_commands, admin_commands, kick_commands, round_commands

from data import createDataBase, requestDataBase
BotDB = requestDataBase.BotBD("data/database.db")

async def main():
    await createDataBase.create_db()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")

    dp.include_routers(
        user_commands.router,
        admin_commands.router,
        kick_commands.router,
        round_commands.router,
        text_commands.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
import asyncio
from aiogram import Bot, Dispatcher, F

from handlers import user_commands, text_commands, admin_commands, game_commands

from config_reader import config
from data import createDataBase, requestDataBase

BotDB = requestDataBase.BotBD("data/database.db")

async def main():
    await createDataBase.create_db()

    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")
    dp = Dispatcher()

    dp.include_routers(
        user_commands.router,
        admin_commands.router,
        game_commands.router,
        text_commands.router
    )

    print("BOT ONLINE!!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
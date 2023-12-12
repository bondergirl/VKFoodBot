import asyncio
import logging
from aiogram import Bot
from settings import BotSettings
from tg_API.utils import cmd_hello, cmd_help, cmd_history, cmd_low, cmd_high, cmd_custom
from database.core import database_initialize

from tg_API.core import dp


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BotSettings().bot_token.get_secret_value())

    dp.include_router(cmd_hello.router)
    dp.include_router(cmd_help.router)
    dp.include_router(cmd_history.router)
    dp.include_router(cmd_low.router)
    dp.include_router(cmd_high.router)
    dp.include_router(cmd_custom.router)

    database_initialize()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())




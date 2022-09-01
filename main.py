"""

   The project will not be further supported by the developer

"""

from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher

from handlers.client import register_client
from handlers.admingroup import register_admingroup

import os
import asyncio


load_dotenv(find_dotenv())


bot = Bot(os.getenv("TOKEN"))
dispatcher = Dispatcher()


async def main():
    dispatcher.include_router(register_client())
    dispatcher.include_router(register_admingroup())

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

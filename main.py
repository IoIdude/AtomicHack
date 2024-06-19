# import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from utils.config import TOKEN

client = Bot(token=TOKEN)


async def main():
    loop = asyncio.get_event_loop()
    dp = Dispatcher(storage=MemoryStorage(), loop=loop)
    # logging.basicConfig(level=logging.INFO)
    from app.handlers import router
    dp.include_router(router)
    await dp.start_polling(client)


if __name__ == '__main__':
    asyncio.run(main())

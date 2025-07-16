import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import TELEGRAM_TOKEN
from app.handlers import router
from app.scheduler import setup_scheduler


async def main():
    bot = Bot(
        token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    setup_scheduler(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

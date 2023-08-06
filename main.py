import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from settings.api import BOT_API
from settings.setting import *
from handlers import commands,different_types

async def run_bot():
    bot = Bot(token=BOT_API, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(commands.router)
    # dp.include_router(different_types.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    logging.basicConfig(
    level=logging.DEBUG,
    filename=f'logging/app.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s'
    )

    asyncio.run(run_bot())


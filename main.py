from os import getenv
import asyncio
import logging
import sys

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.log.log import get_log
from app.routers.start import start_router
from app.routers.age import main_router

# Завантажимо дані середовища з файлу .env(За замовчуванням)
load_dotenv()


# Усі обробники варто закріплювати за Router або Dispatcher
root_router = Router()
root_router.include_routers(start_router, main_router) 

# Головна функція пакету
async def main() -> None:
    # Дістанемо токен бота з середовища
    TOKEN = getenv("API")
    # Створимо об'єкт Bot
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()
    dp.include_router(root_router)
    # Почнемо обробляти події для бота
    await dp.start_polling(bot)


if __name__ == "__main__":
   logging.basicConfig(level=logging.INFO, stream=sys.stdout)
   asyncio.run(main())

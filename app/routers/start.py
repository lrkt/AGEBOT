from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold, hitalic

from app.keyboards.global_menu import build_global_menu


start_router = Router()


# Обробник для команди /start
@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    text = (
        f"👋 Приветствую, {hbold(message.from_user.full_name)}, в {hbold("\"Возраст бот\"")} - {hitalic("боте для определения знака по гороскопу, подсчета возраста, года рождения")}  и т.д. 🤖"
    )
    await message.answer(
        text=text
    )
    await load_replykeyboard(message)


async def load_replykeyboard(update: Message | CallbackQuery):
    keyboard = build_global_menu()
    print("Клавиатура загружена")
    if isinstance(update, Message):
        await update.answer(text="Выберите действие:", reply_markup=keyboard)
    elif isinstance(update, CallbackQuery):
        await update.message.answer(text="Выберите действие:", reply_markup=keyboard)

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.keyboards.global_menu import build_zodiac, build_chinese, build_angel, build_last_num
from app.data import age_actions, open_files
from app.forms.age import AgeForm, YearForm, ZodiacForm, CHYearForm, AngelForm, StatForm

main_router = Router()

last = None

async def edit_or_answer(message: Message, text: str, keyboard=None, *args, **kwargs):
   if message.from_user.is_bot:
       await message.edit_text(text=text, reply_markup=keyboard, **kwargs)
   else:
       await message.answer(text=text, reply_markup=keyboard, **kwargs)


@main_router.message(F.text == "Узнать возраст")
async def ask_date(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AgeForm.date)
    await edit_or_answer(
        message=message,
        text="Выберите опцию:",
        keyboard=build_last_num(last)
        )
    
@main_router.message(F.text == "Узнать возраст")
async def ask_date(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AgeForm.date)
    await edit_or_answer(
        message=message,
        text="Введите дату рождения в формате ДД.ММ.ГГГГ"
        )
 

@main_router.message(AgeForm.date)
async def age_count(message: Message, state: FSMContext):   
    if len(message.text.split('.')) == 3 and len(message.text.split('.')[-1]) == 4:
        last = message
        day, month, year = message.text.split('.')
        data = await state.update_data(day = day, month = month, year = year)
        await state.clear()
        msg = age_actions.age_calculator(data.get("day"), data.get("month"), data.get("year"))
        text = f"Возраст: {msg}."
    else:
        text = "Неверный формат, попробуйте снова."

    await edit_or_answer(
        message=message,
        text = text,
        last = last
    )

@main_router.message(F.text == "Полная сводка")
async def ask_stat(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(StatForm.date)
    await edit_or_answer(
        message=message,
        text="Введите дату рождения в формате ДД.ММ.ГГГГ"
    )

@main_router.message(StatForm.date)
async def full_stat(message: Message, state: FSMContext):
    if len(message.text.split('.')) == 3 and len(message.text.split('.')[-1]) == 4:
        day, month, year = message.text.split('.')
        date = message.text.replace(".", "")
        data = await state.update_data(date = date, day = day, month = month, year = year)
        await state.clear()
        age = age_actions.age_calculator(data.get("day"), data.get("month"), data.get("year"))
        zodiac = age_actions.zodiac_def(data.get("day"), data.get("month"))
        chsign = age_actions.ch_zodiac(data.get("year"))
        angel = age_actions.angel_def(data.get("date"))
        text = f"Возраст: {age}\nЗнак Зодиака: {zodiac}\nКитайский гороскоп: {chsign}\nЧисло ангела: {angel}."
    else:
        text = "Неверный формат, попробуйте снова."

    await edit_or_answer(
        message=message,
        text = text
    )

@main_router.message(F.text == "Узнать год рождения")
async def ask_date(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(YearForm.date)
    await edit_or_answer(
        message=message,
        text=f"Введите дату рождения и возраст через запятую.\n"
        "Пример: 10.10, 22"
        )
    
@main_router.message(YearForm.date)
async def year_count(message: Message, state: FSMContext):    
    date, age = message.text.split(', ')
    day, month = date.split('.')
    data = await state.update_data(day = day, month = month, age = age)
    await state.clear()
    msg = age_actions.year_calculator(data.get("day"), data.get("month"), data.get("age"))
    text = f"Год рождения: {msg}."
    await edit_or_answer(
        message=message,
        text = text
    )

@main_router.message(F.text == "Узнать знак Зодиака")
async def ask_date(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ZodiacForm.date)
    await edit_or_answer(
        message=message,
        text=f"Введите дату рождения в формате ДД.ММ"
        )

@main_router.message(ZodiacForm.date)
async def zodiac_def(message: Message, state = FSMContext):
    if len(message.text.split(".")) == 2:
        day, month = message.text.split(".")
        data = await state.update_data(day = day, month = month)
        await state.clear()
        msg = age_actions.zodiac_def(data.get("day"), data.get("month"))
        keyboard = build_zodiac(msg)

        await edit_or_answer(
        message=message,
        text=f"Знак Зодиака: {msg}.",
        keyboard = keyboard
    )
    else:  
        await edit_or_answer(
            message=message,
            text = "Неверный формат, попробуйте снова."
        )

@main_router.callback_query(F.data.startswith("define_zodiac_"))
async def zodiac_define_sign(call_back: CallbackQuery):
    sign = call_back.data.split("_")[-1]
    meaning = open_files.get_zodiac(sign)
    await edit_or_answer(
        message=call_back.message,
        text=meaning
    )
    
@main_router.message(F.text == "Узнать китайский гороскоп")
async def ask_date(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(CHYearForm.year)
    await edit_or_answer(
        message=message,
        text=f"Введите год рождения..."
        )

@main_router.message(CHYearForm.year)
async def zodiac_def(message: Message, state = FSMContext):
    data = await state.update_data(year = message.text)
    await state.clear()
    msg = age_actions.ch_zodiac(data.get("year"))
    keyboard = build_chinese(msg)
    await edit_or_answer(
        message=message,
        text=f"Китайский гороскоп: {msg}.",
        keyboard=keyboard
        )
    
@main_router.callback_query(F.data.startswith("define_chinese_"))
async def chinese_define_sign(call_back: CallbackQuery):
    sign = call_back.data.split("_")[-1]
    meaning = open_files.get_chinese(sign)
    await edit_or_answer(
        message=call_back.message,
        text=meaning
    )
    
@main_router.message(F.text == "Узнать число ангела")
async def ask_date(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AngelForm.date)
    await edit_or_answer(
        message=message,
        text="Введите дату рождения в формате ДД.ММ.ГГГГ"
        )
    
@main_router.message(AngelForm.date)
async def age_count(message: Message, state: FSMContext):    
    if len(message.text.split('.')) == 3 and len(message.text.split('.')[-1]) == 4:
        date = message.text.replace(".", "")
        data = await state.update_data(date = date)
        await state.clear()
        msg = age_actions.angel_def(data.get("date"))
        keyboard = build_angel(msg)

        await edit_or_answer(
        message=message,
        text = f"Число ангела: {msg}.",
        keyboard=keyboard
    )
    else:
        await edit_or_answer(
        message=message,
        text = "Неверный формат, попробуйте снова."
    )

@main_router.callback_query(F.data.startswith("define_angel_"))
async def angel_define_sign(call_back: CallbackQuery):
    num = call_back.data.split("_")[-1]
    meaning = open_files.get_angel(num)
    await edit_or_answer(
        message=call_back.message,
        text=meaning
    )
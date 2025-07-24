import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup


from app.keyboards.global_menu import build_zodiac, build_chinese, build_angel, build_cancel, build_stat, build_back, build_new, build_global_menu
from app.data import age_actions, open_files
from app.forms.age import AgeForm, YearForm, ZodiacForm, CHYearForm, AngelForm, StatForm
from app.routers.start import load_replykeyboard


main_router = Router()

COMMANDS = {}
STATES = [AgeForm.date.state, YearForm.date.state, ZodiacForm.date.state, CHYearForm.year.state, AngelForm.date.state, StatForm.date.state]

@main_router.message(lambda msg: msg.text in COMMANDS)
async def text_command_dispatcher(message: Message, state: FSMContext):
    handler = COMMANDS.get(message.text)
    if handler:
        print("Перехватчик сработал\n")
        await state.clear()
        await handler(message, state)
    else:
        return

async def edit_or_answer(message: Message, text: str, keyboard=None, *args, **kwargs):
   if message.from_user.is_bot:
       await message.edit_text(text=text, reply_markup=keyboard, **kwargs)
   else:
       await message.answer(text=text, reply_markup=keyboard, **kwargs)

@main_router.callback_query(F.data.startswith("cancel"))
async def cancel(call_back: CallbackQuery, state: FSMContext):
    await state.clear()
    await call_back.message.edit_text (
        message=call_back.message,
        text="Действие отменено ❌")
    await load_replykeyboard(call_back)
    

@main_router.callback_query(F.data.startswith("new_age"))
@main_router.message(F.text == "Узнать возраст 🔎")
async def ask_age_date(update: Message | CallbackQuery, state: FSMContext):
    if isinstance(update, Message):
        await state.clear()
        await state.set_state(AgeForm.date)
        await edit_or_answer(
            message=update,
            text="Введите дату рождения в формате ДД.ММ.ГГГГ",
            keyboard = build_cancel()
            )
    elif isinstance(update, CallbackQuery):
        await state.clear()
        await state.set_state(AgeForm.date)
        await update.message.edit_text(
            message=update,
            text="Введите дату рождения в формате ДД.ММ.ГГГГ",
            reply_markup = build_cancel()
            )


@main_router.message(AgeForm.date)
async def age_count(message: Message, state: FSMContext):   
    if age_actions.valid_fulldate(message.text):
        day, month, year = message.text.split('.')
        data = await state.update_data(day = day, month = month, year = year)
        await state.clear()
        msg = age_actions.age_calculator(data.get("day"), data.get("month"), data.get("year"))
        subj = "age"
        await edit_or_answer(
            message=message,
            text = f"Возраст: {msg}.",
            keyboard = build_new(subj)
        )
    else:
        await edit_or_answer(
            message=message,
            text = "Неверный формат, попробуйте снова."
        )

@main_router.callback_query(F.data.startswith("new_stat"))
@main_router.message(F.text == "Полная сводка 📋")
async def ask_stat(update: Message | CallbackQuery, state: FSMContext):
    if isinstance(update, Message):
        await state.clear()
        await state.set_state(StatForm.date)
        await edit_or_answer(
            message=update,
            text="Введите дату рождения в формате ДД.ММ.ГГГГ",
            keyboard = build_cancel()
            )
    elif isinstance(update, CallbackQuery):
        await state.clear()
        await state.set_state(StatForm.date)
        await update.message.edit_text(
            message=update,
            text="Введите дату рождения в формате ДД.ММ.ГГГГ",
            reply_markup = build_cancel()
            )

@main_router.callback_query(F.data.startswith("back_stat"))
@main_router.message(StatForm.date)
async def full_stat(update: Message | CallbackQuery, state: FSMContext):
    subj = "stat"
    if isinstance(update, Message):
        if age_actions.valid_fulldate(update.text):
            day, month, year = update.text.split('.')
            date = update.text.replace(".", "")
            data = await state.update_data(date = date, day = day, month = month, year = year)
            age = age_actions.age_calculator(data.get("day"), data.get("month"), data.get("year"))
            zodiac = age_actions.zodiac_def(data.get("day"), data.get("month"))
            chsign = age_actions.ch_zodiac(data.get("year"))
            angel = age_actions.angel_def(data.get("date"))
            text = f"Возраст: {age}\nЗнак Зодиака: {zodiac}\nКитайский гороскоп: {chsign}\nЧисло ангела: 😇 {angel}."
            keyboard1 = build_stat(zodiac, chsign, angel)
            keyboard2 = build_new(subj)
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1.inline_keyboard + keyboard2.inline_keyboard)
            await edit_or_answer(
                message=update,
                text = text,
                keyboard = keyboard
            )
        else:
            await edit_or_answer(
                message=update,
                text = "Неверный формат, попробуйте снова."
            )
    elif isinstance(update, CallbackQuery):
        data = await state.get_data()
        age = age_actions.age_calculator(data.get("day"), data.get("month"), data.get("year"))
        zodiac = age_actions.zodiac_def(data.get("day"), data.get("month"))
        chsign = age_actions.ch_zodiac(data.get("year"))
        angel = age_actions.angel_def(data.get("date"))
        text = f"Возраст: {age}\nЗнак Зодиака: {zodiac}\nКитайский гороскоп: {chsign}\nЧисло ангела: 😇 {angel}."
        keyboard1 = build_stat(zodiac, chsign, angel)
        keyboard2 = build_new(subj)
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1.inline_keyboard + keyboard2.inline_keyboard)
        await update.message.edit_text(
            message=update,
            text = text,
            reply_markup = keyboard
        )

@main_router.callback_query(F.data.startswith("new_year"))
@main_router.message(F.text == "Узнать год рождения 📅")
async def ask_year_date(update: Message | CallbackQuery, state: FSMContext):
    if isinstance(update, Message):
        await state.clear()
        await state.set_state(YearForm.date)
        await edit_or_answer(
            message=update,
            text="Введите дату рождения и возраст через запятую:\n"
            "ДД.ММ, возраст",
            keyboard = build_cancel()
            )
    elif isinstance(update, CallbackQuery):
        await state.clear()
        await state.set_state(YearForm.date)
        await update.message.edit_text(
            message=update,
            text=f"Введите дату рождения и возраст через запятую:\n"
            "ДД.ММ, возраст",
            reply_markup = build_cancel()
            )
    
@main_router.message(YearForm.date)
async def year_count(message: Message, state: FSMContext):
    if age_actions.valid_yeardate(message.text):
        subj = "year"    
        date, age = message.text.split(',')
        day, month = date.split('.')
        data = await state.update_data(day = day, month = month, age = age.strip())
        await state.clear()
        msg = age_actions.year_calculator(data.get("day"), data.get("month"), data.get("age"))
        text = f"Год рождения: {msg}."
        await edit_or_answer(
            message=message,
            text = text,
            keyboard = build_new(subj)
        )
    else:
        await edit_or_answer(
                message=message,
                text = "Неверный формат, попробуйте снова."
            )


@main_router.callback_query(F.data.startswith("new_zodiac"))
@main_router.message(F.text == "Узнать знак Зодиака 🔮")
async def ask_zodiac_date(update: Message | CallbackQuery, state: FSMContext):
    if isinstance(update, Message):
        await state.clear()
        await state.set_state(ZodiacForm.date)
        await edit_or_answer(
            message=update,
            text=f"Введите дату рождения в формате ДД.ММ",
            keyboard = build_cancel()
            )
    elif isinstance(update, CallbackQuery):
        await state.clear()
        await state.set_state(ZodiacForm.date)
        await update.message.edit_text(
            message=update,
            text=f"Введите дату рождения в формате ДД.ММ",
            reply_markup = build_cancel()
            )

@main_router.callback_query(F.data.startswith("back_zodiac"))
@main_router.message(ZodiacForm.date)
async def zodiac_def(update: Message | CallbackQuery, state = FSMContext):
    subj = "zodiac"
    if isinstance(update, Message):
        if age_actions.valid_shortdate(update.text):
            day, month = update.text.split(".")
            data = await state.update_data(day = day, month = month) 
            msg = age_actions.zodiac_def(data.get("day"), data.get("month"))
            keyboard1 = build_zodiac(msg)
            keyboard2 = build_new(subj)
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1.inline_keyboard + keyboard2.inline_keyboard)
            await edit_or_answer(
                message=update,
                text=f"Знак Зодиака: {msg}.",
                keyboard = keyboard
        )
        else:  
            await edit_or_answer(
                message=update,
                text = "Неверный формат, попробуйте снова."
            )
    elif isinstance(update, CallbackQuery):
        data = await state.get_data()
        msg = age_actions.zodiac_def(data.get("day"), data.get("month"))
        keyboard1 = build_zodiac(msg)
        keyboard2 = build_new(subj)
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1.inline_keyboard + keyboard2.inline_keyboard)
        await update.message.edit_text(
            message=update,
            text=f"Знак Зодиака: {msg}.",
            reply_markup = keyboard
        )

@main_router.callback_query(F.data.startswith("define_zodiac_"))
async def zodiac_define_sign(call_back: CallbackQuery, state: FSMContext):
    sign = call_back.data.split("_")[-1].split(" ")[-1]
    meaning = open_files.get_zodiac(sign)
    state_name = await state.get_state()
    if state_name == ZodiacForm.date.state:
        subj = "zodiac"
    elif state_name == StatForm.date.state:
        subj = "stat"
    await edit_or_answer(
        message=call_back.message,
        text=f"🔮 Значение знака Зодиака:\n\n{meaning}",
        keyboard = build_back(subj)
    )
    
@main_router.callback_query(F.data.startswith("new_china"))
@main_router.message(F.text == "Узнать китайский гороскоп 🐉")
async def ask_ch_date(update: Message | CallbackQuery, state: FSMContext):
    if isinstance(update, Message):
        await state.clear()
        await state.set_state(CHYearForm.year)
        await edit_or_answer(
            message=update,
            text=f"Введите год рождения...",
            keyboard = build_cancel()
            )
    elif isinstance(update, CallbackQuery):
        await state.clear()
        await state.set_state(CHYearForm.year)
        await update.message.edit_text(
            message=update,
            text=f"Введите год рождения...",
            reply_markup = build_cancel()
            )

@main_router.callback_query(F.data.startswith("back_china"))
@main_router.message(CHYearForm.year)
async def zodiac_def(update: Message | CallbackQuery, state = FSMContext):
    subj = "china"
    if isinstance(update, Message):
        if update.text.isdigit():
            data = await state.update_data(year = update.text)
            msg = age_actions.ch_zodiac(data.get("year"))
            keyboard1 = build_chinese(msg)
            keyboard2 = build_new(subj)
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1.inline_keyboard + keyboard2.inline_keyboard)
            await edit_or_answer(
                message=update,
                text=f"Китайский гороскоп: {msg}.",
                keyboard=keyboard
                )
        else:
            await edit_or_answer(
                message=update,
                text = "Неверный формат, попробуйте снова."
            )
    elif isinstance(update, CallbackQuery):
        data = await state.get_data()
        msg = age_actions.ch_zodiac(data.get("year"))
        keyboard1 = build_chinese(msg)
        keyboard2 = build_new(subj)
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1.inline_keyboard + keyboard2.inline_keyboard)
        await update.message.edit_text(
            message=update,
            text = f"Китайский гороскоп: {msg}.",
            reply_markup = keyboard
        )

@main_router.callback_query(F.data.startswith("define_chinese_"))
async def chinese_define_sign(call_back: CallbackQuery, state = FSMContext):
    sign = call_back.data.split("_")[-1].split(" ")[-1]
    meaning = open_files.get_chinese(sign)
    state_name = await state.get_state()
    if state_name == CHYearForm.year.state:
        subj = "china"
    elif state_name == StatForm.date.state:
        subj = "stat"
    await edit_or_answer(
        message=call_back.message,
        text=f"🐉 Значение Восточного знака:\n\n{meaning}",
        keyboard = build_back(subj)
    )

@main_router.callback_query(F.data.startswith("new_angel"))
@main_router.message(F.text == "Узнать число ангела 😇")
async def ask_angel_date(update: Message | CallbackQuery, state: FSMContext):
    if isinstance(update, Message):
        await state.clear()
        await state.set_state(AngelForm.date)
        await edit_or_answer(
            message=update,
            text="Введите дату рождения в формате ДД.ММ.ГГГГ",
            keyboard = build_cancel()
            )
    elif isinstance(update, CallbackQuery):
        await state.clear()
        await state.set_state(AngelForm.date)
        await update.message.edit_text(
            message=update,
            text="Введите дату рождения в формате ДД.ММ.ГГГГ",
            reply_markup = build_cancel()
            )

@main_router.callback_query(F.data.startswith("back_angel"))
@main_router.message(AngelForm.date)
async def age_count(update: Message | CallbackQuery, state: FSMContext):
    subj = "angel"  
    if isinstance(update, Message):
        if age_actions.valid_fulldate(update.text):
            date = update.text.replace(".", "")
            data = await state.update_data(date = date)
            msg = age_actions.angel_def(data.get("date"))
            keyboard1 = build_angel(msg)
            keyboard2 = build_new(subj)
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1.inline_keyboard + keyboard2.inline_keyboard)
            await edit_or_answer(
                message=update,
                text = f"😇 Число ангела: {msg}.",
                keyboard=keyboard
        )
        else:
            await edit_or_answer(
            message=update,
            text = "Неверный формат, попробуйте снова."
        )
    elif isinstance(update, CallbackQuery):
        data = await state.get_data()
        msg = age_actions.angel_def(data.get("date"))
        keyboard1 = build_angel(msg)
        keyboard2 = build_new(subj)
        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard1.inline_keyboard + keyboard2.inline_keyboard)
        await update.message.edit_text(
            message=update,
            text = f"😇 Число ангела: {msg}.",
            reply_markup = keyboard
        )

@main_router.callback_query(F.data.startswith("define_angel_"))
async def angel_define_sign(call_back: CallbackQuery, state: FSMContext):
    num = call_back.data.split("_")[-1]
    meaning = open_files.get_angel(num)
    state_name = await state.get_state()
    if state_name == AngelForm.date.state:
        subj = "angel"
    elif state_name == StatForm.date.state:
        subj = "stat"
    await edit_or_answer(
        message=call_back.message,
        text=f"😇 Значение числа ангела:\n\n{meaning}\n\nЧисло ангела — это число, полученное из твоей даты рождения, которое считается твоим личным духовным знаком. Чтобы его узнать, нужно сложить все цифры своей даты рождения до одного числа. Например,  → 2+0+0+3+0+7+2+0 = 14 → 1+4 = 5 = 555. Это число будто несёт послание от ангелов или вселенной, помогает понять себя и даёт советы.",
        keyboard = build_back(subj)
    )

@main_router.message() 
async def catch(message: Message):
    keyboard = False
    if "умеешь" in message.text.lower():
        text = "Ну да умею"
    elif "привет" in message.text.lower():
        text = "Привет"
    elif "?" in message.text:
        text = "По всем вопросам пишите сюда: @tg_post_suggest_bot"
    elif any(word in message.text.lower() for word in open_files.bad_words):
        texts = ["1 мат - 80 лет в аду", "Сообщение содержит недопустимую лексику."]
        text = random.choice(texts)
    else:
        texts = [
        "❗️ Сообщение не распознано, воспользуйтесь панелью снизу.",
        "❗️ Неизвестный формат.",
        "Марина хватит писать фигню"
        ]
        text = random.choice(texts)
        if text != texts[-1]:
            keyboard = True
    await message.answer(text)
    if keyboard:
        await load_replykeyboard(message)

COMMANDS["Полная сводка 📋"] = ask_stat
COMMANDS["Узнать возраст 🔎"] = ask_age_date
COMMANDS["Узнать год рождения 📅"] = ask_year_date
COMMANDS["Узнать знак Зодиака 🔮"] = ask_zodiac_date
COMMANDS["Узнать китайский гороскоп 🐉"] = ask_ch_date
COMMANDS["Узнать число ангела 😇"] = ask_angel_date
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder



def build_global_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Полная сводка 📋")
    builder.button(text="Узнать возраст 🔎")
    builder.button(text="Узнать год рождения 📅")
    builder.button(text="Узнать знак Зодиака 🔮")
    builder.button(text="Узнать китайский гороскоп 🐉")
    builder.button(text="Узнать число ангела 😇")
    builder.adjust(2)
    return builder.as_markup()

def build_zodiac(sign):
    builder = InlineKeyboardBuilder()
    builder.button(text="Значение моего знака 🔎", callback_data=f"define_zodiac_{sign}")
    builder.adjust(1)
    return builder.as_markup()

def build_chinese(sign):
    builder = InlineKeyboardBuilder()
    builder.button(text="Значение моего знака 🔎", callback_data=f"define_chinese_{sign}")
    builder.adjust(1)
    return builder.as_markup()

def build_angel(num):
    builder = InlineKeyboardBuilder()
    builder.button(text="Значение моего числа 🔎", callback_data=f"define_angel_{num}")
    builder.adjust(1)
    return builder.as_markup()

def build_stat(z, ch, num):
    builder = InlineKeyboardBuilder()
    builder.button(text="Значение знака Зодиака 🔮", callback_data=f"define_zodiac_{z}")
    builder.button(text="Значение Восточного знака 🐉", callback_data=f"define_chinese_{ch}")
    builder.button(text="Значение числа ангела 😇", callback_data=f"define_angel_{num}")
    builder.adjust(1)
    return builder.as_markup()

def build_cancel():
    builder = InlineKeyboardBuilder()
    builder.button(text="Отмена ❌", callback_data=f"cancel")
    builder.adjust(1)
    return builder.as_markup()

def build_back(subj):
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад ⬅️", callback_data=f"back_{subj}")
    return builder.as_markup()

def build_new(subj):
    builder = InlineKeyboardBuilder()
    builder.button(text="Другая дата ✏️", callback_data=f"new_{subj}")
    return builder.as_markup()
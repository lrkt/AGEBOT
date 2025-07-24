from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_global_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Полная сводка")
    builder.button(text="Узнать возраст")
    builder.button(text="Узнать год рождения")
    builder.button(text="Узнать знак Зодиака")
    builder.button(text="Узнать китайский гороскоп")
    builder.button(text="Узнать число ангела")
    builder.adjust(1)
    return builder.as_markup()

def build_zodiac(sign):
    builder = InlineKeyboardBuilder()
    builder.button(text="Значение моего знака", callback_data=f"define_zodiac_{sign}")
    builder.adjust(1)
    return builder.as_markup()

def build_chinese(sign):
    builder = InlineKeyboardBuilder()
    builder.button(text="Значение моего знака", callback_data=f"define_chinese_{sign}")
    builder.adjust(1)
    return builder.as_markup()

def build_angel(num):
    builder = InlineKeyboardBuilder()
    builder.button(text="Значение моего числа", callback_data=f"define_angel_{num}")
    builder.adjust(1)
    return builder.as_markup()

def build_last_num(last):
    builder = InlineKeyboardBuilder()
    builder.button(text="Новая дата", callback_data=f"new_date")
    builder.button(text=f"Использовать последнюю дату({last})", callback_data=f"last_date")
    builder.adjust(1)
    return builder.as_markup()
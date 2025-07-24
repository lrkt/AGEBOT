from aiogram.fsm.state import State, StatesGroup


class AgeForm(StatesGroup):
   date = State()
   day = State()
   month = State()
   year = State()

class YearForm(StatesGroup):
   date = State()
   day = State()
   month = State()
   age = State()

class ZodiacForm(StatesGroup):
   date = State()
   day = State()
   month = State()

class CHYearForm(StatesGroup):
   year = State()

class AngelForm(StatesGroup):
   date = State()
   day = State()
   month = State()
   year = State()

class StatForm(StatesGroup):
   date = State()
   day = State()
   month = State()
   year = State()
from aiogram.fsm.state import State, StatesGroup


class AddTransaction(StatesGroup):
    amount = State()
    type = State()
    category = State()
    note = State()


class CategoryForm(StatesGroup):
    type = State()
    name = State()


class LimitForm(StatesGroup):
    amount = State()

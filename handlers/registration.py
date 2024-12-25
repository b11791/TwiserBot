import asyncio
import traceback

import aiogram
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import sql_queries
from db import SQLite
from filters.register_check import UnregisterCheckFilter
from handlers.menu import kb_menu

registration_router = Router()

class Reg(StatesGroup):
    name = State()
    age = State()

kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="Зарегистрироваться")],
    ],
)

@registration_router.message(UnregisterCheckFilter(), aiogram.F.text == "Зарегистрироваться")
async def reg1(message: aiogram.types.Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer("Введите своё имя")


@registration_router.message(Reg.name)
async def reg2(message: aiogram.types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.age)
    await message.answer("Введите ваш возраст")


@registration_router.message(Reg.age)
async def reg3(message: aiogram.types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом")
        return
    await state.update_data(age=message.text)
    data = await state.get_data()
    await state.clear()
    try:
        with SQLite() as db:
            db.cursor.execute(sql_queries.insert_user.format(
                message.from_user.id,
                message.from_user.username,
                data["age"],
                data["name"]
            ))
            db.connection.commit()
    except Exception as e:
        await message.answer("Произошла ошибка, попробуйте снова")
        print(e)
    else:
        await message.answer("Вы зарегестрировались", reply_markup=kb_menu)

@registration_router.message(UnregisterCheckFilter())
async def register_handler(message: aiogram.types.Message):
    await message.answer("Зарегистрируйтесь", reply_markup=kb)

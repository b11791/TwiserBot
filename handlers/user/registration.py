import aiogram
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import sql_queries
from db import SQLite
from filters.register_check import UnregisterCheckFilter, BlockedCheckFilter
from handlers.user.menu import kb_menu

registration_router = Router()

class Reg(StatesGroup):
    name = State()
    age = State()
    ref_id = State()

kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="Зарегистрироваться")],
    ],
)
kb_2 = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="Нет реферала")],
    ],
)


@registration_router.message(BlockedCheckFilter())
async def reg1(message: aiogram.types.Message, state: FSMContext):
    await message.answer("Иди нахуй")


@registration_router.message(UnregisterCheckFilter(), aiogram.F.text == "Зарегистрироваться")
async def reg1(message: aiogram.types.Message, state: FSMContext):
    with SQLite() as db:
        reg_status = db.cursor.execute(sql_queries.select_reg).fetchone()

    if not reg_status[0]:
        await message.answer("Хуй соси")
        return
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
    await state.set_state(Reg.ref_id)
    await message.answer("Введите реферал или нажмите на кнопку", reply_markup=kb_2)


@registration_router.message(Reg.ref_id)
async def reg4(message: aiogram.types.Message, state: FSMContext):
    ref_id = message.text

    if ref_id != "Нет реферала":
        with SQLite() as db:
            exist = db.cursor.execute(sql_queries.select_user_by_tg_id.format(ref_id)).fetchone()
        if not exist:
            await message.answer("Такого пользователя нет")
            return
    else:
        ref_id = "NULL"

    data = await state.get_data()
    await state.clear()
    try:
        with SQLite() as db:
            db.cursor.execute(sql_queries.insert_user.format(
                message.from_user.id,
                message.from_user.username,
                data["age"],
                data["name"],
                ref_id,
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

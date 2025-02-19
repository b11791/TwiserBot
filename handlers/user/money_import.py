import aiogram
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import sql_queries
from db import SQLite

money_router = Router()

class Import(StatesGroup):
    summ = State()


@money_router.message(aiogram.F.text == "Ввод")
async def create_tables(message: aiogram.types.Message, state: FSMContext):
    await message.answer("Введите сумму которую хотите ввести")
    await state.set_state(Import.summ)

@money_router.message(Import.summ)
async def create_tables(message: aiogram.types.Message, state: FSMContext):
    summ = message.text
    if not message.text.isdigit():
        await message.answer("Сумма ввода должна быть числом")
        return
    await state.clear()

    with SQLite() as db:
        db.cursor.execute(sql_queries.increase_balance.format(
            summ,
            message.from_user.username,
        ))
        balance = db.cursor.execute(sql_queries.select_user_balance.format(message.from_user.id)).fetchone()[0] or 0
        db.connection.commit()

    await message.answer(f"Вы успешно пополнили баланс\n<b>Текущий баланс: {balance}</b>", parse_mode="html")
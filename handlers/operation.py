import aiogram
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import sql_queries
from db import SQLite

operation_router = Router()

class Transgender(StatesGroup):
    name = State()
    amount = State()


@operation_router.message(aiogram.F.text == "Перевод")
async def create_tables(message: aiogram.types.Message, state: FSMContext):
    await message.answer(f"Введите логин пользователя, которому хотите перевести")
    await state.set_state(Transgender.name)


@operation_router.message(Transgender.name)
async def create_tables(message: aiogram.types.Message, state: FSMContext):
    name = message.text
    with SQLite() as db:
        exist = db.cursor.execute(sql_queries.select_user_by_username.format(name)).fetchone()
    if not exist:
        await message.answer("Такого пользователя нет")
        return

    await state.update_data(name=name)
    await state.set_state(Transgender.amount)
    with SQLite() as db:
        balance = db.cursor.execute(sql_queries.select_user_balance.format(message.from_user.id)).fetchone()[0] or 0
    await message.answer(
        f"Введите сумму, которую хотите перевести пользователю <b>{name}</b>\nТекущий баланс: <b>{balance}</b>",
        parse_mode="html",
    )


@operation_router.message(Transgender.amount)
async def create_tables(message: aiogram.types.Message, state: FSMContext):
    amount = message.text
    if not message.text.isdigit():
        await message.answer("Сумма перевода должна быть числом")
        return

    with SQLite() as db:
        balance = db.cursor.execute(sql_queries.select_user_balance.format(message.from_user.id)).fetchone()[0] or 0
    if balance < int(amount):
        await message.answer(
            f"У вас не хватает денег для перевода \n <b>Текущий баланс: {balance}</b> \n <b>Сумма перевода: {amount}</b>",
            parse_mode="html",
        )
        return
    await state.update_data(amount=amount)

    data = await state.get_data()
    await state.clear()
    perevod = int(data["amount"]) - ((int(data["amount"]) / 100) * 30)
    with SQLite() as db:
        db.cursor.execute(sql_queries.increase_balance.format(
            perevod,
            data["name"],
        ))
        db.cursor.execute(sql_queries.decrease_balance.format(
            data["amount"],
            message.from_user.username,
        ))
        db.connection.commit()

    with SQLite() as db:
        balance = db.cursor.execute(sql_queries.select_user_balance.format(message.from_user.id)).fetchone()[0] or 0

    await message.answer(
        f"Вы перевели <b>{amount}</b> (комиссия 30%) пользователю <b>{data['name']}</b>\nТекущий баланс: <b>{balance}</b>",
        parse_mode="html",
    )
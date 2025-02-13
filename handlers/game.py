import asyncio
import random

import aiogram
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import sql_queries
from db import SQLite

game_router = Router()


class Game(StatesGroup):
    stavka = State()
    user_value = State()


@game_router.message(aiogram.F.text == "Играть")
async def roll_dice(message, state: FSMContext):
    await message.answer("Ваша ставка:")
    await state.set_state(Game.stavka)


@game_router.message(Game.stavka)
async def roll_dice(message, state: FSMContext):
    stavka = message.text
    if not message.text.isdigit():
        await message.answer("Ставка должна быть числом")
        return
    await state.update_data(stavka=int(stavka))

    with SQLite() as db:
        balance = db.cursor.execute(sql_queries.select_user_balance.format(message.from_user.id)).fetchone()[0] or 0
        await state.update_data(balance=balance)
    if balance < int(stavka):
        await message.answer(
            f"У вас не хватает денег для перевода \n <b>Текущий баланс: {balance}</b> \n <b>Ставка: {stavka}</b>",
            parse_mode="html",
        )
        await state.clear()
        return

    stav1 = await message.answer_dice(emoji="🎲")
    stav1_value = stav1.dice.value
    await state.update_data(bot_value=int(stav1_value))
    await asyncio.sleep(3)
    await message.answer("Кидайте кубик")
    await state.set_state(Game.user_value)


@game_router.message(Game.user_value)
async def roll_dice(message, state: FSMContext):
    try:
        stav2 = int(message.dice.value)
    except (AttributeError, ValueError):
        await message.answer("Произошла ошибка, киньте кубик снова")
        return

    data = await state.get_data()
    await state.clear()
    await asyncio.sleep(3)

    if data["bot_value"] > stav2:
        new_balance = data['balance'] - data['stavka']
        await message.answer(
            f"Вы проиграли :( \n",
            parse_mode="html",
        )
    elif data["bot_value"] < stav2:
        new_balance = data['balance'] + data['stavka']
        await message.answer(
            f"ВЫ ПОБЕДИЛИ!!!! :D \n",
            parse_mode="html",
        )
    else:
        new_balance = data['balance']
        await message.answer("Ничья")

    with SQLite() as db:
        db.cursor.execute(sql_queries.set_balance.format(
            new_balance,
            message.from_user.username,
        ))
        db.connection.commit()

    await message.answer(
        f"<b>Текущий баланс: {new_balance}</b>",
        parse_mode="html",
    )

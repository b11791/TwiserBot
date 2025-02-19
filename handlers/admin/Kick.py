import aiogram
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import sql_queries
from db import SQLite
from filters.register_check import AdminCheckFilter

kick_router = Router()

class Kick(StatesGroup):
    username = State()

@kick_router.message(AdminCheckFilter(), aiogram.F.text == "Кикнуть пользователя")
async def create_tables(message: aiogram.types.Message, state: FSMContext):
    with SQLite() as db:
        users = db.cursor.execute(sql_queries.select_all_users).fetchall()

    top_referals_str = "\n".join(f"<i>{row['username']}</i> - {row['name']} - {row['tg_id']}" for row in users)
    await message.answer(f"<b>         Пользователи:</b>\n <b>USERNAME | NAME | ID</b>\n\n{top_referals_str}", parse_mode="html")
    await message.answer(f"Введите username пользователя, которого нужно кикнуть")
    await state.set_state(Kick.username)


@kick_router.message(Kick.username)
async def create_tables(message: aiogram.types.Message, state: FSMContext):
    name = message.text
    with SQLite() as db:
        exist = db.cursor.execute(sql_queries.select_user_by_username.format(name)).fetchone()
    if not exist:
        await message.answer("Такого пользователя нет")
        return

    await state.update_data(username=name)
    data = await state.get_data()
    await state.clear()

    with SQLite() as db:
        db.cursor.execute(sql_queries.block_user.format(data["username"]))

        db.connection.commit()
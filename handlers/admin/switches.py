import aiogram
from aiogram import Router

import sql_queries
from db import SQLite
from filters.register_check import AdminCheckFilter
from handlers.admin.menu import get_kb_menu

switches_router = Router()


@switches_router.message(AdminCheckFilter(), aiogram.F.text.in_(("Регистрация 🟢", "Регистрация 🔴")))
async def switch_registration_handler(message):
    with SQLite() as db:
        reg_status = db.cursor.execute(sql_queries.select_reg).fetchone()

        if reg_status[0]:
            db.cursor.execute(sql_queries.reg_off)
        else:
            db.cursor.execute(sql_queries.reg_on)

        db.connection.commit()

    await message.answer(text="Админ Меню", reply_markup=get_kb_menu())


@switches_router.message(AdminCheckFilter(), aiogram.F.text.in_(("Игра 🟢", "Игра 🔴")))
async def switch_game_handler(message):
    with SQLite() as db:
        game_status = db.cursor.execute(sql_queries.select_game).fetchone()

        if game_status[0]:
            db.cursor.execute(sql_queries.game_off)
        else:
            db.cursor.execute(sql_queries.game_on)

        db.connection.commit()

    await message.answer(text="Админ Меню", reply_markup=get_kb_menu())

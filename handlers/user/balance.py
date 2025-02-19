import aiogram
from aiogram import Router

import sql_queries
from db import SQLite

balance_router = Router()


@balance_router.message(aiogram.F.text == "Баланс")
async def create_tables(message):
    with SQLite() as db:
        balance = db.cursor.execute(sql_queries.select_user_balance.format(message.from_user.id)).fetchone()[0] or 0
    await message.answer(f"<b>Текущий баланс: {balance}</b>", parse_mode="html")


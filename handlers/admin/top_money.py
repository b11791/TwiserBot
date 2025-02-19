import aiogram
from aiogram import Router

import sql_queries
from db import SQLite

top_money_router = Router()


@top_money_router.message(aiogram.F.text == "Топ пользователей по выигрышам")
async def create_tables(message):
    with SQLite() as db:
        top_money_users = db.cursor.execute(sql_queries.select_top_money_users).fetchall()

    top_referals_str = "\n".join(f"<i>{row['username']}</i> - {row['balance']}" for row in top_money_users)
    await message.answer(f"<b>         Пользователи:</b>\n <b>USERNAME | NAME | ID</b>\n\n{top_referals_str}", parse_mode="html")

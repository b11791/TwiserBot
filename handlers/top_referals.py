import aiogram
from aiogram import Router

import sql_queries
from db import SQLite

referal_router = Router()


@referal_router.message(aiogram.F.text == "Топ игроков")
async def create_tables(message):
    with SQLite() as db:
        top_referals = db.cursor.execute(sql_queries.select_top_referals).fetchall()

    top_referals_str = "\n".join(f"<i>{row['username']}</i> - {row['ref_count']}" for row in top_referals)
    await message.answer(f"<b>Топ пользователей по рефералам:</b>\n\n{top_referals_str}", parse_mode="html")

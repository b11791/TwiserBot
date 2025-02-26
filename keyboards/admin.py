from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import sql_queries
from db import SQLite
from funcs import design_buttons


def get_kb_menu() -> ReplyKeyboardMarkup:

    with SQLite() as db:
        reg_status = db.cursor.execute(sql_queries.select_reg).fetchone()
        game_status = db.cursor.execute(sql_queries.select_game).fetchone()
    kb_menu = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=design_buttons([
            KeyboardButton(text="Топ пользователей по выигрышам"),
            KeyboardButton(text="Кикнуть пользователя"),
            KeyboardButton(text=f"Регистрация {'🟢' if reg_status[0] else '🔴' }"),
            KeyboardButton(text=f"Игра {'🟢' if game_status[0] else '🔴' }"),
        ], 2),
    )

    return kb_menu
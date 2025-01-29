from aiogram.filters import BaseFilter
from aiogram.types import Message

import sql_queries
from db import SQLite


class UnregisterCheckFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        with SQLite() as db:
            result = db.cursor.execute(
                sql_queries.select_user_by_tg_id.format(message.from_user.id)
            ).fetchall()
        if not result:
            return True
        return False
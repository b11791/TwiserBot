import asyncio

import aiogram

import sql_queries
from create_bot import bot, config
from db import SQLite
from handlers.registration import registration_router

dp = aiogram.Dispatcher()

dp.include_routers(
    registration_router
)

async def create_tables():
    with SQLite() as db:
        db.cursor.execute(sql_queries.create_table_user)
        db.cursor.execute(sql_queries.create_table_move)
        db.cursor.execute(sql_queries.create_super_user.format(config["ADMIN_TG_ID"], config["ADMIN_USER_NAME"]))
        db.connection.commit()
    print("База данных настроена")


@dp.startup()
async def start():
    await create_tables()
    print("Бот запущен. ИДИТЕ НАХУЙ!")


# @random_router.message(Command("go_joke"))
# async def joke(message: aiogram.types.Message):
#
#     await message.answer(text='', reply_markup=kb_2)


if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
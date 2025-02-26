import asyncio

import aiogram

import sql_queries
from create_bot import bot
from db import SQLite
from handlers.admin.Kick import kick_router
from handlers.admin.switches import switches_router
from handlers.admin.top_money import top_money_router
from handlers.user.balance import balance_router
from handlers.user.game import game_router
from handlers.user.menu import menu_router
from handlers.user.money_import import money_router
from handlers.user.operation import operation_router
from handlers.user.registration import registration_router
from handlers.user.top_referals import referal_router
from handlers.admin.menu import admin_menu_router

dp = aiogram.Dispatcher()


dp.include_routers(
    switches_router,
    admin_menu_router,
    registration_router,
    kick_router,
    menu_router,
    balance_router,
    referal_router,
    operation_router,
    money_router,
    game_router,
    top_money_router,
)


async def create_tables():
    with SQLite() as db:
        db.cursor.execute(sql_queries.create_table_user)
        db.cursor.execute(sql_queries.create_table_switches)
        db.cursor.execute(sql_queries.insert_registration_parameter)
        db.cursor.execute(sql_queries.insert_game_parameter)
        # db.cursor.execute(sql_queries.create_super_user.format(config["ADMIN_TG_ID"], config["ADMIN_USER_NAME"]))
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

import aiogram
from aiogram import Router

from filters.register_check import AdminCheckFilter
from keyboards.admin import get_kb_menu

admin_menu_router = Router()


@admin_menu_router.message(AdminCheckFilter(), aiogram.F.text == "/start")
async def menu(message):
    await message.answer(text="Админ Меню", reply_markup=get_kb_menu())

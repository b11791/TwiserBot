import aiogram
from aiogram import Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from filters.register_check import AdminCheckFilter
from funcs import design_buttons

admin_menu_router = Router()


kb_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=design_buttons([
        KeyboardButton(text="Топ пользователей по выигрышам"),
        KeyboardButton(text="Кикнуть пользователя")
    ], 2),
)


@admin_menu_router.message(AdminCheckFilter(), aiogram.F.text == "/start")
async def menu(message):
    print("Хуй")
    await message.answer(text="Админ Меню", reply_markup=kb_menu)

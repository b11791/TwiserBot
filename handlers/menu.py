import aiogram
from aiogram import Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from funcs import design_buttons

menu_router = Router()

kb_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=design_buttons([
        KeyboardButton(text="Заработать"),
        KeyboardButton(text="Играть"),
        KeyboardButton(text="Баланс"),
        KeyboardButton(text="Топ игроков"),
        KeyboardButton(text="Перевод"),
        KeyboardButton(text="Ввод")
    ], 2),
)

@menu_router.message(aiogram.F.text == "Меню")
async def menu(message):
    await message.answer(show_alert=True, text="Меню", reply_markup=kb_menu)

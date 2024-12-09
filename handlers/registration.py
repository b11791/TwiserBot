import asyncio

import aiogram
from aiogram import Router
from aiogram.fsm.state import StatesGroup, State

import sql_queries
from db import SQLite

registration_router = Router()

class Reg(StatesGroup):
    name = State()
    age = State()


@registration_router.message()
async def reg1(message: aiogram.types.Message):
    await message.answer("Введите с")
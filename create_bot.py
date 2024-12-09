import aiogram
from dotenv import dotenv_values

config = dotenv_values('.env')
bot = aiogram.Bot(config['TOKEN'])

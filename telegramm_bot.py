
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from main import main_f
import time


storage = MemoryStorage()
TOKEN = '6149034262:AAGo_Smp-Z1SbP0Nco15qc_ulucaqHETTRU'
email = "timur.shurak@gmail.com"
psw = "4xUs96YJ5d4vRHD"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
status = True
control_buttons = ["Start", "Stop"]
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(*control_buttons)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer("Hello it's working....", reply_markup=keyboard)


@dp.message_handler(Text(equals='Start'))
async def start_checking(message: types.Message):
    await message.answer('Checking...', reply_markup=keyboard)
    while True:
        if main_f(email, psw):
            await message.answer('Notif')
        time.sleep(5)


if __name__ == '__main__':
    executor.start_polling(dp)

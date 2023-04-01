
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from main import main_f
import time


storage = MemoryStorage()
TOKEN = '5897389295:AAGgjx51OtNn4oT0PoC63re8OnQWQ80m8aw'
email = "timur.shurak@gmail.com"
psw = "4xUs96YJ5d4vRHD"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
status = True
control_buttons = ["Start"]
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(*control_buttons)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer("Hello it's working....", reply_markup=keyboard)


@dp.message_handler(Text(equals='Start'))
async def start_checking(message: types.Message):
    await message.answer('Checking...')
    while True:
        f = main_f(email, psw)
        if f[0]:
            for i in f[1]:
                await message.answer(f'https://www.excapper.com/?action=game&id={i}')
        time.sleep(5)


if __name__ == '__main__':
    executor.start_polling(dp)

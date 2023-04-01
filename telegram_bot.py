import asyncio

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
keyboard_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_start.add(*['Start'])
keyboard_stop = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_stop.add(*['Stop'])


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer("Hello it's working....", reply_markup=keyboard_start)


@dp.message_handler(Text(equals='Start'))
async def start_checking(message: types.Message):
    control_buttons = ["Stop"]
    await message.answer('Checking...', reply_markup=keyboard_stop)
    global status
    status = True
    while status:
        f = await main_f(email, psw)
        print(1)
        if f[0]:
            for i in f[1]:
                await message.answer(f'https://www.excapper.com/?action=game&id={i}')
        await asyncio.sleep(5)


@dp.message_handler(Text(equals='Stop'))
async def stop(message: types.Message):
    global status
    status = False
    print('Stopped')
    await message.answer('its stopped', reply_markup=keyboard_start)


if __name__ == '__main__':
    asyncio.run(executor.start_polling(dp))

import os

from aiogram import Bot, Dispatcher, executor, types

bot = Bot('6126472660:AAEM_qLOIT2D--wsLB07YCvqXsgDamJayI4')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """способы отправить сообщение пользователю"""
    # await bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}\nВон все мои кнопки:')
    # await message.reply(f'Привет, {message.from_user.first_name}\nВон все мои кнопки:')

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('открыть яндекс', url='https://yandex.ru')
    btn2 = types.InlineKeyboardButton('отправить картинку', callback_data='photo')
    markup.add(btn1, btn2)
    await message.answer(f'Привет, {message.from_user.first_name}\nВон все мои кнопки:', reply_markup=markup)


@dp.callback_query_handler()
async def button_functions(callback):
    if callback.data == 'photo':
        file = open('cold.png', 'rb')
        await callback.message.answer_photo(file)


executor.start_polling(dp)

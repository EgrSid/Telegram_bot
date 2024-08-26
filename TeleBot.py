import telebot
from telebot import types
import sqlite3
import requests
import json
from currency_converter import CurrencyConverter
from datetime import datetime
from pycbrf import ExchangeRates
import webbrowser

name = None
amount = 0

bot = telebot.TeleBot('6126472660:AAEM_qLOIT2D--wsLB07YCvqXsgDamJayI4')
API = '16cc4de27418e1dd3146973a27a88df7'
currency = CurrencyConverter()

"""ВВОД ИМЕНИ ПОЛЬЗОВАТЕЛЯ"""


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Enter password: ')
    bot.register_next_step_handler(message, user_password)


"""ВВОД ПАРОЛЯ ПОЛЬЗОВАТЕЛЯ + ПОКАЗАТЬ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ"""


def user_password(message):
    password = message.text.strip()

    conn = sqlite3.connect('TeleBot.sql')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Send all users', callback_data='users')
    markup.row(btn1)
    bot.send_message(message.chat.id, 'User is registered!', reply_markup=markup)


def get_weather(message):
    city = message.text.strip()
    city1 = city.lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city1}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Сейчас температура в городе {city} {int(round(temp, 0))} градусов Цельсия')
        if temp <= 10:
            image = 'cold.png'
        elif 10 < temp <= 23:
            image = 'normal_temperature.png'
        elif temp > 23:
            image = 'high_temperature.png'
        file = open('./' + image, "rb")
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, 'Название города введено некорректно! Введите город повторно:')
        bot.register_next_step_handler(message, get_weather)


def converter(message):
    global amount
    try:
        amount = int(message.text.strip())
    except:
        bot.reply_to(message, 'Введено некорректное значение. Повторите попытку: ')
        bot.register_next_step_handler(message, converter)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('EUR-->USD', callback_data='EUR/USD')
        btn2 = types.InlineKeyboardButton('USD-->EUR', callback_data='USD/EUR')
        btn3 = types.InlineKeyboardButton('Другое значение(с рублем не работает!)', callback_data='else')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, 'Выберите конвертируемые валюты: ', reply_markup=markup)
    else:
        bot.reply_to(message, 'Значение должно быть больше 0. Повторите попытку: ')
        bot.register_next_step_handler(message, converter)


def my_currency(message):
    global amount
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Результат конвертации: {round(res, 2)}')
    except:
        bot.send_message(message.chat.id, 'Введено некорректное значение. Повторите попытку: ')
        bot.register_next_step_handler(message, my_currency)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hi! Enter username:')

    conn = sqlite3.connect('TeleBot.sql')
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS \
        users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.register_next_step_handler(message, user_name)


"""ВЫВОД ИМЕНИ ПОЛЬЗОВАТЕЛЯ(как он записан в самом телеграмме)"""


@bot.message_handler(commands=['call_my_name'])
def call_my_name(message):
    bot.reply_to(message, message.from_user.first_name)


@bot.message_handler(commands=['convert_currency'])
def convert_currency(message):
    bot.send_message(message.chat.id, 'Введите сумму, которую желаете перевести:')
    bot.register_next_step_handler(message, converter)

@bot.message_handler(commands=['conv_cur_to_rub'])
def rub(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('юани в рубли', callback_data='rub')
    markup.add(btn1)
    bot.send_message(message.chat.id, 'перевод в рубли', reply_markup=markup)


"""ПОКАЗЫВАЕТ ВСЕ КНОПКИ БОТА"""


@bot.message_handler(commands=['buttons'])
def buttons(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('open goo', url='http://www.google.com')
    btn2 = types.InlineKeyboardButton('delete prev mes', callback_data='delete')
    btn3 = types.InlineKeyboardButton('weather', callback_data='weather')
    btn4 = types.InlineKeyboardButton('Секретно!', callback_data='audio')
    markup.row(btn1, btn2)
    markup.row(btn3)
    markup.row(btn4)
    bot.send_message(message.chat.id, 'all my buttons:', reply_markup=markup)


"""ПОКАЗАТЬ ВОЗМОЖНОСТИ КНОПОК/РЕАКЦИЯ НА КАРТИНКУ/ОБРАБОТКА ОБЫЧНЫХ СООБЩЕНИЙ"""


@bot.message_handler(content_types=['photo', 'text'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('open goo', url='http://www.google.com')
    btn2 = types.InlineKeyboardButton('delete prev mes', callback_data='delete')
    btn3 = types.InlineKeyboardButton('weather', callback_data='weather')
    btn4 = types.InlineKeyboardButton('Секретно!', callback_data='audio')
    if type(message.text) is not str:
        bot.reply_to(message, f'{message.from_user.first_name}, beautiful picture')
    elif message.text.lower().strip() == 'навыки':
        markup.row(btn1, btn2)
        markup.row(btn3)
        markup.row(btn4)
        bot.reply_to(message, 'all my buttons:', reply_markup=markup)
    else:
        bot.reply_to(message, 'Даже не знаю, что на это ответить')


"""РАБОТА С КНОПКАМИ"""


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'users':
        conn = sqlite3.connect('TeleBot.sql')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        info = ''
        for el in users:
            info += f'name: {el[1]}, password: {el[2]}\n'
        cur.close()
        conn.close()

        bot.send_message(callback.message.chat.id, info)
    elif callback.data == 'weather':
        bot.send_message(callback.message.chat.id, 'Введите город, в котором хотите узнать погоду:')
        bot.register_next_step_handler(callback.message, get_weather)
    elif callback.data in ['EUR/USD', 'USD/EUR', 'else']:
        if callback.data != 'else':
            global amount
            values = callback.data.split('/')
            res = currency.convert(amount, values[0], values[1])
            bot.send_message(callback.message.chat.id, f'Результат конвертации: {round(res, 2)}')
        else:
            bot.send_message(callback.message.chat.id, 'Введите пару валют через слэш("/"):')
            bot.register_next_step_handler(callback.message, my_currency)
    elif callback.data == 'audio':
        bot.send_message(callback.message.chat.id, 'Внимание! Секретные записи телефонного разговора Семёна!')
        audio = open(r'Semen.mp3', 'rb')
        bot.send_audio(callback.message.chat.id, audio)
    elif callback.data == 'rub':
        rates = ExchangeRates(datetime.now())
        bot.send_message(callback.message.chat.id, float(round(rates['CNY'].rate, 2)))


"""# надо доработать(открывает браузер только на моем ноутбуке)
@bot.message_handler(commands=['google'])
def brouser(message):
    webbrowser.open('https://www.google.ru')"""

bot.infinity_polling()

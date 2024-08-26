import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('6649138539:AAHB_6A5d-lQYT7aQd27CtgOxZs7AyESX_M')
surname = ''
name = ''
patronymic = ''
birthday = ''
city = ''
phone_number = ''

def input_surname(message):
    global surname
    surname = message.text.strip()
    bot.send_message(message.chat.id, f'🔑*Регистрация*\n\n*Шаг:* 2 из 6\n\nФамилия: *{surname}*\n\nВведите имя:', parse_mode="Markdown")
    bot.register_next_step_handler(message, input_name)

def input_name(message):
    global name, surname
    name = message.text.strip()
    bot.send_message(message.chat.id, f'*🔑Регистрация*\n\n*Шаг:* 3 из 6\n\nФамилия: *{surname}*\
    \nИмя: *{name}*\n\nВведите отчество:', parse_mode="Markdown")
    bot.register_next_step_handler(message, input_patronymic)

def input_patronymic(message):
    global patronymic, name, surname
    patronymic = message.text.strip()
    bot.send_message(message.chat.id, f'🔑*Регистрация*\n\n*Шаг:* 4 из 6\n\nФамилия: *{surname}*\nИмя: *{name}*\
    \nОтчество: *{patronymic}*\n\nВведите дату рождения:\nФормат ввода: *14.11.1998*', parse_mode="Markdown")
    bot.register_next_step_handler(message, input_birthday)

def input_birthday(message):
    global birthday, patronymic, name, surname
    try:
        if int(message.text[:1]) <= 31 and int(message.text[3:5]) <= 12 and int(
                message.text[6:len(message.text) + 1]) >= 1920 \
                and int(message.text[6:len(message.text) + 1]) <= 2005 and message.text[2] == '.' and message.text[5] == '.':

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton('☎️Отправить номер телефона', request_contact=True)
            markup.add(btn)

            birthday = message.text.strip()

            bot.send_message(message.chat.id, f'🔑*Регистрация*\n\n*Шаг:* 5 из 6\n\nФамилия: *{surname}*\nИмя: *{name}*\
            \nОтчество: *{patronymic}*\nДата рождения: *{birthday} г.*\n\nОтправьте номер телефона:\
                            \n\nНажмите кнопки ниже "☎️*Отправить номер телефона*"⤵️', reply_markup=markup, parse_mode="Markdown")

            bot.register_next_step_handler(message, input_number)
        else:
            bot.send_message(message.chat.id, '❗️Ошибка ввода.\n\nВведите дату рождения:\
            \n\n(14 - день, 11 - месяц, 1998 - год)\nФормат ввода: *14.11.1998*', parse_mode="Markdown")
            bot.register_next_step_handler(message, input_birthday)
    except:
        bot.send_message(message.chat.id, '❗️Ошибка ввода.\n\nВведите дату рождения:\
                    \n\n(14 - день, 11 - месяц, 1998 - год)\nФормат ввода: *14.11.1998*', parse_mode="Markdown")
        bot.register_next_step_handler(message, input_birthday)

def input_number(message):
    global birthday, patronymic, name, surname, phone_number
    phone_number = message.contact.phone_number
    if message.contact is not None:
        bot.send_message(message.chat.id, f'🔑*Регистрация*\n\n*Шаг:* 6 из 6\n\nФамилия: *{surname}*\nИмя: *{name}*\
                \nОтчество: *{patronymic}*\nДата рождения: *{birthday} г.*\nНомер телефона: *{phone_number}*\n\nНапишите город:', parse_mode="Markdown")

        bot.register_next_step_handler(message, input_city)

def input_city(message):
    global city, birthday, patronymic, name, surname, phone_number
    if message.text.lower().strip() == 'иваново':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('✅Подтвердить', callback_data='done')
        btn2 = types.InlineKeyboardButton('🔑Пройти регистрацию заново', callback_data='return')
        markup.add(btn1)
        markup.add(btn2)

        city = message.text.strip().capitalize()
        bot.send_message(message.chat.id, f'🔑*Регистрация*\n\nФамилия: *{surname}*\nИмя: *{name}*\
                        \nОтчество:*{patronymic}*\nДата рождения: *{birthday} г.*\nНомер телефона: *{phone_number}*\nГород: *{city}*\
                        \n\n✅Регистрация завершена!\n\nПодтвердите действие или пройдитерегистрацию заново⤵️', reply_markup=markup, parse_mode="Markdown")

    else:
        bot.send_message(message.chat.id, 'Введен некорректный город, повторите попытку')
        bot.register_next_step_handler(message, input_city)

def registration(message):
    conn = sqlite3.connect('Movers.sql')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (surname, name, patronymic, birthday, phone_number, city, id_tlgrm) VALUES \
    ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (surname, name, patronymic, birthday, phone_number, city, message.chat.id))
    conn.commit()
    cur.close()
    conn.close()

def search_id_tlgrm(id_tlgrm):
    conn = sqlite3.connect('Movers.sql')
    cur = conn.execute('SELECT * FROM users')
    users = cur.fetchall()
    for i in users:
        if i[7] == str(id_tlgrm):
            return True
    return False



@bot.message_handler(commands=['start'])
def strart(message):
    conn = sqlite3.connect('Movers.sql')
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS \
        users (id int auto_increment primary key, surname varchar(50), name varchar(50), patronymic varchar(50), \
        birthday varchar(50), phone_number varchar(50), city varchar(50), id_tlgrm varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    if search_id_tlgrm(message.chat.id):
        bot.send_message(message.chat.id, '✅Добро пожаловать в рабочий чат!\n\nОжидайте появления новых заявок!')
    else:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('🔑Пройдите регистрацию', callback_data='reg')
        markup.add(btn)
        bot.send_message(message.chat.id, 'Вы не зарегестрированы, пройдите регистрацию\nНажмите кнопку ниже⤵️', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_message(call):
    if call.data == 'reg' or call.data == 'return':
        bot.send_message(call.message.chat.id, '🔑*Регистрация*\n\n*Шаг:* 1 из 6\n\nВведите фамилию:', parse_mode="Markdown")
        bot.register_next_step_handler(call.message, input_surname)
    elif call.data == 'done':
        bot.delete_message(call.message.chat.id, call.message.message_id - 3)
        bot.send_message(call.message.chat.id, '✅Поздравляем с успешной регистрацией!')
        bot.send_message(call.message.chat.id, '✅Добро пожаловать в рабочий чат!\n\nОжидайте новых заявок!')
        bot.register_next_step_handler(call.message, registration)


@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        print(message.contact)

bot.infinity_polling()

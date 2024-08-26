import telebot  # Подключили библиотеку Телебот - для работы с Телеграм
from telebot import types  # Подключили дополнения
  # Подключили библиотеку Config, с помощью чего можем хранить токен не в коде программы ;) а в файле config.py. Важно: этот файл должен лежать в той же директории, что и код!

bot = telebot.TeleBot('6126472660:AAEM_qLOIT2D--wsLB07YCvqXsgDamJayI4')  # Подключили токен


@bot.message_handler(commands=['number'])  # Объявили ветку для работы по команде <strong>number</strong>
def phone(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)  # Подключаем клавиатуру
    button_phone = types.KeyboardButton(text="Отправить телефон",
                                        request_contact=True)  # Указываем название кнопки, которая появится у пользователя
    keyboard.add(button_phone)  # Добавляем эту кнопку
    bot.send_message(message.chat.id, 'Номер телефона',
                     reply_markup=keyboard)  # Дублируем сообщением о том, что пользователь сейчас отправит боту свой номер телефона (на всякий случай, но это не обязательно)


@bot.message_handler(content_types=['contact'])  # Объявили ветку, в которой прописываем логику на тот случай, если пользователь решит прислать номер телефона :)
def contact(message):
    if message.contact is not None:  # Если присланный объект <strong>contact</strong> не равен нулю
        print(message.contact)

bot.infinity_polling()
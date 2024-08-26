import telebot

bot = telebot.TeleBot('6711147394:AAFl8IfocQPM89qUKDYXwEFw9r6I-hDpISw')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Отправь фото для прповерки оригинальности!')


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    bot.send_message(message.chat.id, 'legit✅')


bot.infinity_polling()

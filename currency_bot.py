import telebot
from config import token, currents_1
from extensions import Converter, ConvertionException

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Это БОТ по конвеартации валюты.\n" \
           "Пример ввода данных:\n" \
           "----------------------\n" \
           f"доллар рубль 1000 \n" \
           f"юань фунт 1000 \n" \
           "----------------------\n" \
           "Список доступных валют - /values"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for k in currents_1.keys():
        text += (f"{currents_1.get(k)} - {k}\n")
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def test(message: telebot.types.Message):
    text_value = message.text.lower().split(' ')
    try:
        text = Converter.converter(text_value)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    else:
        bot.send_message(message.chat.id, text)

bot.polling()
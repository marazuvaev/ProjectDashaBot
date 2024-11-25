import telebot
from telebot import types

bot = telebot.TeleBot('7424065506:AAHltx0rHaluI_GO-ecKf3HNExQBCCYi0dc')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Добавить чат")
    markup.add(btn1)
    bot.send_message(message.from_user.id, '👋 Привет! Я чат-менеджер Даша. Для начала работы нажми кнопку "Добавить чат"', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == 'Добавить чат':


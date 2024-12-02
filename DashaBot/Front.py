import time

import telebot
from telebot import types
import SQLfunctions

bot = telebot.TeleBot('7424065506:AAHltx0rHaluI_GO-ecKf3HNExQBCCYi0dc')
link = "t.me/Dasha_chat_manager_bot"

def start_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Добавить чат")
    item2 = types.KeyboardButton("Зарегистрироваться для существующего чата")
    markup.add(item)
    markup.add(item2)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Добавить чат")
    markup.add(btn1)
    bot.send_message(message.from_user.id, '👋 Привет! Я чат-менеджер Даша. Для начала работы нажми кнопку "Добавить чат"', reply_markup=start_menu())


@bot.message_handler(func=lambda message: message.text == "Добавить чат")
def add_chat(message):
    bot.send_message(message.from_user.id, "Введите название чата:")
    bot.register_next_step_handler(message, save_chat_name)


def save_chat_name(message):
    print("Name")
    chat_name = message.text
    SQLfunctions.add_admin(message.from_user.id, chat_name)
    bot.send_message(message.from_user.id, "Жду, пока вы добавите меня в чат:)")
    current_time = 0
    while SQLfunctions.chat_cheker(message.from_user.id, chat_name):
        print(f"жду{current_time} seconds")
        current_time += 1
        if current_time > 20:
            bot.send_message(message.from_user.id, "Время вышло, чат не добавлен:(", reply_markup=start_menu())
            return
        time.sleep(1)
    bot.send_message(message.from_user.id, "Напишите список ФИО участников, которые должны быть в группе:")
    bot.register_next_step_handler(message, save_chat, chat_name)


def save_chat(message, chat_name):
    SQLfunctions.add_members(chat_name, message.from_user.id, message.text)
    bot.send_message(message.from_user.id, "Чат успешно добавлен!")



@bot.message_handler(func=lambda message: message.text == "Зарегистрироваться для существующего чата")
def start_registration(message):
    if SQLfunctions.is_user_exists(message.from_user.id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton("сменить ФИО")
        markup.add(btn)
        bot.send_message(message.from_user.id, "Вы уже зарегистрированы", reply_markup=markup)
        return
    bot.send_message(message.from_user.id, "Введите ФИО:")
    bot.register_next_step_handler(message, save_user_name)


def save_user_name(message):
    fio = message.text.split()
    SQLfunctions.add_user(message.from_user.id, fio)
    bot.send_message(message.from_user.id, "Вы успешно зарегистрированы")



@bot.message_handler(func=lambda message: message.text == "сменить ФИО")
def change_user_name(message):
    fio = message.text.split()
    if not SQLfunctions.is_user_exists(message.from_user.id):
        bot.send_message(message.from_user.id, "Вы еще не зарегистрированы", reply_markup=start_menu())
        return
    SQLfunctions.change_user_name(message.from_user.id, fio)
    bot.send_message(message.from_user.id, "Вы успешно сменили имя")


@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        chat_id = message.chat.id
        chat_name = message.chat.title
        user_id = message.from_user.id
        if new_member.id == bot.get_me().id:
            if SQLfunctions.chat_cheker(user_id, chat_name):
                SQLfunctions.add_chat_to_db(chat_name, chat_id, user_id)
                bot.send_message(chat_id, f"Привет! Вот ссылка для регистрации участника чата:{link}")
            else:
                bot.send_message(chat_id, f"Извините, не знаю такого чата")
                bot.leave_chat(chat_id)
                return

            member_count = bot.get_chat_members_count(chat_id)
            for id in range(1, member_count + 1):
                member = bot.get_chat_member(chat_id, id)
                if member.user.id == bot.get_me().id:
                    continue
                if member.user.id == user_id:
                    continue
                SQLfunctions.add_chat_user(member.user.id, chat_id)
        else:
            SQLfunctions.add_chat_user(new_member.id, chat_id)


@bot.polling(none_stop=True)
def main():
    print("Бот запущен")

if __name__ == "__main__":
    main()

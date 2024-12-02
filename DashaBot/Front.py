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
    SQLfunctions.add_admin(message.from_user.id, message.text)
    bot.send_message(message.from_user.id, "Жду, пока вы добавите меня в чат:)")

def save_chat(user_id):
    bot.send_message(user_id, "Напишите список участников, которые должны состоять в группе")



@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        if new_member.id == bot.get_me().id:
            chat_id = message.chat.id
            chat_name = message.chat.title
            user_id = message.from_user.id
            if SQLfunctions.chat_cheker(user_id, chat_name):
                bot.send_message(chat_id, f"Привет! Вот ссылка для регистрации участника чата:{link}")
                save_chat(user_id)


@bot.polling(none_stop=True)
def main():
    print("Бот запущен")

if __name__ == "__main__":
    main()

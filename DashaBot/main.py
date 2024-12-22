import time
from apscheduler.schedulers.background import BackgroundScheduler
import telebot
from telebot import types
import backend.repo as repo
import logging
import random
import backend.checks as checks
import os


# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

bot = telebot.TeleBot(
    '7424065506:AAHltx0rHaluI_GO-ecKf3HNExQBCCYi0dc', num_threads=os.cpu_count())
link = "t.me/Dasha_chat_manager_bot"
scheduler = BackgroundScheduler()
processes = dict()


def add_jobs_from_db():
    for chat_id in repo.all_chats_ids():
        processes[chat_id[0]] = scheduler.add_job(chat_users_checker_job, 'cron', args=[
                                                  chat_id[0]], second=0, id=str(chat_id[0])).id


def begin():
    logging.info("Бот запущен")
    add_jobs_from_db()
    logging.info("Бот восстановил задачи для проверки участников из бд")


def end():
    logging.info("Бот прекратил работу")


def start_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Добавить чат")
    item2 = types.KeyboardButton("Зарегистрироваться для существующего чата")
    item3 = types.KeyboardButton(
        "Сменить список пользователей для существующего чата")
    item4 = types.KeyboardButton("Проверить пользователей существующего чата")
    item5 = types.KeyboardButton("Проверить добавление")
    markup.add(item)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Добавить чат")
    markup.add(btn1)
    logging.info(f"Пользователь {message.from_user.id} начал общение")
    bot.send_message(message.from_user.id,
                     '👋 Привет! Я чат-менеджер Даша. Для начала работы нажми кнопку "Добавить чат"\nДля получения помощи введите /help',
                     reply_markup=start_menu())


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id, checks.help_output)


@bot.message_handler(func=lambda message: message.text == "Добавить чат")
def add_chat(message):
    bot.send_message(message.from_user.id, "Введите название чата:")
    bot.register_next_step_handler(message, save_chat_name)


def save_chat_name(message):
    chat_name = message.text
    repo.add_admin(message.from_user.id, chat_name)

    bot.send_message(message.from_user.id,
                     "Жду, пока вы добавите меня в чат:)", reply_markup=start_menu())
    logging.info(f"Пользователь {
                 message.from_user.id} добавляет бота в группу {chat_name}")

    # current_time = 0
    #
    # while repo.chat_cheker(message.from_user.id, chat_name):
    #     print(chat_name)
    #     current_time += 1
    #     if current_time > 500:
    #         logging.info(f"Пользователь {message.from_user.id} не успел добавить бота в группу {chat_name}")
    #         bot.send_message(message.from_user.id, "Время вышло, чат не добавлен:(", reply_markup=start_menu())
    #         return
    #     time.sleep(1)
    # logging.info(f"Пользователь {message.from_user.id} успешно добавил бота в группу {chat_name}")
    # bot.send_message(message.from_user.id, "Напишите список ФИО участников, которые должны быть в группе:")
    # bot.register_next_step_handler(message, save_chat, chat_name)


@bot.message_handler(func=lambda message: message.text == "Проверить добавление")
def start_adding(message):
    bot.send_message(message.from_user.id, "Какой чат проверить?")
    bot.register_next_step_handler(message, continue_adding)


def continue_adding(message):
    if not repo.is_chat_added(message.from_user.id, message.text):
        bot.send_message(
            message.from_user.id, "В такой чат вы вообще не хотели меня добавить, идиот ебучий!", reply_markup=start_menu())
        return

    if repo.chat_cheker(message.from_user.id, message.text):
        bot.send_message(
            message.from_user.id, "Туда вы меня еще не добавили", reply_markup=start_menu())
        return
    bot.send_message(message.from_user.id, "Чат добавлен")
    bot.send_message(message.from_user.id,
                     "Напишите список ФИО участников, которые должны быть в группе:")
    bot.register_next_step_handler(message, save_chat, message.text)


def save_chat(message, chat_name):
    if not checks.check_members(message.text):
        logging.info(f"Пользователь {
                     message.from_user.id} некорректно ввел список участников чата {chat_name}")
        bot.send_message(message.from_user.id,
                         "Некорректный формат", reply_markup=start_menu())
        return
    repo.add_members(chat_name, message.from_user.id, message.text)
    logging.info(f"Пользователь {
                 message.from_user.id} успешно завершил регистрацию чата {chat_name}")
    bot.send_message(message.from_user.id, "Чат успешно добавлен!")


@bot.message_handler(func=lambda message: message.text == "Зарегистрироваться для существующего чата")
def start_registration(message):
    if repo.is_user_exists(message.from_user.id):
        logging.info(
            "Пользователь {message.from_user.id} начал регистрацию повторно")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton("сменить ФИО")
        markup.add(btn)
        bot.send_message(message.from_user.id,
                         "Вы уже зарегистрированы", reply_markup=markup)
        return
    bot.send_message(message.from_user.id, "Введите ФИО:")
    bot.register_next_step_handler(message, save_user_name)


def save_user_name(message):
    if not checks.check_regestrtion(message.text):
        logging.info(f"Регистрация {
                     message.from_user.id} отклонена в связи с неверным форматом")
        bot.send_message(message.from_user.id,
                         "Некорректный формат", reply_markup=start_menu())
        return
    fio = message.text.split()
    repo.add_user(message.from_user.id, fio)
    logging.info(f"Пользователь {
                 message.from_user.id} зарегестрировался под именем {message.text}")
    bot.send_message(message.from_user.id, "Вы успешно зарегистрированы")


@bot.message_handler(func=lambda message: message.text == "сменить ФИО")
def change_user_name_start(message):
    bot.send_message(message.from_user.id, "Введите ФИО:")
    bot.register_next_step_handler(message, change_user_name)


def change_user_name(message):
    if not checks.check_regestrtion(message.text):
        logging.info(
            "Смена имени {message.from_user.id} была отклонена в связи с некоректным форматом")
        bot.send_message(message.from_user.id,
                         "Некорректный формат", reply_markup=start_menu())
        return
    fio = message.text.split()
    if not repo.is_user_exists(message.from_user.id):
        logging.info(
            "Смена имени {message.from_user.id} была отклонена в связи с отсутствеем регистрации")
        bot.send_message(message.from_user.id,
                         "Вы еще не зарегистрированы", reply_markup=start_menu())
        return
    repo.change_user_name(message.from_user.id, fio)
    logging.info(f"Пользователь {
                 message.from_user.id} сменил имя на {message.text}")
    bot.send_message(message.from_user.id,
                     "Вы успешно сменили имя", reply_markup=start_menu())


@bot.message_handler(func=lambda message: message.text == "Сменить список пользователей для существующего чата")
def start_changing(message):
    bot.send_message(message.from_user.id, "В каком чате?")
    bot.register_next_step_handler(message, get_new_list)


def get_new_list(message):
    members = repo.get_members(message.from_user.id, message.text)
    bot.send_message(message.from_user.id, f"Текущий список:\n {
                     members}\n\n отправьте новый список")
    bot.register_next_step_handler(message, change_chat_users, message.text)


def change_chat_users(message, chat_name):
    if not checks.check_members(message.text):
        logging.info(
            f"Смена пользователей пользователем {message.from_user.id} для чата {chat_name} отклонена в связи с неверным форматом")
        bot.send_message(message.from_user.id,
                         "Некорректный формат", reply_markup=start_menu())
        return
    repo.add_members(chat_name, message.from_user.id, message.text)
    logging.info(f"Пользователь {
                 message.from_user.id} обновил список пользователей для чата {chat_name}")
    bot.send_message(message.from_user.id, "Список изменен")


@bot.message_handler(func=lambda message: message.text == "Проверить пользователей существующего чата")
def start_checking(message):
    bot.send_message(message.from_user.id,
                     f"В каком чате надо осуществить проверку?")
    bot.register_next_step_handler(message, checking)


def checking(message):
    if not repo.is_chat_added(message.from_user.id, message.text):
        bot.send_message(message.from_user.id, "Не знаю такого чата")
        return
    logging.info(f"Пользователь {
                 message.from_user.id} провел проверку в чате {message.text}")
    chat_id = repo.get_chat_by_name(message.from_user.id, message.text)
    users_to_output = chat_users_checker_job(chat_id, True)
    if users_to_output is not None:
        bot.send_message(message.from_user.id,
                         f"Список тех, кто еще не зашел в чат или не зарегистрировался:\n {', '.join(users_to_output)}\n\n")
    else:
        bot.send_message(message.from_user.id,
                         "Все нужные пользователи уже есть в чате")


@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        chat_id = message.chat.id
        chat_name = message.chat.title
        user_id = message.from_user.id
        if new_member.id == bot.get_me().id:
            if repo.chat_cheker(user_id, chat_name):
                repo.add_chat_to_db(chat_name, chat_id, user_id)
                # scheduler.add_job(job, 'cron', args=[chat_id], hour=time.time() % 86400 // 3600, minute=time.time() % 3600 // 60 - 1, id=str(chat_id))
                # scheduler.add_job(job, 'cron', args=[chat_id], hour=19, minute=10, id=str(chat_id))
                processes[chat_id] = scheduler.add_job(chat_users_checker_job, 'cron', args=[
                                                       chat_id], second=0, id=str(chat_id)).id

            else:
                bot.send_message(chat_id, f"Извините, не знаю такого чата")
                logging.info(f"Бот вышел из неизвестного чата {chat_name}")
                bot.leave_chat(chat_id)
                return
        else:
            repo.add_chat_user(new_member.id, chat_id)
            bot.send_message(
                chat_id, f"Привет! Вот ссылка для регистрации участника чата:{link}")


@bot.message_handler(content_types=['left_chat_member'])
def handle_user_left(message):
    if message.left_chat_member.id == bot.get_me().id:
        repo.delete_chat(message.chat.id)
        scheduler.remove_job(processes[message.chat.id])
        return
    chat_id = message.chat.id
    user_id = message.left_chat_member.id
    repo.delete_user_by_chat(user_id, chat_id)
    bot.send_message(chat_id, random.choice('Ну пока('))


def chat_users_checker_job(chat_id, table=False):
    expected_members = repo.get_members_by_chat(chat_id)
    current_members = repo.get_users_by_chat(chat_id)
    needed_members = expected_members.copy()

    for user_id in current_members:
        if repo.is_user_exists(user_id):
            name = repo.get_user_name(user_id)
            if name not in expected_members:
                if not is_bot_admin(chat_id):
                    bot.send_message(
                        chat_id, "Чтобы бот смог выполнять свои функции, его надо сделать администратором")
                    continue

                if not is_user_in_chat(chat_id, user_id):
                    continue

                if bot.ban_chat_member(chat_id, user_id):
                    bot.send_message(chat_id,
                                     f"Пользователь {' '.join(name)} был удален из чата, так как его нет в ожидаемом списке пользователей")
                    repo.delete_user_by_chat(user_id, chat_id)
                    logging.info(f"Пользователь {" ".join(
                        name)} был удален из чата {chat_id}")
            else:
                needed_members.remove(name)

        else:
            if time.time() - repo.get_start_time(user_id, chat_id) > 3 * 24 * 60 * 60:
                if bot.ban_chat_member(chat_id, user_id):
                    bot.send_message(
                        chat_id, f"Пользователь был удален из чата, так как не прошел регистрацию")
                    logging.info(f"Пользователь {
                                 user_id} был удален из чата {chat_id}")

    if table:
        if len(needed_members) > 0:
            return [' '.join(_) for _ in needed_members]
        return []


def is_bot_admin(chat_id):
    try:
        administrators = bot.get_chat_administrators(chat_id)
        for admin in administrators:
            if admin.user.id == bot.get_me().id:
                return True
    except Exception as e:
        logging.ERROR(
            f"Ошибка при проверке администраторов в чате {chat_id}: {e}")
    return False


def is_user_in_chat(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['member']
    except Exception as e:
        logging.ERROR(f"Ошибка при проверке участника в чате {chat_id}: {e}")
        return False


def main():
    begin()
    scheduler.start()
    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        end()
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        end()


if __name__ == "__main__":
    main()

import sqlite3 as sq
import time


def add_admin(user_id: int, chat_name: str) -> None:
    connection = sq.connect('chats.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO admins (admin_id, chat_name) VALUES (?, ?)", (user_id, chat_name))
    connection.commit()
    cursor.close()
    connection.close()


def chat_cheker(user_id: int, chat_name: str) -> bool:
    connection = sq.connect('chats.db')
    cursor = connection.cursor()
    a = cursor.execute("SELECT admin_id, chat_name FROM admins WHERE admin_id = ? AND chat_name = ?", (user_id, chat_name))
    ans = (len(a.fetchall()) != 0)
    cursor.close()
    connection.close()
    return ans


def add_chat_to_db(chat_name: str, chat_id: int, admin_id: int) -> None:
    connection = sq.connect('chats.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM chats WHERE telegram_id = ?", (chat_id,))
    cursor.execute("INSERT INTO chats (telegram_id, admin_id, chat_name) VALUES (?, ?, ?)", (chat_id, admin_id, chat_name))
    connection.commit()
    cursor.execute(("DELETE FROM admins WHERE admin_id = ? AND chat_name = ?"), (admin_id, chat_name))
    connection.commit()
    cursor.close()
    connection.close()


def add_members(chat_name: str, admin_id: int, members: str) -> None:
    connection = sq.connect('chats.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE chats SET users_names = ? WHERE admin_id = ? AND chat_name = ?", (members, admin_id, chat_name))
    connection.commit()
    cursor.close()
    connection.close()


def add_user(user_id: int, initials: list) -> None:
    connection = sq.connect('chats.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (telegram_id, surname, name, middle_name) VALUES (?, ?, ?, ?)", (user_id, *initials))
    connection.commit()
    cursor.close()
    connection.close()


def is_user_exists(user_id: int) -> bool:
    connection = sq.connect('chats.db')
    cursor = connection.cursor()
    a = cursor.execute("SELECT telegram_id FROM users WHERE telegram_id = ?", (user_id, ))
    ans = (len(a.fetchall()) != 0)
    cursor.close()
    connection.close()
    return ans


def change_user_name(user_id: int, new_initials: list) -> None:
    connection = sq.connect('chats.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET surname = ?, name = ?, middle_name = ? WHERE telegram_id = ?", (*new_initials, user_id))
    connection.commit()
    cursor.close()
    connection.close()


def add_chat_user(user_id: int, chat_id: int) -> None:
    connection = sq.connect('chats.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users_and_chats (user_id, chat_id, start_time) VALUES (?, ?, ?)", (user_id, chat_id, int(time.time())))
    connection.commit()
    cursor.close()
    connection.close()


def get_start_time(user_id: int, chat_id: int) -> int:
    connection = sq.connect('chats.db')
    cursor = connection.cursor()
    a = cursor.execute("SELECT start_time FROM users_and_chats WHERE user_id = ? AND chat_id = ?", (user_id, chat_id)).fetchone()
    cursor.close()
    connection.close()
    return a[0]


def get_members(user_id: int, chat_name: str):
    connection = sq.connect('chats.db')
    cursor = connection.cursor()
    a = cursor.execute("SELECT users_names FROM chats WHERE user_id = ? AND chat_name = ?", (user_id, chat_name)).fetchone()
    cursor.close()
    connection.close()
    return a[0]
import sqlite3 as sq


def add_admin(user_id: int, chat_name: str):
    connection = sq.connect('chats.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO admins (admin_id, chat_name) VALUES (?, ?)", (user_id, chat_name))
    cursor.close()
    connection.close()


def chat_cheker(user_id: int, chat_name: str):
    connection = sq.connect('chats.db')
    cursor = connection.cursor()
    a = cursor.execute("SELECT (admin_id, chat_name) from admins WHERE admin_id = ? AND chat_name = ?", (user_id, chat_name))
    cursor.close()
    connection.close()
    return len(a.fetchall()) != 0


def add_chat_to_db(chat_name: str, chat_id: int, admin_id: int):
    connection = sq.connect('chats.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO chats (telegram_id, admin_id, chat_name) VALUES (?, ?, ?)", (chat_id, admin_id, chat_name))
    cursor.close()
    connection.close()


def add_members(chat_name: str, admin_id: int, members: str):
    pass

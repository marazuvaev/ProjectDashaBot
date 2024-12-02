import sqlite3 as sq


def add_admin(user_id: int, chat_name: str):
    connection = sq.connect('chats.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO admins (admin_id, chat_name) VALUES (?, ?)", (user_id, chat_name))
    connection.commit()
    cursor.close()
    connection.close()


def chat_cheker(user_id: int, chat_name: str):
    connection = sq.connect('chats.db')
    cursor = connection.cursor()
    a = cursor.execute("SELECT admin_id, chat_name from admins WHERE admin_id = ? AND chat_name = ?", (user_id, chat_name))
    ans = (len(a.fetchall()) != 0)
    cursor.close()
    connection.close()
    return ans


def add_chat_to_db(chat_name: str, chat_id: int, admin_id: int):
    connection = sq.connect('chats.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO chats (telegram_id, admin_id, chat_name) VALUES (?, ?, ?)", (chat_id, admin_id, chat_name))
    connection.commit()
    cursor.execute(("DELETE FROM admins WHERE admin_id = ? AND chat_name = ?"), (admin_id, chat_name))
    connection.commit()
    cursor.close()
    connection.close()


def add_members(chat_name: str, admin_id: int, members: str):
    pass

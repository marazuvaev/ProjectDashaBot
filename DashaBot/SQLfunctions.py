import sqlite3 as sq

global cursor

cursor = None


def start_connection():
    global cursor
    if (cursor is None):
        connection = sq.connect('chats.db')
        cursor = connection.cursor()


def add_admin(user_id: int, chat_name: str):
    global cursor
    start_connection()
    #cursor.execute("INSERT INTO admins (admin_id, chat_id) VALUES (?, ?)", (user_id, chat_name))


def chat_cheker(user_id: int, chat_name: str):
    start_connection()
    return True


def add_chat_to_db(chat_id: int, admin_id: int, user_names: str):
    start_connection()
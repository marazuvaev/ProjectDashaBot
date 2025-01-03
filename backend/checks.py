def check_regestrtion(string: str) -> bool:
    return len(string.split()) == 3


def check_members(string: str) -> bool:
    return all(map(check_regestrtion, string.split(',')))


help_output = '''
Вас приветствует ваш помощьник по чатам ДашаБот!
Данный бот позволяет контролировать участников вашей группы,
удаляя нежелательных личностей
Для начала общения напишите команду /start
Если вы админ чата, и вы хотите добавить бота в вашу группу, 
то после начала нажмите на кнопку "Добавить чат" в контекстном меню.
После чего вам следуйте инструкциям. Имена пользователей, состоящих в чате 
вводятся в формате ФИО, через запятую.
Если вы уже добавили бота в чат, и вы хотите изменить список участников чата,
нажмите на кнопку "Изменить список участников" и вы введите новый список в указанном 
выше формате
Если вы админ, и вы хотите удалить из чата ненужных пользователей, нажмите на кнопку 
"Проверить пользователей существующего чата", после чего введите название чата.
Если вы не админ, и вас попросили зарегестрироваться, просто нажмите на кнопку 
"Зарегистрироваться для существующего чата" и введите свое ФИО. 
'''

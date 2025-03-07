# Copyright (c) 2024 tacotent43
# All rights reserved.
#
# This software and its source code are the property of tacotent43.
# Unauthorized copying, modification, distribution, or use of this code,
# in whole or in part, without explicit written permission from the author
# is strictly prohibited.
#
# For licensing inquiries, please contact the owner.

import re
import random
import json
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot import formatting

## main functions

# read from json file
def read_json(filename:str):
  fp = open(filename + ".json", "r")
  tmp = json.load(fp)
  fp.close()
  return tmp

# function for creating buttons from current position in 
def create_buttons_from(current_position):
  return [KeyboardButton(theme) for theme in current_position]

# get themes names 
def themes_names(themes):
  return list(themes.keys())

def create_keyboard(current_buttons_names):
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
  buttons = create_buttons_from(current_buttons_names)
  keyboard.add(*buttons)
  keyboard.add(KeyboardButton(back))
  return keyboard

# JSON files opening
config = read_json("config")
all_themes = read_json("themes")
scripts = read_json("scripts")

bot = telebot.TeleBot(config["token"])

###################
start_hello_comma = scripts["start_hello_command"]
back = scripts["back"]

want_to_solve_tasks = scripts["solve_tasks"]
want_to_read_theory = scripts["read_theory"]
###################

# для обработки разных запросов от разных пользователей
# user position saving
users = {}


# function to send long message
def send_long_message(bot, chat_id, text, parse_mode=None, reply_markup=None):
  max_length = 4096
  for i in range(0, len(text), max_length):
    chunk = text[i:i + max_length]
    bot.send_message(chat_id, chunk, parse_mode=parse_mode, reply_markup=reply_markup)


# getting theory from file
def get_theory_file(path):
  with open(path, "r") as theory_file:
    file_text = theory_file.readlines()
  return file_text


# md formatting
def escape_markdown_v2(text):
  # List of characters that need to be escaped in MarkdownV2
  reserved_chars = r'\.\-!()+=|{}\[\]_*~><#&@'
  # Escape each reserved character
  return re.sub(f'([{re.escape(reserved_chars)}])', r'\\\1', text)


def get_user(id):
  global users
  if id not in users:
    users[id] = [
      [], # [0] - paths
      []  # [1] - answers
    ]
  return users[id]


def get_by_path(message):
  path = get_user(message.chat.id)[0]
  current = all_themes
  i = 0
  while (i < len(path)):
    current = current[path[i]]
    i += 1
  return current


def update(message):
  path, answers = get_user(message.chat.id)
  tmp = get_by_path(message)
  
  if (len(path) and path[-1] == "Теория"):
    filepath = get_by_path(message)
    
    # theory_text = "".join(get_theory_file(filepath))
    # escaped_text = escape_markdown_v2(theory_text)
    # # bot.send_message(message.chat.id, escaped_text, parse_mode="MarkdownV2", reply_markup=keyboard)
    # # uncomment
    # # send_long_message(bot, message.chat.id, escaped_text, parse_mode="MarkdownV2", reply_markup=keyboard)
    # send_long_message(bot, message.chat.id, theory_text, parse_mode="Markdown", reply_markup=keyboard)
    
    with open(filepath, "rb") as theory_file:
      theory = theory_file.read()
    
    keyboard = create_keyboard([])
    
    bot.send_document(message.chat.id, theory)
    bot.send_message(message.chat.id, f"Отлично! Держи файл с теорией на тему '{path[-2]}'.", reply_markup=keyboard)
    
    print("THEORY_DEBUG:", message.chat.id, keyboard, "theory opened")
    return 
  
  if (len(path) and path[-1] == "Задачи"):
    keyboard = create_keyboard([])
    # TODO: исправить отображение имен числительных
    bot.send_message(message.chat.id, f"В базе {len(tmp)} задач по теме {path[-2]}", reply_markup=keyboard)  
    print("TASKS_DEBUG:", message.chat.id, keyboard)
    
    return
  
  # обновление клавиатуры
  keyboard = create_keyboard(tmp)
  # было ли главное меню
  if len(answers) == 0:
    main_menu(message)
    return
  
  answer = answers[-1]
  
  print("DEBUG:", message.chat.id, keyboard, answer)
  
  bot.send_message(message.chat.id, answer, reply_markup=keyboard)


# start comma
@bot.message_handler(commands=["start"])
def start(message):
  bot.send_message(message.chat.id, "Привет, " + message.from_user.first_name + "!\n" + start_hello_comma)
  
  # зачистка текущего положения
  get_user(message.chat.id)[0], get_user(message.chat.id)[1] = [], []
  
  main_menu(message)
  print(f"DEBUG: {message.chat.id}:{message.from_user.username} sent a request: {message.text}")


@bot.message_handler(commands=["choose"])
def main_menu(message):
  answer = "Выбери интересующий тебя раздел:"
  get_user(message.chat.id)[1].append(answer)
  update(message)

# REMOVE ALL CODE HERE {start}
# @bot.message_handler(func=lambda message: message.text == "Задача")
# def tmp_func(message):
#   bot.send_message(message.chat.id, """Вот тебе задачка по теме Баллистика:
# ```Условие:
# Два мальчика, находящиеся на расстоянии 9,2 м друг от друга, перебрасывают мяч, сообщая ему скорость 11 м/с.
# ```
# Найди максимальную высоту подъёма мяча.""", parse_mode="Markdown")

# @bot.message_handler(func=lambda message: message.text == "5")
# def tmp_func_2(message):
#   bot.send_message(message.chat.id, "Ура, твой ответ корректен! Выбери другую задачу, если не хочешь - нажми 'Назад'.")

# @bot.message_handler(func=lambda message: message.text == "4")
# def tmp_func_3(message):
#   bot.send_message(message.chat.id, "К сожалению, твой ответ неправильный! Попробуй ещё раз.")
# REMOVE END


# Функция для выбора подразделов
@bot.message_handler(func=lambda message: message.text in get_by_path(message))
def theme(message):
  get_user(message.chat.id)[0].append(message.text)
  answer = f"Выбери интересующий тебя подраздел в теме '{message.text}':"
  get_user(message.chat.id)[1].append(answer)
  update(message)


# Функция для получения задачи. Надо реализовать
@bot.message_handler(func=lambda message: message.text )
def get_task(message):
  pass






"""
TODO: 
Сделать классификацию по разделам 
Реализовать систему вывода задач
Реализовать систему проверки задач

Дотехать все файлы
Довнести все изменения в themes.json


починить кнопку back
"""



# Откат на одну позицию назад (кнопка BACK)
@bot.message_handler(func=lambda message: message.text == back)
def return_back(message):
  if (len(get_user(message.chat.id)[0]) > 0):
    get_user(message.chat.id)[0].pop()
  if (len(get_user(message.chat.id)[1]) > 1):
    get_user(message.chat.id)[1].pop()
  print(f"DEBUG: {message.chat.id} pressed back button")
  update(message)
  


# bot.polling(none_stop=True, interval=0, timeout=20)
bot.polling(none_stop=True)
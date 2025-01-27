# Copyright (c) 2024 tacotent43
# All rights reserved.
#
# This software and its source code are the property of tacotent43.
# Unauthorized copying, modification, distribution, or use of this code,
# in whole or in part, without explicit written permission from the author
# is strictly prohibited.
#
# For licensing inquiries, please contact the owner.

import random
import time
import json
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

## main functions

# read from json file
def read_json(filename:str):
  fp = open(filename + ".json", "r")
  tmp = json.load(fp)
  fp.close()
  return tmp

# полностью переписать
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
requests_by_users = {}

path = []

answers = []

def get_by_path():
  current = all_themes
  i = 0
  while (i < len(path)):
    current = current[path[i]]
    i += 1
  return current

def update(message):
  keyboard = create_keyboard(get_by_path())
  if len(answers) == 0:
    main_menu(message)
    return
  answer = answers[-1]
  print("DEBUG:", keyboard, answer)
  bot.send_message(message.chat.id, answer, reply_markup=keyboard)


# сделать для каждого message.chat.id отдельный path и отдельный answers
# обработка задач (сделать обработчик), сами задачи через метод get_by_path()

# start comma
@bot.message_handler(commands=["start"])
def start(message):
  bot.send_message(message.chat.id, "Привет, " + message.from_user.first_name + "!\n" + start_hello_comma)
  main_menu(message)
  print(f"DEBUG: {message.chat.id}:{message.from_user.username} sent a request: {message.text}")


### переписать через inline keyboard button
@bot.message_handler(commands=["choose"])
def main_menu(message):
  answer = "Выбери интересующий тебя раздел:"
  answers.append(answer)
  update(message)


# Функция для выбора подразделов
@bot.message_handler(func=lambda message: message.text in get_by_path())
def theme(message):
  path.append(message.text)
  answer = f"Выбери интересующий тебя подраздел в теме '{message.text}':"
  answers.append(answer)
  update(message)




# выбор тем задач
@bot.message_handler(func=lambda message: message.text in want_to_solve_tasks)
def tasks_topics(message):
  bot.send_message(message.chat.id, "TASK_OPEN")


# выбор тем теории
@bot.message_handler(func=lambda message: message.text in want_to_read_theory)
def themes_topics(message):
  bot.send_message(message.chat.id, "THEORY_OPEN")


# Откат на одну позицию назад (кнопка BACK)
@bot.message_handler(func=lambda message: message.text == back)
def return_back(message):
  if (len(path) > 0):
    path.pop()
  if (len(answers) > 1):
    answers.pop()
  update(message)
  


# bot.polling(none_stop=True, interval=0, timeout=20)
bot.polling(none_stop=True)
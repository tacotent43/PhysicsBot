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

# read from json file
def read_json(filename:str):
  fp = open(filename + ".json", "r")
  tmp = json.load(fp)
  fp.close()
  return tmp

config = read_json("config")
all_themes = read_json("themes")
scripts = read_json("scripts")

bot = telebot.TeleBot(config["token"])

### spec_commas ###
start_hello_comma = """
enter hello comma here
"""

# back button text
bck = scripts["back"]

want_to_solve_tasks = scripts["solve_tasks"]
want_to_read_theory = scripts["read_theory"]
###################

# start comma
@bot.message_handler(commands=["start"])
def start(message):
  bot.send_message(message.chat.id, start_hello_comma)

@bot.message_handler(commands=["choose"])
def main_menu(message):
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
  themes = list(all_themes.keys())
  buttons = [KeyboardButton(theme) for theme in themes]
  keyboard.add(*buttons)
  keyboard.add(KeyboardButton(bck))

  # keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
  # # Кнопка для решения задач
  # keyboard.add(KeyboardButton(want_to_solve_tasks))
  # # Кнопка для просмотра теории
  # keyboard.add(KeyboardButton(want_to_read_theory))
  bot.send_message(message.chat.id, "Выбери интересующий тебя раздел:", reply_markup=keyboard)

# @bot.message_handler(func=lambda message: message.text )


# выбор тем задач
@bot.message_handler(func=lambda message: message.text in want_to_solve_tasks)
def tasks_topics(message):
  bot.send_message(message.chat.id, "TASK_OPEN")

# выбор тем теории
@bot.message_handler(func=lambda message: message.text in want_to_read_theory)
def themes_topics(message):
  bot.send_message(message.chat.id, "THEORY_OPEN")

@bot.message_handler(func=lambda message: message.text == bck)
def return_back(message):
  pass

bot.polling(none_stop=True, interval=0, timeout=20)
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

# function for creating buttons from current position in 
def create_buttons_from(current_position):
  return [KeyboardButton(theme) for theme in current_position]

# get themes names 
def themes_names(themes):
  return list(themes.keys())

# JSON files opening
config = read_json("config")
all_themes = read_json("themes")
scripts = read_json("scripts")


bot = telebot.TeleBot(config["token"])


# тут хранится текущий открытый раздел
global current_pos
current_pos = all_themes

###################
start_hello_comma = scripts["start_hello_command"]
bck = scripts["back"]

want_to_solve_tasks = scripts["solve_tasks"]
want_to_read_theory = scripts["read_theory"]
###################



# start comma
@bot.message_handler(commands=["start"])
def start(message):
  bot.send_message(message.chat.id, "Привет, " + message.from_user.first_name + "!\n" + start_hello_comma)
  main_menu(message)


@bot.message_handler(commands=["choose"])
def main_menu(message):
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
  buttons = create_buttons_from(current_pos)
  keyboard.add(*buttons)
  keyboard.add(KeyboardButton(bck))
  bot.send_message(message.chat.id, "Выбери интересующий тебя раздел:", reply_markup=keyboard)


# @bot.message_handler(func=lambda message: message.text in list(current_pos.keys()))
# def find_next_themes(message):
#   print(message.from_user.username, "pressed", message.text)
#   global current_pos
#   current_pos = current_pos[str(message.text)]
#   bot.send_message(message.chat.id, *current_pos)
  

###################
# желательно переписать

# раздел 1
@bot.message_handler(func=lambda message: message.text == "Механика")
def mechanics_theme(message):
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
  buttons = create_buttons_from(all_themes[message.text])
  keyboard.add(*buttons)
  keyboard.add(KeyboardButton(bck))
  bot.send_message(message.chat.id, f"Выбери интересующий тебя подраздел в теме {message.text}:", reply_markup=keyboard)


# кинематика
@bot.message_handler(func=lambda message: message.text == "Кинематика")
def kinematics_mechanics_subtheme(message):
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
  buttons = create_buttons_from(all_themes["Механика"]["Кинематика"])
  keyboard.add(*buttons)
  keyboard.add(KeyboardButton(bck))
  bot.send_message(message.chat.id, f"Что будем делать в разделе {message.text}?", reply_markup=keyboard)
  
# динамика
@bot.message_handler(func=lambda message: message.text == "Динамика")
def dynamics_mechanics_subtheme(message):
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
  buttons = create_buttons_from(all_themes["Механика"]["Динамика"])
  keyboard.add(*buttons)
  keyboard.add(KeyboardButton(bck))
  bot.send_message(message.chat.id, f"Что будем делать в разделе {message.text}?", reply_markup=keyboard)

# статика
@bot.message_handler(func=lambda message: message.text == "Статика")
def statics_mechanics_subtheme(message):
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
  buttons = create_buttons_from(all_themes["Механика"]["Статика"])
  keyboard.add(*buttons)
  keyboard.add(KeyboardButton(bck))
  bot.send_message(message.chat.id, f"Что будем делать в разделе {message.text}?", reply_markup=keyboard)

# закон сохранения в механике
@bot.message_handler(func=lambda message: message.text == "Закон сохранения в механике")
def zsi_mechanics_subtheme(message):
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
  buttons = create_buttons_from(all_themes["Механика"]["Закон сохранения в механике"])
  keyboard.add(*buttons)
  keyboard.add(KeyboardButton(bck))
  bot.send_message(message.chat.id, f"Что будем делать в разделе {message.text}?", reply_markup=keyboard)

# механические колебания и волны
@bot.message_handler(func=lambda message: message.text == "Механические колебания и волны")
def mechanical_koleb_mechanics_subtheme(message):
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
  buttons = create_buttons_from(all_themes["Механика"]["Механические колебания и волны"])
  keyboard.add(*buttons)
  keyboard.add(KeyboardButton(bck))
  bot.send_message(message.chat.id, f"Что будем делать в разделе {message.text}?", reply_markup=keyboard)



# раздел 2
@bot.message_handler(func=lambda message: message.text == "Электродинамика")
def electrodynamics_theme(message):
  pass


# раздел 3
@bot.message_handler(func=lambda message: message.text == "Квантовая физика")
def quantum_physics_theme(message):
  pass


# раздел 4
@bot.message_handler(func=lambda message: message.text == "Молекулярная физика. Термодинамика")
def molecular_physics_and_thermodynamics_theme(message):
  pass
#
###################


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
  main_menu(message)


# bot.polling(none_stop=True, interval=0, timeout=20)
bot.polling(none_stop=True)
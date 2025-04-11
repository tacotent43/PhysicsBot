# Copyright (c) 2024 tacotent43
# All rights reserved.
#
# This software and its source code are the property of tacotent43.
# Unauthorized copying, modification, distribution, or use of this code,
# in whole or in part, without explicit written permission from the author
# is strictly prohibited.
#
# For licensing inquiries, please contact the owner.

import json
from typing import Dict, List, Tuple
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def read_from_json(filename: str) -> dict:
  with open(f"{filename}.json", "r", encoding="utf-8") as fp:
    return json.load(fp)

config = read_from_json("config")
all_themes = read_from_json("themes")
scripts = read_from_json("scripts")

bot = Bot(token=config["token"])
dp = Dispatcher()

START_HELLO_COMMAND = scripts["start_hello_command"]
BACK_BUTTON = scripts["back"]
SOLVE_TASKS = scripts["solve_tasks"]
READ_THEORY = scripts["read_theory"]

users: Dict[int, Tuple[List[str], List[str]]] = {}

def get_user(user_id: int) -> Tuple[List[str], List[str]]:
  if user_id not in users:
    users[user_id] = ([], [])
  return users[user_id]

def get_by_path(path: List[str]) -> dict:
  current = all_themes
  for step in path:
    current = current[step]
  return current

def pluralize_tasks(n: int) -> str:
  if n % 10 == 1 and n % 100 != 11:
    return "задача"
  elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
    return "задачи"
  return "задач"

def create_keyboard(items: List[str]) -> ReplyKeyboardMarkup:
  builder = ReplyKeyboardBuilder()
  for item in items:
    builder.add(KeyboardButton(text=item))
  builder.add(KeyboardButton(text=BACK_BUTTON))
  builder.adjust(2)
  return builder.as_markup(resize_keyboard=True)

async def update_state(message: types.Message):
  user_id = message.chat.id
  path, answers = get_user(user_id)
  current = get_by_path(path)
  
  if path and path[-1] == "Теория":
    filepath = get_by_path(path)
    with open(filepath, "rb") as theory_file:
      await bot.send_document(user_id, theory_file)
    await message.answer(
      f"Отлично! Держи файл с теорией на тему '{path[-2]}'.",
      reply_markup=create_keyboard([])
    )
    return
  
  if path and path[-1] == "Задачи":
    await message.answer(
      f"В базе {len(current)} {pluralize_tasks(len(current))} по теме {path[-2]}",
      reply_markup=create_keyboard([])
    )
    return
  
  keyboard = create_keyboard(list(current.keys()))
  
  if not answers:
    await main_menu(message)
    return
  
  await message.answer(answers[-1], reply_markup=keyboard)

@dp.message(Command("start"))
async def start_command(message: types.Message):
  user_id = message.chat.id
  users[user_id] = ([], [])
  await message.answer(f"Привет, {message.from_user.first_name}!\n{START_HELLO_COMMAND}")
  await main_menu(message)

@dp.message(Command("choose"))
async def main_menu(message: types.Message):
  user_id = message.chat.id
  path, answers = get_user(user_id)
  answers.append("Выбери интересующий тебя раздел:")
  await update_state(message)

@dp.message(lambda message: message.text in get_by_path(get_user(message.chat.id)[0]))
async def theme_handler(message: types.Message):
  user_id = message.chat.id
  path, answers = get_user(user_id)
  path.append(message.text)
  answers.append(f"Выбери интересующий тебя подраздел в теме '{message.text}':")
  await update_state(message)

@dp.message(lambda message: message.text == BACK_BUTTON)
async def back_handler(message: types.Message):
  user_id = message.chat.id
  path, answers = get_user(user_id)
  if path:
    path.pop()
  if len(answers) > 1:
    answers.pop()
  await update_state(message)

async def main():
  await dp.start_polling(bot)

if __name__ == "__main__":
  import asyncio
  asyncio.run(main())
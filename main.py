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
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

@dataclass
class UserData:
  # List of selected menu paths (navigation history)
  paths: List[str] = field(default_factory=list)
  # List of bot responses to the user
  answers: List[str] = field(default_factory=list)


class UserStorage:
  def __init__(self):
    # Dictionary to store user data (user_id -> UserData)
    self._users: Dict[int, UserData] = {}
  
  # Add new user to storage
  def add_user(self, user_id: int) -> None:
    self._users[user_id] = UserData()
  
  # Get user data (creates new entry if doesn't exist)
  def get_user(self, user_id: int) -> UserData:
    if user_id not in self._users:
      self.add_user(user_id)
    return self._users[user_id]
  
  # Reset user data to initial state
  def clear_user(self, user_id: int) -> None:
    if user_id in self._users:
      self._users[user_id] = UserData()


class PhysicsBot:
  def __init__(self):
    # Load configuration files
    self.config = self._read_from_json("config")
    self.all_themes = self._read_from_json("themes")
    self.scripts = self._read_from_json("scripts")
    
    # Initialize bot and dispatcher
    self.bot = Bot(token=self.config["token"])
    self.dp = Dispatcher()
    self.users = UserStorage()
    
    # Set up message handlers
    self._register_handlers()

  # Helper method to read JSON files
  @staticmethod
  def _read_from_json(filename: str) -> dict:
    with open(f"{filename}.json", "r", encoding="utf-8") as fp:
      return json.load(fp)

  # Register all message handlers
  def _register_handlers(self) -> None:
    # /start command handler
    self.dp.message.register(self._start_command, Command("start"))
    # /choose command handler
    self.dp.message.register(self._main_menu, Command("choose"))
    # Theme selection handler
    self.dp.message.register(self._theme_handler, 
      lambda message: message.text in self._get_by_path(
        self.users.get_user(message.chat.id).paths))
    # Back button handler
    self.dp.message.register(self._back_handler,
      lambda message: message.text == self.scripts["back"])

  # Get current menu level based on navigation path
  def _get_by_path(self, path: List[str]) -> dict:
    current = self.all_themes
    for step in path:
      current = current[step]
    return current

  # Pluralize "task" based on count
  @staticmethod
  def _pluralize_tasks(n: int) -> str:
    if n % 10 == 1 and n % 100 != 11:
      return "задача"
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
      return "задачи"
    return "задач"

  # Create reply keyboard with dynamic buttons
  def _create_keyboard(self, items: List[str]) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for item in items:
      builder.add(KeyboardButton(text=item))
    builder.add(KeyboardButton(text=self.scripts["back"]))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

  # Update bot state based on current navigation
  async def _update_state(self, message: types.Message) -> None:
    user = self.users.get_user(message.chat.id)
    current = self._get_by_path(user.paths)
    
    # Обработка выбора теории - отправка файла
    if user.paths and user.paths[-1] == "Теория":
      filepath = self._get_by_path(user.paths)
      await message.answer(
        f"Отлично! Держи файл с теорией на тему '{user.paths[-2]}'.",
        reply_markup=self._create_keyboard([])
      )
      print("LOG:", message.chat.id, "requested file", filepath)
      try:
        with open(filepath, 'rb') as file:
          await self.bot.send_document(
            chat_id=message.chat.id,
            document=types.BufferedInputFile(
              file.read(),
              filename=filepath.split('/')[-1]
            )
          )
      except FileNotFoundError:
        await message.answer("Файл не найден. Пожалуйста, сообщите администратору.")
      except Exception as err:
        await message.answer("Произошла ошибка при отправке файла.")
        print(f"Ошибка отправки файла: {err}")
      return
    
    # Handle tasks selection - show tasks count
    if user.paths and user.paths[-1] == "Задачи":
      await message.answer(
        f"В базе {len(current)} {self._pluralize_tasks(len(current))} по теме {user.paths[-2]}",
        reply_markup=self._create_keyboard([])
      )
      return
    
    # Create keyboard for current menu level
    keyboard = self._create_keyboard(list(current.keys()))
    
    # Show main menu if no answers exist
    if not user.answers:
      await self._main_menu(message)
      return
    
    # Send last response with appropriate keyboard
    await message.answer(user.answers[-1], reply_markup=keyboard)

  # Handle /start command - reset and greet user
  async def _start_command(self, message: types.Message) -> None:
    self.users.clear_user(message.chat.id)
    await message.answer(
      f"Привет, {message.from_user.first_name}!\n{self.scripts['start_hello_command']}"
    )
    print("LOG:", message.chat.id, "sent /start command")
    await self._main_menu(message)

  # Show main menu options
  async def _main_menu(self, message: types.Message) -> None:
    user = self.users.get_user(message.chat.id)
    user.answers.append("Выбери интересующий тебя раздел:")
    await self._update_state(message)

  # Handle theme selection - navigate deeper
  async def _theme_handler(self, message: types.Message) -> None:
    user = self.users.get_user(message.chat.id)
    user.paths.append(message.text)
    user.answers.append(f"Выбери интересующий тебя подраздел в теме '{message.text}':")
    await self._update_state(message)

  # Handle back button - navigate up
  async def _back_handler(self, message: types.Message) -> None:
    user = self.users.get_user(message.chat.id)
    if user.paths:
      user.paths.pop()
    if len(user.answers) > 1:
      user.answers.pop()
    await self._update_state(message)

  # Start the bot
  async def run(self) -> None:
    await self.dp.start_polling(self.bot)

# TODO: починить отправку документов
# TODO: реализовать отправку задач
# TODO: реализовать анализ ответов, отправку фидбека
# TODO: реализовать отправку правильных решений

if __name__ == "__main__":
  bot = PhysicsBot()
  import asyncio
  asyncio.run(bot.run())
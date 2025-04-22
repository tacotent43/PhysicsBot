from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from bot.utils import pluralize_tasks
from bot.utils import send_file
from bot.keyboards import create_keyboard

#! [register_handlers]
def register_handlers(dp: Dispatcher, app):
  dp.message.register(constants(app), Command("constants"))
  dp.message.register(start_command(app), Command("start"))
  dp.message.register(choose_command(app), Command("choose"))
  dp.message.register(theme_handler(app))
  dp.message.register(menu_selector(app))
  dp.message.register(back_handler(app))
#! [register_handlers]


#! [start_command]
def start_command(app):
  async def handler(message: Message):
    app.users.clear_user(message.chat.id)
    await message.answer(
      f"Привет, {message.from_user.first_name}!\n{app.scripts['start_hello_command']}"
    )
    print(f"LOG: {message.chat.id} ({message.from_user.username}) requested /start")
    await choose_command(app)(message)
  return handler
#! [start_command]


#! [choose_command]
def choose_command(app):
  async def handler(message: Message):
    user = app.users.get_user(message.chat.id)
    user.answers.append("Выбери интересующий тебя раздел:")
    await update_state(message, app)
  return handler
#! [choose_command]


#! [constants]
def constants(app):
  async def handler(message: Message):
    user = app.users.get_user(message.chat.id)
    user.answers.append("Держи файл со всеми константами и табличными значениями.")
    await update_state(message, app)
  return handler
#! [constants]


#! [theme_handler]
def theme_handler(app):
  async def handler(message: Message):
    user = app.users.get_user(message.chat.id)
    current_level = get_by_path(app, user.paths)
    if message.text in current_level:
      user.paths.append(message.text)
      user.answers.append(
        f"Выбери интересующий тебя подраздел в теме '{message.text}':"
      )
      await update_state(message, app)
  return handler
#! [theme_handler]


#! [menu_selector]
def menu_selector(app):
  async def handler(message: Message):
    user = app.users.get_user(message.chat.id)
    current_level = get_by_path(app, user.paths)
    if message.text in current_level:
      user.paths.append(message.text)
      user.answers.append(
        f"Что будем делать в теме {message.text} – решать задачи или читать теорию?"
      )
      await update_state(message, app)
  return handler
#! [menu_selector]


#! [back_handler]
def back_handler(app):
  async def handler(message: Message):
    user = app.users.get_user(message.chat.id)
    if user.paths:
      user.paths.pop()
    if len(user.answers) > 1:
      user.answers.pop()
    
    await update_state(message, app)
  
  return handler
#! [back_handler]

#! [get_by_path]
def get_by_path(app, path: list) -> dict:
  current = app.all_themes
  
  for step in path:
    current = current[step]
  
  return current
#! [get_by_path]


#! [update_state]
async def update_state(message: Message, app) -> None:
  user = app.users.get_user(message.chat.id)
  current = get_by_path(app, user.paths)
  
  
  if user.paths and user.paths[-1] == "Теория":
    filepath = get_by_path(app, user.paths)
    await message.answer(
      f"Отлично! Держи файл с теорией на тему '{user.paths[-2]}'.",
      reply_markup=create_keyboard([], "Назад")
    )
    print(f"DEBUG: {type(message.chat.id)}")
    await send_file(app, filepath, message)
    return

  #! tasks
  if user.paths and user.paths[-1] == "Задачи":
    count = len(current)
    await message.answer(
      f"В базе {count} {pluralize_tasks(count)} по теме {user.paths[-2]}.\nКакую задачу выберите?",
      reply_markup=create_keyboard([], "Назад")
    )
    return
  #! tasks
  
  #! constants
  if user.paths and user.paths[-1] == "Константы и табличные значения":
    await message.answer(
      f"Держи файл со всеми константами и табличными значениями.", 
      reply_markup=create_keyboard([], "Назад")
    )
    await send_file(app, current, message)
    return
  #! constants

  #! showing buttons
  keyboard = create_keyboard(list(current.keys()), "Назад")
  if not user.answers:
    await choose_command(app)(message)
    return
  await message.answer(user.answers[-1], reply_markup=keyboard)
  #! showing buttons

#! [update_state]

from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from bot.utils import pluralize_tasks
from bot.keyboards import create_keyboard


def register_handlers(dp: Dispatcher, app):
  dp.message.register(constants(app), Command("constants"))
  dp.message.register(start_command(app), Command("start"))
  dp.message.register(choose_command(app), Command("choose"))
  dp.message.register(theme_handler(app))
  dp.message.register(menu_selector(app))
  dp.message.register(back_handler(app))


def start_command(app):
  async def handler(message: Message):
    app.users.clear_user(message.chat.id)
    await message.answer(
      f"Привет, {message.from_user.first_name}!\n{app.scripts['start_hello_command']}"
    )
    print(f"LOG: {message.chat.id} ({message.from_user.username}) requested /start")
    await choose_command(app)(message)
  return handler


def choose_command(app):
  async def handler(message: Message):
    user = app.users.get_user(message.chat.id)
    user.answers.append("Выбери интересующий тебя раздел:")
    await update_state(message, app)
  return handler


def constants(app):
  async def handler(message: Message):
    user = app.users.get_user(message.chat.id)
    user.answers.append("Держи файл со всеми константами.")
    await update_state
  return handler


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


def back_handler(app):
  async def handler(message: Message):
    user = app.users.get_user(message.chat.id)
    if user.paths:
      user.paths.pop()
    if len(user.answers) > 1:
      user.answers.pop()
    await update_state(message, app)
  
  return handler


def get_by_path(app, path: list) -> dict:
  current = app.all_themes
  for step in path:
    current = current[step]
  return current


async def update_state(message: Message, app) -> None:
  user = app.users.get_user(message.chat.id)
  current = get_by_path(app, user.paths)
  
  # Теория
  if user.paths and user.paths[-1] == "Теория":
    filepath = get_by_path(app, user.paths)
    await message.answer(
      f"Отлично! Держи файл с теорией на тему '{user.paths[-2]}'.",
      reply_markup=create_keyboard([], "Назад")
    )
    print(f"DEBUG: {type(message.chat.id)}")
    try:
      with open(filepath, 'rb') as file:
        await app.bot.send_document(
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

  # Задачи
  if user.paths and user.paths[-1] == "Задачи":
    count = len(current)
    await message.answer(
      f"В базе {count} {pluralize_tasks(count)} по теме {user.paths[-2]}.\nКакую задачу выберите?",
      reply_markup=create_keyboard([], "Назад")  # Кнопка Назад
    )
    return

  # Показываем кнопки
  keyboard = create_keyboard(list(current.keys()), "Назад")
  if not user.answers:
    await choose_command(app)(message)
    return
  await message.answer(user.answers[-1], reply_markup=keyboard)
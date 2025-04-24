import json

from aiogram import *
from asyncio import *
from aiogram.types import Message

#! [read_from_json]
def read_from_json(filename: str) -> dict:
  with open(f"{filename}.json", "r", encoding="utf-8") as fp:
    return json.load(fp)
#! [read_from_json]

#! pluralize_tasks
def pluralize_tasks(n: int) -> str:
  if n % 10 == 1 and n % 100 != 11:
    return "задача"
  elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
    return "задачи"
  return "задач"
#! [pluralize_tasks]

#! [generate_task_list]
def generate_task_list(tasks: dict) -> str:
  task_list = []
  for i, task in enumerate(tasks.values(), start=1):
    task_list.append(f'Задача {i}. "{task['Name']}"')
  return "\n".join(task_list)
#! [generate_task_list]

#! [send_file]
async def send_file(app, filepath, message:Message) -> None:
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
    print(f"WARNING: {message.chat.id} ({message.from_user.username}) requested file, but it was not found in {filepath}")
    
  except Exception as err:
    await message.answer("Произошла ошибка при отправке файла.")
    print(f"ERROR: {message.chat.id} ({message.from_user.username}) caught error: {err}")
#! [send_file]

#! [send_photo]
async def send_photo(app, filepath, message:Message) -> None:
  try:
    with open(filepath, 'rb') as file:
      await app.bot.send_photo(
        chat_id=message.chat.id,
        photo=types.BufferedInputFile(
          file.read(),
          filename=filepath.split('/')[-1]
        )
      )
      
  except FileNotFoundError:
    await message.answer("Фотография не найдена. Пожалуйста, сообщите администратору.")
    print(f"WARNING: {message.chat.id} ({message.from_user.username}) requested photo, but it was not found in {filepath}")
    
  except Exception as err:
    await message.answer("Произошла ошибка при отправке файла.")
    print(f"ERROR: {message.chat.id} ({message.from_user.username}) caught error while receiving photo: {err}")
#! [send_photo]
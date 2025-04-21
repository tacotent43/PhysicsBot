import json
from aiogram import *
from asyncio import *


def read_from_json(filename: str) -> dict:
  with open(f"{filename}.json", "r", encoding="utf-8") as fp:
    return json.load(fp)


def get_tasks_from_json(path: str) -> dict:
  try:
    with open(path + "tasks.json", "r", encoding="utf-8") as fp:
      return json.load(fp)
  except FileNotFoundError:
    print("tasks file not found")


def pluralize_tasks(n: int) -> str:
  if n % 10 == 1 and n % 100 != 11:
    return "задача"
  elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
    return "задачи"
  return "задач"


#TODO: move send_file function here (check await and message type)
# def send_file(filepath:str, app, chat_id:) -> None:
#   try:
#     with open(filepath, 'rb') as file:
#       await app.bot.send_document(
#         chat_id=message.chat.id,
#         document=types.BufferedInputFile(
#           file.read(),
#           filename=filepath.split('/')[-1]
#         )
#       )
#   except FileNotFoundError:
#     await message.answer("Файл не найден. Пожалуйста, сообщите администратору.")
#   except Exception as err:
#     await message.answer("Произошла ошибка при отправке файла.")
#     print(f"Ошибка отправки файла: {err}")
#   return
from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

from bot.utils import pluralize_tasks
from bot.utils import send_file
from bot.utils import read_from_json
from bot.utils import generate_task_list
from bot.utils import send_photo
from bot.utils import check_task

from bot.keyboards import create_task_keyboard
from bot.keyboards import create_keyboard

#! [register_handlers]
def register_handlers(dp: Dispatcher, app):
  dp.message.register(start_command(app), Command("start"))
  dp.message.register(choose_command(app), Command("choose"))
  dp.message.register(main_handler(app))
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

#! [main_handler] <- !!!
def main_handler(app):
  async def handler(message: Message):
    user = app.users.get_user(message.chat.id)
    print(f"LOG: in main_handler '{message.text}' len: {len(user.paths)} paths: {user.paths}")
    if len(user.paths) == 0:
      await theme_handler(app)(message)
    elif len(user.paths) == 1:
      await subtheme_handler(app)(message)
    elif len(user.paths) == 2:
      await theory_handler(app)(message)
    elif len(user.paths) == 3:
      await task_handler(app)(message)
    elif len(user.paths) == 4:
      await subtask_handler(app)(message)
    elif len(user.paths) == 5:
      await answer_check_handler(app)(message)
    else:
      await back_handler(app)(message)
  return handler
#! [main_handler]

#! [theme_handler]
def theme_handler(app):
  async def handler(message: Message):
    print(f"LOG: in theme_handler: {message.text}")
    user = app.users.get_user(message.chat.id)
    current_level = get_by_path(app, user.paths)
    # TODO: refactor this
    if message.text in current_level and message.text != "Константы и табличные значения":
      user.paths.append(message.text)
      user.answers.append(
        f"Выбери интересующий тебя подраздел в теме '{message.text}':"
      )
      await update_state(message, app)
    elif message.text in current_level and message.text == "Константы и табличные значения": 
      user.paths.append(message.text)
      user.answers.append(
        f"Держи файл со всеми константами и табличными значениями."
      )
      await send_file(app, current_level, message)
      user.paths.pop()
      await update_state(message, app)
    else:
      await back_handler(app)(message)
  return handler
#! [theme_handler]

#! [subtheme_handler]
def subtheme_handler(app):
  async def handler(message: Message):
    print(f"LOG: in SUBTHEME_HANDLER {message.text}")
    user = app.users.get_user(message.chat.id)
    current_level = get_by_path(app, user.paths)
    if message.text in current_level:
      user.paths.append(message.text)
      user.answers.append(
        f"Что будем делать в теме {message.text} – решать задачи или читать теорию?"
      )
      await update_state(message, app)
    else:
      await back_handler(app)(message)
  return handler
#! [subtheme_handler]

#! [back_handler]
def back_handler(app):
  async def handler(message: Message):
    print(f"LOG: in BACK_HANDLER {message.text}")
    user = app.users.get_user(message.chat.id)
    if message.text == "Назад":
      if user.paths:
        user.paths.pop()
      if len(user.answers) > 1:
        user.answers.pop()
    await update_state(message, app)
  
  return handler
#! [back_handler]

#! [theory_handler]
def theory_handler(app):
  async def handler(message: Message):
    user = app.users.get_user(message.chat.id)
    paths = user.paths
    current = get_by_path(app, user.paths)
    print(f"LOG: in THEORY_HANDLER {message.text}; current: {current}")
    if message.text == "Теория":
      paths.append("Теория")
      print(f"LOG: in THEORY_HANDLER {message.text}; current: {current}")
      current = get_by_path(app, user.paths)
      await message.answer(
        f"Отлично! Держи файл с теорией на тему '{user.paths[-2]}'.",
        reply_markup=create_keyboard([], "Назад")
      )
      print(f"LOG: {message.chat.id} ({message.from_user.username}) requested file: {current}")
      await send_file(app, current, message)
      paths.pop()
      await update_state(message, app)
    elif message.text == "Задачи":
      paths.append("Задачи")
      print(f"LOG: in THEORY_HANDLER Задачи / paths: {paths}; current: {current}")
      current = get_by_path(app, user.paths)
      tasks = read_from_json(current)
      user.answers.append(
        f"Отлично! Держи список задач на тему <b>'{user.paths[-2]}'</b>.\n\n{generate_task_list(tasks)}.\n\n<b>Чтобы выбрать задачу, просто отправь мне её номер.</b>\n",
      )
      print(f"LOG: in theory/tasks: {app.users.get_user(message.chat.id).paths}")
      await update_state(message, app)
    else:
      await back_handler(app)(message)
  return handler
#! [theory_handler]

#! [task_handler]
# TODO: fix and recheck numeration here (& refactor) ->
def task_handler(app):
  async def handler(message: Message):
    user = app.users.get_user(message.chat.id)
    paths = user.paths
    current_level = get_by_path(app, user.paths)
    tasks = read_from_json(current_level)
    if message.text.isdigit() and 1 <= int(message.text) <= len(tasks):
      task_number = int(message.text)
      user.answers.append(
        f"Отлично! Вы выбрали задачу номер <b><i>{task_number}</i></b> - <b>'{tasks["task" + str(task_number)]["Name"]}</b>'.\n"
        f"<b>Условие: </b>\n{tasks["task" + str(task_number)]['Condition']}\n"
      )
      print(f"LOG: in TASK_HANDLER 'Задача номер'; current: {current_level}; tasks: {tasks["task" + str(task_number)]}")
      user.current_task = tasks["task" + str(task_number)]
      paths.append(task_number)
      await update_state(message, app)
    else:
      await back_handler(app)(message)
  return handler
#! [task_handler]

#! [subtask_handler]
# TODO: implement & find potential problems
def subtask_handler(app):
  async def handler(message: Message):
    user = app.users.get_user(message.chat.id)
    current_level = get_by_path(app, user.paths)
    paths = app.users.get_user(message.chat.id).paths
    
    print(f"DEBUG: subtask_handler {paths}")
    print(f"LOG: in SUBTASK_HANDLER {message.text}; current: {current_level}")
    
    if message.text == "Решить задачу":
      print(f"LOG: in SUBTASK_HANDLER 'Решить задачу'; current: {current_level}")
      if not(user.current_task['Answer']):
        user.answers.append(
          f"К сожалению, на эту задачу временно нет ответа.\n"
          f"Но ты можешь попробовать решить задачу самостоятельно.\n"
        )
        print(f"LOG: NO_ANSWER_WARN")
        await update_state(message, app)
      
      paths.append("Решить задачу")
      await message.answer(f"Хорошо! Я жду от тебя ответ, проверю его, и скажу, правильный ли он.")

      user_answer = str(message.text)
      
      if check_task(user_answer, user.current_task['Answer']):
        await message.answer(f"Отлично, твой ответ правильный!")
      else:
        await message.answer(f"К сожалению, твой ответ не правильный. Можешь подумать ещё или посмотреть ответ на задачу.")
      
      # user.answers.append(
      #   f"К сожалению, данная функция временно недоступна.\n"
      #   f"Но ты можешь попробовать решить задачу самостоятельно, а затем посмотреть ответ или решение.\n"
      # )
      
      print(f"LOG: in SUBTASK_HANDLER (end) 'Решить задачу'; paths: {paths}")
      await update_state(message, app)
      
    elif message.text == "Посмотреть ответ":
      print(f"LOG: in SUBTASK_HANDLER 'Посмотреть ответ'; current: {current_level}")
      await message.answer(f"Ответ: {user.current_task['Answer']}")
      
    elif message.text == "Посмотреть решение":
      print(f"LOG: in SUBTASK_HANDLER 'Посмотреть решение'; paths: {paths}")
      
      if user.current_task['ExplanationPicture']:
        await send_photo(app, user.current_task['ExplanationPicture'], message, f"Держи решение задачи №{paths[-1]}:")
      
      else:
        await message.answer(f"К сожалению, решение задачи этой задачи временно отсутствует.\nНо ты можешь попробовать решить задачу самостоятельно, а затем посмотреть ответ или решение.\n")
        
    else:
      await back_handler(app)(message)
  return handler
#! [subtask_handler]

#! [answer_check_handler]
# TODO: ?maybe refactor
def answer_check_handler(app):
  async def handler(message: Message):
    user = app.users.get_user(message.chat.id)
    current_level = get_by_path(app, user.paths)
    
    print(f"LOG: in ANSWER_CHECK_HANDLER {message.text}; current: {current_level}")
    if message.text == user.current_task["Answer"]:
      user.answers.append(
        f"Поздравляю! Ты правильно решил задачу номер {user.paths[-2]}.\n"
        f"Если ты хочешь, можешь посмотреть решение задачи."
      )
    
    else:
      user.answers.append(
        f"К сожалению, ты ошибся в решении задачи номер {user.paths[-2]}.\n"
        f"Попробуй ещё раз или посмотри решение задачи."
      )
      
    user.paths.pop()
    print(f"LOG: in ANSWER_CHECK_HANDLER (end) {message.text}; path: {user.paths}")
    await update_state(message, app)
    
  return handler
#! [answer_check_handler]

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
  
  print(f"LOG: in update_state {message.text};\t\ncurrent: {current};\t\npaths: {user.paths}\t\nlatest: {user.paths[-1] if user.paths else ""}")
  
  #! showing buttons
  # TODO: refactor this piece of craph
  if user.paths and (user.paths[-1] == "Задачи" or user.paths[-1] == "Решить задачу"):
    keyboard = create_keyboard([], "Назад")
  
  elif user.paths and isinstance(user.paths[-1], int) and user.paths[-2] == "Задачи":
    keyboard = create_keyboard(["Решить задачу", "Посмотреть ответ", "Посмотреть решение"], "Назад")
    
  elif user.paths and user.paths[-1] == "Константы и табличные значения":
    keyboard = create_keyboard([], "Назад")
  
  else: 
    buttons_names = list(current.keys())
    if len(user.paths) == 0:
      keyboard = create_keyboard(buttons_names)
    else:
      keyboard = create_keyboard(buttons_names, "Назад")
  
  if not user.answers:
    await choose_command(app)(message)
    return

  await message.answer(user.answers[-1], reply_markup=keyboard, parse_mode="HTML")
  #! showing buttons

#! [update_state]

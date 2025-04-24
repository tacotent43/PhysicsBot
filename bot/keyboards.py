from typing import List
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def create_keyboard(items: List[str], back_text=None) -> ReplyKeyboardMarkup:
  builder = ReplyKeyboardBuilder()
  for item in items:
    builder.add(KeyboardButton(text=item))
    
  if back_text is not None:
    builder.add(KeyboardButton(text=back_text))
    
  builder.adjust(2)
  return builder.as_markup(resize_keyboard=True)

def create_task_keyboard() -> ReplyKeyboardMarkup:
  builder = ReplyKeyboardBuilder()
  builder.add(KeyboardButton(text="Решить задачу"))
  builder.add(KeyboardButton(text="Посмотреть ответ"))
  builder.add(KeyboardButton(text="Посмотреть решение"))
  builder.add(KeyboardButton(text="Назад"))
  return builder.as_markup(resize_keyboard=True)
from typing import List
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def create_keyboard(items: List[str], back_text: str) -> ReplyKeyboardMarkup:
  builder = ReplyKeyboardBuilder()
  for item in items:
    builder.add(KeyboardButton(text=item))
  builder.add(KeyboardButton(text=back_text))
  builder.adjust(2)
  return builder.as_markup(resize_keyboard=True)

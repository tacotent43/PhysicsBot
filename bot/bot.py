from aiogram import Bot, Dispatcher
from state.storage import UserStorage
from bot.utils import read_from_json
from bot.handlers import register_handlers

class PhysicsBot:
  def __init__(self):
    self.config = read_from_json("./data/config")
    self.all_themes = read_from_json("./data/themes")
    self.scripts = read_from_json("./data/scripts")

    self.bot = Bot(token=self.config["API_KEY"])
    self.dp = Dispatcher()
    self.users = UserStorage()

    register_handlers(self.dp, self)

  def _get_by_path(self, path):
    current = self.all_themes
    for step in path:
      current = current[step]
    return current

  async def run(self):
    await self.dp.start_polling(self.bot)

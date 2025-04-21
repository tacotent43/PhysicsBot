from typing import Dict
from state.user_data import UserData

class UserStorage:
  def __init__(self):
    self._users: Dict[int, UserData] = {}

  def add_user(self, user_id: int) -> None:
    self._users[user_id] = UserData()

  def get_user(self, user_id: int) -> UserData:
    if user_id not in self._users:
      self.add_user(user_id)
    return self._users[user_id]

  def clear_user(self, user_id: int) -> None:
    if user_id in self._users:
      self._users[user_id] = UserData()

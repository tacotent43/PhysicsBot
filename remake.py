import json
from dataclasses import dataclass


@dataclass
class Debug:
  pass

@dataclass
class userData:
  paths = []
  answers = []
  
class Users:
  def __init__(self):
    self._users = {}
  
  def addUser(id, self):
    self._users[id] = userData
  
  def getUsers(id, self):
    if id not in self._users:
      self.addUser(id, self)
    return self._users
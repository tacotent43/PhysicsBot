from dataclasses import dataclass, field
from typing import List

@dataclass
class UserData:
  paths: List[str] = field(default_factory=list)
  answers: List[str] = field(default_factory=list)
  current_task: str = ""

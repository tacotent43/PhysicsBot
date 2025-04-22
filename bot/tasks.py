import json
import aiogram


def get_task_from_json(task_number: int) -> dict:
  with open(f"task{task_number}.json", "r", encoding="utf-8") as fp:
    return json.load(fp)
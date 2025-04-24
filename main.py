from bot.bot import PhysicsBot
import asyncio

if __name__ == "__main__":
  bot = PhysicsBot()
  asyncio.run(bot.run())
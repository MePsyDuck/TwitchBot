from tortoise import Tortoise

from db.config import DB_URL
from db.models import *


async def init():
    await Tortoise.init(db_url=DB_URL, modules={"models": ['db.models']})
    await Tortoise.generate_schemas(safe=True)


async def close():
    await Tortoise.close_connections()

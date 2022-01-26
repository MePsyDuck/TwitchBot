from tortoise import Tortoise

from .config import DB_URL
from .models import *


async def init():
    await Tortoise.init(db_url=DB_URL, modules={"models": ['db.models']})
    await Tortoise.generate_schemas(safe=True)


async def close():
    await Tortoise.close_connections()

import urllib.parse as up

from pony.orm import db_session

from db.config import DB_URL, DB_PROVIDER
from db.models import db, FishingStats, User


class DatabaseAPI:
    def __init__(self):
        self.db = db
        if DB_PROVIDER == 'sqlite':
            self.db.bind(provider='sqlite', filename=DB_URL, create_db=True)
        elif DB_PROVIDER == 'mysql':
            up.uses_netloc.append("mysql")
            url = up.urlparse(DB_URL)
            self.db.bind(provider='mysql', host=url.hostname, user=url.username, passwd=url.password, db=url.path[1:])
        elif DB_PROVIDER == 'postgres':
            up.uses_netloc.append("postgres")
            url = up.urlparse(DB_URL)
            self.db.bind(provider='postgres', user=url.username, password=url.password, host=url.hostname,
                         database=url.path[1:])
        else:
            self.db.bind(provider='sqlite', filename='bot.db', create_db=True)

        self.db.generate_mapping(check_tables=False)

    @db_session
    def add_user(self, username: str):
        user = User(username=username)
        fishing_stats = FishingStats(user=user)
        return user

    @db_session
    def get_fishing_stats(self, username: str):
        username = username.lower()

        user = User.get(username=username) or self.add_user(username)
        stats = user.fishing_stats
        return stats

    @db_session
    def update_for_snaps(self, username: str):
        username = username.lower()

        user = User.get(username=username) or self.add_user(username)
        user.fishing_stats.casts += 1
        user.fishing_stats.snaps += 1

    @db_session
    def update_for_catch(self, username: str, fish: str, points: int):
        username = username.lower()
        fish = fish.lower()

        user = User.get(username=username) or self.add_user(username)
        user.fishing_stats.casts += 1
        user.fishing_stats.catches += 1
        user.fishing_stats.biggest_catch = max(user.fishing_stats.biggest_catch, points)

        fish = User.get(username=fish) or self.add_user(fish)
        fish.times_caught += 1

    @db_session
    def update_casts(self, username: str):
        username = username.lower()

        user = User.get(username=username) or self.add_user(username)
        user.fishing_stats.casts += 1


db_api = DatabaseAPI()

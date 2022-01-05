from pony.orm import Database, Required, Optional

db = Database()


class FishingStats(db.Entity):
    user = Required(lambda: User, column="user_id")
    casts = Required(int, default=0)
    snaps = Required(int, default=0)
    catches = Required(int, default=0)
    times_caught = Required(int, default=0)
    biggest_catch = Required(int, default=0)


class User(db.Entity):
    username = Required(str, max_len=50, unique=True)
    fishing_stats = Optional(FishingStats)

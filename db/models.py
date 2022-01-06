from tortoise import fields

from tortoise.models import Model


class FishingStats(Model):
    username = fields.CharField(max_length=64, unique=True)
    casts = fields.IntField(default=0)
    snaps = fields.IntField(default=0)
    catches = fields.IntField(default=0)
    times_caught = fields.IntField(default=0)
    biggest_catch = fields.IntField(default=0)

    def __str__(self):
        return f'{self.username}, casts={self.casts}, snaps={self.snaps}, catches={self.catches}, biggest_catch={self.biggest_catch}, ' \
               f'times_caught={self.times_caught}'


class RandomPingStats(Model):
    username = fields.CharField(max_length=64, unique=True)
    random_pings = fields.IntField(default=0)
    times_pinged = fields.IntField(default=0)

    def __str__(self):
        return f'{self.username}, random_pings={self.random_pings}, times_pinged={self.times_pinged}'

from tortoise import fields

from tortoise.models import Model


class FishingStats(Model):
    fisherman = fields.CharField(max_length=64, unique=True)
    casts = fields.IntField(default=0)
    snaps = fields.IntField(default=0)

    def __str__(self):
        return f'{self.fisherman}, casts={self.casts}, snaps={self.snaps}'


class FishingLogs(Model):
    fisherman = fields.CharField(max_length=64, index=True)
    fish = fields.CharField(max_length=64, index=True)
    points = fields.IntField(default=1)
    when = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.fisherman}, caught {self.fish} for {self.points} points at {self.when}'


class RandomPingStats(Model):
    username = fields.CharField(max_length=64, unique=True)
    random_pings = fields.IntField(default=0)
    times_pinged = fields.IntField(default=0)

    def __str__(self):
        return f'{self.username}, random_pings={self.random_pings}, times_pinged={self.times_pinged}'


class ChannelStats(Model):
    channel = fields.CharField(max_length=64)
    key = fields.CharField(max_length=64)
    value = fields.CharField(max_length=256, default='')

    def __str__(self):
        return f'{self.channel}: [{self.key} = {self.value}]'

    class Meta:
        unique_together = ("channel", "key")

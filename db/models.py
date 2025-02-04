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


class ShootoutStats(Model):
    username = fields.CharField(max_length=64, unique=True)
    current_loss_streak = fields.IntField(default=0)
    highest_loss_streak = fields.IntField(default=0)
    total_lost = fields.IntField(default=0)
    current_win_streak = fields.IntField(default=0)
    highest_win_streak = fields.IntField(default=0)
    total_won = fields.IntField(default=0)
    duels_started = fields.IntField(default=0)
    duels_accepted = fields.IntField(default=0)

    def __str__(self):
        return f'{self.username}({self.duels_started}/{self.duels_accepted}), ' \
               f'loss :[{self.current_loss_streak}/{self.highest_loss_streak}/{self.total_lost}], ' \
               f'won :[{self.current_win_streak}/{self.highest_win_streak}/{self.total_won}]'


class ShootoutLogs(Model):
    challenger = fields.CharField(max_length=64)
    target = fields.CharField(max_length=64)
    winner = fields.CharField(max_length=64)
    loser = fields.CharField(max_length=64)
    when = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.challenger} vs {self.target} : {self.loser} lost at {self.when}'


class RollLogs(Model):
    username = fields.CharField(max_length=64, unique=True)
    rolled_value = fields.IntField(default=-1)
    when = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username} rolled {self.rolled_value} at {self.when}'


class RollStats(Model):
    username = fields.CharField(max_length=64, unique=True)
    rolls = fields.IntField(default=0)

    def __str__(self):
        return f'{self.username} tried rolling {self.rolls} times'

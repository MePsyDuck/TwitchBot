"""
1) stop bot
2) rename old log to bot.log.old
3) rename db to bot.db.old
4) start bot

5) make a copy of bot.log.old called bot.txt
6) download bot.txt

7) find the cutoff date
8) truncate app.txt content before cut off date
9) test replay script

10) upload bot.txt
11) run replay script
"""
from dotenv import load_dotenv

load_dotenv()  # should happen first, even before imports


async def replay():
    await Tortoise.init(db_url=DB_URL, modules={"models": ['db.models']})
    await Tortoise.generate_schemas(safe=True)

    with open('bot.txt') as f:
        lines = f.readlines()

    for line in lines:
        if 'event_message' in line:
            # logger.info(f'{fisherman} snapped')
            if match := regex.search(r'(?P<fisherman>[\p{L}|\p{N}_]+) snapped', line):
                fisherman = match.group('fisherman')
                fisherman_stats, _ = await FishingStats.get_or_create(fisherman=fisherman)
                fisherman_stats.snaps = F('snaps') + 1
                await fisherman_stats.save()

            # logger.info(f'{fisherman} caught {fish} for {points} points')
            elif match := regex.search(r'(?P<when>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) INFO\s+bot\s+'
                                       r'event_message\s+(?P<fisherman>[\p{L}|\p{N}_]+) caught '
                                       r'(?P<fish>[\p{L}|\p{N}_]+) for (?P<points>\d+) points', line):
                when = match.group('when')
                fisherman = match.group('fisherman')
                fish = match.group('fish')
                points = int(match.group('points'))
                await FishingLogs.create(fisherman=fisherman, fish=fish, points=points, when=when)

            # logger.info(f'{fisherman} tried casting')
            elif match := regex.search(r'(?P<fisherman>[\p{L}|\p{N}_]+) tried casting', line):
                fisherman = match.group('fisherman')
                fisherman_stats, _ = await FishingStats.get_or_create(fisherman=fisherman)
                fisherman_stats.casts = F('casts') + 1
                await fisherman_stats.save()

            # logger.info(f'pinged: {pinged_users}')
            elif match := re.search(r'pinged: (?P<users>([a-zA-Z0-9_]{4,25}\s?)+)', line):
                pinged_users = match.group('users').lower()

                for user in re.findall(r'([a-zA-Z0-9_]{4,25})\s?', pinged_users):
                    ping_stats, _ = await RandomPingStats.get_or_create(username=user)
                    ping_stats.times_pinged = F('times_pinged') + 1
                    await ping_stats.save()

            # logger.info(f'{user} randompinged')
            elif match := regex.search(r'(?P<user>[\p{L}|\p{N}_]+) randompinged', line):
                user = match.group('user')
                ping_stats, _ = await RandomPingStats.get_or_create(username=user)
                ping_stats.random_pings = F('random_pings') + 1
                await ping_stats.save()
            else:
                print(f'didnt match any pattern : {line}')
        else:
            print(f'not event_message : {line}')


if __name__ == "__main__":
    import re
    from regex import regex

    from tortoise import Tortoise, run_async
    from tortoise.expressions import F

    from db import FishingStats, FishingLogs, RandomPingStats, DB_URL

    run_async(replay())

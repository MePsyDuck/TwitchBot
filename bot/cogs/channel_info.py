import datetime

import humanize
from twitchio import HTTPException
from twitchio.ext import commands
from twitchio.ext.eventsub import NotificationEvent

from bot.cogs.base import BaseCog, bot_client, eventsub_client
from bot.config import COOLDOWN, CHANNELS, DATETIME_FORMAT
from db import ChannelStats
from logs import logger

KEY_LAST_OFFLINE = 'last_offline'
KEY_LAST_LIVE = 'last_live'


@bot_client.event()
async def event_eventsub_notification_stream_start(notification_event: NotificationEvent):
    live_event = notification_event.data
    last_live, _ = await ChannelStats.get_or_create(channel=live_event.broadcaster.name, key=KEY_LAST_LIVE)
    last_live.value = live_event.started_at.strftime(DATETIME_FORMAT)
    await last_live.save()


@bot_client.event()
async def event_eventsub_notification_stream_end(notification_event: NotificationEvent):
    offline_event = notification_event.data
    last_offline, _ = await ChannelStats.get_or_create(channel=offline_event.broadcaster.name,
                                                       key=KEY_LAST_OFFLINE)
    last_offline.value = datetime.datetime.utcnow().strftime(DATETIME_FORMAT)
    await last_offline.save()


class ChannelInfoCog(BaseCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @commands.Cog.event()
    async def event_ready(self):
        users = [user.id for user in await self.bot.fetch_users(names=CHANNELS)]
        subs = await eventsub_client.get_subscriptions()
        for sub in subs:
            if sub.type in ['stream.online', 'stream.offline']:
                await eventsub_client.delete_subscription(sub.id)
        for user in users:
            try:
                await eventsub_client.subscribe_channel_stream_start(broadcaster=user)
                await eventsub_client.subscribe_channel_stream_end(broadcaster=user)
            except HTTPException as e:
                logger.critical(e, exc_info=True)

    @commands.command()
    @commands.cooldown(rate=1, per=COOLDOWN * 10, bucket=commands.Bucket.default)
    async def downtime(self, ctx: commands.Context):
        last_live = await ChannelStats.get_or_none(channel=ctx.channel.name, key=KEY_LAST_LIVE)
        last_offline = await ChannelStats.get_or_none(channel=ctx.channel.name, key=KEY_LAST_OFFLINE)
        if last_offline:
            last_offline_dt = datetime.datetime.strptime(last_offline.value, DATETIME_FORMAT)
            if last_live and datetime.datetime.strptime(last_live.value, DATETIME_FORMAT) > last_offline_dt:
                await ctx.send('strimer is currently live you Pepega')
            else:
                delta = humanize.precisedelta(datetime.datetime.utcnow() - last_offline_dt, minimum_unit="minutes",
                                              format="%0.0f")
                await ctx.send(f'strimer last streamed {delta} ago')

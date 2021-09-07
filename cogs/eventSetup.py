import discord, json, asyncio, datetime

from discord.ext import commands
from discord.utils import get 
from lib import FileHandler

fh = FileHandler()


class EventSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    def load_data(self):
        self.id = fh.load_file('id')
        self.event = fh.load_file("event")

    def validate_date(self, date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError as e:
            raise e

    def validate_time(self, time_text):
        try:
            datetime.datetime.strftime(time_text, '%H:%M')    
        except ValueError as e:
            raise e

    @commands.command(name = "eventsetup")
    async def eventsetup_cmd(self, ctx):
        guild = ctx.message.guild
        member = guild.get_member(ctx.author.id)
        dt_role = discord.utils.get(guild.roles, name = "Dream Team")

        if dt_role in member.roles:
            self.load_data()
            new_events_channel = self.bot.get_channel(self.id["events_channel"])
            if new_events_channel == ctx.channel:
                await new_events_channel.purge(limit = 50)
                await self.NewEventMsg
            else:
                await ctx.channel.send("Wrong channel")

    async def NewEventMsg(self):
        self.load_data() 

        new_event_embed = discord.Embed(title = "Create new events here!", color=0x303136)
        new_event_embed.add_field(name = "\u200B", value = "**React to this mesage with the type of event you would like to create", inline = False)
        new_event_embed.add_field(name = "\u200B", value = ":alarm_clock: Doodle(Time finder)\n:date: Meeting\n:game_die: Game Jam")


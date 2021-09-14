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
        new_event_channel = self.bot.get_channel(self.id["new_events_channel"])

        new_event_embed = discord.Embed(title = "Create new events here!", color=0x303136)
        new_event_embed.add_field(name = "\u200B", value = "**React to this mesage with the type of event you would like to create", inline = False)
        new_event_embed.add_field(name = "\u200B", value = ":alarm_clock: Doodle(Date finder)\n:date: Meeting\n:game_die: Game Jam")
        new_event_msg = await new_event_channel.send(embed = new_event_embed)
        new_event_msg_id = new_event_msg.id

        await new_event_msg.add_reaction(emoji = '\u23F0')          # alarm clock
        await new_event_msg.add_reaction(emoji = '\U0001F4C5')      # date
        await new_event_msg.add_reaction(emoji = '\U0001F3B2')      # game die

        self.id["new_event_msg_id"] = new_event_msg_id
        fh.save_file(self.id, "id")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        self.load_data()
        if payload.user_id == self.id['bot_id']:
            return

        elif payload.message_id == self.id['new_event_msg_id']:
            guild = self.got.get_guild(payload.guild_id)
            events_channel = self.bot.get_channel(self.id['events_channel'])
            reaction = payload.emoji.name

            event_type = "none"
            if reaction == '\u23F0':            # alarm clock
                event_type = "doodle"
            elif reaction == '\U0001F4C5':
                event_type = "meeting"
            elif reaction == '\U0001F3B2':
                event_type = "jam"
            await events_channel.purge(limit = 5)

            date_embed = discord.Embed(title = f"You have chosen to create a **{event_type}** event", color=0x303136)
            
        



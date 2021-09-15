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
            new_events_channel = self.bot.get_channel(self.id["new_events_channel"])
            if new_events_channel == ctx.channel:
                await new_events_channel.purge(limit = 50)
                await self.NewEventMsg()
            else:
                await ctx.channel.send("Wrong channel")

    async def NewEventMsg(self):
        self.load_data() 
        new_event_channel = self.bot.get_channel(self.id["new_events_channel"])

        new_event_embed = discord.Embed(title = "Create new events here!", color=0x303136)
        new_event_embed.add_field(name = "\u200B", value = "**React to this mesage with the type of event you would like to create**", inline = False)
        new_event_embed.add_field(name = "\u200B", value = ":alarm_clock: Doodle (Date finder)\n:date: Meeting\n:game_die: Game Jam")
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
            guild = self.bot.get_guild(payload.guild_id)
            new_events_channel = self.bot.get_channel(self.id['new_events_channel'])
            reaction = payload.emoji.name

            event_type = "none"
            if reaction == '\u23F0':            # alarm clock
                event_type = "Doodle"
            elif reaction == '\U0001F4C5':
                event_type = "Meeting"
            elif reaction == '\U0001F3B2':
                event_type = "Game Jam"
            await new_events_channel.purge(limit = 5)

# DESCRIPTION
            desc_embed = discord.Embed(title = f"You have chosen to create a **{event_type}** event", color=0x303136)
            desc_embed.add_field(name = '\u200B', value = "Please enter a description for the event.\nMust not be longer than 1020 characters.", inline = False)
            desc_embed.add_field(name = '\u200B', value = ":octagonal_sign: = cancel")
            desc_embed_msg = new_events_channel.send(embed = desc_embed)
            await desc_embed.add_reaction(emoji = '\U0001F6D1')     # :octagonal_sign:
            await asyncio.sleep(1) 

            input_msg = await self.bot.wait_for('message', check=lambda message: message.author == message.author and message.channel == new_events_channel)
            input_msg = input_msg.content
            await new_events_channel.purge(5)

            if input_msg == "cancel":
                await self.NewEventMsg()
                return

            event_desc = ""
            if len(input_msg) < 1020:
                event_desc = input_msg
            else:
                await new_events_channel.send(input_msg)
                desc_too_long_embed = discord.Embed(title = "Your description includes more than 1020 characters. Reduce the amount of characters in order to make an event!")
                await new_events_channel.send(embed = desc_too_long_embed)
                await asyncio.sleep(6)
                await self.NewEventMsg
                return 

# DOODLE
    # Doodle start
            if event_type == "Doodle":
                doodle_start_embed = discord.Embed(title = "The description has been set!", color=0x303136)
                doodle_start_embed.add_field(name = "\u200B", value = "**What date should the doodle start?**\nWrite in this channel.\n*Ex: 2021-01-31*", inline = False)
                doodle_start_embed.add_field(name = '\u200B', value = ":octagonal_sign: = cancel")
                doodle_start_embed_msg = await new_events_channel.send(embed = doodle_start_embed)
                await doodle_start_embed_msg.add_reaction(emoji = '\U0001F6D1')     # :octagonal_sign:
                await asyncio.sleep(1)

                input_msg = await self.bot.wait_for('message', check=lambda message: message.author == message.author and message.channel == new_events_channel)
                input_msg = input_msg.content
                await new_events_channel.purge(limit = 5)

                if input_msg == "cancel":
                    await self.NewEventMsg()
                    return

                doodle_start = ""
                try:
                    self.validate_date(input_msg)
                    if self.validate_date(input_msg) == None:
                        doodle_start = input_msg
                except ValueError:
                    await new_events_channel.send("You have entered a wrong date format.\nFormat must be **YYYY-MM-DD**.\nTry again!")
                    await asyncio.sleep(5)
                    await self.NewEventMsg()
                    return

    # Doodle end
                doodle_end_embed = discord.Embed(title = f"Doodle will start on **{doodle_start}", color = 0x303136)
                doodle_end_embed.add_field(name = "\u200B", value = "**When should the doodle end?**\nWrite in this channel.\n*Ex: 2021-01-31*", inline = False)
                doodle_end_embed.add_field(name = '\u200B', value = ":octagonal_sign: = cancel")
                doodle_end_embed_msg = await new_events_channel.send(embed = doodle_end_embed)
                await doodle_end_embed_msg.add_reaction(emoji = '\U0001F6D1')     # :octagonal_sign:
                await asyncio.sleep(1)
                
                input_msg = await self.bot.wait_for('message', check=lambda message: message.author == message.author and message.channel == new_events_channel)
                input_msg = input_msg.content
                await new_events_channel.purge(limit = 5)

                if input_msg == "cancel":
                    await self.NewEventMsg()
                    return

                doodle_end = ""
                try:
                    self.validate_date(input_msg)
                    if self.validate_date(input_msg) == None:
                        doodle_end = input_msg
                except ValueError:
                    await new_events_channel.send("You have entered a wrong date format.\nFormat must be **YYYY-MM-DD**.\nTry again!")
                    await asyncio.sleep(5)
                    await self.NewEventMsg()
                    return

# MEETING / GAME JAM
    # DATE
            if event_type == "Meeting" or event_type == "Game Jam":
                date_embed = discord.Embed(title = "The description has been set!", color=0x303136)
                date_embed.add_field(name = '\u200B', value = "**What date should the event take place?**\nWrite in this channel.\n*Ex: 2021-01-31*", inline = False)
                date_embed.add_field(name = '\u200B', value = ":octagonal_sign: = cancel")
                date_embed_msg = await new_events_channel.send(embed = date_embed)
                await date_embed_msg.add_reaction(emoji = '\U0001F6D1')     # :octagonal_sign:
                await asyncio.sleep(1)

                input_msg = await self.bot.wait_for('message', check=lambda message: message.author == message.author and message.channel == new_events_channel)
                input_msg = input_msg.content
                await new_events_channel.purge(limit = 5)

                if input_msg == "cancel":
                    await self.NewEventMsg()
                    return

                event_date = ""
                try:
                    self.validate_date(input_msg)
                    if self.validate_date(input_msg) == None:
                        event_date = input_msg
                except ValueError:
                    await new_events_channel.send("You have entered a wrong date format.\nFormat must be **YYYY-MM-DD**.\nTry again!")
                    await asyncio.sleep(5)
                    await self.NewEventMsg()
                    return

    # TIME
                time_embed = discord.Embed(title = f"The chosen date for **{event_type} event** is **{event_date}", color=0x303136)
                time_embed.add_field(name = '\u200B', value = "**What time of day should the event take place?**\nWrite in this channel.\n*Ex: 18:00*", inline = False)
                time_embed.add_field(name = '\u200B', value = ":octagonal_sign: = cancel")
                time_embed_msg = await new_events_channel.send(embed = time_embed)
                await time_embed_msg.add_reaction(emoji = '\U0001F6D1')     # :octagonal_sign:
                await asyncio.sleep(1)

                input_msg = await self.bot.wait_for('message', check=lambda message: message.author == message.author and message.channel == new_events_channel)
                input_msg = input_msg.content
                await new_events_channel.purge(5)

                if input_msg == "cancel":
                    await self.NewEventMsg()
                    return
                
                event_time = ""
                try:
                    self.validate_time(input_msg)
                    if self.validate_time(input_msg) == None:
                        event_time = input_msg
                except ValueError:
                    await new_events_channel.send("You have entered a wrong time date format.\nFormat must be **HH:MM**.\nTry again!")
                    await asyncio.sleep(5)
                    await self.NewEventMsg()
                    return

    # DATE AND TIME CHECK
                event_date_time = f"{event_date} {event_time}"
                if event_date_time in self.event:
                    if event_date == self.event[event_date_time]['date'] and event_time == self.event[event_date_time]['time']:
                        await new_events_channel.send("An event already exists on this date and time.\nTry again with another date or time!")
                        await asyncio.sleep(5)
                        await new_events_channel.purge(5)
                        await self.NewEventMsg()
                        return 

                complete_embed = discord.Embed(title = f"a new event type **{event_type}** has been created!")
                complete_embed.add_field(name = "**Date**", value = event_date, inline = False)
                complete_embed.add_field(name = "**Time**", value = event_time, inline = False)
                complete_embed.add_field(name = "Description", value = event_desc, inline = False)
                await new_events_channel.send(embed = complete_embed)
                await asyncio.sleep(6)
                await new_events_channel.purge(5)
                

def setup(bot):
    bot.add_cog(EventSetup(bot))
            
        



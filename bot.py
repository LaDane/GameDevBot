import discord
import time

from discord.ext import commands
from pathlib import Path
from datetime import datetime 


class GameDevBot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./cogs/*.py")]
        super().__init__(
            command_prefix = self.prefix,
            case_insensitive = True,
            intents = discord.Intents.all()
        )

    def setup(self):
        print("Running setup...")
        for cog in self._cogs:
            self.load_extension(f"cogs.{cog}")
            print(f"Loaded '{cog}' cog.")
        print("Setup complete.")

    def run(self):
        self.setup()

        with open("token/token.0", "r", encoding="utf-8") as f:
            TOKEN = f.read()

        print("Running bot...")
        super().run(TOKEN, reconnect=True)

    async def shutdown(self):
        print("Closing connection to Discord")
        
        starting = False
        await self.StartStopMessage(starting)

        await super().close()

    async def close(self):
        print("Closing on keyboard interrupt...")
        await self.shutdown()

    async def on_connect(self):
        print(f"Connected to Discord (latency: {self.latency*1000:,.0f} ms).")

    async def on_resumed(self):
        datetimeNow = datetime.now()
        resumeTime = datetimeNow.strftime("%A  %d-%m-%Y  %H:%M:%S")
        print(f"Bot resumed at:            {resumeTime}")

    # async def on_error(self, err, *args, **kwargs):
    #     try:
    #         raise Exception()
    #     except Exception as e:
    #         raise e

    # async def on_command_error(self, ctx, exc):
    #     rdf_guild = self.get_guild(rdfID)
    #     leifbot_channel = rdf_guild.get_channel(leifBotChannelID)        
    #     error_exception = getattr(exc, "original", exc)
    #     error_embed = discord.Embed(description = f"Error\n\n**{error_exception}**", color=0x303136)
    #     await leifbot_channel.send(embed = error_embed)
    #     raise getattr(exc, "original", exc)

    async def on_command_error(self, ctx, exc):
        error_exception = getattr(exc, "original", exc)
        error_embed = discord.Embed(description = f"Error\n\n**{error_exception}**", color=0x303136)
        raise getattr(exc, "original", exc)

    # async def on_ready(self):
    #     self.client_id = (await self.application_info()).id
    #     guild = self.get_guild(rdfID)
    #     registeredTime = now.strftime("%A  %d-%m-%Y  %H:%M:%S")     # the time at which the bot started
    #     print(f"Bot started at:            {registeredTime}")
    #     print(f"Bot logged in as:          {self.user.name}")
    #     print(f"Bot running on server:     {guild}")        
    #     print("Bot ready.")

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or("+")(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)
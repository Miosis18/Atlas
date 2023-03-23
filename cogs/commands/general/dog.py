import discord
import os
import yaml
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class Dog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # Dog command

    @app_commands.command(name="dog", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def dog(self, interaction: discord.Interaction) -> None:

        pass


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Dog(bot))

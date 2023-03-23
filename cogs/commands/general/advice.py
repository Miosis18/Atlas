import discord
import os
import yaml
import requests
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class Advice(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # Ping command

    @app_commands.command(name="advice", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def advice(self, interaction: discord.Interaction) -> None:

        request = requests.get("http://api.adviceslip.com/advice").json()
        advice_message = request["slip"]["advice"]

        await interaction.response.send_message(advice_message)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Advice(bot))

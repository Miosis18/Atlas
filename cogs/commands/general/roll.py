import discord
import os
import yaml
import random
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class Roll(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # Meme command

    @app_commands.command(name="roll", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def roll(self, interaction: discord.Interaction) -> None:

        await interaction.response.send_message(f"{interaction.user.mention} has rolled {random.randint(0, 100)}.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Roll(bot))

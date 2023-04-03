import discord
import os
import yaml
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class SlowMode(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # Suggest command

    @app_commands.command(name="slowmode", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.default_permissions(manage_messages=True)
    async def slow_mode(self, interaction: discord.Interaction, duration: int) -> None:

        if duration > 21600:
            duration = 21600
        elif duration < 0:
            duration = 1
        else:
            duration = duration

        if duration != 0:
            await interaction.response.send_message(f"Slowmode has been enabled for **{duration}** seconds.")
        else:
            if interaction.channel.slowmode_delay == 0:
                await interaction.response.send_message("Slowmode was already disabled in this channel.")
            else:
                await interaction.response.send_message("Slowmode has been **disabled** in this channel.")

        await interaction.channel.edit(slowmode_delay=duration)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SlowMode(bot))

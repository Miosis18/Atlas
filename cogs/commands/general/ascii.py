import discord
import os
import yaml
from pyfiglet import figlet_format
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class ASCII(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # Ascii command

    @app_commands.command(name="ascii", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def ascii(self, interaction: discord.Interaction, text: str) -> None:

        try:
            await interaction.response.send_message(f"```{figlet_format(text, font='starwars')}```")
        except discord.errors.HTTPException:
            await interaction.response.send_message("That message is too long, please try again with a shorter message",
                                                    ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ASCII(bot))

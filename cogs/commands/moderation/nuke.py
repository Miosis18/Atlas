import discord
import os
import yaml
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class Nuke(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # Nuke command

    @app_commands.command(name="nuke", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def nuke(self, interaction: discord.Interaction) -> None:

        guild = await interaction.client.fetch_guild(CONFIG["GuildID"])
        new_channel = await guild.create_text_channel(name=interaction.channel.name,
                                                      category=interaction.channel.category,
                                                      position=interaction.channel.position,
                                                      overwrites=interaction.channel.overwrites)
        await interaction.channel.delete()
        await new_channel.send(f"This channel was nuked by {interaction.user.mention}")
        await new_channel.send(
            "https://media1.tenor.com/images/e275783c9a40b4551481a75a542cdc79/tenor.gif?itemid=3429833")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Nuke(bot))
